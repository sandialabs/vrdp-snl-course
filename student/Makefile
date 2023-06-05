# Minimal makefile for Sphinx documentation
#
SHELL = /bin/bash

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build
CWD           = $(shell pwd)
INSTRUCTOR    = ../instructor

SHAREDFILES = Intro,Modules,Reading,Videos,StudentFAQ
SHAREDDIRS  = _static,modules

.PHONY: all slides refs clean Makefile

all: Makefile slides refs
	cp $(INSTRUCTOR)/{$(SHAREDFILES)}.rst .
	cp -r $(INSTRUCTOR)/{$(SHAREDDIRS)} .
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)

slides:
	cd ../slides && make BUILDDIR=$(CWD)/$(BUILDDIR)/html/modules/slides CUSTOMCSS=student

refs:
	mkdir -p $(BUILDDIR)/ref
	cp -r ../ref/* $(BUILDDIR)/ref/

clean:
	rm -rf _build {$(SHAREDDIRS)} {$(SHAREDFILES)}.rst
