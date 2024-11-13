import polars as pl

# Create df1 with coverage data for 13 chromosomes
df1 = pl.DataFrame({
    "chr": [1] * 5 + [2] * 5 + [3] * 5 + [4] * 5 + [5] * 5 + [6] * 5 + [7] * 5 +
           [8] * 5 + [9] * 5 + [10] * 5 + [11] * 5 + [12] * 5 + [13] * 5,
    "pos": [1, 5, 10, 15, 20] * 13,
    "depth": [344, 345, 319, 310, 300, 305, 312, 315, 320, 325, 330, 335, 340, 345, 350,
              355, 360, 365, 370, 375, 380, 385, 390, 395, 400, 405, 410, 415, 420, 425,
              430, 435, 440, 445, 450, 455, 460, 465, 470, 475, 480, 485, 490, 495, 500,
              505, 510, 515, 520, 525, 530, 535, 540, 545, 550, 555, 560, 565, 570, 575,
              580, 585, 590, 595, 600]
})

# Create df2 with region information for each chromosome
df2 = pl.DataFrame({
    "chr": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    "start": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    "end": [10, 10, 10, 20, 20, 20, 30, 30, 30, 40, 40, 40, 50],
    "region": [f"region{chr_num}" for chr_num in range(1, 14)]
})

# Perform the join and filtering
result = (
    df1.join(
        df2,
        left_on="chr",
        right_on="chr",
        how="inner"
    )
    .filter(
        (pl.col("pos") >= pl.col("start")) & (pl.col("pos") <= pl.col("end"))
    )
    .select(["chr", "pos", "depth", "region"])
)

print(result)
