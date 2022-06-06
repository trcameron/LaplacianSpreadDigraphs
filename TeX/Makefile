#####################################################
#   Alpha Values TeX Make File   				    #
#####################################################
include ../make.inc

all: balanced fig polygonal clean
	
balanced:
	@lualatex balanced_vals6.tex
	@lualatex balanced_vals6_zoom.tex
	@lualatex balanced_vals7.tex
	@lualatex balanced_vals7_zoom.tex
	
fig:
	@lualatex fig1.tex
	@lualatex fig2.tex
	@lualatex fig3.tex
	@lualatex fig4.tex
	
polygonal:
	@lualatex polygonal_vals6.tex
	@lualatex polygonal_vals6_zoom.tex
	@lualatex polygonal_vals7.tex
	@lualatex polygonal_vals7_zoom.tex
	
clean: copy
	@rm -f *.log
	@rm -f *.aux
	@rm -f *.pdf
	
copy:
	@cp -r *.pdf ../pdffiles/