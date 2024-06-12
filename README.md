# ReferenceGenomeProcessing
Scripts to download and index a reference genome

## How to execute the script

The program `HumanReferenceGenome_DownloadAndIndexing.py` download the human reference genome (GRC38) and create the index for further processing with `BWA`

- The program requires the arguments `-g` and `-o`
   - `-g`: link to human reference genome
   - `-o`: Name of the output

```
python3 HumanReferenceGenome_DownloadAndIndexing.py -g https://ftp.ensembl.org/pub/release-112/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.1.fa.gz -o HS.Chr1.fa.gz

```
