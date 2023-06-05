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

.. _FLIC2:

FLIC Decoder (part 2)
=====================

.. .. external

.. code-block:: c
   :linenos:

   start_line = (data[0] + (data[1] << 8));
   lines = (data[2] + (data[3] << 8));
   if (start_line + lines > flxdec->hdr.height) {
     GST_ERROR_OBJECT (flxdec, "Invalid FLI packet detected. too many lines.");
     return FALSE;
   }
   data += 4;
 
   /* start position of delta */
   dest += (flxdec->hdr.width * start_line);
   start_p = dest;
 
   while (lines--) {
     /* packet count */
     packets = *data++;
 
     while (packets--) {
       /* skip count */
       guchar skip = *data++;
       dest += skip;
 
       /* RLE count */
       count = *data++;
 
       if (count > 0x7f) {
         /* literal run */
         count = 0x100 - count;
 
         if (skip + count > flxdec->hdr.width) {
           GST_ERROR_OBJECT (flxdec, "Invalid FLI packet detected. "
               "line too long.");
           return FALSE;
         }
 
         x = *data++;
         while (count--)
           *dest++ = x;


**Context**

 * Did the developers of the FLIC decoder properly fix their problems?

**Solution**

.. container:: toggle

 .. container:: toggle-header

    Show/Hide

 .. container:: toggle-body

    .. code-block:: c
       :linenos:
       :emphasize-lines: 17,20,23,29

	   start_line = (data[0] + (data[1] << 8));
	   lines = (data[2] + (data[3] << 8));
	   if (start_line + lines > flxdec->hdr.height) {
		 GST_ERROR_OBJECT (flxdec, "Invalid FLI packet detected. too many lines.");
		 return FALSE;
	   }
	   data += 4;
	 
	   /* start position of delta */
	   dest += (flxdec->hdr.width * start_line);
	   start_p = dest;
	 
	   while (lines--) {
		 /* packet count */
		 packets = *data++;
	 
		 while (packets--) {
		   /* skip count */
		   guchar skip = *data++;
		   dest += skip;
	 
		   /* RLE count */
		   count = *data++;
	 
		   if (count > 0x7f) {
			 /* literal run */
			 count = 0x100 - count;
	 
			 if (skip + count > flxdec->hdr.width) {
			   GST_ERROR_OBJECT (flxdec, "Invalid FLI packet detected. "
				   "line too long.");
			   return FALSE;
			 }
	 
			 x = *data++;
			 while (count--)
			   *dest++ = x;

    Let's use desk checking (assume remaining ``dest`` and ``width`` is 100 bytes):

    ======== =========== ======== ========= ==================== ==========
    Loop\@17 ``packets`` ``skip`` ``count`` ``skip+count>width`` Δ ``dest``
    ======== =========== ======== ========= ==================== ==========
        1         2        99        1            false             100 
        2         1        99        1            false           **200**
    ======== =========== ======== ========= ==================== ==========


    Multiple packets can each indicate a skip and as long as no individual skip
    plus count is larger than the width, there is still the ability to write past
    the end of the ``dest`` buffer.


    `Original article with more details including exploits
    <https://scarybeastsecurity.blogspot.com/2016/11/0day-poc-incorrect-fix-for-gstreamer.html>`_
    [`cached version <../../../ref/FLIC_gstreamer_incorrect_fix_scarybeasts.html>`_]

