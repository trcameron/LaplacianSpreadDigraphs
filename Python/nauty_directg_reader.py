# Nauty DIRECTG Read and Write Functions
from sys import stdin
from networkx import DiGraph, draw
from matplotlib import pyplot as plt
from itertools import islice
import traceback

###############################################
###             read_digraph6               ###
###############################################
def read_digraph6(bytes_in):
    def data_to_n(data):
        """Read initial one-, four- or eight-unit value from digraph6 integer sequence.
        Return (value, rest of seq.)"""
        if data[0] <= 62:
            return data[0], data[1:]
        elif data[1] <= 62:
            return (data[1] << 12) + (data[2] << 6) + data[3], data[4:]
        else:
            return (data[2] << 30) + (data[3] << 24) + (data[4] << 18) + (data[5] << 12) + (data[6] << 6) + data[7], data[8:]
    def bits():
        """Returns sequence of individual bits from 6-bit-per-value list of data values."""
        for d in data:
            for i in [5, 4, 3, 2, 1, 0]:
                yield (d >> i) & 1
    # check for digraph6 data type
    if(bytes_in[0]!=38):
        raise Exception("digraph6 characters must start with &")
    else:
        bytes_in = bytes_in[1:]
    # subtract 63 from each bit, check for bits that are over 126
    data = [c - 63 for c in bytes_in]
    if any(c > 63 for c in data):
        raise Exception("digraph6 characters must be in range(63, 127)")
    # extract size of graph (n) and remaining bits which hold edge information
    n, data = data_to_n(data)
    # check if we have the correct number of bits
    nd = (n**2 + 5) // 6
    if len(data) != nd:
        raise Exception(f"Expected {nd*6} bits and got {len(data) * 6} in digraph6")
    # build digraph   
    digraph = DiGraph()
    digraph.add_nodes_from(range(n))
    for (i, j), b in zip([(i, j) for i in range(n) for j in range(n)], bits()):
        if b:
            digraph.add_edge(i,j)
    # return
    return digraph
    
###############################################
###             write_digraph6              ###
###############################################
def write_digraph6(digraph):
    def n_to_data(n):
        """convert integer to one-, four- or eight-unit digraph6 sequence"""
        if n<=62:
            return [n]
        elif n <= 258047:
            return [63, (n>>12) & 0x3F, (n>>6) & 0x3F, n & 0x3F]
    # get order
    n = digraph.order()
    # start string encoding for digraph
    x = chr(38)
    # yield string encoding for order
    for d in n_to_data(n):
        x += chr(d+63)
    # bits
    nodes = list(digraph.nodes)
    bits = (nodes[j] in digraph.neighbors(nodes[i]) for i in range(n) for j in range(n))
    chunck = list(islice(bits,6))
    while chunck:
        d = sum(b << 5 - i for i,b in enumerate(chunck))
        x += chr(d+63)
        chunck = list(islice(bits,6))
    # return string
    x += "\n"
    return x
    

###############################################
###             main                        ###
###############################################
def main():
    try:
        # read input stream
        for line in stdin:
            print(line.rstrip())
            g = read_digraph6(bytes(line.rstrip(),'utf-8'))
            test = write_digraph6(g)
            print(test)
            draw(g,ax=plt.subplot(111),with_labels=True)
            plt.show()
    except Exception as e:
        print(traceback.format_exc())
if __name__ == '__main__':
    main()