# Display Values
from sys import argv
from traceback import format_exc
from numpy import arange, sqrt, real, imag, diag, sum
from matplotlib import pyplot as plt
from networkx import draw_shell, adjacency_matrix
from nauty_directg_reader import read_digraph6
from rnr import qnr
###############################################
###             main                        ###
###############################################
def main(arg):
    try:
        # graph order
        n = int(arg[1])
        # type
        typ = arg[2]
        # open file
        if(typ=='b'):
            fin = open("csvfiles/balanced%d.csv"%n)
        elif(typ=='p'):
            fin = open("csvfiles/polygonal%d.csv"%n)
        else:
            return
        # read lines
        line = fin.readline()
        x = []
        y = []
        while line != '':
            lst = line.split(", ")
            x.append(float(lst[0]))
            y.append(float(lst[1]))
            line = fin.readline()
        # plot
        fig, axes = plt.subplots(nrows=1,ncols=1)
        fig.tight_layout()
        axes.set_aspect('equal', 'box')
        axes.scatter(x,y,c='blue',marker='.')
        x = arange(0,n-1+0.1,0.1)
        f = lambda x : n-1-x
        axes.plot(x,f(x),'red')
        plt.show()
    except Exception as e:
        print(format_exc())
if __name__ == '__main__':
    main(argv)