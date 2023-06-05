.. Copyright 2022 National Technology & Engineering Solutions of Sandia, LLC
   (NTESS).  Under the terms of Contract DE-NA0003525 with NTESS, the U.S.
   Government retains certain rights in this software.
   
   Redistribution and use in source and binary/rendered forms, with or without
   modification, are permitted provided that the following conditions are met:
   
    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.
    2. Redistributions in binary/rendered form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.
    3. Neither the name of the copyright holder nor the names of its contributors
       may be used to endorse or promote products derived from this software
       without specific prior written permission.
   
   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
   ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
   WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
   DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
   FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
   DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
   SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
   CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
   OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
   OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

.. _Resources:

Resources
=========

Books
-----

.. _taossa:

*The Art of Software Security Assessment*
+++++++++++++++++++++++++++++++++++++++++

.. .. external

.. sidebar:: *Image from publisher www.pearson.com*

   .. figure:: _static/taossa.jpg
      :scale: 50%

You can consider *The Art of Software Security Assessment* (TAOSSA) by Dowd
et.  al. as the main **text book** for the course.  Since it was first published
in 2006 it has remained an influential source book for learning how to apply
rigor to the vulnerability research process.  Students should each have their
own copy of this book as many reading assignments and references are contained
in it.

**Highlights**

Chapter 4 on Auditing Strategies is particularly influential for its
discussion on vulnerability research strategies.  It is the inspiration for how
a course like this could work in a field where growth is measured over years.
Keep in mind that in TAOSSA they use different terminology than we use in the
course.  Whereas we use the terms top-down and bottom-up they call it "trace
malicious input" and "analyze a module" respectively.

Chapter 7 on the C Language ends up being simultaneously the most hated
and loved chapter by students for its in depth discussion of obscure and
esoteric bugs.  This one language specific knowledge base we tap for the
course is meant to be an example of how in depth one must get sometimes in
order to be successful at VR.


.. _mis:

*Make It Stick*
+++++++++++++++

.. .. external

.. sidebar:: *Image from publisher www.hup.harvard.edu*

   .. figure:: _static/make_it_stick.jpg
      :scale: 50%

Some of the teaching philosophy in the VRDP course comes from the ideas
laid out in this book.  It is highly encouraged that prospective instructors
read this as it not only motivates some of the way we designed the course, but
is also a good primer on the science of learning that will likely serve you
well in your role as an instructor.  As the book is also designed for students,
you can encourage your students to read it although there is no assigned reading
from this book.  Further resources can be found at `www.retrievalpractice.org
<https://www.retrievalpractice.org>`_.

**Highlights**

Learning strategies are often not based on scientific rigor.  Rote repetition
is not the best way to learn things deeply yet is still the most widely used
method to prepare for tests.  Instead, having a systematic practice that forces
the retrieval of information is the best way to promote enduring learning.

In particular, the practice of *reflection* is something that promotes three
key learning activities.  Retrieval is necessary to describe what was learned.
Elaboration is encouraged to connect what was learned to past experience.  Finally,
generation makes students frame new concepts in their own words which is shown to
help concepts persist in memory.

Spot The Bug Exercises
----------------------

For each of these, display the code on a shared screen or just link the
page to the students.  They can click to see the answer but you can just run
the exercise on the honor system.  If you are really worried about them
looking ahead, just copy and paste only the code into whatever mechanism you
are using to collaborate (e.g. Mattermost, Wiki, desktop share, etc.).

There is a template for adding new STB exercises that appears below and the
source for which is contained in the `stb` directory of this document's source
tree.  We try to organize them by name into **easy**, **medium**, **hard** so
can choose one that you feel fits the capabilities of the students.

.. toctree::
   :maxdepth: 1

   stb/spot_the_bug_template.rst

.. toctree::
   :caption: Easy Difficulty
   :maxdepth: 1
   :glob:

   stb/easy/*

.. toctree::
   :caption: Medium Difficulty
   :maxdepth: 1
   :glob:

   stb/medium/*

.. toctree::
   :caption: Hard Difficulty
   :maxdepth: 1
   :glob:

   stb/hard/*

.. include:: Reading.rst

.. include:: Videos.rst
