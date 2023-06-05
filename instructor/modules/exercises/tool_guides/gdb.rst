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

.. _gdb:

GDB
=======

If you are learning GDB, most resources are not great for learning the
features of GDB you need for examining a binary without debug info.  This is a
good resource for the kinds of things you will need as a reverse engineer.
    
`UMD GDB Tutorial <http://users.umiacs.umd.edu/~tdumitra/courses/ENEE757/Fall15/misc/gdb_tutorial.html>`_
[`cached version <../../ref/gdb_tutorial.html>`__]
   
.. note::

   GDB by default does not save command history between sessions. Add the following
   to your ``~/.gdbinit`` file to turn it on.
 
   .. code::
 
    set history save on
    set history size 10000
    set history filename ~/.gdb_history

Most of the things you will need for VRDP are contained in that tutorial.
There are a few things however that missing:

 * The **backtrace** or **bt** command list the current stack trace at the
   point you have interrupted the program the addresses listed are the
   locations that will be returned to.

 * You can use registers in expressions.  For example ``x/100i $rip`` will
   work to disassemble starting a the current instruction pointer.  This is
   useful because sometimes the ``disassemble`` command doesn't work.

Remote Debugging 
---------------------

gdbserver is used to remotely attach to a debugger running on a different
device.  This is useful for embedded systems.  On the target device simply run either:

.. code::

  $ gdbserver <port> <binary>
  $ gdbserver <port> --attach <pid>
  
The on the client side, run gdb with a copy of the binary on the target
machine and connect:

.. code::

 $ gdb <binary>
 ...
 (gdb) target remote <ip>:<port>

Exercise
-------------

If you want to practice you gdb skills in isolation, try this.  Download the following
source code and compile it, but don't look!  Also, don't reverse engineer this little
program, try to answer some questions just with gdb.

Program: `muck_with_stdin.c <../../../_static/muck_with_stdin.c>`_

Once you compile the program run it in gdb as described below.  The program expects
input from stdin and the best way to do that is by giving it a file.  Throw a few dozen
recognizable characters in a text file as your input.

.. code::

 $ gcc muck_with_stdin.c
 $ strip a.out
 $ gdb a.out
 (gdb) r < input.txt

The code only has two functions that you can set breakpoints on, ``main``
and ``read``.  The goal will be to see if you can figure out how this program
"mucks" with stdin.  Also answer the following questions:

* What memory region is the output of ``read`` stored in?
* What is the return value of ``read``, what about the function that calls ``read``?

.. admonition:: Hint

 The first calls to ``read`` happen before main.  You may need to skip a few of those.

.. admonition:: Hint

 In POSIX, arguments are passed to functions in registers ``rdi``, ``rsi``,
 ``rcx``, and ``rdx``.  The return value of functions will be in the ``rax``
 register.

Try this yourself but you may click below to revel one way to do this.

