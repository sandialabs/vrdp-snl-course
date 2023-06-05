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

.. Module 6 - Auditing Binaries

.. include:: <s5defs.txt>
.. include:: custom.txt

.. header::

 UNCLASSIFIED

.. footer::

 UNCLASSIFIED

.. class:: title-slide

 Vulnerability Research Development Program
   :small:`Module 6`

   :small:`Auditing Binaries`

.. class:: handout instructor

 These instructor call outs are a basic script for an example lecture.  They
 will oftentimes be specific to Sandia but can be a good guide for giving the
 lecture anywhere.

Last Module In Review
=====================

.. class:: handout instructor

 Last time we had somewhat of a confrontation with the nuances of C.

.. class:: incremental

  * C can be really weird!
  * Integer conversions can be hard to understand, especially for programmers
  * Embrace the complex
  * Add rigor to your process when confronted with complexity

.. class:: handout instructor

 I want to make a special note of the reading for this week.  The pair
 of articles are about a bug in a Java program.  This is really to give
 you a different flavor for the what it means to get into the details
 of a different language other than C.  To find that bug, you really
 have to know a lot more about Java than the developers of Jenkin's
 Stapler framework knew when they were making their clever system.


This Module - Overview
======================

.. class:: handout instructor

 We have looked at a lot of C code.  You might have asked...

How do I change up my VR process when I don't have source?

When can we get to exploiting a bug!?

.. class:: tight-list

 * Menagerie of tools
 * Ghidra for noobs
 * Reading disassembly vs decompilation
 * Process changes for binaries
 * Primitive exploitation

.. class:: handout instructor

 There is too much about reverse engineering **and** and bug-hunting **and**
 exploitation to get into any one thing too deeply in just two weeks.  So we
 are going for breadth on this one.  Just be aware of this and understand that
 you are probably going to have to go into a lot of this stuff on your own
 outside the course later.  In some cases, whole topics like reverse
 engineering could be their own VRDP length course in and of themselves.

 So we have a lot of tools we are going to use briefs.  One we are going to use
 a lot will be Ghidra so you will get a crash course on that if you haven't
 used it before.  Even if you have, there may be a trick or two you haven't seen
 before.

 We are going to get into reading disassembly, decompilation, and how to
 transform the process knowledge you have gained into this new setting.

 Finally, we will do some very basic exploitation.  By the end of the module,
 you will be making a real program with a real bug do things it was not
 designed to do.

Tools!
======

.. class:: incremental

    There are too many tools....

    Nevertheless we will talk about these ones

    .. class:: tight-list

     * Ghidra
     * binwalk
     * busybox
     * gdb
     * wireshark
     * python sockets

.. class:: handout instructor

 Each one of these we are really going to use in its default or canonical way.
 There is much more to know about all of these and I highly recommend looking
 for ways to get more familiar with each of these if you aren't already.

Ghidra, not just a poor man's IDA
=================================

Demo Time!

.. class:: handout instructor

 (Use the Ghidra tool guide as a reference for giving a demo of Ghidra)

Process changes
===============

.. class:: handout instructor

 Some things are slightly different when it comes to process, though.
 You can sort of think about what you have been doing as a manifestation
 of what you always have to do when reverse engineering.  You are building
 something or in this case re-building something.

 So you have to be active if you want to take advantage of what the RE
 tools are providing for you. They to raise the abstraction so you don't
 have to be looking at machine code the whole time.

 RE is continually constructive because as you saw, you are learning about
 the code as you change it.

 (read and emphasize last paragraph)

Active auditing really isn't a choice anymore.

Reverse Engineering is a continual / constructive process.

You are learning about the code while you change it. (fix decompilation)

You are "merely" at a lower level of detail.  It is okay to feel out of sorts.
Just don't get **lost**.  You can always slow down and break up the problem
into smaller pieces.


Process changes (continued)
===========================

What about this code being disassembly / decompilation stops you from using
the strategies you already know?

Are there additional tactics you think should apply?

 * Can you trust decompilation to be correct?
 * What should you do if you can't?

