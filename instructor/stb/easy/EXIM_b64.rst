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

.. _EXIM_b64:

EXIM base64decode
=================

.. .. external

.. code-block:: c
   :linenos:

   b64decode(const uschar *code, uschar **ptr)
   {
   int x, y;
   uschar *result = store_get(3*(Ustrlen(code)/4) + 1);
   
   *ptr = result;
   // perform decoding
   }

**Context**

* ``code`` is controlled.
* ``store_get`` is an allocator.
* You need to consider the decoder but the implementation details don't matter.
* We recommending reading the Base64 `Wikipedia <https://en.wikipedia.org/wiki/Base64>`_ page, 
  up to and including the section "Output padding". Here is a summary of that info:
  *When decoding Base64 text, four characters are typically converted back to
  three bytes. The only exceptions are when padding characters exist at the
  end of the encoded string. A single '=' indicates that the last four characters 
  will decode to only two bytes, while '==' indicates that the four characters 
  will decode to only a single byte.*
  
  *Without padding, after normal decoding of four characters to three bytes
  over and over again, fewer than four encoded characters may remain. In this
  situation only two or three characters shall remain. A single remaining
  encoded character is not possible (because a single Base64 character only
  contains 6 bits, and 8 bits are required to create a byte, so a minimum of 2
  Base64 characters are required: The first character contributes 6 bits, and
  the second character contributes its first 2 bits.)*

**Solution**

.. container:: toggle

 .. container:: toggle-header

    Show/Hide

 .. container:: toggle-body

    Let's use desk checking! The only thing to change is the length of ``code``
    
    * "Bytes needed (N)" is computed using the formula ``floor( len(code) * 6 / 8 )``
    * "Bytes computed (C)" is computed using the formula from the EXIM code, ``( floor( len(code)/4 ) * 3 ) + 1``

    ============= ================ ================== =====
    Ustrlen(code) Bytes needed (N) Bytes computed (C) C - N
    ============= ================ ================== =====
        0             0                     1           1
        1             0                     1           1
        2             1                     1           0
        3             2                     1           -1!
        4             3                     4           1
        5             3                     4           1
        6             4                     4           0
        7             5                     4           -1!
        8             6                     7           1
        9             6                     7           1
        10            7                     7           0
        11            8                     7           -1!
    ============= ================ ================== =====

    Once you understand the decoding behavior of base64, the bug is quite
    apparent using desk checking.  There is a mapping based on the number of
    input (6-bit) characters to output bytes.  4 input chars produces 3 bytes
    of output, 3 input chars produces 2 bytes, 2 produces 1, and 1 produces 0.
    The author of this code either assumed that the base64 input length would
    always be a multiple of 4 or would always be padded, and thus the math used
    to provide the allocation rounds down inappropriatly.  The result is an
    out-of-bounds write by one byte. Given carefully crafted input this is
    actually exploitable.

    `Original article with more details including exploits
    <https://devco.re/blog/2018/03/06/exim-off-by-one-RCE-exploiting-CVE-2018-6789-en>`_
    [`cached version <../../../ref/Exim_Off-by-one_RCE.html>`_]

