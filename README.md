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
   You need to mount your local directory to access data from inside the Docker container. The following command mounts the `path/to/repo` directory and processes files located inside `fasta` folder:
   ```bash
   docker run --rm -v <path/to/repo>:/app <image-name>
   ```
   Example (Windows):
   ```bash
   docker run --rm -v C:/Users/John/asmscan-proteinbert-run:/app pbert
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

   Results for each subsequence are averaged from all folds before selecting one with highest value
