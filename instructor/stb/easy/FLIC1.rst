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

.. _FLIC1:

FLIC Decoder (part 1)
=====================

.. .. external

.. code-block:: c
   :linenos:

   flx_decode_delta_fli (GstFlxDec * flxdec, guchar * data, guchar * dest)
   {
     ...
     /* use last frame for delta */
     memcpy (dest, flxdec->delta_data, flxdec->size);
   
     start_line = (data[0] + (data[1] << 8));
     lines = (data[2] + (data[3] << 8));
     data += 4;
   
     /* start position of delta */
     dest += (flxdec->hdr.width * start_line);
     start_p = dest;
   
     while (lines--) {
       /* packet count */
       packets = *data++;
   
       while (packets--) {
         /* skip count */
         dest += *data++;
   
         /* RLE count */
         count = *data++;
   
         if (count > 0x7f) {
           ...
         } else {
           /* replicate run */
           while (count--)
             *dest++ = *data++;

**Context**

 * `data` contains attacker controlled bytes.
 * Are there bugs in this code, if so how many?

**Solution**

.. container:: toggle

 .. container:: toggle-header

    Show/Hide

 .. container:: toggle-body

    .. code-block:: c
       :linenos:
       :emphasize-lines: 12,21,24

	   flx_decode_delta_fli (GstFlxDec * flxdec, guchar * data, guchar * dest)
	   {
		 ...
		 /* use last frame for delta */
		 memcpy (dest, flxdec->delta_data, flxdec->size);
	   
		 start_line = (data[0] + (data[1] << 8));
		 lines = (data[2] + (data[3] << 8));
		 data += 4;
	   
		 /* start position of delta */
		 dest += (flxdec->hdr.width * start_line);
		 start_p = dest;
	   
		 while (lines--) {
		   /* packet count */
		   packets = *data++;
	   
		   while (packets--) {
			 /* skip count */
			 dest += *data++;
	   
			 /* RLE count */
			 count = *data++;
	   
			 if (count > 0x7f) {
			   ...
			 } else {
			   /* replicate run */
			   while (count--)
				 *dest++ = *data++;

    It almost doesn't matter how large you can conceive ``dest`` to be, there are three ways to advance
    the dest pointer by user controlled amounts that are never checked for safety.

     * ``start_line`` is composed of 2 attacker controlled bytes.  Depending on
       what the header width is, the pointer can be advanced by varying
       multiples of MAX_SHORT.  If signedness is a factor, this can put you
       large distances relative to the starting location of `dest`
     * This format apparently allows you to skip by amount defined in the
       format.  Yet the amount to skip is never checked to be safe.
     * The amount of data to be copied is not checked to see if it will fit at the destination.

    `Original article with more details including exploits
    <https://scarybeastsecurity.blogspot.com/2016/11/0day-exploit-advancing-exploitation.html>`_
    [`cached version <../../../ref/FLIC_gstreamer_0day_and_exploit_scarybeasts.html>`_]

