import sys
import os
import multiprocessing

# Constants
LOG_FILE = "logs/logfile.log"  # Update this with the actual log file path
OUTPUT_DIR = "output"
NUM_WORKERS = min(8, multiprocessing.cpu_count())  # Limit workers for efficiency

def process_chunk(chunk, date):
    """Processes a chunk and extracts log lines for the given date."""
    return [line for line in chunk if line.startswith(date)]

def chunked_file_reader(file_path, chunk_size=10**6):
    """Yields chunks of lines from a large file."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        chunk = []
        for line in f:
            chunk.append(line)
            if len(chunk) >= chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk

def extract_logs_for_date(date):
    """Extracts logs for the given date using multiprocessing."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    output_file = os.path.join(OUTPUT_DIR, f"output_{date}.txt")

    with multiprocessing.Pool(NUM_WORKERS) as pool:
        results = pool.starmap(process_chunk, [(chunk, date) for chunk in chunked_file_reader(LOG_FILE)])

    # Writing results efficiently
    with open(output_file, 'w', encoding='utf-8') as f:
        for result in results:
            f.writelines(result)
    
    print(f"Log extraction complete. Output saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_logs.py YYYY-MM-DD")
        sys.exit(1)

    date = sys.argv[1]
    extract_logs_for_date(date)
