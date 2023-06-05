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

.. _Linux_keyring:

Linux Keyring
=============

.. .. external

.. code-block:: c
   :linenos:

   long join_session_keyring(const char *name)
   {
          ...
          new = prepare_creds();
          ...
          keyring = find_keyring_by_name(name, false);
          if (PTR_ERR(keyring) == -ENOKEY) {
                  /* not found - try and create a new one */
                  keyring = keyring_alloc(
                          name, old->uid, old->gid, old,
                          KEY_POS_ALL | KEY_USR_VIEW | KEY_USR_READ | KEY_USR_LINK,
                          KEY_ALLOC_IN_QUOTA, NULL);
                  if (IS_ERR(keyring)) {
                          ret = PTR_ERR(keyring);
                          goto error2;
                  }
          } else if (IS_ERR(keyring)) {
                  ret = PTR_ERR(keyring);
                  goto error2;
          } else if (keyring == new->session_keyring) {
                  ret = 0;
                  goto error2;
          }
   
          /* we've got a keyring - now install it */
          ret = install_session_keyring_to_cred(new, keyring);
          if (ret < 0)
                  goto error2;
   
          commit_creds(new);
          mutex_unlock(&key_session_mutex);
   
          ret = keyring->serial;
          key_put(keyring);
   okay:
          return ret;
   
   error2:
          mutex_unlock(&key_session_mutex);
   error:
          abort_creds(new);
          return ret;
   }

**Context**

The functions ``find_keyring_by_name`` and ``key_put`` must be called in
sequence in order to maintain the reference count on the keyring.

**Solution**

.. container:: toggle

 .. container:: toggle-header

    Show/Hide

 .. container:: toggle-body

    .. code-block:: c
       :linenos:
       :emphasize-lines: 22

       long join_session_keyring(const char *name)
       {
              ...
              new = prepare_creds();
              ...
              keyring = find_keyring_by_name(name, false);
              if (PTR_ERR(keyring) == -ENOKEY) {
                      /* not found - try and create a new one */
                      keyring = keyring_alloc(
                              name, old->uid, old->gid, old,
                              KEY_POS_ALL | KEY_USR_VIEW | KEY_USR_READ | KEY_USR_LINK,
                              KEY_ALLOC_IN_QUOTA, NULL);
                      if (IS_ERR(keyring)) {
                              ret = PTR_ERR(keyring);
                              goto error2;
                      }
              } else if (IS_ERR(keyring)) {
                      ret = PTR_ERR(keyring);
                      goto error2;
              } else if (keyring == new->session_keyring) {
                      ret = 0;
                      goto error2;
              }
       
              /* we've got a keyring - now install it */
              ret = install_session_keyring_to_cred(new, keyring);
              if (ret < 0)
                      goto error2;
       
              commit_creds(new);
              mutex_unlock(&key_session_mutex);
       
              ret = keyring->serial;
              key_put(keyring);
       okay:
              return ret;
       
       error2:
              mutex_unlock(&key_session_mutex);
       error:
              abort_creds(new);
              return ret;
       }

    When a keyring is a duplicate, the function chooses to reuse an error path to
    execute the necessary cleanup code and return success.  Nevertheless, calling the
    necessary ``key_put`` is not a feature of that error path and it is left uncalled
    leading to a reference count bug which is exploitable.

    `Original article with more details including exploits
    <https://perception-point.io/analysis-and-exploitation-of-a-linux-kernel-vulnerability-2/>`_
    [`cached version <../../../ref/Linux_kernel_keyring_exploit.html>`_]


