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

.. _LIVE555:

Live555
===========

.. .. external

.. code-block:: c
   :linenos:

   void RTSPServer::RTSPClientConnection::handleRequestBytes(int newBytesRead) {
   [...]
       // The request was not (valid) RTSP, but check for a special case: HTTP commands 
       // (for setting up RTSP-over-HTTP tunneling):
      char sessionCookie[RTSP_PARAM_STRING_MAX];
      char acceptStr[RTSP_PARAM_STRING_MAX];
             *fLastCRLF = '\0'; // temporarily, for parsing
             parseSucceeded = parseHTTPRequestString(cmdName, sizeof cmdName,
                         urlSuffix, sizeof urlPreSuffix,
                         sessionCookie, sizeof sessionCookie,
                         acceptStr, sizeof acceptStr)
   
.. code-block:: c
   :linenos:
   :lineno-start: 100

   Boolean RTSPServer:: RTSPClientConnection::parseHTTPRequestString(char* resultCmdName,
   unsigned resultCmdNameMaxSize,
   char* eurlSuffix, unsigned urlSuffixMaxSize,
   char* sessionCookie, unsigned sessionCookieMaxSize,
   char* acceptStr, unsigned acceptStrMaxSize) { 
   
   [...]
   lookForHeader("x-sessioncookie", &reqStr[i], reqStrSize-i, sessionCookie, sessionCookieMaxSize);
   lookForHeader("Accept", &reqStr[i], reqStrSize-i, acceptStr, acceptStrMaxSize);
   
.. code-block:: c
   :linenos:
   :lineno-start: 200
   
   static void lookForHeader(char const* headerName, char const* source, unsigned
                             sourceLen, char* resultStr, unsigned resultMaxSize) {
     resultStr[0] = '\0'; // by default, return an empty string
     unsigned headerNameLen = strlen(headerName);
     for (int i = 0; i < (int)(sourceLen-headerNameLen); ++i) {
       if (strncmp(&source[i], headerName, headerNameLen) == 0 && source[i+headerNameLen] == ':') {
         // We found the header. Skip over any whitespace, then copy the rest of the line to "resultStr":
         for (i += headerNameLen+1; i < (int)sourceLen && (source[i] == ' ' || source[i] == '\t'); ++i) {} 
         for (unsigned j = i; j < sourceLen; ++j) {
           if (source[j] == '\r' || source[j] == '\n') {
             // We've found the end of the line. Copy it to the result (if it will fit):
             if (j-i+1 > resultMaxSize) break;
             char const* resultSource = &source[i];
             char const* resultSourceEnd = &source[j];
             while (resultSource < resultSourceEnd) *resultStr++ = *resultSource++;
             *resultStr = '\0';
             break;
           }
         }
       }
     }
   }

**Context**

 * ``reqStr`` is a controllable string and ``reqStrSize`` is its actual length.

**Solution**

.. container:: toggle

 .. container:: toggle-header

    Show/Hide

 .. container:: toggle-body

    .. code-block:: c
       :linenos:
       :lineno-start: 200
       :emphasize-lines: 5,12,15,17
       
       static void lookForHeader(char const* headerName, char const* source, unsigned
                                 sourceLen, char* resultStr, unsigned resultMaxSize) {
         resultStr[0] = '\0'; // by default, return an empty string
         unsigned headerNameLen = strlen(headerName);
         for (int i = 0; i < (int)(sourceLen-headerNameLen); ++i) {
           if (strncmp(&source[i], headerName, headerNameLen) == 0 && source[i+headerNameLen] == ':') {
             // We found the header. Skip over any whitespace, then copy the rest of the line to "resultStr":
             for (i += headerNameLen+1; i < (int)sourceLen && (source[i] == ' ' || source[i] == '\t'); ++i) {} 
             for (unsigned j = i; j < sourceLen; ++j) {
               if (source[j] == '\r' || source[j] == '\n') {
                 // We've found the end of the line. Copy it to the result (if it will fit):
                 if (j-i+1 > resultMaxSize) break;
                 char const* resultSource = &source[i];
                 char const* resultSourceEnd = &source[j];
                 while (resultSource < resultSourceEnd) *resultStr++ = *resultSource++;
                 *resultStr = '\0';
                 break;
               }
             }
           }
         }
       }

    The outer for-loop is responsible for matching the header name.  Then the inner
    for-loop reads until the end of the line and makes sure the header contents are less
    than ``resultMaxSize`` bytes.  The problem is that the break statment at the end of
    the copy only breaks out of the inner loop. Because the destination pointer is
    modified as part of the copy a second, duplicate header matched by the outer
    loop will **also** copy up to ``resultMaxSize`` bytes to where the destination
    pointer was left after the first copy, overflowing the allocated space.

    This can be a tricky bug to spot but is obvious when you use ACC logs with extended
    attributes for the copy section. An ACC log entry that makes this bug easier to spot
    might look like the following:

    .. code-block:: none

       | #ACC
       | Allocate: On lines 5 & 6, 2 RTSP_PARAM_STRING_MAX stack buffers are declared
       | Copy:
       |   Size: The size of the copy into the buffers is determined by the length
       |         of the input line minus the header. This is calcualted on line 211.
       |   Location: The copy occurs on line 214 in a while loop incrementing both
       |             the source and destination pointers.
       |   Frequency: The copy is inside of a nested for-loop. The copy can be
       |              triggered as many times as the outer loop matches the header.
       | Check: The check on line 211 makes sure a single match will fit into the
       |        declared size of the space.
       | Issues: Because the copy can happen multiple times, the check is
       |         insufficent for safeguarding the destination buffer if more than
       |         one header is present.



    `Further Reading <https://talosintelligence.com/vulnerability_reports/TALOS-2018-0684>`_
    [`cached version <../../../ref/Live555_stack_overflow.html>`_]




