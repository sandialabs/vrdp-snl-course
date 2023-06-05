# Mimic Sphinx
BUILDDIR       = _build/html

SLIDESRC       = src
SLIDES         = $(wildcard $(SLIDESRC)/*.rst)
SLIDETRGTS     = $(patsubst $(SLIDESRC)/%.rst, $(BUILDDIR)/%.html, $(SLIDES)) 

THEME          = theme
THEMESRC       = $(SLIDESRC)/$(THEME)
THEMEFILES     = $(shell find $(THEMESRC) -type f)

STATIC         = static
STATICSRC      = $(SLIDESRC)/$(STATIC)
STATICFILES    = $(shell find $(STATICSRC) -type f)

CUSTOMCSS      = instructor

.PHONY: slides

slides: $(BUILDDIR) $(BUILDDIR)/index.html $(BUILDDIR)/$(THEME) $(BUILDDIR)/$(STATIC) $(SLIDETRGTS) $(THEMEFILES) $(STATICFILES)

$(BUILDDIR)/%.html: $(SLIDESRC)/%.rst Makefile $(THEMEFILES) $(STATICFILES)
	cd $(SLIDESRC) && rst2s5.py \
        --syntax-highlight=short \
        --stylesheet=$(THEME)/syntax.css,$(THEME)/custom-$(CUSTOMCSS).css \
        --theme-url $(THEME) \
        `basename $<` `basename $@`
	mv $(SLIDESRC)/$*.html $(BUILDDIR)

$(BUILDDIR)/index.html: $(BUILDDIR) $(BUILDDIR)/$(STATIC) $(SLIDESRC)/index.py $(SLIDES)
	cd $(SLIDESRC) && python index.py > index.html
	mv $(SLIDESRC)/index.html $(BUILDDIR)
	cp ../main/_static/* $(BUILDDIR)/$(STATIC)

$(BUILDDIR):
	mkdir -p $(BUILDDIR)

$(BUILDDIR)/$(THEME): $(BUILDDIR) $(THEMEFILES)
	cp -r $(THEMESRC) $(BUILDDIR)

$(BUILDDIR)/$(STATIC): $(BUILDDIR) $(STATICFILES)
	cp -r $(STATICSRC) $(BUILDDIR)

clean:
	rm -rf $(BUILDDIR)
