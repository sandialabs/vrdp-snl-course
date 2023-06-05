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

MikroTik VR and Exploitation
+++++++++++++++++++++++++++++++++

If you search the internet for this bug, you will find it and it will
spoil the experience.  Stay away from articles discussing MikroTik CVEs
from 2018.

This module is designed to cover quite a lot of **breadth** on the topic
of binary VR and exploitation.  You will get a chance to touch a lot of tools
which the goal that it should give you a sense for when you should pick it up
off the shelf, how to use it in its basic mode, what what it might be more
capable of if you spent more time with it.  To truly become an expert at
any individual tool or phase of this process will require a lot more work
and practice.

.. only:: instructor

 .. admonition:: **Instructor Note**

  This lab was based on the following bug and related article.
 
  `Finding and exploiting CVE-2018–7445 (unauthenticated RCE in MikroTik’s RouterOS SMB)
  <https://medium.com/@maxi./finding-and-exploiting-cve-2018-7445-f3103f163cc1>`_
  [`cached version <../../../ref/Unauthenticated_RCE_in_MikroTik_RouterOS_SMB.html>`__]
 
  This lab is a little bit loose intentionally.  Part of being a good
  vulnerability researcher is looking into the ways that problems have been
  solved in the past and applying them to your situation.  Encourage students
  to figure things out for themselves as much as they can and provide
  hits or nudges in the right direction as necessary for time or if 
  someone is struggling.
 
  The first time we ran this lab, the students did the setup of the
  router VM themselves.  This may be a spot where you could save time by
  providing a ready-to-go VM assuming all the students have the same
  hypervisor (i.e. VMware).
 
  It is very useful to have a good in depth demo of Ghidra.  Many of these
  exist on the internet now but it comes best from the instructor and should
  especially highlight some of the skills needed to manage C++ nuances
  (i.e. the identification of vtables, creation of structures, etc). You should
  cover the same content that it is the :ref:`Ghidra <ghidra>` guide and use it as a
  reference for the students throughout the week.
 
  In addition to basic Ghidra knowledge, it is also useful to go into a
  little bit of C++ reverse engineering because unless they are clever enough to
  get around function indirection with debugging, they need to RE past some
  virtual functions to trace the bug up to the top.
 
  When it is time to find bugs, you should provide a list of functions to
  look at or encourage them to use the `Archaea <../../_static/Archaea.py>`_ script.
  The bug in this binary happens to be in a leaf function which lets you explore
  the concept of performing bottom-up analysis on the binary.  This puts the
  students into a familiar situation process-wise.  This isn't a class on
  reverse engineering so the story here is that we are using the bottom-up
  strategy.  The way we define "bottom" in the binary is to look at leaf
  functions.  The Archaea script lists functions by caller/callee counts and by
  size.  The last "interesting" column sorts by both callee counts plus size so
  you end up getting a list of the most substantial leaf functions.  
 
  The top 10 largest leaf functions are:
 
      * FUN_0804f93e
      * FUN_08054607
      * FUN_08054596
      * FUN_0804f2fc
      * FUN_080502d8
      * FUN_08053f52
      * FUN_08053fb8
      * FUN_08053eee
      * FUN_080537d8
      * FUN_0805646a
 
  The second of which is the buggy function. Remember this is a lab about
  breadth and therefore doing hardcore RE or binary VR is not the true goal.
  Don't let students struggle for too long on the bug hunt.  Encourage them to
  go back if they blow by it.
 
  This is also the time to encourage the combination of dynamic and static
  analysis.  For those who get stuck tracking the vulnerable function to data,
  you can at some point show them how to set breakpoints at virtual functions
  and watch them get hit with a normal packet.  That should get them over the
  hump.
 
  When it comes to exploitation give the students a chance to think of
  what they might do and have a discussion of what is possible.  At the end
  of the day, having control of the function pointer presents lots of options
  and the creative part of the lab is solve the problems depending on what
  you want to accomplish.
 
  No matter what, a solution will involve some kind of code-reuse attack.
  The lecture covers this somewhat but a nice alternate resource is the video
  at the end of the student guide.
 
  A couple of facts that are useful to gift to the students are the existence
  and use of the VDSO section of the binary.  The VDSO section contains the only source
  of gadgets allowing you to do a system call in this situation.  Getting a ROP
  payload to do a simple kernel system call, (i.e. call `exit(0)`) should be the
  low bar for success.
 
  For more enterprising students, you can either let them come up with
  something on their own or suggest using `mprotect` to enable shell code or to
  find they way into libc to use the `system` interface using the GOT.  In
  either case, some basic knowledge of reverse-shells, and the need to
  establish comms back to the attacking machine is a reasonable boost that
  doesn't spoil the exercise.

  Below are some reasonably good student solutions from the past.
  
  Basic system call to ``mprotect`` with a jump to a NOP sled and shellcode.
  Many students will probably implement something similar.

  .. container:: toggle
  
   .. container:: toggle-header
  
      Show/Hide
  
   .. container:: toggle-body

    .. include:: mikrotik_solution1.rst

  A more sophisticated call to ``mprotect`` after discovering that the
  exact location to the shellcode is able to be calculated based on
  references to objects at known locations.

  .. container:: toggle
  
   .. container:: toggle-header
  
      Show/Hide
  
   .. container:: toggle-body

    .. include:: mikrotik_solution2.rst

  Finding ``libc`` via the GOT and calling ``system``.

  .. container:: toggle
  
   .. container:: toggle-header
  
      Show/Hide
  
   .. container:: toggle-body

    .. include:: mikrotik_solution3.rst

