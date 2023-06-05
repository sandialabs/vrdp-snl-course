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

.. _python_sandbox:

Python Sandbox Escape
=====================

.. .. external

.. code-block:: c
   :linenos:

   NPY_NO_EXPORT PyObject *
   PyArray_Resize(PyArrayObject *self, PyArray_Dims *newshape, int refcheck,
           NPY_ORDER order)
   {
       // npy_intp is `long long`
       npy_intp* new_dimensions = newshape->ptr;
       npy_intp newsize = 1;
       int new_nd = newshape->len;
       int k;
       // NPY_MAX_INTP is MAX_LONGLONG (0x7fffffffffffffff)
       npy_intp largest = NPY_MAX_INTP / PyArray_DESCR(self)->elsize;
       for(k = 0; k < new_nd; k++) {
           newsize *= new_dimensions[k];
           if (newsize <= 0 || newsize > largest) {
               return PyErr_NoMemory();
           }
       }
       if (newsize == 0) {
           sd = PyArray_DESCR(self)->elsize;
       }
       else {
           sd = newsize*PyArray_DESCR(self)->elsize;
       }
       /* Reallocate space if needed */
       new_data = realloc(PyArray_DATA(self), sd);
       if (new_data == NULL) {
           PyErr_SetString(PyExc_MemoryError,
                   "cannot allocate memory for array");
           return NULL;
       }
       ((PyArrayObject_fields *)self)->data = new_data;

**Context**

No context needed

**Solution**

.. container:: toggle

 .. container:: toggle-header

    Show/Hide

 .. container:: toggle-body

    .. code-block:: c
       :linenos:
       :emphasize-lines: 13,25

       NPY_NO_EXPORT PyObject *
       PyArray_Resize(PyArrayObject *self, PyArray_Dims *newshape, int refcheck,
               NPY_ORDER order)
       {
           // npy_intp is `long long`
           npy_intp* new_dimensions = newshape->ptr;
           npy_intp newsize = 1;
           int new_nd = newshape->len;
           int k;
           // NPY_MAX_INTP is MAX_LONGLONG (0x7fffffffffffffff)
           npy_intp largest = NPY_MAX_INTP / PyArray_DESCR(self)->elsize;
           for(k = 0; k < new_nd; k++) {
               newsize *= new_dimensions[k];
               if (newsize <= 0 || newsize > largest) {
                   return PyErr_NoMemory();
               }
           }
           if (newsize == 0) {
               sd = PyArray_DESCR(self)->elsize;
           }
           else {
               sd = newsize*PyArray_DESCR(self)->elsize;
           }
           /* Reallocate space if needed */
           new_data = realloc(PyArray_DATA(self), sd);
           if (new_data == NULL) {
               PyErr_SetString(PyExc_MemoryError,
                       "cannot allocate memory for array");
               return NULL;
           }
           ((PyArrayObject_fields *)self)->data = new_data;

    The ``newsize`` varible is a signed 64 bit value.  It is intended to compute the
    new size of the array and because python arrays can have multiple dimensions, must make
    multiplicative increases in the size.  While the new value is checked against boundary
    conditions they fail to take into account the possiblity of integer overflow.  This
    creates a condition where the interpreter thinks it has an incredibly large array that
    is mapped to most of memory but is actually a very small allocation.  Normal python
    operations into that array therefore modify other memory locations.

    `Original article with more details including exploits
    <https://hackernoon.com/python-sandbox-escape-via-a-memory-corruption-bug-19dde4d5fea5>`_
    [`cached version <../../../ref/python_sandbox_escape.html>`_]

