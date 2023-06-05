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

Spot The Bug Template
=====================

.. code-block:: c
   :linenos:

   // This is where you should put the code.  Try to keep it brief yet include
   // the necessary context.  Alternatively, if you need to save space, explain
   // explicitly out of band if the students can make any assumptions that they
   // want such as types of variables or lengths of arrays

   printf("Buggy code goes here!");

**Context**

Put any non-code context or stuff that helps you keep the code short here such as:

 * The integer types don't matter.
 * You don't need to see the definition of the structs to see the bug.
 * The following variables are controlled ...
 * This code operates in a multi-threaded environment.
 * This code runs in kernel mode.
 * etc...

**Solution**

.. container:: toggle

 .. container:: toggle-header

    Show/Hide

 .. container:: toggle-body

    This section can be hidden by a click if you want to just link this page
    to your students.  Inside this section, you can either describe the bug and/or
    show the code again with highlighting to point out the flaws.

    .. code-block:: c
       :linenos:
       :emphasize-lines: 6

       // This is where you should put the code.  Try to keep it brief yet include
       // the necessary context.  Alternatively, if you need to save space, explain
       // explicitly out of band if the students can make any assumptions that they
       // want such as types of variables or lengths of arrays

       printf("Buggy code goes here!");

    If there articles related to the bug, link them here either for yourself
    so that you can send the URL to the students after the reveal, or just in-situ
    for the students to find if you give them this whole page.

    `Further Reading <../../ref/placeholder.html>`_ [`cached version <../../ref/placeholder.html>`_]