Tool Guides
________________

This lab covers a lot of tools.  Many of these will be demonstrated in class but
basic guides with links to other resources for each tool can be found here:

.. toctree::
   :maxdepth: 1
   :glob:

   tool_guides/*

Setup
__________

Vulnerability researchers have been finding bugs in MikroTik routers for
a long time.  So much so that they have put together general information about
how to get started doing VR on MikroTik systems.  Start off the exercise by
creating a MikroTik environment following the steps at the *Making it rain* link below.
However, download the OS version and other tools using the links below first:

 * Download RouterOS version 6.40.5 (mikrotik-6.40.5.iso) from
   `this link <https://mikrotik.com/download/archive>`__
   [`local copy <../../_static/mikrotik-6.40.5.iso>`__] instead.
 * Get busybox from
   `here <https://busybox.net/downloads/binaries/1.30.0-i686/busybox>`__
   [`local copy <../../_static/busybox>`__].
 * Get the latest version of gdbserver from
   `here <https://github.com/rapid7/embedded-tools/tree/master/binaries/gdbserver>`__
   [`local copy <../../_static/gdbserver.i686>`__].
   *(upload this to your RouterOS VM the same time you do busybox, you will need it later.)*

`Make it rain with MikroTik <https://medium.com/tenable-techblog/make-it-rain-with-mikrotik-c90705459bc6>`_
[`cached version <../../../ref/Make_It_Rain_with_MikroTik.html>`__]

You will have to translate the steps if you are using VirtualBox.  However, here
are the basic steps in concept form if you don't want to follow the article:

 #. Create a small x86 VM, ~1GB disk, ~1GB ram
 #. Install using the mikrotik-6.40.5.iso
 #. Select all the packages to install using 'a', and then 'i'
 #. One it reboots post install, login with 'admin' and an empty password
 #. Setup DHCP ``ip dhcp-client add interface=ether1 disabled=no``
 #. Get its new IP ``ip dhcp-client print detail``
 #. On another machine FTP over busybox and gdbserver
 #. Shutdown the MikroTik VM ``system shutdown``
 #. Change the boot disk to some other Linux live CD
 #. Boot into the live CD, mount the MikroTik hard drives
 #. In a root terminal find the disk that has a ``./rw/pckg`` directory
 #. Change into that directory and alter the permissions for busybox and gdbserver ``chmod +x <binary>``
 #. Move to the ``./rw`` folder, add the following contents to a file called DEFCONF:
    ``ok; /rw/disk/busybox telnetd -l /bin/sh -p 1270;``
 #. Unmount the disks and reboot from the hard drive
 #. Telnet into the MikroTik VM (should be the same IP as before)
 #. Execute command using busybox ``/rw/disk/busybox whoami``
 #. **Take a snapshot of your VM at this point!**

The changes you make to the DEFCONF file do not persist across multiple
reboots.  If your VM crashes, it had a tendency to become unstable because
of the changes you made.  It is a very good idea to use the snapshot feature
of your hypervisor to avoid this.  If you don't have a snapshot feature,
don't boot it after creating the DEFCONF file.  Instead, shutdown the
VM, copy the disk to a backup, then boot it up for the first time.  If you
ever wreck your Mikrotik VM, simply replace the disk image and try again.

Explore RouterOS and SMB
_____________________________

For this lab you will be looking at the SMB service.  Explore the RouterOS
`documentation <https://wiki.mikrotik.com/wiki/Manual:TOC>`__ and see if you can
figure out how to enable it.  You do not need to setup any shared folders.  Simply
turning the service on and making the port available is enough.  **Consider
taking another snapshot of your VM at this point.**

.. only:: instructor

 .. admonition:: **Instructor Note**

   Enable smb with ``ip smb set enabled=yes``

Learn how to talk to SMB
_____________________________

Try talking to the smb service using ``smbclient``.  The ``-L`` flag asks
to list the available shares on a server.  Try ``smbclient -L \\\\<ipaddr>``.
Even if you don't have any shares setup, you should get a valid response from
the Mikrotik VM.  Capture the traffic using wireshark and duplicate the initial
message using python sockets instead.  You will need this later to talk to the
service in a programmatic way.

Here is a basic form of a python script to communicate to a TCP service:

.. code:: python

    import socket
    import sys
    import hexdump
    import struct

    payload = b"\x ... some bytes " # Literal payload bytes
    payload += struct.pack("iii", 1, 2, 3) # Or use struct.pack to format
    with open('http.bin', 'rb') as f: # Or read a payload in from a file
        payload = f.read()
 
    if len(sys.argv) != 2:
        print("{} <ip>".format(sys.argv[0]))
        sys.exit(1)
    
    ip = sys.argv[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    print("Sending:")
    hexdump.hexdump(payload)
    
    s.connect((ip,8080))
    s.sendall(payload)
    
    data = s.recv(1000)
    print("Received:")
    hexdump.hexdump(data)


.. only:: instructor

 .. admonition:: **Instructor Note**

  While running under wireshark, just use ``smbclient -L \\\\<ipaddr>``
  to talk to the service.  If you filter on smb messages, the bytes of a Negotiate Protocol packet
  should be enough to emulate what ``smbclient`` is doing.

Investigate the smb binary
_______________________________

Use ``binwalk`` to extract the ``smb`` binary from the RouterOS iso file.

.. only:: instructor

 .. admonition:: **Instructor Note**

  ``binwalk -e mikrotik-6.40.5.iso``

Load the binary into Ghidra and explore it using the guidance from your
instructor.  Look for bugs!  

You might get some mileage out of this experimental Ghidra script called
`Archaea <../../_static/Archaea.py>`_.  Your instructor should go over this with
you in class.

.. only:: instructor

 .. admonition:: **Instructor Note**

   Just drop the file in ``ghidra_scripts`` and run
   it from the script manager.  It should pop a window where you can sort the
   functions according to various statistics.  The **interesting** statistic
   is the one that works the best but it is also tailored to this bug.  Make
   sure to discuss the pros and cons of frequently called vs not-frequently
   called functions.

You should find a bug relatively quickly.  If you don't, speak up and let's
figure out why not.

Trigger the bug
____________________

Use a combination of gdbserver, your knowledge of the bug, and your ability to 
talk to the service over python sockets to craft a trigger for the bug.  Start
with the message replays you built with python sockets.  What do you need to alter
to change the course of execution toward the target function?

It is easier to run ``smb`` by hand.  Find and kill the default process with
``/rw/disk/busybox ps`` and then ``kill <pid>``.  You can run it with
``/nova/bin/smb`` or under gdb ``/rw/disk/gdbserver :1234 /nova/bin/smb``.  If you
attach to the gdbserver, make sure to give it a copy of ``smb`` that you fished
out using binwalk with ``gdb ./smb`` and then ``target remote <ip>:1234`` once at
the gdb prompt.

Exploitation
_________________

What kind of challenges are necessary to overcome to successfully exploit this bug?
Use the ``checksec`` tool to figure out what mitigations are present in this binary.

`Checksec website <http://www.trapkit.de/tools/checksec.html>`_
[`checksec.sh script <../../_static/checksec.sh>`_]

.. note::

  Make sure to explore the rest of the Mikrotik system.  Is there anything else
  that already exists there that might help you exploit the system?

Transform your trigger into a fully fledged exploit using guidance from your instructor.
You may find the following resources helpful in addition to the lecture.  You may need more
or less of this depending on how ambitious you are with your exploit goals.


* `Intro to ROP <https://www.youtube.com/watch?v=XZa0Yu6i_ew>`_
* `Guide to Linux System Calls <https://blog.packagecloud.io/eng/2016/04/05/the-definitive-guide-to-linux-system-calls>`_
  [`cached version <../../../ref/Definitive_Guide_Linux_System_Calls.html>`__]
* `List of Linux System Calls <https://man7.org/linux/man-pages/man2/syscalls.2.html>`_
  [See ``man syscalls`` for offline or non-web copy]
* `Understanding Reverse Shells <https://www.netsparker.com/blog/web-security/understanding-reverse-shells>`_
  [`cached version <../../../ref/Understanding_Reverse_Shells.html>`__]
* `GOT and PLT for pwning <https://systemoverlord.com/2017/03/19/got-and-plt-for-pwning.html>`_
  [`cached version <../../../ref/GOT_and_PLT_for_pwning.html>`__]
* `MSFVENOM <https://www.offensive-security.com/metasploit-unleashed/msfvenom/>`_
  [`cached version <../../../ref/MSFvenom.html>`__]

