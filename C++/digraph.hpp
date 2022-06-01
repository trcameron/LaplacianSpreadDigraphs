#ifndef DIGRAPH_H
#define DIGRAPH_H
#include <iostream>
#include <map>
#include <utility>
#include <vector>
#include <set>
using namespace std;
/* DiGraph class */
class DiGraph{
public: 
	int order, size;
	set<pair<int,int>> edges;
	
	void print(){
		cout << "order: " << order << endl;
		cout << "size: " << size << endl;
		cout << "edges:" << endl;
		for(auto i = edges.cbegin(); i!= edges.cend(); ++i){
			cout << "\t (" << i->first << "," << i->second << ")" << endl;
		}
	}
	
	DiGraph(){}
	DiGraph(const char* str, size_t length){
		// loop variables
		int i, j, k;
		// data arrays
		length -= 1;
		int data[length], *edge_data;
		// subtract 63 from each line character and store integer in data
		for(i = 0; i<length; ++i){
			data[i] = str[i+1] - 63;
		}
		// graph order and edge data
		if(data[0]<=62){
			order = data[0];
			edge_data = &data[1];
			length -= 1;
		}
		else if(data[1]<=62){
			order = (data[1] << 12) + (data[2] << 6) + data[3];
			edge_data = &data[4];
			length -= 4;
		}
		else{
			order = (data[2] << 30) + (data[3] << 24) + (data[4] << 18) + (data[5] << 12) + (data[6] << 6) + data[7];
			edge_data = &data[8];
			length -= 8;
		}
		// graph size and edge bits
		k = 0;
		size = 0;
		bool bits[length*6];
		for(i=0; i<length; ++i){
			for(j=5; j>=0; j--){
				bits[k] = (edge_data[i] >> j) & 1;
				if(bits[k]){
					size += 1;
				}
				k += 1;
			}
		}
		// store edges
		k=0;
		for(i=0; i<order; ++i){
			for(j=0; j<order; ++j){
				if(bits[k]){
					edges.insert(make_pair(i,j));
				}
				k += 1;
			}
		}
	}
};
#endif