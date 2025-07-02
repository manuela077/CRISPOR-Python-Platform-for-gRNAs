import subprocess
import argparse

# def getInputs():
#     parser = argparse.ArgumentParser(
#         description="Create Fasta file of a mouse genome over a given interval"
#     )
#     parser.add_argument("version", default="mm10", help="genome version title (default: mm10)")
#     parser.add_argument(
#         "--chr", type=str,
#         help="Chromosome number"
#     )
#     parser.add_argument(
#         "--start", type=str,
#         help="start location in base pairs"
#     )
#     parser.add_argument(
#         "--end", type=str,
#         help="end location in nucleotide base pairs"
#     )
#     parser.add_argument(
#         "--output",
#         help="Write final #guideId/targetSeq pairs to this CSV"
#     )
#     args = parser.parse_args()

#     return (args.version, args.chr, args.start, args.end, args.output)

def commandLine(vers, chro, st, en, outpt):
    command='./twoBitToFa '+vers+".2bit stdout -seq=" + chro+ " -start="+st+" -end="+en+" > "+outpt
    subprocess.run(command, shell=True)
    return outpt
# WSL command as a single string

# commandLine(getInputs())
