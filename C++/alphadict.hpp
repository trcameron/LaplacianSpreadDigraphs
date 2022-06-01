#ifndef ALPHA_DICT_H
#define ALPHA_DICT_H
#include <iostream>
#include <map>
#include <utility>
#include <vector>
#include <string>
#include <math.h>
using namespace std;
/* AlphaDict class */
class AlphaDict{
public:
	double tol = pow(2.0,-46.0);
	map<pair<double,double>,vector<string>> dict;
	
	void add(const double alpha,const double alpha_comp,const string d6){
		double x,y;
		bool not_found = true;
		for(auto i = dict.begin(); i != dict.end(); ++i){
			x = (i->first).first;
			y = (i->first).second;
			if(sqrt(pow(x-alpha,2.0)+pow(y-alpha_comp,2.0)) < fmax(tol,tol*sqrt(pow(x,2.0)+pow(y,2.0)))){
				(i->second).push_back(d6);
				not_found = false;
				break;
			}
		}
		if(not_found){
			dict.insert(pair<pair<double,double>,vector<string>>(make_pair(alpha,alpha_comp),{d6}));
		}
	}
	
	AlphaDict(){}
	AlphaDict(const double alpha,const double alpha_comp,const string d6){
		dict.insert(pair<pair<double,double>,vector<string>>(make_pair(alpha,alpha_comp),{d6}));
	}
};
#endif