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

.. _Squid_nonce:

Squid nonce processing 
======================

.. .. external

.. code-block:: c
   :linenos:

   struct _digest_nonce_h : public hash_link {
       digest_nonce_data noncedata;
       /* number of uses we've seen of this nonce */
       unsigned long nc;
       /* reference count */
       short references;
       /* the auth_user this nonce has been tied to */
       Auth::Digest::User *user;
       /* has this nonce been invalidated ? */
       struct {
           bool valid;
           bool incache;
       } flags;
   };

.. code-block:: c
   :linenos:
   :lineno-start: 100

   void authDigestNonceUnlink(digest_nonce_h * nonce)
   {
       assert(nonce != NULL);
       if (nonce->references > 0) {
           -- nonce->references;
       } else {
           debugs(29, DBG_IMPORTANT, "Attempt to lower nonce " << nonce << " refcount below 0!");
       }
       debugs(29, 9, "nonce '" << nonce << "' now at '" << nonce->references << "'.");
       if (nonce->references == 0)
           authenticateDigestNonceDelete(nonce);
   }
   

**Context**

 * ``digets_nonce_h`` objects can be created indiscriminately by an attacker opening connections.

**Solution**

.. container:: toggle

 .. container:: toggle-header

    Show/Hide

 .. container:: toggle-body

    .. code-block:: c
       :linenos:
       :lineno-start: 100
       :emphasize-lines: 5
       
       void authDigestNonceUnlink(digest_nonce_h * nonce)
       {
           assert(nonce != NULL);
           if (nonce->references > 0) {
               -- nonce->references;
           } else {
               debugs(29, DBG_IMPORTANT, "Attempt to lower nonce " << nonce << " refcount below 0!");
           }
           debugs(29, 9, "nonce '" << nonce << "' now at '" << nonce->references << "'.");
           if (nonce->references == 0)
               authenticateDigestNonceDelete(nonce);
       }

    The small width value ``references`` used to keep track of memory
    references to a ``digest_nonce_h`` object is easy to overflow causing a
    negative reference count.  The same code even notices that this condition
    can occur but does nothing other than warn about it.  With a choreographed
    authentication attempt, an attacker can cause one of these objects to be
    freed while other parts of the code still hold references to the object
    causing a use-after-free vulnerability.  An exploit was never made for
    this bug but it represents a common way that UAF bugs exist in the wild.

    `Further Reading <https://www.synacktiv.com/en/publications/memory-leak-and-use-after-free-in-squid.html>`_
    [`cached version <../../../ref/Squid_UAF.html>`_]





