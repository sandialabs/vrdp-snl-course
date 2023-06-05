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

.. _PHPImageColorMatch:

PHP gdImageColorMatch
=====================

.. .. external

.. code-block:: c
   :linenos:

   int gdImageColorMatch (gdImagePtr im1, gdImagePtr im2)
   {
           unsigned long *buf; /* stores our calculations */
           unsigned long *bp; /* buf ptr */
           int color, rgb;
           int x,y;
           int count;
  
           if( !im1->trueColor ) {
                   return -1; /* im1 must be True Color */
           }
           if( im2->trueColor ) {
                   return -2; /* im2 must be indexed */
           }
           if( (im1->sx != im2->sx) || (im1->sy != im2->sy) ) {
                   return -3; /* the images are meant to be the same dimensions */
           }
           if (im2->colorsTotal<1) {
                   return -4; /* At least 1 color must be allocated */
           }
  
           buf = (unsigned long *)safe_emalloc(sizeof(unsigned long), 5 * im2->colorsTotal, 0);
           memset( buf, 0, sizeof(unsigned long) * 5 * im2->colorsTotal );
  
           for (x=0; x<im1->sx; x++) {
                   for( y=0; y<im1->sy; y++ ) {
                           color = im2->pixels[y][x];
                           rgb = im1->tpixels[y][x];
                           bp = buf + (color * 5);
                           (*(bp++))++;
                           *(bp++) += gdTrueColorGetRed(rgb);
                           *(bp++) += gdTrueColorGetGreen(rgb);
                           *(bp++) += gdTrueColorGetBlue(rgb);
                           *(bp++) += gdTrueColorGetAlpha(rgb);
                   }
           }
           bp = buf;
           for (color=0; color<im2->colorsTotal; color++) {
                   count = *(bp++);
                   if( count > 0 ) {
                           im2->red[color]         = *(bp++) / count;
                           im2->green[color]       = *(bp++) / count;
                           im2->blue[color]        = *(bp++) / count;
                           im2->alpha[color]       = *(bp++) / count;
                   } else {
                           bp += 4;
                   }
           }
           gdFree(buf);
           return 0;
   }

**Context**

The attacker controls all relevant fields of ``im1`` and ``im2``.

**Solution**

.. container:: toggle

 .. container:: toggle-header

    Show/Hide

 .. container:: toggle-body

    .. code-block:: c
       :linenos:
       :emphasize-lines: 27,29,30,31,32,33,34

       int gdImageColorMatch (gdImagePtr im1, gdImagePtr im2)
       {
               unsigned long *buf; /* stores our calculations */
               unsigned long *bp; /* buf ptr */
               int color, rgb;
               int x,y;
               int count;
      
               if( !im1->trueColor ) {
                       return -1; /* im1 must be True Color */
               }
               if( im2->trueColor ) {
                       return -2; /* im2 must be indexed */
               }
               if( (im1->sx != im2->sx) || (im1->sy != im2->sy) ) {
                       return -3; /* the images are meant to be the same dimensions */
               }
               if (im2->colorsTotal<1) {
                       return -4; /* At least 1 color must be allocated */
               }
      
               buf = (unsigned long *)safe_emalloc(sizeof(unsigned long), 5 * im2->colorsTotal, 0);
               memset( buf, 0, sizeof(unsigned long) * 5 * im2->colorsTotal );
      
               for (x=0; x<im1->sx; x++) {
                       for( y=0; y<im1->sy; y++ ) {
                               color = im2->pixels[y][x];
                               rgb = im1->tpixels[y][x];
                               bp = buf + (color * 5);
                               (*(bp++))++;
                               *(bp++) += gdTrueColorGetRed(rgb);
                               *(bp++) += gdTrueColorGetGreen(rgb);
                               *(bp++) += gdTrueColorGetBlue(rgb);
                               *(bp++) += gdTrueColorGetAlpha(rgb);
                       }
               }
               bp = buf;
               for (color=0; color<im2->colorsTotal; color++) {
                       count = *(bp++);
                       if( count > 0 ) {
                               im2->red[color]         = *(bp++) / count;
                               im2->green[color]       = *(bp++) / count;
                               im2->blue[color]        = *(bp++) / count;
                               im2->alpha[color]       = *(bp++) / count;
                       } else {
                               bp += 4;
                       }
               }
               gdFree(buf);
               return 0;
       }

    The writers of this code plainly read a ``color`` value out of the
    ``im2`` pixels array and use it to index ``buf`` without checking that it
    is within the bounds.  If you missed this, ask yourself why.  Consider
    if you would have found it using an ACC log.

    .. code-block:: none

       | #ACC
       | Allocate: buf is allocated on line 22 based on im2->colorsTotal
       | Copy: Values are written to buf in a loop on line 31-34 after
       |       being offset by the color of the retrieved pixel.
       | Check: None exists!
       | Issues: There is protection on writing somewhat arbitrarily off the end
       |         of the buf array by a `color` sized amount.

    `Original article with more details including exploits
    <https://www.exploit-db.com/exploits/46677>`_
    [`cached version <../../../ref/PHP_imagecolormatch.html>`_]
