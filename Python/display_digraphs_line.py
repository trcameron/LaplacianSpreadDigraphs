# Display DiGraphs
from sys import argv
from traceback import format_exc
from numpy import sqrt, real, imag, diag, sum
from matplotlib import pyplot as plt
from networkx import draw_shell, adjacency_matrix
from nauty_directg_reader import read_digraph6
from rnr import qnr
###############################################
###             main                        ###
###############################################
def main(arg):
    TOL = 2**(-48)
    try:
        # graph order
        n = int(arg[1])