# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build
CWD           = $(shell pwd)

.PHONY: all slides refs clean Makefile

all: Makefile refs slides
	@$(SPHINXBUILD) -t instructor -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)

slides:
	cd ../slides && make BUILDDIR=$(CWD)/$(BUILDDIR)/html/modules/slides

refs:
	mkdir -p $(BUILDDIR)/ref
	cp -r ../ref/* $(BUILDDIR)/ref/

clean:
	rm -rf $(BUILDDIR)
	@$(SPHINXBUILD) -M clean -t instructor

