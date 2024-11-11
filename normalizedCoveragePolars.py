# Compute Normalized Coverage Script
# Version: 1.1
# Author: Jorge Luis Cuamatzi-Flores
# Date: 20240815
# Description: This script computes the genome coverage after aligning reads to a reference genome.
#              1. Estimates global coverage.
#              2. Calculates median coverage in non-overlapping windows.
#              3. Computes normalized coverage by dividing window median by global coverage.

import argparse
import sys
import time
import importlib
import subprocess

# Record start time
start_time = time.time()

# Required libraries and aliases
libraries = {
    'polars': 'pl'  # import polars as pl
}

# Function to install missing libraries
def install_pymodule(module):
    subprocess.check_call([sys.executable, "-m", "pip", "install", module])

# Check and install libraries
for library in libraries:
    try:
        importlib.import_module(library)
        print(f"'{library}' is already installed.")
    except ImportError:
        print(f"'{library}' is not installed. Installing...")
        install_pymodule(library)

# Import libraries and assign aliases
imported_libraries = {}
for library, alias in libraries.items():
    try:
        imported_libraries[alias] = importlib.import_module(library)
        globals()[alias] = imported_libraries[alias]  # Assign to global namespace
    except ImportError:
        print(f"Failed to import '{library}'.")

# Define coverage calculation function
def calculate_window_medians(df, window_size):
    """Calculate windowed median and normalized coverage."""
    global_coverage_median = df['depth'].median()

    df = df.with_columns(
        (pl.col('position') // window_size).alias('window_index')
    )

    result = df.group_by(['chromosome', 'window_index'], maintain_order=True).agg(
        [
            pl.col('depth').median().alias('window_median_coverage')
        ]
    )

    result = result.with_columns(
        [
            (pl.col('window_index') * window_size + 1).alias('window_start'),
            (pl.col('window_index') * window_size + window_size).alias('window_end')
        ]
    )

    result = result.with_columns(
        pl.lit(global_coverage_median).alias('global_coverage_median')
    )

    result = result.with_columns(
        (pl.col('window_median_coverage') / pl.col('global_coverage_median')).alias('normalized_coverage')
    )

    return result

def main(args):
    # Load input data
    try:
        df = pl.read_csv(args.input, separator='\t', has_header=False)
        df = df.rename({'column_1': 'chromosome', 'column_2': 'position', 'column_3': 'depth'})
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)

    # Perform coverage calculation
    result_df = calculate_window_medians(df, args.window_size)

    # Save result to output file
    try:
        result_df.write_csv(args.output)
        print(f"Normalized coverage results saved to {args.output}")
    except Exception as e:
        print(f"Error saving output file: {e}")
        sys.exit(1)

    # Print execution time
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description="Compute normalized genome coverage.")
    parser.add_argument('-i', '--input', required=True, help="Input depth file (gzipped).")
    parser.add_argument('-o', '--output', required=True, help="Output CSV file for normalized coverage results.")
    parser.add_argument('-w', '--window_size', type=int, default=1000, help="Window size for median calculation (default: 1000).")
    
    args = parser.parse_args()
    main(args)
