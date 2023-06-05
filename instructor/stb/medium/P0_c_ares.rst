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

.. _P0_c_ares:

Chrome OS - c-ares library
==========================

.. .. external

.. code-block:: c
   :linenos:

   void ares_create_query(const char *name, int dnsclass)
   {
     unsigned char *q;
     const char *p;
   
     /* Compute the length of the encoded name so we can check buflen. */
     int len = 0;
     for (p = name; *p; p++)
       {
         if (*p == '\\' && *(p + 1) != 0)
           p++;
         len++;
       }
     /* If there are n periods in the name, there are n + 1 labels, and
      * thus n + 1 length fields, unless the name is empty or ends with a
      * period.  So add 1 unless the name is empty or ends with a period.
      */
     if (*name && *(p - 1) != '.')
       len++;
   
     /* +1 for dnsclass below */
     q = malloc(len + 1);
   
     while (*name)
       {
         *q++ = /* ... label length, calculation omitted for brevity */;
         for (p = name; *p && *p != '.'; p++)
           {
             if (*p == '\\' && *(p + 1) != 0)
               p++;
             *q++ = *p;
           }
   
         /* Go to the next label and repeat, unless we hit the end. */
         if (!*p)
           break;
         name = p + 1;
       }
   
     *q = dnsclass & 0xff;
   }

**Context**

* ``name`` is controlled

**Solution**

.. container:: toggle

 .. container:: toggle-header

    Show/Hide

 .. container:: toggle-body

    .. code-block:: c
       :linenos:
       :emphasize-lines: 10,11,18,19,40

       void ares_create_query(const char *name, int dnsclass)
       {
         unsigned char *q;
         const char *p;
       
         /* Compute the length of the encoded name so we can check buflen. */
         int len = 0;
         for (p = name; *p; p++)
           {
             if (*p == '\\' && *(p + 1) != 0)
               p++;
             len++;
           }
         /* If there are n periods in the name, there are n + 1 labels, and
          * thus n + 1 length fields, unless the name is empty or ends with a
          * period.  So add 1 unless the name is empty or ends with a period.
          */
         if (*name && *(p - 1) != '.')
           len++;
       
         /* +1 for dnsclass below */
         q = malloc(len + 1);
       
         while (*name)
           {
             *q++ = /* ... label length, calculation omitted for brevity */;
             for (p = name; *p && *p != '.'; p++)
               {
                 if (*p == '\\' && *(p + 1) != 0)
                   p++;
                 *q++ = *p;
               }
       
             /* Go to the next label and repeat, unless we hit the end. */
             if (!*p)
               break;
             name = p + 1;
           }
       
         *q = dnsclass & 0xff;
       }

    Characters that are escaped as well as a trailing dot character are not counted
    when computing the ``len`` of the eventual allocation of the ``q`` buffer.  The
    character sequence ``\.`` at the end of ``name`` however will consume one byte of
    the buffer leaving nothing left over for the write of the ``dnsclass`` byte at the
    end of the function.  This causes a 1 byte overwrite of a known but uncontrolled value
    which happens to be exploitable!

    `Original article with more details including exploits
    <https://googleprojectzero.blogspot.com/2016/12/chrome-os-exploit-one-byte-overflow-and.html>`_
    [`cached version <../../../ref/P0_Chrome_OS_one_byte_overflow.html>`_]

