# Build the paper. Run from paper/.
#   make paper      the paper            -> build/main.pdf
#   make anon       anonymous render     -> build/main_anon.pdf
#   make figure     regenerate the figures from their YAML data
#   make clean      remove build products

LATEXMK  ?= latexmk
PYTHON   ?= python3
OUTDIR   := build
LMK      := $(LATEXMK) -pdf -bibtex -interaction=nonstopmode -halt-on-error -file-line-error -outdir=$(OUTDIR)
DEPS     := main.tex references.bib includes/release_metadata.tex ../paper_prep/A3_macros.tex figures/argument_map.tex figures/three_body.tex figures/three_records.tex

.PHONY: all paper anon figure clean

all: paper anon

paper: $(OUTDIR)/main.pdf
anon: $(OUTDIR)/main_anon.pdf

$(OUTDIR)/main.pdf: $(DEPS)
	$(LMK) -jobname=main main.tex

$(OUTDIR)/main_anon.pdf: $(DEPS)
	$(LMK) -jobname=main_anon -usepretex='\def\anonrender{}' main.tex

figure: figures/argument_map.tex figures/three_body.tex figures/three_records.tex

figures/argument_map.tex: figures/argument_map.yaml figures/make_argument_map.py
	$(PYTHON) figures/make_argument_map.py

figures/three_body.tex figures/three_records.tex: figures/three_body.yaml figures/three_records.yaml figures/make_reader_figures.py
	$(PYTHON) figures/make_reader_figures.py

clean:
	-$(LATEXMK) -C -outdir=$(OUTDIR) -jobname=main main.tex
	-$(LATEXMK) -C -outdir=$(OUTDIR) -jobname=main_anon main.tex
	rm -rf $(OUTDIR)
