#!/usr/bin/python
#  Copyright 2022 National Technology & Engineering Solutions of Sandia, LLC
#  (NTESS).  Under the terms of Contract DE-NA0003525 with NTESS, the U.S.
#  Government retains certain rights in this software.
#
#  Redistribution and use in source and binary/rendered forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#   1. Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#   2. Redistributions in binary/rendered form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#   3. Neither the name of the copyright holder nor the names of its contributors
#      may be used to endorse or promote products derived from this software
#      without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# This file generates the index.html based on the slides that exist.

import glob

doc = \
"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>VRDP Course Slides</title>
  <script type="text/javascript" src="static/jquery.js"></script>
  <link rel="stylesheet" href="static/style.css" type="text/css" />
  <style>
    .portal {{
      display: inline-block;
      color: black;
      background: #2980B9;
      width: 100%;
      padding: 0;
      margin: .1em;
    }}

    .portal:hover {{
        border: 3px solid black;
        opacity: 1;
    }}
  </style>
</head>

<body>
  <div class="sidebar">
    <img src="static/SNL_Logo.png" class="logo" alt="Logo"/>
  </div>

  <div id="main">
    <h1> VRDP Course Slides </h1>
    <div style="margin: auto; width: 75%;">
{}
    </div>
    <footer>
      <hr/>
      <p> &copy; Copyright 2019, Sandia National Laboratories </p>
    </footer>
  </div>

</body>
</html>
"""

slide_fmt = "<a href=\"{}\"><div class=\"portal\"><h3>{}</h3></div></a>\n"

link_block = ""
for fname in sorted(glob.glob("*.rst")):
    # On Windows, open uses cp1252 by default; Sphinx pages are utf-8-sig
    with open(fname, "r", encoding="utf-8-sig") as f:
        header = f.readline()
        if header.startswith(".. "):
            link_block += slide_fmt.format(fname[:-3]+"html", header[3:].strip())
        else:
            raise ValueError("Invalid header in slide file {}".format(fname))

print(doc.format(link_block))
