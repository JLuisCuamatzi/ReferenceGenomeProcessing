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
- To test this script, I use download the <b>chromosome 1</b> of the <b>human genome</b>

- The execution of the previous command generate the next outputs:
  <br>
  <b>The reference genome for chromosome 1</b>
   - HS.Chr1.fa.gz
<br>
  <b>The index files for the given sequence</b>
  <br>
   - HS.Chr1.fa.gz.bwt<br>
   - HS.Chr1.fa.gz.pac<br>
   - HS.Chr1.fa.gz.ann<br>
   - HS.Chr1.fa.gz.amb<br>
   - HS.Chr1.fa.gz.sa<br>
