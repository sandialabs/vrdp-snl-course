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

.. Module 4 - Auditing Functions

.. include:: <s5defs.txt>
.. include:: custom.txt

.. header::

 UNCLASSIFIED

.. footer::

 UNCLASSIFIED

.. class:: title-slide

 Vulnerability Research Development Program
   :small:`Module 4`

   :small:`Auditing Functions`

.. class:: handout instructor

 These instructor call outs are a basic script for an example lecture.  They
 will oftentimes be specific to Sandia but can be a good guide for giving the
 lecture anywhere.

Last Module In Review
=====================

.. class:: incremental

  * All things control flow!
  * Looping, branching, special keywords, etc
  * Desk checking FTW!

.. class:: handout instructor

 Last time we talked a lot about the nitty gritty of control flow, especially
 loops and how programmers can twist themselves into knots with the ways they
 try to be clever about things.

 Hopefully by now you have seen enough desk checking to be convinced of its
 utility.  I know it's annoying to slow down, get out a piece of paper, figure
 out what you are going to track, etc.  But it really does super power your
 reasoning.  You are all smart people but your brain is just not good at
 keeping state around very accurately or for very long.  When you manifest
 things in the real world, you will reason better.  Its just true!

This Module - Overview
======================

.. class:: handout instructor

 This week we are going to keep adding to our bug vocabulary.  Functions are
 already the unit of things we have been looking at.  For the most part though,
 we have been tearing apart their insides. Now we are going to start
 considering what can go wrong with them as the focus of attention.

What are all the things that can go wrong with functions?

.. class:: tight-list

   * Return values are misinterpreted or ignored
   * Misunderstood argument meaning, relationships, or types
   * Side effects to arguments
   * Misunderstood relationships to other functions
   * Mismanagement of global state

.. class:: handout instructor

 Some of you may have already been considering things like return values.  For
 example, if you were doing more than the bare minimum in your function audit
 logs, you may have commented on the meaning of the return value or arguments
 to a function.  Try adding this to your process and see if it helps.

Return Value ``malloc`` Example
===============================

.. class:: handout instructor

 Here is a silly example of a common way that not checking a return value can
 cause a problem.

.. code-block:: c
   :number-lines:

   char * buf = malloc(len)
   ...
   memcpy(buf, src, len)

This will just dereference null and crash, but how different would it need to be interesting?

.. class:: handout instructor

 Here is a hint, in the long past, it was possible for a process to map the
 null page into memory.

 We are used to modern computers where a *null pointer dereference* will cause
 a crash but it was not always true.  If you could trick the program into using
 the first page in address space, what we now call the null page, then a mistake
 like this was much easier to exploit.  Now, the more common way to refer to
 this is called a *denial of service*.  If you can crash the process on demand,
 that is still potentially very bad, but not as bad as gaining arbitrary
 execution.

 These kinds of problems are common and sometimes they have a secondary utility.
 Imaging that you have a heap bug and to use it you need to groom the heap.  If
 your victim process is managed by a watchdog, crashing the process might not
 cause any harm and what you end up doing is resetting the heap to a more known
 state. 

\
===================

.. class:: handout instructor

 Some more, hopefully obvious wisdom from TAOSSA ...

.. .. external

*"Generally speaking, if a function call returns a value, as opposed to
returning nothing (such as a void function), a conditional statement should
follow each function call to test for success or failure."* -TAOSSA

See the reading for an example of an exploitable bug related to failure to
check return values.

.. class:: handout instructor

 This is also just a very simple mechanical thing to check.  If any function
 being called is non-void, what happens to its return value.  This can even be
 its own rereading pass if the function is complex enough to warrant it.

Return Value Misinterpretation
==============================

Misunderstood meaning

Misunderstood type *(we will go into this in more detail next module)*

.. class:: handout instructor

 Even if a return value is handled though, you should also be on the lookout
 to see if it is handled properly.  For a status code, does 0 mean success or
 failure? Is it the number of "things" read or the number of "bytes" read?

 You can also consider the types.  We are going to go into this a lot more next
 module but if you notice that the return types of the function and variable it
 is stored in are different, that should raise a red flag.

Misunderstood Meaning Example
=============================

.. class:: handout instructor

 Here is a classic case of misunderstanding the meaning of a return value.

.. class:: small

 .. code-block:: c
    :number-lines:

    #define SIZE(x,y) (sizeof(x) - ((y) - (x)))

    char buf[1024], *ptr;

    ptr += snprintf(ptr, SIZE(buf, ptr), "user: %s\n", user);
    ptr += snprintf(ptr, SIZE(buf, ptr), "pass: %s\n", pass);

