UNCLASSIFIED

# VRDP Course Guide

This repository contains the course content for the 6 months to 1 year VRDP
class.

# Quick start

```
python3 -m venv env
source ./env/bin/activate
pip3 install -r requirements.txt
make
```

# How to use this repo

You really only need this repo if you intend to develop new or alter old
course content.  The instructor and student guide is written for Sphinx
(http://sphinx-doc.org) but includes other content scraped or compiled from the
Internet.

Slides are written using docutils so that the only markup language you need
to know is reStructuredText.

## Building the guides

The top level makefile will create all 3 main components of the guide, the
instructor guide, the student guide, and the slides.  In addition, it will link
them together with a top level portal defined by the static page inside the
`main` directory.

The guides are separate in case you would like to provide the student guide
to a class while hiding the instructor guide.  For either the instructor or
student guide just `cd` into their directory and type `make`. If you want
slides linked into the guide itself, also type `make slides`.  If you are building
the guides for use disconnected from the internet, type `make refs` to link in cached 
versions of external sites.

For only slides, do `cd slides && make`.

In all cases, the resulting output will be relative to the component
directory in `_build/html`

There is some duplication in all of this in order to support building each
guide independently.  For example, the ref directory is copied into each
guide's build chain.  It's a little messy but it makes it so that you can just
build the student guide with changes you want to send to a class.

Speaking of the ref directory, it contains offline copies of any material
that is relevant to teaching the course when possible.  These are often stripped
down to be as small as possible.  We make no ownership claim about any of that
material and it can be removed without affecting a course that is taught with
internet access.  They exist solely to support moving the course to isolated
networks where that content cannot be accessed.

## Adding custom exercises

This guide is designed so that you can keep a module intact and replace the
exercises that students do according to your needs.  In both the instructor and
student guides, there is a sub-directory called `modules/merged-exercises`
which contains either the default exercise for a module or a blank page.  You
are encouraged to branch or fork this repo and replace those exercises as needed.

There should be complimentary version of the exercise in each guide.  The
instructor's version of the exercise should have solutions and information
about what students get hung up on if there is historical data on how the
exercise has gone in the past.  The students' version should simply outline
the task, any hints or suggested strategies, and any other pertinent information
they need before starting.

## Changing Classification

The master branch of this repo is and should remain UNCLASSIFIED.  We do
encourage and support using real mission examples to teach when possible. Many
real world examples are motivating and relevant or can change the flavor of the
course to focus on skills in particular technology areas. If you include
classified lab exercises, examples, or spot-the-bug exercises, you must change
the classification banners accordingly.

### Instructor/Student Guide Banners

There is a minor extension to the RTD theme contained in
`_static/class_banner.js` and `_static/class_banner.css` in both the
`instructor` and `student` folders.  You can adjust the classification text in
the JavaScript file and you can adjust the colors in the CSS file.  The banners
will appear for the entire documentation on all pages.

### Slide Banners

The banners in the slides can only be changed for the entire deck.  Simply
change the `.. header::` and `.. footer::` directives at the top of each `rst`
file and that will change the banners for all slides contained in that file.

# Odds and Ends

## Instructor / Student Overlap

The student guide is mostly derivative of the instructor guide.  You will
see in the makefile that many pages are copied in before the student guide is
built.  This is done intentionally in order to avoid duplicating content.
When editing the instructor guide, pages can include special tags that only
render content for the instructor.

	.. only:: instructor

       Instructor only content goes here.

This is mostly used in the module and exercise files.  In this way, you can
create a single document and it will only render the "answers" in the
instructor version of the final product.

## Slides and Pygments integration

The slides are not built by Sphinx but we wanted to use reStructuredText there
as well. As such, the slides are generated directly with docutils and linked 
into the Sphinx tree.

For that reason, the syntax highlighting for code is not generated by sphinx and
instead baked into the repo.  If you want to change it, you need to run Pygments
directly and overwrite the style sheet for the syntax for slides:

  `pygmentize -S vim -f html -a .code > slides/src/theme/syntax.css`

The above uses the `vim` theme from pygments to colorize the code in slides.

UNCLASSIFIED