.. class:: handout instructor

 Process-wise, you should still be able to everything else you have been
 doing.  All of your tactics still apply.  You can still use function audit
 logs, etc.

 One of the things you have to consider is that the decompiler is going
 to do its best job but it is not perfect.

 You have some other things that you can add to your process however...

Disassembly vs decompilation
============================

The disassembly is the ground truth.

Decompilation is **reconstructed** semantics.  You are used to thinking
about how C code becomes machine code, now you need to think the opposite.

You are auditing **two** streams of code.

.. class:: handout instructor

 This means that you can cross check what you think is true about the world
 with the other code and document things that seems weird.  You may not
 run into it in this exercise but it is an important thing to remember.

Dynamic analysis in the mix
===========================

.. class:: handout instructor

 Now this is something you can do this with source too, but here it is
 potentially going to help you understand things that are much easier to
 track down when given access to source.

You can actually run this code and debug it.  That is not always possible but
when it is, you can take advantage of that!

Where are some good places to debug?

What are the limitations of debugging?

.. class:: handout instructor

 How about places where input might come in?  Network code?
 How about ``read`` or ``recv``? Spending some time doing this might help
 you decide on what strategy to use. (i.e. top-down vs bottom-up)

 The limitations of this really are the same things that make testing a
 somewhat cumbersome tactic.  You can't always drive the program to where you
 want to analyze.

Ghidra Exploration
==================

Spend the rest of today auditing the function in the Ghidra tool guide.

There is too much to learn in two weeks and so all of this is just a
taste.

You shouldn't struggle.  Remember that this module is about **breadth** of
experiences.  If you are stuck, you must ask for help.

Learning Objectives
====================

#. Learn a little bit about a lot of tools and techniques.
#. Gain experience applying the same tactics you have been using on source code to disassembled binary.
#. Go beyond finding vulnerabilities into basic proof of concept exploit development.
#. Practice pair auditing and techniques for sharing information.

.. class:: handout instructor

 These really are the goals for the whole two weeks.  Roughly we will be
 doing RE and VR the first week and exploitation the next week.  This is
 the first time you will be able to work with your classmates.  You
 should have been paired according to your relative background experience
 with RE or Ghidra.  So if you are somewhat familiar with these tools please
 lend a hand to your teammates.  Take turns driving the tools so that
 everyone gets a chance to have hands on the problem.

\
===========================

.. class:: handout instructor

 (The next day, go over the reversing challenge the day before and
  resume a Ghidra demo cover the C++ content)

*(slide intentionally left mostly blank to remind me to stop here for the day)*

Thinking about Exploitation
===========================

.. class:: handout instructor

 (Should be given Monday the following week)

.. class:: incremental

    Sometimes exploitation is easy!

    .. code-block:: php

        <?php
          $address = $_GET["address"];
          $output = shell_exec("ping -n 3 $address");
          echo "<pre>$output</pre>";
        ?>

    Sometimes it is incredibly difficult.

    With memory corruption, what gets corrupted **matters**.

.. class:: handout instructor

 Sometimes finding a bug is synonymous with exploiting it.  In the case of the
 code above, input comes in via GET parameters and is immediately given to a
 shell command.  Because you can send input with a semi-colon, the shell
 command will terminate and you can run whatever else you want in a shell.
 This is a class of vulnerability called a command injection which is one of
 the easiest kinds of bugs to exploit.

 The other kinds of vulnerabilities we have been exploring involve memory
 corruption and what you can once discovering the vulnerability can really
 depend on what you can mess with.

Mostly its about control
========================

What do you control at the point being considered?

What can you influence with that control?

Are there secondary, tertiary, effects that are useful?

Are features of the program useful, can you pivot to something else?

