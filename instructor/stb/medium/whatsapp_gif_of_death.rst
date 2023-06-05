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

.. _whatsapp_gif_of_death:

WhatsApp GIF of Death
=====================

.. .. external

.. code-block:: c
   :linenos:

   void DDGifSlurp(GifInfo *info, bool decode, bool exitAfterFrame) {
     GifRecordType RecordType;
     GifByteType *ExtData;
     int ExtFunction;
     GifFileType *gifFilePtr;
     gifFilePtr = info->gifFilePtr;
     uint_fast32_t lastAllocatedGCBIndex = 0;
     do {
       if (DGifGetRecordType(gifFilePtr, &RecordType) == GIF_ERROR && gifFilePtr->Error != D_GIF_ERR_WRONG_RECORD) {
         break;
       }
       bool isInitialPass = !decode && !exitAfterFrame;
       switch (RecordType) {
         case IMAGE_DESC_RECORD_TYPE:
   
           ...
   
           if (decode) {
             const uint_fast32_t newRasterSize = gifFilePtr->Image.Width * gifFilePtr->Image.Height;
             if (newRasterSize == 0) {
               free(info->rasterBits);
               info->rasterBits = NULL;
               info->rasterSize = newRasterSize;
               return;
             }
             const int_fast32_t widthOverflow = gifFilePtr->Image.Width - info->originalWidth;
             const int_fast32_t heightOverflow = gifFilePtr->Image.Height - info->originalHeight;
             if (newRasterSize > info->rasterSize || widthOverflow > 0 || heightOverflow > 0) {
               void *tmpRasterBits = reallocarray(info->rasterBits, newRasterSize, sizeof(GifPixelType));
               if (tmpRasterBits == NULL) {
                 gifFilePtr->Error = D_GIF_ERR_NOT_ENOUGH_MEM;
                 break;
               }
               info->rasterBits = tmpRasterBits;
               info->rasterSize = newRasterSize;
             }

             ...

           break;

        ...
   
       }
     } while (RecordType != TERMINATE_RECORD_TYPE);
   
     info->rewindFunction(info);
   }

**Context**

The attacker controls all relevant fields of ``info``.

**Solution**

.. container:: toggle

 .. container:: toggle-header

    Show/Hide

 .. container:: toggle-body

    .. code-block:: c
       :linenos:
       :emphasize-lines: 23, 39

       void DDGifSlurp(GifInfo *info, bool decode, bool exitAfterFrame) {
         GifRecordType RecordType;
         GifByteType *ExtData;
         int ExtFunction;
         GifFileType *gifFilePtr;
         gifFilePtr = info->gifFilePtr;
         uint_fast32_t lastAllocatedGCBIndex = 0;
         do {
           if (DGifGetRecordType(gifFilePtr, &RecordType) == GIF_ERROR && gifFilePtr->Error != D_GIF_ERR_WRONG_RECORD) {
             break;
           }
           bool isInitialPass = !decode && !exitAfterFrame;
           switch (RecordType) {
             case IMAGE_DESC_RECORD_TYPE:
       
               ...
       
               if (decode) {
                 const int_fast32_t widthOverflow = gifFilePtr->Image.Width - info->originalWidth;
                 const int_fast32_t heightOverflow = gifFilePtr->Image.Height - info->originalHeight;
                 const uint_fast32_t newRasterSize = gifFilePtr->Image.Width * gifFilePtr->Image.Height;
                 if (newRasterSize > info->rasterSize || widthOverflow > 0 || heightOverflow > 0) {
                   void *tmpRasterBits = reallocarray(info->rasterBits, newRasterSize, sizeof(GifPixelType));
                   if (tmpRasterBits == NULL) {
                     gifFilePtr->Error = D_GIF_ERR_NOT_ENOUGH_MEM;
                     break;
                   }
                   info->rasterBits = tmpRasterBits;
                   info->rasterSize = newRasterSize;
                 }

                 ...

               break;

            ...
       
           }
         } while (RecordType != TERMINATE_RECORD_TYPE);
       
         info->rewindFunction(info);
       }


    It is actually valid for the ``Image.Width`` or ``Image.Height``
    variable to either be zero or to overflow such that the result is zero.  The
    behavior of realloc when given zero is to become a free.  Because there are
    multiple record types to process in the GIF, ``the info->rasterBits`` can
    actually be double-freed leading to memory corruption that can be leveraged
    to achieve remote code execution.

    `Original article with more details including exploits
    <https://awakened1712.github.io/hacking/hacking-whatsapp-gif-rce>`_
    [`cached version <../../../ref/Double_free_WhatsApp_RCE.html>`_]

