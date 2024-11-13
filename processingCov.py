import polars as pl
import argparse

def process_coverage_data(df1_path, df2_path, output_path):
    """
    Reads coverage and region data files, adds a 'region' column to the coverage data 
    based on specified regions, filters rows to include only those within regions, 
    and saves the result to a CSV file.

    Args:
        df1_path (str): Path to the coverage data file (CSV or TXT format).
        df2_path (str): Path to the region data file (CSV or TXT format).
        output_path (str): Path to save the output file.
    """
    # Load data
    df1 = pl.read_csv(df1_path)
    df2 = pl.read_csv(df2_path)

    # Merge and filter based on regions
    result = (
        df1.join(df2, left_on="chr", right_on="chr", how="inner")
        .filter((pl.col("pos") >= pl.col("start")) & (pl.col("pos") <= pl.col("end")))
        .select(["chr", "pos", "depth", "region"])
    )

    # Save the filtered DataFrame to a CSV file
    result.write_csv(output_path)
    print(f"Processed data saved to {output_path}")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process coverage data and add regions.")
    parser.add_argument("-d", "--depth_file", type=str, required=True, help="Path to the coverage data file (CSV or TXT format)")
    parser.add_argument("-b", "--bed_file", type=str, required=True, help="Path to the region data stored in a bedfile")
    parser.add_argument("-o", "--output_file", type=str, required=True, help="Path to save the output file")
    args = parser.parse_args()

    # Run the processing function with the provided arguments
    process_coverage_data(args.depth_file, args.bed_file, args.output_file)
