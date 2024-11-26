import os
import subprocess
import argparse
import pandas as pd
import matplotlib.pyplot as plt

def split_cram(cram_file, cram_fwd, cram_rev):
    """
    Divide el archivo CRAM en reads forward y reverse.
    """
    subprocess.run(["samtools", "view", "-F", "16", "-C", "-o", cram_fwd, cram_file])
    subprocess.run(["samtools", "index", cram_fwd])

    subprocess.run(["samtools", "view", "-f", "16", "-C", "-o", cram_rev, cram_file])
    subprocess.run(["samtools", "index", cram_rev])

def extract_coverage(cram_file, bed_file, output_file, quality):
    """
    Extrae la cobertura por posición usando samtools depth.
    """
    quality_option = f"-Q {quality}" if quality > 0 else ""
    cmd = f"samtools depth {quality_option} -b {bed_file} {cram_file} | gzip > {output_file}"
    subprocess.run(cmd, shell=True, check=True)

def calculate_mean_coverage(depth_file, output_file):
    """
    Calcula la cobertura promedio por cromosoma.
    """
    df = pd.read_csv(depth_file, sep="\t", header=None, compression="gzip")
    df.columns = ["chrom", "pos", "depth"]
    mean_coverage = df.groupby("chrom")["depth"].mean().reset_index()
    mean_coverage.columns = ["chrom", "mean_depth"]
    mean_coverage.to_csv(output_file, sep="\t", index=False, compression="gzip")
    return mean_coverage

def plot_coverage(means, output_file, sample_prefix, quality):
    """
    Genera un boxplot comparativo de la cobertura media por cromosoma.
    """
    plt.figure(figsize=(12, 6))
    categories = ["BothStrands", "ForwardStrand", "ReverseStrand"]
    data = [means[cat]["mean_depth"] for cat in categories]

    plt.boxplot(data, labels=categories)
    plt.title(
        f"Comparative Analysis of Coverage by Strand Bias in sample: {sample_prefix}\n"
        f"Mean depth both strands: {data[0].mean():.2f}, "
        f"Mean depth forward strands: {data[1].mean():.2f}, "
        f"Mean depth reverse strands: {data[2].mean():.2f}"
    )
    plt.xlabel("Strand")
    plt.ylabel("Mean Coverage")
    plt.savefig(output_file)
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="Analyze CRAM files for strand-specific coverage.")
    parser.add_argument("-input", required=True, help="Input CRAM file.")
    parser.add_argument("-cram_fwd", required=True, help="Output CRAM file for forward reads.")
    parser.add_argument("-cram_rev", required=True, help="Output CRAM file for reverse reads.")
    parser.add_argument("-prefix", required=True, help="Sample prefix.")
    parser.add_argument("-bed", required=True, help="BED file with regions of interest.")

    args = parser.parse_args()

    # Tarea 1: Dividir el CRAM
    split_cram(args.input, args.cram_fwd, args.cram_rev)

    # Tarea 2: Extraer la cobertura
    output_files = {
        "BothStrands.Q00": f"{args.prefix}_DepthCoverage.BothStrands.Q00.txt.gz",
        "ForwardStrand.Q00": f"{args.prefix}_DepthCoverage.ForwardStrand.Q00.txt.gz",
        "ForwardStrand.Q30": f"{args.prefix}_DepthCoverage.ForwardStrand.Q30.txt.gz",
        "ReverseStrand.Q30": f"{args.prefix}_DepthCoverage.ReverseStrand.Q30.txt.gz",
    }

    extract_coverage(args.input, args.bed, output_files["BothStrands.Q00"], quality=0)
    extract_coverage(args.cram_fwd, args.bed, output_files["ForwardStrand.Q00"], quality=0)
    extract_coverage(args.cram_fwd, args.bed, output_files["ForwardStrand.Q30"], quality=30)

    # Tarea 3: Calcular y graficar coberturas medias
    means = {}
    for category, file in output_files.items():
        mean_output = file.replace("DepthCoverage", "Mean")
        means[category] = calculate_mean_coverage(file, mean_output)

    plot_coverage(means, f"{args.prefix}_CoveragePlot.Q00.png", args.prefix, quality="Q00")
    plot_coverage(means, f"{args.prefix}_CoveragePlot.Q30.png", args.prefix, quality="Q30")

if __name__ == "__main__":
    main()


# python script.py -input sample.cram -cram_fwd forward.cram -cram_rev reverse.cram -prefix sample_prefix -bed regions.bed










import pandas as pd
import matplotlib.pyplot as plt
import gzip

# Datos simulados
data_both = """chrom\tpos\tdepth
chr1\t1\t25
chr1\t2\t30
chr1\t3\t20
chr2\t1\t15
chr2\t2\t10
chr3\t1\t5
chr3\t2\t10
"""

data_forward = """chrom\tpos\tdepth
chr1\t1\t15
chr1\t2\t20
chr1\t3\t10
chr2\t1\t5
chr2\t2\t5
chr3\t1\t2
chr3\t2\t5
"""

data_reverse = """chrom\tpos\tdepth
chr1\t1\t10
chr1\t2\t10
chr1\t3\t10
chr2\t1\t10
chr2\t2\t5
chr3\t1\t3
chr3\t2\t5
"""

# Función para escribir datos en archivos gzip
def write_gzip_file(filename, data):
    with gzip.open(filename, "wt") as f:
        f.write(data)

# Crear archivos simulados
write_gzip_file("DepthCoverage.BothStrands.Q00.txt.gz", data_both)
write_gzip_file("DepthCoverage.ForwardStrand.Q00.txt.gz", data_forward)
write_gzip_file("DepthCoverage.ReverseStrand.Q00.txt.gz", data_reverse)
os.getcwd()

# Función para calcular la media de cobertura
def calculate_mean_coverage(file):
    """
    Calcula la cobertura promedio por cromosoma desde un archivo comprimido.
    """
    df = pd.read_csv(file, sep="\t", compression="gzip")
    mean_coverage = df.groupby("chrom")["depth"].mean().reset_index()
    mean_coverage.columns = ["chrom", "mean_depth"]
    return mean_coverage

# Función para generar el boxplot
def plot_coverage(means, output_file, sample_prefix):
    """
    Genera un boxplot comparativo de la cobertura media por cromosoma.
    """
    categories = list(means.keys())
    data = [means[cat]["mean_depth"] for cat in categories]

    plt.figure(figsize=(12, 6))
    plt.boxplot(data, labels=categories)
    plt.title(
        f"Comparative Analysis of Coverage by Strand Bias in sample: {sample_prefix}\n"
        f"Mean depth both strands: {data[0].mean():.2f}, "
        f"Mean depth forward strands: {data[1].mean():.2f}, "
        f"Mean depth reverse strands: {data[2].mean():.2f}"
    )
    plt.xlabel("Strand")
    plt.ylabel("Mean Coverage")
    plt.savefig(output_file)
    plt.close()

# Archivos de datos simulados
files = {
    "BothStrands": "DepthCoverage.BothStrands.Q00.txt.gz",
    "ForwardStrand": "DepthCoverage.ForwardStrand.Q00.txt.gz",
    "ReverseStrand": "DepthCoverage.ReverseStrand.Q00.txt.gz"
}

# Cálculo de medias
means = {key: calculate_mean_coverage(file) for key, file in files.items()}

# Generar boxplot
sample_prefix = "TestSample"
plot_coverage(
    means,
    output_file=f"{sample_prefix}_CoveragePlot.Q00.png",
    sample_prefix=sample_prefix
)

print(f"Boxplot generado: {sample_prefix}_CoveragePlot.Q00.png")







