#include "digraph.hpp"
#include <fstream>
#include <stdio.h>
#include <string>
#include <iostream>
/* sizeof_char function */
int sizeof_char(const char* line){
	int ind = 0;
	while(line[ind] != '\n'){
		ind++;
	}
	return ind;
}
/* is_balanced function */
bool is_balanced(const DiGraph* digraph){
	for(unsigned int i=0; i<digraph->order; ++i){
		int out_deg = 0, in_deg = 0;
		for(auto j = digraph->edges.cbegin(); j != digraph->edges.cend(); ++j){
			if(j->first == i){
				in_deg += 1;
			}
			else if(j->second == i){
				out_deg += 1;
			}
		}
		if(out_deg != in_deg){
			return false;
		}
	}
	return true;
}
/* main function */
int main(int argc,char** argv){
	// store order
	int n = atoi(argv[1]);
	// output files
	ofstream fout;
	fout.open("d6files/balanced" + to_string(n) + ".d6");
	// input nauty stream
	char nauty_call[85];
	char line[PATH_MAX];
	char *str;
	FILE *pipe;
	int status, size;
	DiGraph *digraph;
	sprintf(nauty_call,"/usr/local/Cellar/nauty/2.7r3/bin/geng %d | /usr/local/Cellar/nauty/2.7r3/bin/directg",n);
	pipe = popen(nauty_call, "r");
	while(fgets(line, PATH_MAX, pipe) != NULL){
		// size of line and str decleration
		size = sizeof_char(line);
		str = new char[size+1];
		for(unsigned int i=0; i<size; ++i){
			str[i] = line[i];
		}
		str[size] = '\0';
		// create digraph
		digraph = new DiGraph(str,size);
		// check if balanced
		if(is_balanced(digraph)){
			fout << str << endl;
		}
		// free digraph memory
		delete digraph;
		// free str memory
		delete str;
	}
	// close files
	fout.close();
}
