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

.. _Module2:

Module 2 - Auditing Variables
=================================

.. only:: instructor

 Instructor Guidance
 -----------------------

 This module's goal for you is to start trickling in something for students
 to look out for while auditing.  In this case, theoretical variable issues
 should start popping up in their annotation logs.  Depending on the auditing
 assignment, there may not be any real bugs to find but if you find a student
 not commenting on initialization, relationships, or structures, you can give
 the proper feedback that they should be practicing looking out for those issues
 and at least commenting on them so that you know they are paying attention.

 **Lecture**

 Be prepared to have a discussion about what happens when a variable is
 used uninitialized.  This is a time to let the student's knowledge or imagination go
 to work so don't answer right away.  Try to go down to fundamentals to get them
 to figure it out.  Either as a followup or to get them thinking, you can 
 ask the question, "what happens if I declare a variable on the stack versus
 pointing to some memory on the heap?" You want to get them to the point of
 realization that real data could exist in memory at those locations.  Followup
 further with some discussion on how data like that could be controlled in
 theory (e.g. overlapping stack frames or heap grooming).

 In the ``netobj`` example from TAOSSA, there are actually 2 bugs. After
 you go over the one in the book, challenge the class to find the other one.
 If ``read`` returns 0 there is still a potential uninitialized issue because
 ``data`` will be the result of ``malloc(0)`` which is a valid non-zero amount
 of memory.  The fact that the list doesn't show a subsequent update to
 ``datalen`` may be a typo in TAOSSA.

 In the next example, for those stuck after reading the explanation in
 TAOSSA or those who haven't read it yet, explain that after establishing
 the relationship between ``cdata`` and ``len``, go line-by-line looking for
 a statement that will make the relationship definition between them no
 longer true.  The line ``++cdata`` with no corresponding ``--len`` is the
 exact moment that the two variables are no longer related to each other in
 the same way.  The downstream effects of that should be clear.

 The structure padding example is another motivator for a kind of bug
 that is subtle but can be teased out with proper process and a plan if
 you encounter a structure containing a variety of types.

 **Exercise**

 In contrast to the variability in annotations from module 1, you should hope
 for evidence that students are paying very close attention to variables,
 commenting on their meanings and if there are any relationships.  If they
 don't, you can question why and try to get into their heads as to what part of
 the material they are or are not integrating into the auditing process.

 **Rubric**

 You should keep looking for things from the first module but in addition:

 1. Are they recognizing variable relationships when they get a chance?  If
    not, tell them to slow down and treat every expression containing more
    than one variable as potentially creating a relationship.
 2. Are they noticing allocations and if initialization occurs?  Emphasize
    that initialization bugs are based on what is **not** present and
    therefore requires special consideration.  Encourage the use of
    a re-reading pass to check for initialization.
 3. Are they generating hypotheses around variable usage and/or initialization?

 **Duration**

 Typically this module takes one 20 hour week.

Learning Objectives
-----------------------

#. Understand basic vulnerability patterns around variable usage.
#. Practice auditing with variable usage in mind.
#. Reinforce hypothesis generation and using bottom-up methodology.

Reading Assignments
-----------------------

Required

* TAOSSA Chapter 7 pg 297-316 (Beginning up to subsection "Arithmetic Boundaries")
* TAOSSA Chapter 6 pg 284-297 (Subsection "Structure Padding" to end of chapter)
* `Attacks on uninitialized local variables <https://www.blackhat.com/presentations/bh-europe-06/bh-eu-06-Flake.pdf>`_
  [`cached version <../../ref/Attacks-on-uninitialized-local-variables_Flake.pdf>`__]



Recommended

* `Hey Man, Have You Forgotten to Initialize Your Memory? <https://www.blackhat.com/docs/eu-15/materials/eu-15-Chen-Hey-Man-Have-You-Forgotten-To-Initialize-Your-Memory-wp.pdf>`_
  [`cached version <../../ref/Hey-Man-Have-You-Forgotten-To-Initialize-Your-Memory.pdf>`__]
* `Linux Kernel AF_PACKET Info Leak
  <https://xorl.wordpress.com/2011/10/07/cve-2011-2898-linux-kernel-af_packet-information-leak/>`_
  [`cached version <../../ref/Linux_kernel_AF_PACKET_leak.html>`__]
* `Samba Uninitialized Pointer Vulnerability <https://access.redhat.com/blogs/766093/posts/1976553>`_
  [`cached version <../../ref/Samba_vulnerability_CVE-2015-0240.html>`__] 

  * `Exploitability Analysis <https://www.nccgroup.trust/uk/about-us/newsroom-and-events/blogs/2015/march/samba-_netr_serverpasswordset-expoitability-analysis>`_
    [`cached version <../../ref/Samba_netr_ServerPasswordSet_Expoitability_Analysis.html>`__]

Slides
----------

`Slides <slides/02_vars_slides.html>`_


Auditing Exercises
----------------------

.. toctree::
   :maxdepth: 1
   :glob:

   exercises/*02*

.. only:: instructor

 Spot The Bug
 ----------------

 The :ref:`FLIC1` and :ref:`FLIC2` STB exercises are great for newbies.  We
 recommend doing one on Tuesday and Wednesday as a warm up.  You could also
 split them between Week 2 and :ref:`Module 3 <Module3>`.
