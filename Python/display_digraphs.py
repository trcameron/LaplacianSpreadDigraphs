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
        # alpha values
        alpha = float(arg[2])
        alpha_comp = float(arg[3])
        # type
        typ = arg[4]
        # open file
        if(typ=='b'):
            fin = open("csvfiles/balanced%d.csv"%n)
        elif(typ=='p'):
            fin = open("csvfiles/polygonal%d.csv"%n)
        else:
            return
        # read lines
        line = fin.readline()
        while line != '':
            lst = line.split(", ")
            x = float(lst[0])
            y = float(lst[1])
            if(sqrt((x-alpha)**2 + (y-alpha_comp)**2) < max(TOL,TOL*sqrt(x**2 + y**2))):
                graphs = lst[2]
                lst = graphs.split(" : ")
                for d6 in lst:
                    digraph = read_digraph6(bytes(d6.rstrip(),'utf-8'))
                    fig, axes = plt.subplots(nrows=1, ncols=2)
                    fig.tight_layout()
                    axes[0].axis("off");
                    draw_shell(digraph,node_color='#606060',ax=axes[0],with_labels=True)
                    
                    a = adjacency_matrix(digraph)
                    a = a.toarray(order='C')
                    l = diag(sum(a,axis=1)) - a
                    
                    f,e = qnr(l)
                    axes[1].plot(real(f),imag(f),color='#000000',fillstyle='right')
                    axes[1].fill(real(f),imag(f),color='#C0C0C0')
                    axes[1].plot(real(e),imag(e),color='#606060',linestyle='none',marker='*',markersize=10.0)
                    
                    plt.show()
            
            line = fin.readline()
    except Exception as e:
        print(format_exc())
if __name__ == '__main__':
    main(argv)