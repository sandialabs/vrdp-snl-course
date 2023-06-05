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

.. _ZDI_libvorbis:

libvorbis
=========

.. .. external

.. code-block:: c
   :linenos:
   :lineno-start: 396

   /* decode vector / dim granularity guarding is done in the upper layer */
   long vorbis_book_decodev_add(codebook *book,float *a,oggpack_buffer *b,int n){
     if(book->used_entries>0){
       int i,j,entry;
       float *t;

       if(book->dim>8){
         for(i=0;i<n;){
           entry = decode_packed_entry_number(book,b);
           if(entry==-1)return(-1);
           t     = book->valuelist+entry*book->dim;
           for (j=0;j<book->dim;)
             a[i++]+=t[j++];
         }
       }else{
         for(i=0;i<n;){
           entry = decode_packed_entry_number(book,b);
           if(entry==-1)return(-1);
           t     = book->valuelist+entry*book->dim;
           j=0;
           switch((int)book->dim){
           case 8:
             a[i++]+=t[j++];
           case 7:
             a[i++]+=t[j++];
           case 6:
             a[i++]+=t[j++];
           case 5:
             a[i++]+=t[j++];
           case 4:
             a[i++]+=t[j++];
           case 3:
             a[i++]+=t[j++];


**Context**

All of the relevant members of ``book`` are controlled.


**Solution**

.. container:: toggle

 .. container:: toggle-header

    Show/Hide

 .. container:: toggle-body

    .. code-block:: c
       :linenos:
       :emphasize-lines: 8,12,13
       :lineno-start: 396

       /* decode vector / dim granularity guarding is done in the upper layer */
       long vorbis_book_decodev_add(codebook *book,float *a,oggpack_buffer *b,int n){
         if(book->used_entries>0){
           int i,j,entry;
           float *t;

           if(book->dim>8){
             for(i=0;i<n;){
               entry = decode_packed_entry_number(book,b);
               if(entry==-1)return(-1);
               t     = book->valuelist+entry*book->dim;
               for (j=0;j<book->dim;)
                 a[i++]+=t[j++];
             }
           }else{
             for(i=0;i<n;){
               entry = decode_packed_entry_number(book,b);
               if(entry==-1)return(-1);
               t     = book->valuelist+entry*book->dim;
               j=0;
               switch((int)book->dim){
               case 8:
                 a[i++]+=t[j++];
               case 7:
                 a[i++]+=t[j++];
               case 6:
                 a[i++]+=t[j++];
               case 5:
                 a[i++]+=t[j++];
               case 4:
                 a[i++]+=t[j++];
               case 3:
                 a[i++]+=t[j++];


    The nested looping structure starting on line 403 allows for ``i`` to be incremented
    farther than the loop counter is guarding against.  For a sufficiently large value of
    ``book->dim``, it is possible to get ``i`` to be larger than ``n``.  This causes an
    out-of-bounds write that is exploitable.

    `Original article with more details including exploits
    <https://www.thezdi.com/blog/2018/4/5/quickly-pwned-quickly-patched-details-of-the-mozilla-pwn2own-exploit>`_
    [`cached version <../../../ref/ZDI_Mozilla_Pwn2Own_Exploit.html>`_]
