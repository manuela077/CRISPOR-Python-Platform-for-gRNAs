import mysql.connector
import subprocess
import tempfile
import os

# # -------- USER INPUT --------
# GENOME_BUILD = "mm10"
# GENE_NAME = "Pou5f1"
# TWOBIT_FILE = "mm10.2bit"
# TSS_FLANK = 100  # Set to 0 if you want exact TSS only

# -------- GET TSS FROM UCSC --------
def get_gene_tss(gene_name, genome="mm10"):
    print(f"🔍 Searching UCSC for gene: {gene_name} in {genome}")
    conn = mysql.connector.connect(
        host="genome-mysql.soe.ucsc.edu",
        user="genome",
        password="",
        database=genome
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT chrom, strand, txStart, txEnd
        FROM refGene
        WHERE name2 = %s
        ORDER BY ABS(txEnd - txStart) DESC
        LIMIT 1
        """, (gene_name,)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if not result:
        raise ValueError(f"❌ Gene {gene_name} not found in {genome}")
    
    tss = result['txStart'] if result['strand'] == '+' else result['txEnd']
    # print(f"✅ Gene {gene_name} TSS: {result['chrom']}:{tss} ({result['strand']})")
    return result['chrom'], result['strand'], tss

# -------- RUN --------
# chrom, strand, tss = get_gene_tss(GENE_NAME, GENOME_BUILD)

# if TSS_FLANK > 0:
#     seq = extract_tss_sequence(TWOBIT_FILE, chrom, tss, strand, TSS_FLANK)
#     print(f"\n📤 Sequence ±{TSS_FLANK} bp around TSS:")
#     print(f">{GENE_NAME}_TSS_{chrom}:{tss}:{strand}\n{seq}")
# else:
#     print(f"\n📍 TSS position only (no sequence): {chrom}:{tss} ({strand})")
