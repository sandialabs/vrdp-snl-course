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

systemd VR
+++++++++++++++

If you search the internet for this bug, you will find it and it will
spoil the experience.  Stay away from articles discussing systemd CVEs
from prior to 2020.

This is the first module in VRDP and you may or may not know what to
look out for.  That is okay!  You should have come into this with some
programming experience and all programmers have dealt with debugging.  You
have also probably experienced those frustrating moments trying to hunt
down a bug that was evading you.  In this first exercise, what you are
being asked to do is to go into that mode but instead of hunting down
a misbehavior of a program you are trying to build, you are looking for
any **potential** misbehavior of a program that you don't know.  You are
also just trying to learn what the program does in general!

The name of the game is hypothesis generation.  Would you make the
same choices this programmer did if you were writing the program?  Why?
Did they make choices that concern you?  What could theoretically go wrong
if someone else tried to use this code and didn't understand some of
the assumptions they were making?  Are there any particularly fragile
assumptions that you can identify? All these kinds of questions and more
should rattle in your mind as you read the code.

Document what you find making sure to **at least** have one function
audit log per function you come across.  You can also document problems
or assumptions with structures, classes, macros, or anything else you think
is relevant. The most important thing is to follow the process, practice
active auditing, and give your instructors a baseline for any VR skills
you may already have.

.. only:: instructor

 .. admonition:: **Instructor Note**

  This lab is chance for students to find CVE-2018-15688, a 
  basic but subtle length check error leading to a heap overflow
  in systemd.
 
  There is not a lot of public information about this bug.
  As far as we know, there is no exploit for it but it is
  interesting because it sits in that middle ground of a simple
  overflow but not so obvious that students should find it very
  quickly.  You need to understand a little bit about DHCP
  messages, what you could control, or make very forward-thinking
  hypotheses about the vulnerable function if it is encountered
  in isolation.
 
  The github patch for this issue is
  `here <https://github.com/systemd/systemd/pull/10518>`__
 
  The patched version is commit 4dac5eaba4e419b29c97da38a8b1f82336c2c892

  The vulnerable version is commit 990668aa4cf04ea1c05791af97b1c05080378016
 
  Having this one bug to find is mainly for motivation and to
  have something to discuss at the end of the module. Really what you should
  be doing is making sure students are engaging with the code in a healthy
  way.  Do they have a plan on where to start?  Are they using function
  audit logs everywhere?  Are they making good hypotheses?

Getting the code
_____________________

The git repo for systemd is here
`https://github.com/systemd/systemd.git <https://github.com/systemd/systemd.git>`_
but you should be auditing at commit 990668aa4cf04ea1c05791af97b1c05080378016.

.. code::

 git clone https://github.com/systemd/systemd.git
 cd systemd
 git checkout 990668aa4cf04ea1c05791af97b1c05080378016

Where to start
___________________

systemd is sometimes a network client! To that end we will be looking for
bugs in some of its networking code.  One of the things it can do is act as
a DHCP client so let's see if there anything could be done to systemd by a
rogue DHCP server.  All of the following files are in
``systemd/src/libsystemd-network/``:

 * dhcp-protocol.h, dhcp6-protocol.h
 * dhcp-internal.h, dhcp6-internal.h
 * dhcp-identifier.c
 * dhcp-packet.c
 * dhcp-option.c, dhcp6-option.c
 * dhcp-network.c, dhcp6-network.c
 * sd-dhcp-client.c, sd-dhcp6-client.c

You are welcome to look at the files in whatever order you like based
on your instincts.  They are roughly listed in the order where you might
need to understand the code in one to fully understand the next but you
don't need to follow that if you don't want to.  The client can handle both
DHCPv4 and DHCPv6 addresses so consider both.

