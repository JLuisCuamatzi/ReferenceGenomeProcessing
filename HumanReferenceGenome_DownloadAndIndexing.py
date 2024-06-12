import ftplib
import gzip
import os
import argparse
import subprocess

def download_reference_genome_ftp(ftp_url, output_path):
    """
    Download the human reference genome from the given FTP URL and save it to the specified output path.
    
    Arguments:
    ftp_url (str): The FTP URL to download the reference genome from. This url is provided with the flag -g, --genome_url
    output_path (str): The file path where the downloaded genome should be saved. The name for the final files is indicated with the flag, -o, --output_file
    
    Returns:
    str: The file path where the genome was saved.
    """
    # Parse the FTP URL
    from urllib.parse import urlparse
    parsed_url = urlparse(ftp_url)
    
    ftp = ftplib.FTP(parsed_url.netloc)
    ftp.login()  # Log in as anonymous
    ftp.cwd(os.path.dirname(parsed_url.path))
    
    with open(output_path, 'wb') as file:
        ftp.retrbinary(f"RETR {os.path.basename(parsed_url.path)}", file.write)
    
    ftp.quit()
    return output_path

def index_genome_with_bwa(genome_file):
    """
    Index the genome using BWA.
    
    Args:
    genome_file (str): The path to the genome file to be indexed.
    """
    print(f"Indexing genome file {genome_file} with BWA")
    subprocess.run(["bwa", "index", genome_file], check=True)

def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Download and index human reference genome")
    parser.add_argument("-g", "--genome_url", required=True, help="URL of the genome file") # https://ftp.ensembl.org/pub/release-112/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.1.fa.gz
    parser.add_argument("-o", "--output_file", required=True, help="Path to save the gzipped genome file")
    args = parser.parse_args()

    # Configuration
    GENOME_URL = args.genome_url
    OUTPUT_FILE = args.output_file
    

    # Download and process the genome
    try:
        gz_file = download_reference_genome_ftp(GENOME_URL, OUTPUT_FILE)
        print(f"Downloaded genome to {gz_file}")

        # Index the genome using BWA
        index_genome_with_bwa(gz_file)
        print(f"Indexed genome file {gz_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
