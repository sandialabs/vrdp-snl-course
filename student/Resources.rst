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

.. _Resources:

Resources
=============

Books
---------

.. _taossa:

*The Art of Software Security Assessment*
+++++++++++++++++++++++++++++++++++++++++++++


.. figure:: _static/taossa.jpg
   :scale: 50%

   *Image from publisher www.awprofessional.com*

.. _mis:

*Make It Stick*
+++++++++++++++++++



.. figure:: _static/make_it_stick.jpg
   :scale: 50%

   *Image from publisher www.hup.harvard.edu*

Tools
---------

Snippet
+++++++

**Installing**

.. code:: text

 git clone git@gitlab.sandia.gov:Coyote/snippet.git
 cd snippet
 git checkout dev
 sudo apt install cscope exuberant-ctags libz-dev openjdk-8-jre \
   postgresql-server-dev-all build-essential \
   libxml2-dev libigraph0-dev python3-pip \
   python3-pyqt5 pyqt5-dev-tools qttools5-dev-tools
 pip3 install --upgrade pip --user
 pip3 install SQLAlchemy psycopg2 sklearn Pygments pyqt5 --user
 pip3 install python-igraph --user
 python3 setup.py install --user

**Using**

Creating and using a local repo:

.. code:: text

 > cd yoursourcecodedir
 > ctx init .

Creating and using a shared repo:

.. code:: text

 > cd yoursourcecodedir
 > ctx init . --project-dir yoursharedprojectdir


Ghidra
++++++

Download and install from `https://ghidra-sre.org <https://ghidra-sre.org>`_.

Comms
---------

Chat with your peers and me using Teams.


Reflections
---------------

Maintain reflections however you like. Since we are not all on the same systems, it is not as easy to have a single repo for the class.  Please email me your reflections on Fridays with the word "reflection" somewhere in the subject.


.. include:: Reading.rst

.. include:: Videos.rst