.. class:: handout instructor

 After you discover a memory corruption bug, the next thing to do is to reason
 about what you control at the instant.  For example, if you have a buffer
 overflow bug, what can you overwrite and what constraints are placed on the
 contents of that memory? Does your input have to have certain characteristic?
 Can the nul-byte be included?

 Sometime the effects you can have are indirect.  For example, in a stack
 overflow, the traditional thing to do is to overwrite the return address.  You
 may not **want** to do that if there are stack canaries though but instead,
 maybe you can overwrite another local variable to have a secondary effect
 later in time.

 The more you know about a program the more options you may have to consider as
 well. Perhaps there is a natural file write capability that the program has
 and your ability to influence data can change where that write happens.  That
 could be enough to take full control of the system.

 Sometimes the answers to these questions might leave an otherwise perfectly
 good bug non-exploitable or so annoying to exploit that you wouldn't
 bother.

What do we want to corrupt?
===========================

Ultimately, this is where lots of creativity can be involved.

We have seen examples of single byte overflows being manipulated
into *control-flow hijacking* or *arbitrary execution*.

Hijacking is often considered the pinnacle of success but lots of
other effects that you can have might matter more and be easier.
(i.e. information disclosure, authentication bypass, etc.)

Code pointers are traditionally, a good thing to corrupt.

.. class:: handout instructor

 We are going to go after one of the only code pointers you can pretty
 much guarantee to be on the stack, the return address.  Code pointers
 inside of structures are also an ideal thing to overwrite in most
 normal situations.  For example, if you have a heap overflow instead,
 you might need to explore ways to line up objects such that your
 overflow will let you whack a code pointer in some object ahead of
 you on the heap.  That is a process call *heap grooming*.

 We are going to go old-school for this exercise though so let's
 get into the knowledge you will need.

Exploiting like it is 1996!
===========================

.. class:: scrollable

 .. code-block::

              (high addr)
            _____ stack _____
            .     ...       .
            |  caller frame |
            .     ...       .
            |_______________|
            |               |
            |  return addr  |   <----- There's one!  Let's get it!
            |_______________|
            |               |
            |    locals     |
            |_______________|
              (low addr)

.. class:: handout instructor

 So we want to go after function pointers, like we said, there's one!

Exploiting like it is 1996!
===========================

.. class:: scrollable

 .. code-block::

              (high addr)
            _____ stack _____
            .     ...       .
            |  caller frame |
            .     ...       .
            |_______________|
            |               |
            |  return addr  |   
            |_______________|
            |               |  ^
            |   buf[10]     |  |
            |_______________|   \---- Overflow of buf
              (low addr)

.. class:: handout instructor

 The reason you can hit it with a buffer overflow is because your local
 variables are nearby on the stack frame for your vulnerable function.

Exploiting like it is 1996!
===========================

.. class:: scrollable

 .. code-block::

              (high addr)
            _____ stack _____
            .     ...       .
            |               |  ^
            |  <shellcode>  |  |
         /->|_______________|  |
         \  |               |  |
          \-|  <stack+4>    |  |
            |_______________|  |
            |               |  |
            |   buf[10]     |  |
            |_______________|   \---- Overflow of buf
              (low addr)

.. class:: handout instructor

 Because stacks grow downward in address space, when you write increasing
 addresses in your buffer you corrupt up the stack onto higher address
 elements such as the return address.  Back in the day, what you could do
 is simply write new machine code.  This was often called shellcode
 because the shortest most decisive thing you could do was to pop a
 shell.  In theory though, it could be any code.  You would then overwrite the
 return address to point to the stack itself causing your code to execute.

Exploiting like it is 2007!
===========================

.. class:: scrollable

 .. code-block::

              (high addr)
            _____ stack _____
            .     ...       .
            |               |
            |               |                      ^
            |               |                      |
            |               |                      |
            |               |                      |
            |               |                      |
            |               |                      |
            |               |                      | 
            |  <lib+0x100>  |    pop rdi           |
            |    <arg1>     |    ret               |
            |_______________|    ^                 |
            |               |    |                 |
            |  <lib+0x10>   |----/                 |
            |_______________|                      |
            |               |                      |
            |   buf[10]     |                      |
            |_______________|                       \---- Overflow of buf
              (low addr)

