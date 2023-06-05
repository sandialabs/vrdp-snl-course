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

.. _Module3:

Module 3 - Auditing Control Flow
====================================

.. only:: instructor

 Instructor Guidance
 -----------------------

 This section is all about focusing on how control flow elements
 contribute to certain bug patterns.  This overall goal is to help the
 students start being explicit with reasoning about certain paths.

 **Lecture**

 Other than learning about some more things to look for, this lab will
 have students start using their own reasoning about where to start
 auditing.  A common way to do that is to get some function statistics to find
 frequently called functions.  Even better are those that don't call many other
 functions themselves.  Another way to phrase it is to seek out "popular leaf
 function" of the call graph.  Furthermore, they should look out for files that
 contain multiple functions if they exist.  The *cscopeparser.py* script linked
 below is a way to gather and sort those statistics.

 Also encourage students to make heavy use of the re-reading tactic.  The
 statistics will help you but it doesn't hurt to make a very quick pass on
 the files of interest.  They should ask the question, "Can I understand the
 functions in this file in isolation?"  If not, then maybe it is not that great
 of a place to start.

 There is a STB in libvorbis that is all about loops and how certain paths
 can get loop variables to go wrong.  This is a simple one that you can either
 let them do independently and then restart the lecture or just do it together
 in class.

 When discussing listing 7-20 this is also an example of reasoning about
 branching paths.  This is a very basic situation which simply splits the
 single path through the loop but it is relevant because it is the one that
 breaks the loop invariant as TAOSSA suggests in the auditing tip.

 The rest of the lecture should follow the slides directly and is a pretty
 good reflection of the assigned section of TAOSSA.

 **Exercise**

 Traditionally this module is used as an opportunity to do some open
 ended VR. The hard part for the instructor is picking a code base to audit
 that provides an opportunity to practice the material.  Also, you will
 want to spend some time with the code base finding good places to do
 bottom-up analysis.  It should jive with the statistical method of
 locating a good place to start or be prepared to explain the nuance
 of why it doesn't.

 This is also a good opportunity to fire the students up about finding
 novel bugs.  Instead of hunting for a known bug, they are now hunting for
 zero days!  That comes with a cost, of not knowing the "right" path but
 it should also come with the excitement that if they do find something
 that it could lead to an important disclosure!

 **Rubric**

 By now, students should be making relevant annotations with respect
 to variables due to last module's experience. They are hopefully paying
 more attention to loop conditions as evidenced by their annotations.

 1. Are the students identifying loops that need to be examined more
    carefully and are their annotations calling out things like the
    loop constraints, exits, etc?
 2. Where there is opportunity, do the students mention aspects of
    path analysis as part of their hypotheses?

 **Duration**

 Typically this module takes one 20 hour week.

Learning Objectives
-----------------------

#. Learn common ways control-flow constructs fail.
#. Practice tactics for untangling control-flow.
#. Reinforce hypothesis generation and using bottom-up methodology.

Reading Assignments
-----------------------

Required

* TAOSSA Chapter 7 pg 326-339 (Section "Auditing Control Flow")
* Read after class discussion `goto fail <https://www.imperialviolet.org/2014/02/22/applebug.html>`_
  [`cached version <../../ref/goto_fail.html>`_]

Slides
----------

`Slides <slides/03_control_slides.html>`_

Deciding where to start
----------------------------

In this module you are going to be using your own discretion on where to
start.  Take some time to pre-analyze this code and see if you can find out
where good places might be to start a bottom-up strategy.  Seek answers to the
following questions.

1. What files or directories in the source seem to have a high
   concentration of utility, glue, or foundational code?
2. For a given file, can you understand the functions it contains in isolation?
3. Are there any context clues in the names of the file or functions
   that make you think this might be reachable from input?

Pick a spot where you want to start and be prepared to argue for your
choice and provide evidence for why you think it is a good place.

Gathering statistics about how often functions are called or how many calls they
make can be a way to determine what functions or files are important.  You can either
index the code with Snippet or use cscope directly in conjunction with the following
script to get basic function call data.

`cscopeparser.py <../../_static/cscopeparser.py>`_
(*depending on the size of the source, this might take a while to run*)

From within the top of the source directory you can either do:

.. code::

 find . -type f -exec file {} \; | grep source | cut -f1 -d':' > cscope.files
 cscope -i cscope.files -b
 ./cscopeparser.py

or

.. code::

 ctx init .
 ./cscopeparser.py -d .ctx/xrefs/linux-64/cscope.out

See the ``--help`` menu of the script for more options.

These function statistics are not everything.  Don't only base your decision
on the fact that a function is used a lot.  Do however let it guide your analysis
and use other evidence to help you.  Scanning the code quickly to determine things
like complexity, and the ability to understand things in isolation, will make a
stronger case for your selection.


Auditing Exercises
----------------------

.. toctree::
   :maxdepth: 1
   :glob:

   exercises/*03*

.. only:: instructor

 Spot The Bug
 ----------------

 The :ref:`ZDI_libvorbis` STB is referred to in the slides.  Do this exercise
 as a part of the lecture.
