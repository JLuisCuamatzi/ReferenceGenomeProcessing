annovar

gatk SelectVariants \
    -V raw_variants.vcf \
    --select-type-to-include SNP \
    -O raw_snps.vcf

gatk VariantFiltration \
    -V raw_snps.vcf \
    --filter-expression "QD < 2.0 || FS > 60.0 || MQ < 40.0" \
    --filter-name "SNP_filter" \
    -O filtered_snps.vcf

gatk SelectVariants \
    -V raw_variants.vcf \
    --select-type-to-include INDEL \
    -O raw_indels.vcf

gatk VariantFiltration \
    -V raw_indels.vcf \
    --filter-expression "QD < 2.0 || FS > 200.0" \
    --filter-name "INDEL_filter" \
    -O filtered_indels.vcf

gatk MergeVcfs \
    -I filtered_snps.vcf \
    -I filtered_indels.vcf \
    -O filtered_variants.vcf

# Navigate to the desired directory and download ANNOVAR
wget http://www.openbioinformatics.org/annovar/download/humandb/hg38_refGene.txt.gz

# RefGene database for gene annotation
annotate_variation.pl -downdb -buildver hg38 refGene humandb/

# dbSNP database for known SNPs
annotate_variation.pl -downdb -buildver hg38 avsnp150 humandb/

# ClinVar database for clinical significance
annotate_variation.pl -downdb -buildver hg38 clinvar_20220320 humandb/

# COSMIC database for cancer variants (optional)
annotate_variation.pl -downdb -buildver hg38 cosmic70 humandb/

convert2annovar.pl -format vcf4 input.vcf -outfile input.avinput

table_annovar.pl input.avinput humandb/ -buildver hg38 \
    -out output \
    -remove \
    -protocol refGene,avsnp150,clinvar_20220320 \
    -operation g,f,f \
    -nastring . \
    -vcfinput
