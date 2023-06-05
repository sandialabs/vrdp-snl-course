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

.. _ropper:

Ropper 
==========

Ropper is a simple tool that helps you find gadgets in a binary.  Install
it with ``pip install ropper``.  It is a bit better to run ropper in its
interpreted mode.  Using `unknownlib.so <../../../_static/unknownlib.so>`_ as
a source binary, run ropper alone and the load the file after.

.. code::

 $ ropper
 (ropper)> file unknownlib.so
 [INFO] Load gadgets from cache
 [LOAD] loading... 100%
 [LOAD] removing double gadgets... 100%
 [INFO] File loaded.
 
 (unknownlib.so/ELF/x86_64)> search pop rbx
 [INFO] Searching for gadgets: pop rbx
 
 [INFO] File: unknownlib.so
 0x0000000000001fea: pop rbx; mov rax, qword ptr [rax + 0x28]; jmp rax; 
 0x000000000000301c: pop rbx; pop rbp; pop r12; mov rax, qword ptr [rax + 0x110]; mov esi, 0x13; jmp rax; 
 0x0000000000001d28: pop rbx; pop rbp; pop r12; pop r13; ret; 
 0x0000000000002062: pop rbx; pop rbp; pop r12; ret; 
 0x0000000000001e99: pop rbx; pop rbp; ret; 
 0x0000000000001cc4: pop rbx; ret; 
 
That's all there really is in terms of what you need for any exercises.
Feel free to play around with ropper and search for gadgets.

