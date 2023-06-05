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

.. _Module1:

Module 1 - Introduction & Methodologies
=======================================

.. only:: instructor

 Instructor Guidance
 -----------------------

 This first module is all about setting the tone and the expectations for the
 rest of the course. The slides will guide most of the discussion clearly so be
 familiar with them in advance. The slides expect you to at some point switch to
 a Snippet demo so make sure it is installed and working where you can show it
 off.

 **Lecture**

 Emphasize active auditing!  This is the main thing to drill this early.

 For the section on strategies, emphasize the difference between the way
 we have simplified the strategies to the way TAOSSA talks about them.  In VRDP
 we group a lot of the similar strategies down to just 3 as shown in the slides.
 It is a simplification that is helpful down the line.

 For the section on tactics, that is a good time to just go over what is in
 TAOSSA on the topic.  Introduce it in your own words if student's haven't read
 it or have a discussion on those tactics if they have.  Time and time again,
 students seem to dismiss re-reading as a tactic.  Make sure to talk about it
 and emphasize how useful it can really be.  Planning to re-read the code is
 very powerful.  You can also use re-reading to subdivide what you want to focus on
 to make complex things more manageable.
 
 This is the time to make your expectations around desk checking for exercises
 clear.  Students should expect to be asked, "have you desk-checked it" if they
 come to you with a supposed bug, even if you know they found it.

 The desk checking example near the end comes from a 
 `CVE-2019-3822 <https://curl.haxx.se/docs/CVE-2019-3822.html>`_ in curl. It is
 a pretty good example because it will set you up to talk about variable
 relationships in the next module.  You can also subtly introduce integer overflow
 issues without it being too complicated.

 Feedback from prior classes commonly said that this is a rough way to
 start.  One thing that seemed to help is early on, having the students watch
 you audit for a bit as early as possible.  Because the first day is so packed
 full of content, perhaps day 2 should be reserved for about 30 minutes of this
 to show some of what is expected on any code base that you feel comfortable.

 **Exercise**

 This module is all about making sure the students are remaining active with
 the code so check in on them frequently.  Function audit logs should be
 required.  If students miss bugs because they don't understand the patterns yet
 or are not 100% equipped to see all the nuances of C, that is okay and
 emphasize that.  It is about the process and you can admonish a sharp eye who
 saw bugs but didn't do their logs while praising someone who clearly followed
 the process but missed them.

 Starting out is a bit tricky because the students don't have anything to
 look for yet.  They only have whatever background knowledge about program
 safety coming into the course to work with.  That shouldn't stop them from
 using the processes though.  An analogy that seems to work with students for
 this week is working as a QA analyst on an important project like a Mars
 rover.  Imagine that you are responsible for making sure that rover will never
 crash.  Any bug that might case a problem is fair game, even theoretically.
 So in a sense, they are just using their forward development experience to
 look for any kind of issue, even obscure or unlikely ones.

 Generally, using the historical exercises, it is the case that the students
 who more closely follow the process end up finding more issues than those who
 blow it off.  If you are fortunate enough for that to be the case, a little bit
 of light ribbing has more than once left a deep and important lesson in the
 heart of an overconfident student. Keep it fun though!

 **Rubric**

 For this first module, the main thing to look for is process.
 Individually you can get into some specific reasoning and fix lingering
 misconceptions about code if you see it. That is a whack-a-mole game though
 and sometimes it is best left until later modules where we teach specific C
 nuances.  This week you should also get a better feel for their background
 knowledge and how we might need to help with that during the course if they
 are light on technical experience.

 Things to look for during feedback sessions:

 1. Are they putting thoughts into annotations enough? Or put another way,
    have they bought into the active auditing concept?
 2. Are they doing complete function audit logs with at least a "What" and
    "WCGW" section?  Sometimes students get paralyzed here a little bit.
    It is helpful to encourage them to put in thoughts even if they are wrong.
    This is not about getting it right first try.  It's about making progress.
 3. Are they forming any kind of hypotheses, even crazy, nonsensical, or
    wrong ones?  The point here is just to get the creative juices flowing.
    They might come up with bizarre stuff but just encourage it or suggest
    that they might need to apply tactics more than they are such as
    desk-checking or re-reading.

 **Duration**

 Typically this module takes one 20 hour week.

Learning Objectives
-------------------

#. Understand, at a high level, the strategies and tactics you can employ to do VR.
#. Practice active auditing and using function audit logs.
#. Practice applying tactics.
#. Practice using a bottom-up strategy to understand code.

Reading Assignments
-------------------

.. only:: instructor

 If possible, assign this reading before the first day.  If that is not
 possible you can narrow it down to the essential elements of Chapters 4 & 7
 before beginning the auditing task.  It is not necessary to know everything
 about memory corruption in order to practice bottom-up and active auditing. If
 the memory corruption content is not read in advance, it should be completed
 throughout the module or as part of free exploration at the end.

Read before exercise 
 * TAOSSA Chapter 4 pg 133-147 (Section "Code Auditing Tactics")
 * TAOSSA Chapter 7 pg 339-340 (Section "Auditing Functions" up to subsection "Return Value Testing and Interpretation")

Read at any time during the module
 * TAOSSA Chapter 4 pg 111-133 (Section "Code Auditing Strategies")
 * TAOSSA Chapter 5 as needed

Slides
------

`Slides <slides/01_intro_slides.html>`_


Auditing Exercises
------------------

.. toctree::
   :maxdepth: 1
   :glob:

   exercises/*01*

.. only:: instructor

 Spot The Bug
 ----------------

 Because this is the first module and there is a lot of lecture material
 including some examples that are like a STB, a separate STB is not recommended.
