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

.. _Module6:

Module 6 - Binary Auditing
==============================

.. only:: instructor

 Instructor Guidance
 -----------------------

 This module is about changing things up and giving students a chance to
 look for bugs in a binary and to talk about exploitation.  The goal is to
 spend a little time on RE, a little time on binary bug-hunting skills, and the
 rest of the time trying to exploit something and playing with the frustration
 that can sometimes come with dealing with a memory corruption bug.

 .. note::
    In a perfect world, an example might have a memory corruption bug and
    a nearby logic bug (e.g. path traversal) so that you can drive home the point
    that dealing with memory corruption is hard and that there is an opportunity
    cost for "success" when you find a bug of this type.  We don't have such
    a perfect example thus far but are always on the lookout!

 **Lecture**

 There needs to be a number of mini-lectures for this module as you probably
 don't want to drop drop everything on them at once.  For example, talk about
 RE first, then get into ROP and exploitation later.  A reasonable
 outline for the week that can be tweaked is as follows:

 * Monday - Follow the slides on RE.  Give a Ghidra demo as outlined in the
   Ghidra tool guide.  Have the students RE the other function in the guide.
 * Tuesday - Give a brief primer on C++, vtables, and how that might confuse
   you when doing RE.  Give the reveal that the function from yesterday is
   the same as the :ref:`FLIC1` spot-the-bug!  Get them started on the exercise.
   (The advice to dive into C++ is tailored to the one Mikrotik based exercise
   that exists so far.  If you have different exercise, get into the nucances of
   RE for **that** code.)
 * Wednesday - Give demos of some of the other tools to catch people up
   who may have been struggling with them.
 * Next Monday - Reveal the bug to catch everyone up and get the class started
   on exploitation. Give the remaining portion of the lecture on exploitation.
 * Next Tuesday - Talk about advanced exploit options like locating libc
   in the GOT.
 * Thursday - Share solutions.

 Of course, this all depends on having a binary with a bug that is reasonably
 exploitable in a week's time.  Basically you can divide the module into 1 week
 of RE/VR, and one week of exploitation.  Depending on the exercise, you may 
 deviate somewhat.

 This isn't a class on reverse-engineering.  Given that, you will need to
 equip the students with enough of the basics to get the job done for the
 exercise.  That is why the first day is all about using Ghidra to hone some
 skills there.  It is also a good idea to give some massive hints at where to
 look and caveat that those who want to get better at RE should practice lots.

 Exploitation is a wide topic so don't get too far in the weeds.  The
 stock lecture talks only about basic stack corruption, deferring the details
 about complex side-issues such as grooming and getting around common
 mitigations.  This is a good time to bring up mitigations, especially
 the older and simpler ones such as DEP/ASLR.  Students should have been
 reading some of the STB writeups so they should be exposed to some complex
 exploit writeups by now.  They should be eager to answer some simple questions
 about basic exploitation.

 **Exercise**

 This historically is the first time students work as a team, in
 particular pairs.  It is probably a good idea to hand-pick the teams for the
 auditing and exploitation exercise.  Hopefully, you have a mix of people with
 some amount of RE background.  If so, try to pair up someone with RE experience
 with someone who lacks it.  Make sure they know to let the inexperienced
 person drive sometimes.  Make sure they know that you want to see both
 students' "fingerprints" on the eventual solution and make sure to ask about
 that throughout the exercise.

 **Duration**

 Typically this module takes two 20 hour weeks.

Learning Objectives
-----------------------

#. Learn a little bit about a lot of tools and techniques.
#. Gain experience applying the same tactics you have been using on source code to disassembled binary.
#. Go beyond finding vulnerabilities into basic proof of concept exploit development.
#. Practice pair auditing and techniques for sharing information.

Reading Assignments
-----------------------

This is some food for thought after going through the depths of C last module.
Being good at VR means learning about the subtle intricacies of the language. This
is true for any language.  This article is about a bug in the Stapler framework which
is a component of Jenkins, a Java application.  This is a bug that was missed by
first year VRDP students!

Required

* `Jenkins dynamic routing hack <https://blog.orange.tw/2019/01/hacking-jenkins-part-1-play-with-dynamic-routing.html>`_
  [`cached version <../../ref/Orange_Hacking_Jenkins_Part_1.html>`__]
* `Exploitation of the bug <https://blog.orange.tw/2019/02/abusing-meta-programming-for-unauthenticated-rce.html>`_
  [`cached version <../../ref/Orange_Hacking_Jenkins_Part_2.html>`__]

Slides
----------

`Slides <slides/06_binary_slides.html>`_


Auditing Exercises
----------------------

.. toctree::
   :maxdepth: 1
   :glob:

   exercises/*06*

.. only:: instructor

 Spot The Bug
 ----------------

 None selected for this module.