.. class:: handout instructor

 Then came along memory protections.  They simply disallow the stack as
 being a place where you can execute code.  So what hackers did was just
 use code that already exists.  In a sufficiently large binary, you can
 find these little bits of useful code that end in a return instruction.
 That way you can do something small that you want and be in the same
 logical position you were at the point of exploitation, namely returning
 to a controlled code pointer.  So here let's say we wanted to control
 the first argument in the standard POSIX calling convention.  The value
 would come from the stack which we controlled with our overflow and then
 we go to the next step.

Exploiting like it is 2007!
===========================

.. class:: scrollable

 .. code-block::

              (high addr)
            _____ stack _____
            .     ...       .
            |               |
            |               |                      ^
            |               |                      |
            |               |                      |
            |               |                      |
            |  <lib+0x1337> |    pop rsi           |
            |    <arg2>     |    ret               |
            |               |                      | 
            |  <lib+0x100>  |    pop rdi           |
            |    <arg1>     |    ret               |
            |_______________|    ^                 |
            |               |    |                 |
            |  <lib+0x10>   |----/                 |
            |_______________|                      |
            |               |                      |
            |   buf[10]     |                      |
            |_______________|                       \---- Overflow of buf
              (low addr)

.. class:: handout instructor

 Very simply, we just find another gadget that let's us control the
 next argument and once again, continue our paradigm.

Exploiting like it is 2007!
===========================

.. class:: scrollable

 .. code-block::

              (high addr)
            _____ stack _____
            .     ...       .
            |               |                                       
            |               |                      ^
            |  <lib+999>    |    pop RDX           |
            |    <arg3>     |    ret               |
            |               |                      |
            |  <lib+0x1337> |    pop rsi           |
            |    <arg2>     |    ret               |
            |               |                      | 
            |  <lib+0x100>  |    pop rdi           |
            |    <arg1>     |    ret               |
            |_______________|    ^                 |
            |               |    |                 |
            |  <lib+0x10>   |----/                 |
            |_______________|                      |
            |               |                      |
            |   buf[10]     |                      |
            |_______________|                       \---- Overflow of buf
              (low addr)

.. class:: handout instructor

 One more time for the third argument.
 

Exploiting like it is 2007!
===========================

.. class:: scrollable

 .. code-block::

              (high addr)
            _____ stack _____
            .     ...       .
            |  <mprotect>   |    (what will mprotect do at the end?)
            |               |                      ^
            |  <lib+999>    |    pop rdx           |
            |    <arg3>     |    ret               |
            |               |                      |
            |  <lib+0x1337> |    pop rsi           |
            |    <arg2>     |    ret               |
            |               |                      | 
            |  <lib+0x100>  |    pop rdi           |
            |    <arg1>     |    ret               |
            |_______________|    ^                 |
            |               |    |                 |
            |  <lib+0x10>   |----/                 |
            |_______________|                      |
            |               |                      |
            |   buf[10]     |                      |
            |_______________|                       \---- Overflow of buf
              (low addr)

.. class:: handout instructor

 And finally we "return" to the first instruction of the function we want
 to call.  The target function can't know the difference if we set it up
 just like it would expect.  Even better, it is going to execute a return
 instruction when its done, we we can keep exploiting!

 This particular function can change memory permissions so we can actually
 undo the mitigation that keeps us from injecting our own shellcode.
 
 This technique is called Return Oriented Programming, or ROP for short.  That
 is what you are going to need to do this week.
 

Learning Objectives
===================

#. Learn a little bit about a lot of tools and techniques.
#. Gain experience applying the same tactics you have been using on source code to disassembled binary.
#. Go beyond finding vulnerabilities into basic proof of concept exploit development.
#. Practice pair auditing and techniques for sharing information.

.. class:: handout instructor

 So last week we learned a little about RE and we found a bug.  This week
 you and your team are going to explore some of these exploitation
 concepts on your bug.  Follow the student guide and ask for help if you
 get stuck.  There are multiple ways to "win" on this assignment so
 get those creative juices flowing and see what you can come up with.
