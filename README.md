# asmscan-proteinbert

This tool is intended for binary classification of potentially amyloidogenic protein sequences from `FASTA` files. 

## Features
- Read protein sequences from a `.fa` file
- Generate prediction results as tab-separated CSVs

## Build and Run using Docker

1. **Build the Docker image**:
   ```bash
   docker build -t <image-name> .
   ```
2. **Run the application**:
   You need to mount your local directory to access data from inside the Docker container. The following command mounts the `path/to/repo` directory as a baseline for your container:
   ```bash
   docker run --rm -v <path/to/repository>:/app <image-name> --fasta_path <path/to/file> --output_path <path/to/directory>
   ```
   If you want to provide access to additional directories (docker images cannot access directories which were not explicitly mounted) you need to assign additional volumes:
   ```bash
   docker run --rm \
   -v <path/to/repository>:/app \
   -v <path/to/fasta/directory>:/app/fasta \
   -v <path/to/output/directory>:/app/output \
   <image-name> --fasta_path fasta/test.fa --output_path output
   ```

   Example for predicting specific file (Windows):
   ```bash
   docker run --rm -v /c/Users/John/asmscan-proteinbert-run:/app pbert --fasta_path ./fasta/test.fa --output_path ./output
   ```

   Example for predicting all files in a folder with a custom chunk size (Windows):
   ```bash
   docker run --rm -v /c/Users/John/asmscan-proteinbert-run:/app pbert --fasta_path ./fasta --output_path ./output --multi --chunk_size 50
   ```

Prediction results will be saved in `output` folder.

## FAQ
1. **What does each column in generated result contain?**

   `id`: FASTA identifier of the primary sequence

   `prob`: predicted probability of the highest-scoring subsequence within the primary sequence to be amyloidogenic

   `frag`: highest-scoring amino-acid sequence within the primary sequence


2. **How are output files formatted?**

   `fasta_filename`.`fold`.csv


3. **How are the `comb` results calculated?**

   Results for each subsequence are averaged from all folds before selecting one with the highest value


4. **What is the default `chunk_size`?**

   100
