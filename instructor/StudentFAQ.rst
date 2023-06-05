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

.. _StudentFAQ:

Frequently Asked Student Questions
==================================

**How can I get Snippet on my personal machine?**

Unfortunately, Snippet is a tool that is a product of the Kachina program and
therefore is owned by the government.  That is why it can only be used on
government computers.  We are in frequent discussion about open sourcing
Snippet but that can oftentimes be a hard ask.

**How often "should" you find bugs?**

Oftentimes hackers work like water, they follow the path of least
resistance.  If you just want to find bugs, you can target things where
bugs are likely and then you should probably be finding them all the time.

The counterpoint to that is often for our job we are asked to look
at code that is designed to be secure and so you can expect to go through
quite long droughts of finding any bugs.  A laudable veteran of VR fame
once estimated that in this case, you may only find an impactful bug
about once a year.

In the end, it really depends.  VR by its nature is a search problem
and is speculative.  Your success will be punctuated but it will happen
if you put in the work.

**What environment should I use?**

Use the environment that puts the least amount of mental strain on you.
You need to be as comfortable a possible.  Many aspects of this course assume
at least a passing familiarity with a UNIX like environment but that is not
required to do well.

**What good tools are there out there to help with VR?**

More tools are coming out all the time to help with bug hunting and
exploitation.  Until recently, there was really only one world-class
reverse engineering tool, IDA.  Now there are many such as Binary Ninja,
Ghidra, and radare2.  Tools for source analysis, that really have code
auditing in mind, seem to be lagging a little bit.  Most of the time,
auditors use the IDEs that the developers would use to do their auditing.
This of course has some limitations, such as the inability to add
inline artifacts.

Other tools are going to be situational.  Once you get through module 6 of
the course, you will be introduced to a number of other tools.  It is going to
be a good idea to be fluent in one major debugger such as gdb, lldb, or windbg.
Beyond that, the tools become very situational.

**What about static analyzers like CodeSonar, Github Advanced Security, etc?**

Static analysis tools are getting more advanced as time goes on but they
still don't catch everything.  You can consider a static analysis tool as the
source of a candidate points analysis.  This is a perfectly valid means of
hunting down bugs.  VR is an any-means-possible kind of art so if you can bend a
complicated tool toward your problem, by all means do it.  Just be aware of the
potential cost of ramping up on a new tool.  Consider how much code you could
be auditing, when investing time in a static analysis tool.

**Are we going to learn about fuzzing?**

The official stance of VRDP is that fuzzing is a perfectly valid method of
finding bugs that is enhanced by powerful auditing skills.  That is why we
focus more on your reasoning and skills than teaching you how to use automated
tools like fuzzers.  Fuzzers also have a few major downsides when considering
*teaching* about them.  For starters, they don't tend to contribute to
knowledge.  After you have fuzzed for a long while, you maybe have done a lot
of work, but have little else to show for it.  Second, fuzzing tends to be
difficult to generalize.  We can learn how to fuzz one program, but how you
would effectively fuzz a different program might change, even dramatically.

We encourage students who are curious about fuzzing to study it outside the
course.  Become a good auditor first, it will help you be better at fuzzing.
