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

Stump the Teacher/Student
++++++++++++++++++++++++++++++

Use your newfound C knowledge to create a program that exhibits unexpected
behavior if you are simply looking at it with human eyes.  You can create a
situation where an expected value comes out due to type promotions, unexpected
control flow happens due to operator precedent, or anything else you can come
up with from what you have learned in chapter 6.  Some examples are shown in
the lecture slides and may have fooled you when you went over them in class.

.. only:: instructor

 .. admonition:: **Instructor Note**

  Feel free to make your own stump challenges beyond the ones in the
  lecture.  Some are available from previous years in a different repository
  but they didn't have the same rules as outline below so they may not
  be great examples.  This week is all about fun, learning about C-isms,
  and demonstrating your humanity to them.  It's totally okay if you
  fail some of these challenges.  That is somewhat the point, that
  humans are really bad at remembering all this stuff.

Rules / Instructions
_________________________

#. Put your name in the first line in a comment.
#. Create a small C program. 30 lines max
#. Control flow should end in one of at most 3 paths.
#. Each path must print something unique in order to identify it.
#. Print a label and a value that was calculated along the way so that it is
   harder for someone to guess the right path.
#. Should be intellectually difficult, not mathematically difficult or just
   messy code.  You are not trying to stump someone by overwhelming them with
   calculations.  You are trying to be clever.  Challenges that ignore this
   may be discarded and that's no fun.
#. No library calls other than printf.
#. It must compile and run in gcc.
#. A calculator, the book, and the C spec are permitted to be used.
#. No undefined or implementation defined float behavior may be used.
#. You may use anything you have learned in Chapter 6 or the C spec.
#. You may not intentionally use any undefined or implementation defined behavior.
   For example, a stack overflow is undefined behavior.  Heck even the existence
   of a stack is implementation defined!

Submit your challenge to your instructor by the end of week 1 of this module.
**Do you think you can stump your teacher?**
