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

.. _Module5:

Module 5 - C Language Issues
================================

.. only:: instructor

 Instructor Guidance
 -----------------------

 This module is a deep dive into the nuances of the C language.  Even if
 you feel comfortable as an instructor with C nuances, its is probably a good
 idea to review the material in depth yourself as the quirkiness of C can get
 the best of anyone.  Also, having a growth mindset and doing recall learning
 is practicing what we preach!

 One important meta point to make during this module is that finding
 vulnerabilities sometimes means knowing a lot about the nuances in the
 technology.  We happen to be looking at C but there are plenty of issues in
 other languages that are similar.  C nuances just also happen to be an
 important component of vulnerability history as well as still being an
 important aspect of security as a lot of code is still being written in
 memory unsafe languages today.

 Because Chapter 6 is so long, we historically have emphasized that class
 time is okay to cover the reading.  This is typically a longer module so it is
 more than okay for some of that time to be granted for reading around the
 lecture and class activities.

 **Lecture**

 The lecture is meant to be delivered slowly and have the students ponder
 some of the questions such as, "What is the width of long?"  The lecture can
 also be broken up, is naturally done so over two sections of the existing
 slides but can be done so further as needed.

 Really try to make this lecture more interactive. This is a difficult
 topic and you don't want to leave anyone behind.  Ask lots of probing
 questions. 

 **Exercise**

 There is two components to exercise for this module.  Auditing and a
 "stump challenge" where students write a small C program to try and fool
 people about what the program will do using C nuances.  

 The first component which combined with reading should consume the first
 week are these "stump" challenges. The introduction to this is Stump The
 Student where students try to figure out what a program designed to trick them
 will print.  These challenges exist in the slide deck and you can run them
 during lecture on one of the days by doing the following: Show the student
 the sample and give them 5-10 minutes to say what the program will print. They
 cannot compile the program, they just have to use their newfound C reasoning
 skills.  Throughout the week you can pepper in some more challenges that you
 create to create more opportunities for interaction.

 By the end of the week, they should submit their own code for the second
 version of this called Stump The Teacher.  These are challenges where they
 apply some tricky C-isms they have learned to see if you the instructor can
 decipher them.  It is important to make time to do some of these together in
 class so they can hear how you reason about the code out loud.  This ends up
 being a quite fun game and students have come up with some pretty amazing
 challenges.  One favorite is:

 .. code::

   #include <stdlib.h>
   #include <stdio.h>
   
   typedef int i;
   
   int main(void)
   {
       char a[5] = { 1, 2, 3, 4, 5 };
       struct i { i i; } i;
       i: i.i = 0;
   
       if ((1 ? (int)1 : (unsigned long)2) > -++i.i)
           i.i = -1;
       else if (!(i.i == 0)) i.i += (i.i / i.i);
       else
           i.i = 11;
   
       i.i = -~i.i;
   
       if (i.i >= 0 && i.i <= 4)
           printf("i.i[a]++ = %d\n", i.i[a]++);
       else
           printf("i.i = %d\n", i.i);
       return 0;
   }

 One of the more nefarious portions of this code is by using the
 ternary operator to control the type of comparison operator performed.
 Type promotion happens to unify the return type for both options!

 You can go through the challenges the following week to break-up the
 monotony of auditing which is the primary task for that week.  These sort of
 fill the space that the spot-the-bug sessions fill but there are more
 personal.

 One session in particular we had a very large class and so playing Stump
 The Teacher was impractical.  Instead we had a tournament where students in
 teams tried to stump each other.  This went fine but was missing the component
 of having students listen to the instructor reasoning through the code.  If
 there is not enough time to play Stump The Teacher, you should still make time
 to have them listen to you breaking down the code.

 For the auditing, students should be "overly" documenting all of the
 internal changes that happen to integers in a piece of code as demonstrated
 in the lecture.  The goal for this week is to really get them into the
 mode of tearing down code much more carefully then they perhaps had been
 up to this point.

 This is a particular hard module to find new code that exercises this
 skill.  Try to make sure there are lots of different types to look at when
 you pick a code base to audit.

 **Rubric**

 During the auditing portion, have the students show you a spot of code
 where they really had to grapple with C issues.

 1. Did they identify each type in relevant expressions?
 2. Did they notice all opportunities for integer conversion?
 3. Are any hypotheses related to integer issues, even if unlikely?

 **Duration**

 Typically this module takes two 20 hour weeks.

Learning Objectives
-----------------------

#. Understand many nuances of the C language and how they contribute to
   memory safety.
#. Practice deliberately documenting things like
   boundary conditions, type conversions, promotions, etc.

Reading Assignments
-----------------------

Required

* TAOSSA Chapter 6

Slides
----------

`Slides <slides/05_c_language_slides.html>`_

Exercises
-------------

.. toctree::
   :maxdepth: 1
   :glob:

   exercises/05_stump_challenge
   exercises/*05*

.. only:: instructor

 Spot The Bug
 ----------------

 We generally skip STB during this module because of the stump exercises.
