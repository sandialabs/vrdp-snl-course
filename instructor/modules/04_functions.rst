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

.. _Module4:

Module 4 - Auditing Functions
=================================

.. only:: instructor

 Instructor Guidance
 -----------------------

 This module is all about security relevant issues surrounding functions.
 It follows the assigned reading rather closely so being familiar with that
 material, the examples, and the slides before class is all that is necessary
 to properly walk though this material with the class.

 **Lecture**

 The only thing in the lecture to call out specifically is the last
 example.  As it is long, you can use it to talk through how an experienced
 person might approach it from a bottom-up perspective.  First, note what
 could go wrong in the function containing the ``realloc``.  You can
 then talk about either backtracking or using candidate points to find
 the subsequent callers and run into the main issue of the dangling pointers.

 **Exercise**

 Traditionally, students work on the same code they started in module 3.
 Continue looking for zero days but add in the content from this lab and focus
 on that in the feedback sessions.

 **Rubric**

 Function audit blocks really should be locked in by now because it is
 something you should have been requiring since module one.  What you might
 want to look out for now are more detailed descriptions of not just what
 the functions do, but how they behave or are related to other functions
 nearby. Also, you can encourage students to make sure they are considering
 relationships among function arguments if they haven't been already after
 the lecture on variables.  They should also be paying more attention to
 the referential nature of arguments and their consequences.

 1. Are they commenting on return values of functions?
 2. Where there is opportunity, do they notice functions that have a
    relationship (i.e. funcA must always be paired with a call to funcB)
 3. Do they notice when callers fail to capture or check a return values?
 4. Are they forming more hypotheses related to return values? There should
    be a lot more of these after this lecture.

 **Duration**

 Typically this module takes one 20 hour week.

Learning Objectives
-----------------------

#. Understand some basic vulnerability patterns involving functions.
#. Practice auditing with function properties and relationships in mind.
#. Reinforce hypothesis generation and using bottom-up methodology.

Reading Assignments
-----------------------

Required

* TAOSSA Chapter 7 pg 340-362 (Subsection "Return Value Testing and Interpretation" up to section "Auditing Memory Management")
* `Return value check failure example <https://blog.trendmicro.com/trendlabs-security-intelligence/an-analysis-of-a-windows-kernel-mode-vulnerability-cve-2014-4113>`__
  [`cached version <../../ref/windows_kernel_retval_check_fail.html>`__]
* `Misunderstood meaning example <https://nakedsecurity.sophos.com/2012/06/13/anatomy-of-a-bug-the-mysql-authentication-disaster-patch-now>`__
  [`cached version <../../ref/MySQL_authentication_disaster.html>`__]

Slides
----------

`Slides <slides/04_functions_slides.html>`_


Auditing Exercises
----------------------

.. toctree::
   :maxdepth: 1
   :glob:

   exercises/*04*

.. only:: instructor

 Spot The Bug
 ----------------

 The :ref:`Linux_keyring` STB is used as part of this lecture.
