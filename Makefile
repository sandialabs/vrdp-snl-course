BUILDDIR        = _build/html

all: $(BUILDDIR)
	cd instructor && make && make slides
	cd student && make && make slides
	cd slides && make
	mkdir -p $(BUILDDIR)/instructor
	mkdir -p $(BUILDDIR)/student
	mkdir -p $(BUILDDIR)/slides
	mkdir -p $(BUILDDIR)/ref
	cp -r instructor/_build/html/* $(BUILDDIR)/instructor
	cp -r student/_build/html/* $(BUILDDIR)/student
	cp -r slides/_build/html/* $(BUILDDIR)/slides
	cp -r ref/* $(BUILDDIR)/ref
	cp -r main/* $(BUILDDIR)

$(BUILDDIR):
	mkdir -p $(BUILDDIR)

clean:
	rm -rf $(BUILDDIR)
	cd instructor && make clean
	cd student && make clean
	cd slides && make clean