.. container:: toggle

 .. container:: toggle-header

    Show/Hide

 .. container:: toggle-body

  Make some input, debug the program, break at ``read``, and run it.

  .. code::

    $ echo 'aaaaaaaaaaaaaaaaaaaaaaaaaaaa' > a.txt
    $ gdb a.out
    GNU gdb (Ubuntu 8.1.1-0ubuntu1) 8.1.1
    Copyright (C) 2018 Free Software Foundation, Inc.
    License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
    This is free software: you are free to change and redistribute it.
    There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
    and "show warranty" for details.
    This GDB was configured as "x86_64-linux-gnu".
    Type "show configuration" for configuration details.
    For bug reporting instructions, please see:
    <http://www.gnu.org/software/gdb/bugs/>.
    Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.
    For help, type "help".
    Type "apropos word" to search for commands related to "word"...
    Reading symbols from a.out...(no debugging symbols found)...done.
    (gdb) break read
    Breakpoint 1 at 0x580
    (gdb) run < a.txt
    Starting program: a.out < a.txt

    Breakpoint 1, __libc_read (fd=fd@entry=3, buf=0x7fffffff8bf8, nbytes=832) at ../sysdeps/unix/sysv/linux/read.c:27
    27	../sysdeps/unix/sysv/linux/read.c: No such file or directory.
    (gdb) bt
    #0  __libc_read (fd=fd@entry=3, buf=0x7fffffff8bf8, nbytes=832) at ../sysdeps/unix/sysv/linux/read.c:27
    #1  0x00007ffff7dd8c35 in open_verify (
        name=name@entry=0x7ffff7ffedd0 "/usr/lib/x86_64-linux-gnu/libgtk3-nocsd.so.0", fbp=fbp@entry=0x7fffffff8bf0, 
        loader=<optimized out>, whatcode=whatcode@entry=8, mode=mode@entry=67108864, 
        found_other_class=found_other_class@entry=0x7fffffff8bdf, free_name=false, fd=3) at dl-load.c:1742
    #2  0x00007ffff7ddc57e in _dl_map_object (loader=0x7ffff7ffe170, name=0x7fffffff9140 "libgtk3-nocsd.so.0", type=1, 
        trace_mode=trace_mode@entry=0, mode=<optimized out>, nsid=nsid@entry=0) at dl-load.c:2363
    #3  0x00007ffff7dd4305 in map_doit (a=a@entry=0x7fffffff9120) at rtld.c:591
    #4  0x00007ffff7deee4b in _dl_catch_exception (exception=exception@entry=0x7fffffff90b0, 
        operate=operate@entry=0x7ffff7dd42e0 <map_doit>, args=args@entry=0x7fffffff9120) at dl-error-skeleton.c:196
    #5  0x00007ffff7deeebf in _dl_catch_error (objname=objname@entry=0x7fffffff9110, 
        errstring=errstring@entry=0x7fffffff9118, mallocedp=mallocedp@entry=0x7fffffff910f, 
        operate=operate@entry=0x7ffff7dd42e0 <map_doit>, args=args@entry=0x7fffffff9120) at dl-error-skeleton.c:215
    #6  0x00007ffff7dd5568 in do_preload (where=0x7ffff7df5464 "LD_PRELOAD", main_map=0x7ffff7ffe170, 
        fname=0x7fffffff9140 "libgtk3-nocsd.so.0") at rtld.c:762
    #7  handle_ld_preload (preloadlist=<optimized out>, main_map=main_map@entry=0x7ffff7ffe170) at rtld.c:860
    #8  0x00007ffff7dd6e55 in dl_main (phdr=<optimized out>, phnum=<optimized out>, user_entry=<optimized out>, 
        auxv=<optimized out>) at rtld.c:1618
    #9  0x00007ffff7dedf50 in _dl_sysdep_start (start_argptr=start_argptr@entry=0x7fffffffa480, 
        dl_main=dl_main@entry=0x7ffff7dd5660 <dl_main>) at ../elf/dl-sysdep.c:253
    #10 0x00007ffff7dd5128 in _dl_start_final (arg=0x7fffffffa480) at rtld.c:414
    #11 _dl_start (arg=0x7fffffffa480) at rtld.c:521
    #12 0x00007ffff7dd4098 in _start () from /lib64/ld-linux-x86-64.so.2
    #13 0x0000000000000001 in ?? ()
    #14 0x00007fffffffacab in ?? ()
    #15 0x0000000000000000 in ?? ()

  Note that we are not at main. Use ``continue`` or ``c`` for short, until
  we get to a call to read that is after main.  You can check each time using
  ``backtrace`` or ``bt``.

  .. code::

    (gdb) c
    Continuing.

    Breakpoint 1, __libc_read (fd=fd@entry=3, buf=0x7fffffff9b38, nbytes=832) at ../sysdeps/unix/sysv/linux/read.c:27
    27	in ../sysdeps/unix/sysv/linux/read.c
    (gdb) c
    Continuing.

    Breakpoint 1, __libc_read (fd=fd@entry=3, buf=0x7fffffff99e8, nbytes=832) at ../sysdeps/unix/sysv/linux/read.c:27
    27	in ../sysdeps/unix/sysv/linux/read.c
    (gdb) c
    Continuing.

    Breakpoint 1, __libc_read (fd=fd@entry=3, buf=0x7fffffff99b8, nbytes=832) at ../sysdeps/unix/sysv/linux/read.c:27
    27	in ../sysdeps/unix/sysv/linux/read.c
    (gdb) c
    Continuing.
    [Thread debugging using libthread_db enabled]
    Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

    Breakpoint 1, __GI___libc_read (fd=0, buf=0x7fffffffa360, nbytes=42) at ../sysdeps/unix/sysv/linux/read.c:27
    27	../sysdeps/unix/sysv/linux/read.c: No such file or directory.
    (gdb) bt
    #0  __GI___libc_read (fd=0, buf=0x7fffffffa360, nbytes=42) at ../sysdeps/unix/sysv/linux/read.c:27
    #1  0x00005555555546cf in ?? ()
    #2  0x0000555555554752 in ?? ()
    #3  0x00007ffff77fcbf7 in __libc_start_main (main=0x55555555472a, argc=1, argv=0x7fffffffa488, init=<optimized out>, 
        fini=<optimized out>, rtld_fini=<optimized out>, stack_end=0x7fffffffa478) at ../csu/libc-start.c:310
    #4  0x00005555555545ca in ?? ()
    (gdb) break *0x00005555555546cf
    Breakpoint 2 at 0x5555555546cf
    (gdb) break *0x0000555555554752 
    Breakpoint 3 at 0x555555554752

  Once we think we are past main, set some breakpoints up the call stack
  to each return spot.  Let's look at how ``read`` was called.

  .. code::

    (gdb) info reg
    rax            0x7fffffffa360	140737488331616
    rbx            0x0	0
    rcx            0x555555554780	93824992233344
    rdx            0x2a	42
    rsi            0x7fffffffa360	140737488331616
    rdi            0x0	0
    rbp            0x7fffffffa340	0x7fffffffa340
    rsp            0x7fffffffa318	0x7fffffffa318
    r8             0x7ffff7bc7d80	140737349713280
    r9             0x7ffff7bc7d80	140737349713280
    r10            0x0	0
    r11            0x0	0
    r12            0x5555555545a0	93824992232864
    r13            0x7fffffffa480	140737488331904
    r14            0x0	0
    r15            0x0	0
    rip            0x7ffff78eb140	0x7ffff78eb140 <__GI___libc_read>
    eflags         0x202	[ IF ]
    cs             0x33	51
    ss             0x2b	43
    ds             0x0	0
    es             0x0	0
    fs             0x0	0
    gs             0x0	0

  It looks like it was called with 0 as the file handle (stdin),
  ``0x7fffffffa360`` as a destination buffer, and 42 a the size.  Let's see
  where that address is and what is in that buffer now.

  .. code::

    (gdb) info proc map 
    process 20450
    Mapped address spaces:

              Start Addr           End Addr       Size     Offset objfile
          0x555555554000     0x555555555000     0x1000        0x0 /home/a.out
          0x555555754000     0x555555755000     0x1000        0x0 /home/a.out
          0x555555755000     0x555555756000     0x1000     0x1000 /home/a.out
          0x7ffff73b8000     0x7ffff73d2000    0x1a000        0x0 /lib/x86_64-linux-gnu/libpthread-2.27.so
          0x7ffff73d2000     0x7ffff75d1000   0x1ff000    0x1a000 /lib/x86_64-linux-gnu/libpthread-2.27.so
          0x7ffff75d1000     0x7ffff75d2000     0x1000    0x19000 /lib/x86_64-linux-gnu/libpthread-2.27.so
          0x7ffff75d2000     0x7ffff75d3000     0x1000    0x1a000 /lib/x86_64-linux-gnu/libpthread-2.27.so
          0x7ffff75d3000     0x7ffff75d7000     0x4000        0x0 
          0x7ffff75d7000     0x7ffff75da000     0x3000        0x0 /lib/x86_64-linux-gnu/libdl-2.27.so
          0x7ffff75da000     0x7ffff77d9000   0x1ff000     0x3000 /lib/x86_64-linux-gnu/libdl-2.27.so
          0x7ffff77d9000     0x7ffff77da000     0x1000     0x2000 /lib/x86_64-linux-gnu/libdl-2.27.so
          0x7ffff77da000     0x7ffff77db000     0x1000     0x3000 /lib/x86_64-linux-gnu/libdl-2.27.so
          0x7ffff77db000     0x7ffff79c2000   0x1e7000        0x0 /lib/x86_64-linux-gnu/libc-2.27.so
          0x7ffff79c2000     0x7ffff7bc2000   0x200000   0x1e7000 /lib/x86_64-linux-gnu/libc-2.27.so
          0x7ffff7bc2000     0x7ffff7bc6000     0x4000   0x1e7000 /lib/x86_64-linux-gnu/libc-2.27.so
          0x7ffff7bc6000     0x7ffff7bc8000     0x2000   0x1eb000 /lib/x86_64-linux-gnu/libc-2.27.so
          0x7ffff7bc8000     0x7ffff7bcc000     0x4000        0x0 
          0x7ffff7bcc000     0x7ffff7bd2000     0x6000        0x0 /usr/lib/x86_64-linux-gnu/libgtk3-nocsd.so.0
          0x7ffff7bd2000     0x7ffff7dd1000   0x1ff000     0x6000 /usr/lib/x86_64-linux-gnu/libgtk3-nocsd.so.0
          0x7ffff7dd1000     0x7ffff7dd2000     0x1000     0x5000 /usr/lib/x86_64-linux-gnu/libgtk3-nocsd.so.0
          0x7ffff7dd2000     0x7ffff7dd3000     0x1000     0x6000 /usr/lib/x86_64-linux-gnu/libgtk3-nocsd.so.0
          0x7ffff7dd3000     0x7ffff7dfc000    0x29000        0x0 /lib/x86_64-linux-gnu/ld-2.27.so
          0x7ffff7fbb000     0x7ffff7fbf000     0x4000        0x0 
          0x7ffff7ff7000     0x7ffff7ffa000     0x3000        0x0 [vvar]
          0x7ffff7ffa000     0x7ffff7ffc000     0x2000        0x0 [vdso]
          0x7ffff7ffc000     0x7ffff7ffd000     0x1000    0x29000 /lib/x86_64-linux-gnu/ld-2.27.so
          0x7ffff7ffd000     0x7ffff7ffe000     0x1000    0x2a000 /lib/x86_64-linux-gnu/ld-2.27.so
          0x7ffff7ffe000     0x7ffff7fff000     0x1000        0x0 
          0x7ffffffda000     0x7ffffffff000    0x25000        0x0 [stack]
      0xffffffffff600000 0xffffffffff601000     0x1000        0x0 [vsyscall]
    (gdb) x/20c $rsi
    0x7fffffffa360:	1 '\001'	0 '\000'	0 '\000'	0 '\000'	0 '\000'	0 '\000'	0 '\000'	0 '\000'
    0x7fffffffa368:	-51 '\315'	71 'G'	85 'U'	85 'U'	85 'U'	85 'U'	0 '\000'	0 '\000'
    0x7fffffffa370:	64 '@'	59 ';'	-34 '\336'	-9 '\367'

  So ``0x7fffffffa360`` is clearly in range of the stack, this must be a
  stack buffer.  There looks to be garbage in it right now.  Now let's go see
  what the read returns.  Also move up and see what the next function returns.

  .. code::

    (gdb) c
    Continuing.

    Breakpoint 2, 0x00005555555546cf in ?? ()
    (gdb) info reg rax 
    rax            0x1d	29
    (gdb) c
    Continuing.

    Breakpoint 3, 0x0000555555554752 in ?? ()
    (gdb) info reg rax
    rax            0x1d	29

  It looks like read returned 29, which is the number of bytes we passed
  in!  The next function up also returns 29 so it must be passing through the
  return of read.  What happened to our input?

  .. code::

    (gdb) x/20c 0x7fffffffa360
    0x7fffffffa360:	97 'a'	63 '?'	97 'a'	63 '?'	97 'a'	63 '?'	97 'a'	63 '?'
    0x7fffffffa368:	97 'a'	63 '?'	97 'a'	63 '?'	97 'a'	63 '?'	97 'a'	63 '?'
    0x7fffffffa370:	97 'a'	63 '?'	97 'a'	63 '?'

  It looks like every other letter was replaced with a ``?`` character.