.. class:: handout instructor

 What the code is attempting to do is serially put stuff into the buffer by
 using snprintf.  It is getting the bounds safety feature of snprintf correct
 but it is missing something very important.  The pointer is advanced after
 each call to snprintf to get it ready for the next write.  It advances it by
 the return value of snprintf which we can only assume by the intent of this
 code is the amount of bytes snprintf wrote, but is that what the return value
 actually is?

Selected Reading from ``man snprintf``
======================================

.. class:: handout instructor

 Let's take a look at the man page for snprintf ...

 *(as you read emphasize the phrase **would have been written**)*

.. .. external

.. class:: smaller

 .. code-block::

    RETURN VALUE
       Upon successful return, these functions return the number of
       characters printed (excluding the null byte used to end output
       to strings).

       The functions snprintf() and vsnprintf() do not write more than
       size bytes (including the  terminating  null byte ('\0')).  If
       the output was truncated due to this limit, then the return
       value is the number of characters (excluding the terminating
       null byte) which would have been written to the final string if
       enough space had been available. Thus, a return value of size
       or more means that the output was truncated.

.. class:: handout instructor

 So if there is enough room, the return value is as the programmers expect, the
 number of bytes that were in fact written.  But snprintf has this nice
 feature.  Because it can potentially truncate your format string due to
 running out of space, it needs a way to tell you that it did that.  If it
 returns **this** value, the amount it would like to write, it gives the caller
 an opportunity to do something different in the case the buffer got full, like
 reallocate more memory and try again.

 If you don't know this however, and you use it like they did in the previous
 code, you will end up increasing the pointer past the end of your allocation
 causing a buffer overflow.
 
Misunderstood Meaning MySQL ``memcmp`` Example
==============================================

.. class:: handout instructor

 Here is an real world example of a misunderstood return value.  Go look
 at ``man memcmp`` and see if you can see what is wrong.  Let's make this
 a mini spot the bug exercise.

.. .. external

.. class:: tiny

 .. code-block:: c
 
    typedef char my_bool;

    my_bool
    check_scramble(char *scramble_arg, char *message, uint8 *hash_stage2) {
        ...
        return memcmp(hash_stage2, hash_stage2_reassured, SHA1_HASH_SIZE);
    }

.. class:: tight-list

 .. class:: incremental

    * What is the meaning of memcmp return value?
    * One in 256 times, msql interpreted a non-zero value as true!
    * See the reading for details

.. class:: handout instructor

 As it turns out, ``memcmp`` will return a positive, negative, or zero value so
 that you can order memory.  It does not say however that those have to be any
 particular value.  As it turns out, on some implementations it can return a
 value that is positive or negative but whose least significant byte is still
 zero.  Because this function returns a single byte, it could truncate and
 still return 0, meaning success, even when the check function failed.  On
 MySQL, this mean that one out of 256 times on average, a random password when
 log you into the database successfully!


WCGW with Arguments?
====================

.. class:: handout instructor

 So we have talked about return value and there are a lot of similarities
 to things that can go wrong with arguments too, plus a few more.

.. class:: incremental

   * Type conversions
   * Assumptions/meaning of arguments

     .. class:: tight-list
     
        * (is this ``count`` var the number of bytes or the number of elements?)
        * (does the function assume a string is null terminated?)

   * Argument relationships
   * Side effects

.. class:: handout instructor

 You have already been identifying relationships between arguments and
 variables, now you can consider other things like meaning, side effects, etc.

Function Relatedness
====================

.. class:: handout instructor

 You have considered variable relationships but as it turns out, functions can
 also have relationships that are worth documenting.

.. class:: incremental

   * Should ``foo()`` be called before ``bar()``?
   * Should ``foo()`` and ``bar()`` always be called together (e.g. lock/unlock)?
   * What are the consequences of related functions not being used according to design?

.. class:: handout instructor

 You end up seeing this a lot with semaphores, reference counting, asynchronous
 behavior, etc.  The consequences are often very context dependent but for
 example, ``malloc`` and ``free`` are related but the consequences for failing
 to call them in tandem is simply a memory leak.  Other missed relationships can
 have more serious side effects when they are misused.  Keep this in mind for a
 spot the bug later.

Function Side Effects
=====================

.. class:: handout instructor

 Now we need to add some vocabulary so we can talk about side effects.

**Referentially Transparent** - Function is a stand in for its return

**Referentially Opaque** - Function causes side effects

.. class:: handout instructor

 A referentially transparent function you could call over and over again, with
 no changes to the program state.  A lot of code is referentially opaque
 because having side effects is often the point.  

 Referentially opaque functions however have a very complicated job of
 considering many extra factors and some of those factors may have to do with
 the safety of the program.

