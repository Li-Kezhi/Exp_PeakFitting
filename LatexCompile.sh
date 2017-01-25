#!/bin/bash
# Compile LaTeX files to generate pdf file and a log file
# Example:
#     ./latexCompile.sh file_name_1 file_name_2
# Notes: Do not append .tex at the end of file name

for args in $@
do
    pdflatex -interaction=nonstopmode $args.tex > $args.log
    bibtex $args.aux > $args.log
    pdflatex -interaction=nonstopmode $args.tex > $args.log
    pdflatex -interaction=nonstopmode $args.tex > $args.log
    rm $args.aux $args.bbl $args.blg $args.spl
    open -a Preview $args.pdf
done