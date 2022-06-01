#####################################################
#   Alpha Values Make File   						#
#####################################################
include make.inc

install_balanced_gen:
	@$(CPP) $(CARGS) -o balanced_gen C++/balanced_gen.cpp $(INC) $(CPPLIB) -lm
	
install_load_balanced_dict:
	@$(CPP) $(CARGS) -o load_balanced_dict C++/load_balanced_dict.cpp $(INC) $(CPPLIB) -lm
	
install_load_polygonal_dict:
	@$(CPP) $(CARGS) -o load_polygonal_dict C++/load_polygonal_dict.cpp $(INC) $(CPPLIB) -lm
	
display_digraphs:
	@python3 Python/display_digraphs.py $(ORDER) $(ALPHA) $(ALPHA_COMP) $(TYPE)
	
display_values:
	@python3 Python/display_values.py $(ORDER) $(TYPE)
	
compile:
	@$(MAKE) all -C TeX
	
uninstall:
	@rm -f balanced_gen
	@rm -f load_balanced_dict
	@rm -f load_polygonal_dict