\
===========

.. class:: handout instructor

 One way in C/C++ to be more opaque is updates to either globals or 
 arguments.  If you ever see arguments being assigned to, or commented
 as OUT or IN/OUT, slow down and pay attention to what is going on.
 Here is some more wisdom from the book on this issue.

.. .. external

*"Vulnerabilities resulting from manipulating pass-by-reference arguments
can occur because the calling function's author neglects to account for
possibility of changes to the arguments, or the function can be made to
manipulate its arguments in an unanticipated or inconsistent fashion."* -TAOSSA

.. class:: handout instructor

 Let's see an example of this in action.

``realloc`` Example
===================

.. .. external

.. class:: scrollable

 .. code-block:: c
    :number-lines:

    int buffer_append(struct data_buffer *buffer, char *data),
                      size_t n)
    {
        if(buffer->size - buffer->used < n){
            if(!(buffer->data =
                 realloc(buffer->data, buffer->size+n)))
                return -1;
            buffer->size = buffer->size+n;
        memcpy(buffer->data + buffer->used, data, n);
        }
    
        buffer->used += n;
    
        return 0;
    }
    
    int read_line(int sockfd, struct data_buffer *buffer)
    {
        char data[1024], *ptr;
        int n, n1 = 0;
    
        for(;;){
            n = read(sockfd, data, sizeof(data)-1);
    
            if(n <= 0)
                return -1;
    
            if((ptr = strchr(data, '\n'))){
                n = ptr - data;
               n1 = 1;
            }
    
            data[n] = '\0';
    
            if(buffer_append(buffer, data, n) < 0)
                return -1;
    
            if(n1)
                break;
    
        }
    
        return 0;
    }
    
    int process_token_string(int sockfd)
    {
        struct data_buffer *buffer;
        char *tokstart, *tokend;
        int i;
    
        buffer = buffer_allocate();
    
        if(!buffer)
            goto err;
    
        for(i = 0; i < 5; i++){
            if(read_data(sockfd, buffer) < 0)
                goto err;
    
            tokstart = strchr(buffer->data, ':');
    
            if(!tokstart)
                goto err;
    
            for(;;){
                tokend = strchr(tokstart+1, ':');
    
                if(tokend)
                    break;
    
                if(readline(sockfd, buffer) < 0)
                    goto err;
            }
    
            *tokend = '\0';
    
            process_token(tokstart+1);
    
            buffer_clear(buffer);
        }
    
        return 0;
    
    err:
        if(buffer)
            buffer_free(buffer);
        return -1;
    }

.. class:: small

 TAOSSA Listing 7-30

.. class:: handout instructor

 (scroll through / highlight the code as you describe)

 * Here was have this ``buffer_append`` function but right away we see that
   this will do much more than just append. If what is intended to be appended
   wont fit, it will reallocate the backing buffer for you.  How nice!
 * Any time you see something like this, you can add a default hypothesis
   here.  The potential issue is that any existing references to data in the
   old buffer are now dead if this reallocation occurs.  These are called
   "stale" pointers and they can be quite dangerous.
 * Here we have the intermediate function ``read_line`` which takes input
   and continues to append to a passed in buffer until it hits a newline.
   This function should inherit the same problem as ``buffer_append``
   because it does nothing (in fact **can** do nothing) to mitigate the
   issue.
 * Finally here we are in the function where one of these buffer objects
   are born. Here we also see a manifestation of our hypothesis.  The variables
   ``tokstart`` and ``tokend`` both index into the backing buffer, totally
   unaware that the buffer might be ripped out from underneath them during a
   call to ``read_line``.  These can therefore become stale, in this case
   leading to a use after free situation.
 * What is more insidious about this case is that if ``read`` is pulling
   bytes from a network socket, often times an attack can control the timing of
   the execution by holding bytes back.  So an attacker can trigger those
   pointers going stale, perhaps manipulate the application to allocate new
   object in the old memory that was freed during the realloc, and then trigger
   a bug by releasing input to call ``process_token`` when everything is just
   right.  This is quite dangerous code.

Learning Objectives
===================

.. class:: handout instructor

 So once again we have some new things to look for to layer on top of what
 we have already been doing.  Our goals for this week are:

#. Understand some basic vulnerability patterns involving functions.
#. Practice auditing with function properties and relationships in mind.
#. Reinforce hypothesis generation and using bottom-up methodology.

.. class:: handout instructor

 Keep up with function audit logs and consider adding in sections for
 return values and arguments.  We will be checking to see if you are
 considering some of these things during feedback. Good luck!
