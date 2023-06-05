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

Redis VR
+++++++++++++

For this module we will again be looking at some source code with
no known bugs.  Redis is an in-memory database with a relatively solid
history for security.  That however, doesn't mean it is immune to bugs.
Maybe you can find a chink in its armor.

Use the techniques you learned in module 3 to decide where to start.
Discuss your choices with your instructor and get hunting!

.. only:: instructor

 .. admonition:: **Instructor Note**

  One downside to Redis is that it is a pretty solid code base.
  Unlike other open ended VR exercises like Exim, this source doesn't
  have a huge history of bugs.  There is one recent CVE regarding an
  integer overflow so it's not bulletproof.

  * `Advisory <https://github.com/redis/redis/releases/tag/6.2.4>`
  * `Diff <https://github.com/redis/redis/commit/e9a1438ac4c52aa68dfa2a8324b6419356842116>`
  * `Vulnerable Version 6.2.3 <https://github.com/redis/redis/blob/6.2.3/src/t_string.c>`

  The reason it was selected for this lab is simply because it
  uses a variety of types and therefore may lend itself to practicing
  some of the type conversion issues mentioned in the lecture.

  The exercise for this module gets changed out often.  So
  this can be used as is or as an example for substituting a
  different code base.  The selection criteria is really that:

  1. Has opportunity to notice C issues
  2. Does well with a bottom-up strategy
  3. Has potential for bugs

  It is hard to nail all three of those, but its worth continuing
  to look.  There is a lot of C code out there.

Getting the code
_____________________

The git repo for Redis is here:

`<https://github.com/redis/redis>`_


Ask your instructor which tag or commit to start auditing at so that
everyone is on the same code.

.. code::

 git clone https://github.com/redis/redis
 cd redis
 git checkout <tag_from_instructor>

