import argparse
import glob
import os
import time
from typing import Tuple, List

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import numpy as np
import tensorflow as tf

from utils.FragmentedSet import FragmentedSet
from utils.config import (SEQ_CUTOFF, MODEL_NAME, ADDED_TOKENS_PER_SEQ, MODEL_PATH, SEP, GO_SIZE, makedir)
from utils.tokenizer import tokenize_seqs


def predict(model_dir: str, fasta_path: str, output_path: str, multi: bool, chunk_size: int) -> None:
    cv_models_filepaths = glob.glob(os.path.join(model_dir, "*"))

    if multi:
        fasta_filepaths = glob.glob(os.path.join(fasta_path, "*.fa"))
    else:
        fasta_filepaths = [fasta_path]

    comb_model_name = f"{MODEL_NAME}comb{''.join(str(i) for i in range(1, len(cv_models_filepaths) + 1))}"

    # Load all models once
    print(f"Loading {len(cv_models_filepaths)} models...")
    models = [tf.keras.models.load_model(model_filepath) for model_filepath in cv_models_filepaths]

    for fasta_filepath in fasta_filepaths:
        fs = FragmentedSet(fasta_filepath, SEQ_CUTOFF, chunk_size)
        print(f"Processing file: {fasta_filepath}")
        print(f"Chunk size: {chunk_size}")
        print(f"Progress will be logged after first chunk is processed...")

        # Initialize CSV files for each model and the combined model
        model_files = {model_path: initialize_csv(model_path, fs, output_path) for model_path in cv_models_filepaths}
        model_files[comb_model_name] = initialize_csv(comb_model_name, fs, output_path)

        start_time = time.time()
        chunk_count = 0
        sequences_count = 0
        fragments_count = 0
        while True:

            if not fs.process_next_chunk():
                break  # No more chunks to process

            chunk_count += 1

            # Process the current chunk
            x_tst = tokenize_seqs(fs.frags, SEQ_CUTOFF + ADDED_TOKENS_PER_SEQ)

            y_pred = []
            for i, model in enumerate(models):
                preds = model.predict(
                    [x_tst, np.zeros((len(x_tst), GO_SIZE), dtype=np.int8)], verbose=0)

                y_pred.append(preds.flatten())

                # Save cv results
                append_predictions_to_csv(model_files[cv_models_filepaths[i]], fs.ids, y_pred[i], fs.frags, fs.scopes)

            # Save combined results
            if len(models) > 1:
                y_pred_combined = np.mean(y_pred, axis=0)
                append_predictions_to_csv(model_files[comb_model_name], fs.ids, y_pred_combined, fs.frags, fs.scopes)

            # Calculate and display progress
            chunk_end_time = time.time()
            elapsed_time = chunk_end_time - start_time
            sequences_count += len(fs.ids)
            fragments_count += len(fs.frags)

            print(
                f"Chunk {chunk_count} processed in {elapsed_time / 60:.2f} minutes. Total sequences processed: {sequences_count}")
            print("--------------------")

            # Clear the current chunk data
            fs.ids.clear()
            fs.frags.clear()
            fs.scopes.clear()

        # Close all CSV files
        for file in model_files.values():
            file.close()

        elapsed_time = time.time() - start_time
        print(f"Finished processing {fasta_filepath}")
        print(f"Total time taken: {elapsed_time / 60:.2f} minutes")
        print(f"Total chunks processed: {chunk_count}")
        print(f"Total sequences processed: {sequences_count}")
        print(f"Total fragments processed: {fragments_count}")
        print(f"Time per sequence: {elapsed_time / sequences_count:.3f} seconds")
        print(f"Time per fragment: {elapsed_time / fragments_count * 1000:.3f} milliseconds")
        print("====================")


def initialize_csv(model_name: str, fs: FragmentedSet, output_path: str) -> object:
    filepath = os.path.join(output_path, f"{fs.set_name}.{os.path.basename(model_name)}.csv")
    file = open(makedir(filepath), 'w')
    file.write(f"id{SEP}prob{SEP}beg{SEP}end{SEP}frag\n")  # Write header
    return file


def get_new_fragments(fs: FragmentedSet, processed_ids: set) -> Tuple[List[str], List[int], List[str]]:
    new_frags = []
    new_scopes = []
    new_ids = []

    start_idx = 0
    for id, scope in zip(fs.ids, fs.scopes):
        if id not in processed_ids:
            new_ids.append(id)
            new_scopes.append(scope)
            new_frags.extend(fs.frags[start_idx:start_idx + scope])
        start_idx += scope

    return new_frags, new_scopes, new_ids


def append_predictions_to_csv(file: object, ids: List[str], fragments_prediction: np.ndarray, frags: List[str],
                              scopes: List[int]) -> None:
    pred, selected_frags, start_index = to_sequence_prediction(fragments_prediction, frags, scopes)
    for id, p, s_i, f in zip(ids, pred, start_index, selected_frags):
        if len(f) < 40:
            e_i = -1
        else:
            e_i = s_i + 40
        file.write(f"{id}{SEP}{p:.3f}{SEP}{s_i + 1}{SEP}{e_i}{SEP}{f}\n")


def to_sequence_prediction(fragments_prediction: np.ndarray, frags: List[str], scopes: List[int]) -> Tuple[
    List[float], List[str], List]:
    pred = []
    selected_frags = []
    start_index = []

    p = 0
    for ss in scopes:
        scoped_frags_pred = fragments_prediction[p:p + ss]
        max_pred_index = np.argmax(scoped_frags_pred)
        pred.append(scoped_frags_pred[max_pred_index])
        selected_frags.append(frags[p + max_pred_index])
        start_index.append(max_pred_index)
        p += ss

    return pred, selected_frags, start_index


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict using models for FASTA files.")
    parser.add_argument("--fasta_path", required=True, help="Path to FASTA file or directory")
    parser.add_argument("--output_path", required=True, help="Output path for prediction results")
    parser.add_argument("--multi", action="store_true", help="Process multiple FASTA files in the directory")
    parser.add_argument("--chunk_size", type=int, default=100,
                        help="Number of sequences to process in a single chunk. Lower in case of memory issues")
    args = parser.parse_args()

    print(f"Starting prediction process. Output directory: {args.output_path}")
    predict(MODEL_PATH, args.fasta_path, args.output_path, args.multi, args.chunk_size)
    print("Prediction process completed.")
