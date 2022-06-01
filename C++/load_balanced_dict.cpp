#include "alphadict.hpp"
#include "digraph.hpp"
#include <fstream>
#include <stdio.h>
#include <string>
#include <iostream>
#include "Eigen/Eigenvalues"
/* sizeof_char function */
int sizeof_char(const char* line){
	int ind = 0;
	while(line[ind] != '\n'){
		ind++;
	}
	return ind;
}
/* main function */
int main(int argc,char** argv){
	// store order
	int n = atoi(argv[1]);
	// declare alphadict
	AlphaDict dict = AlphaDict();
	// input file
	ifstream fin;
	fin.open("d6files/balanced" + to_string(n) + ".d6");
	string line;
	char *str;
	DiGraph *digraph;
	while(getline(fin,line)){
		// str decleration
		str = new char[line.size()+1];
		copy(line.begin(),line.end(),str);
		// create digraph
		digraph = new DiGraph(str,line.size());
		// create h matrix
		Eigen::MatrixXd l = Eigen::MatrixXd::Zero(n,n);
		for(unsigned int i=0; i<digraph->order; ++i){
			int out_deg = 0;
			for(unsigned int j=0; j<digraph->order; ++j){
				if(digraph->edges.find(make_pair(i,j)) != digraph->edges.cend()){
					l(i,j) = -1;
					out_deg += 1;
				}
			}
			l(i,i) = out_deg;
		}
		Eigen::MatrixXd h = 0.5*(l + l.transpose());
		// compute eigenvalues of h matrix
		Eigen::SelfAdjointEigenSolver<Eigen::MatrixXd> es;
		es.compute(h);
		// add values to alphadict
		dict.add(es.eigenvalues()[1],n-es.eigenvalues()[n-1],line);
		// free digraph memory
		delete digraph;
		// free str memory
		delete str;
	}
	// close input file
	fin.close();
	// output file
	ofstream fout;
	// fout.precision(5);
	fout.open("csvfiles/balanced" + to_string(n) + ".csv");
	for(auto i = dict.dict.cbegin(); i != dict.dict.cend(); ++i){
		fout << scientific << (i->first).first << ", ";
		fout << scientific << (i->first).second << ", ";
		for(auto j = (i->second).cbegin(); j != (i->second).cend(); ++j){
			if(j < (i->second).cend()-1){
				fout << *j << " : ";
			}
			else{
				fout << *j << endl;
			}
		}
	}
	// close output file
	fout.close();
	// return
	return 0;
}