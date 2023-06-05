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

.. Module 3 - Auditing Control Flow

.. include:: <s5defs.txt>
.. include:: custom.txt

.. header::

 UNCLASSIFIED

.. footer::

 UNCLASSIFIED

.. class:: title-slide

 Vulnerability Research Development Program
   :small:`Module 3`

   :small:`Auditing Control Flow`

.. class:: handout instructor

 These instructor call outs are a basic script for an example lecture.  They
 will often times be specific to Sandia but can be a good guide for giving the
 lecture anywhere.

Last Module In Review
=====================

.. class:: incremental

  * Variable initialization
  * Variable relationships
  * Structure member relationships / padding

.. class:: handout instructor

 So last time we started with some thing to look for.  Initialization,
 relationships, and structure issues. The next two modules were are going to
 slowly keep adding to that *vocabulary* of potential issues in the C language.
 Bear in mind, these are still processes that you can use in many VR
 situations not just for C.

This Module - Overview
======================

.. class:: handout instructor

 This module is going to be all about control flow.

What are all the things that can go wrong with control flow?

* Looping constructs
* Branching paths
* Order of operations
* ``switch`` and ``goto`` weirdness

.. class:: handout instructor

 You have been following control flow all along but perhaps in a less rigorous
 way than you could be.  Control flow is hard because every time you make a
 branch, you have doubled the potential number of paths through a piece of code.
 Because it is difficult for you to reason about, it means it is also difficult
 for programmers to reason about.  So you should isolate instances of complex
 control flow and really examine them for bug potential.

WCGW with loops?
================

.. class:: handout instructor

 Even though any control flow mechanism can introduce bugs, we are going to
 focus a lot on loops because they can be complicated and they often work over
 memory that we are concerned with in terms of safety.

 Here are some questions you can ask any time you come across a reasonably complex
 loop.

.. class:: tight-list

 .. class:: incremental

    * Does the loop fully cover or over cover the allocation of memory it is working on?
    * Do loop control variables get modified in the body of the loop?
    * Do the uses of loop interruption commands (e.g. break) make sense for all possible paths?
    * Are there pretest or posttest issues?
    * Are there "too-clever" use of loop semantics (e.g. assignment inside of check)?
    * Is punctuation and indentation okay?

A Very Simple Example 
=====================

.. class:: handout instructor

 This very simple function from the book is mainly something I want to point
 out because this is as simple as it can get and be somewhat interesting.  This
 is basically ``strcpy`` but you should be able to look at a loop like this
 and quickly identify a couple of things.

.. .. external

.. class:: small

 .. code-block:: c
    :number-lines:
 
    int copy(char *dst, char *src)
    {
        char *dst0 = dst;
    
        while(*src)
            *dst++ = *src++;
    
        *dst++='\0';
    
        return dst - dst0;
    }

.. class:: tiny

   TAOSSA Listing 7-15, pg 328

.. class:: handout instructor

 First, you should notice that this is both reading and writing memory, so the
 loop is interesting from a security perspective.  Second, the loop control
 variable, is modified in the body of the loop.  So you should be on the look
 out for ways to invalidate the intent of the loop check.  For example, in 
 a similar loop, you might wonder if you could skip over the nul-byte and
 therefore copy more memory than is expected.  Last, you might consider what
 happens if the loop never runs at all.  Is it always safe to write the
 nul-byte as it does in that last step? Did the programmer assume that the
 loop will always execute once?  If so, why didn't they use a do-while
 construct?

 Whose responsibility is it to make sure this copy is safe?

Auditing Tip #1
===============

.. class:: handout instructor

 This should be obvious, but just to highlight something from the textbook
 in case it is not.

.. .. external

.. class:: small

 *"When data copies in loops are performed with no size validation, check
 every code path leading to the dangerous loop and determine whether it can be
 reached in such a way that the source buffer can be larger than the destination
 buffer."* -TAOSSA
 
 This is fancy textbook language for: *"consider all paths when desk checking."*
 
 This is also an automatic hypothesis whenever there is no explicit size limitation.

Auditing Tip #2
===============

.. class:: handout instructor

 Also ...

.. .. external

.. class:: small

 *"Mark all the conditions for exiting a loop as well as all variables
 manipulated by the loop.  Determine whether any conditions exist in which
 variables are left in an inconsistent state. Pay attention to places where the
 loop is terminated because of an unexpected error, as these situations are more
 likely to leave variables in an inconsistent state."* -TAOSSA

 More fancy words for desk checking!  As part of desk checking, make sure
 you understand what loop elements have restrictions on their safety.  Loops
 also create variable relationships and constraints.

A Slightly More Complex Example 
===============================

.. .. external

.. class:: tiny 

 .. code-block:: c
    :number-lines:

    char npath[MAXPATHLEN];
    int i;

    for (i = 0; *name != '\0' && i < sizeof(npath) - 1;
         i++, name++) {
        npath[i] = *name;
        if (*name == '"')
            npath[++i] = '"';
    }
    npath[i] = '\0';

.. class:: tiny

   TAOSSA Listing 7-20, pg 333

.. class:: handout instructor

 Based on what we have already discussed,  you should have some suspicions
 about this loop.  Clearly there is memory manipulation happening and there is
 complexity around the loop control variables and the branching paths within
 the loop.  If you don't see the problem right away, this is a time for
 desk checking!

Desk Checking a Loop
====================

.. class:: tiny 

 .. code-block:: c
    :number-lines:

    char npath[MAXPATHLEN];
    int i;

    for (i = 0; *name != '\0' && i < sizeof(npath) - 1;
         i++, name++) {
        npath[i] = *name;
        if (*name == '"')
            npath[++i] = '"';
    }
    npath[i] = '\0';

 .. class:: center

    === ========== ==============
     i   name=foo   npath(writes)
    === ========== ==============
     0      f          0 <- f
     1      o          1 <- o
     2      o          2 <- o
     3                 3 <- 0
    === ========== ==============

.. class:: handout instructor

 This is just another way to desk check.  Instead of line numbers you can track
 loop iterations.  In this case we will try it with an innocuous input.
 Nothing strange happens but then again, we aren't exercising all of the
 control flow paths.


Desk Checking a Loop
====================

.. class:: tiny 

 .. code-block:: c
    :number-lines:

    char npath[MAXPATHLEN];
    int i;

    for (i = 0; *name != '\0' && i < sizeof(npath) - 1;
         i++, name++) {
        npath[i] = *name;
        if (*name == '"')
            npath[++i] = '"';
    }
    npath[i] = '\0';

 .. class:: center

    ==== ============ ===================
     i    name=ab"cd   npath(writes)
    ==== ============ ===================
     0        a         0 <- a
     1        b         1 <- b
     2,3      "         2 <- ", 3 <- "
     4        c         4 <- c
     5        d         5 <- d
     6                  6 <- 0
    ==== ============ ===================

.. class:: handout instructor

 Next let's try an input that forces control flow down one of the paths.  As you
 can see down some paths, a single loop iteration will do a lot of work and
 might give you a hint on a pathological case to desk check.

Desk Checking a Loop
====================

.. class:: tiny 

 .. code-block:: c
    :number-lines:

    char npath[MAXPATHLEN];
    int i;

    for (i = 0; *name != '\0' && i < sizeof(npath) - 1;
         i++, name++) {
        npath[i] = *name;
        if (*name == '"')
            npath[++i] = '"';
    }
    npath[i] = '\0';

 .. class:: center
 
    ======== ========================= ======================
     i         name=a{xMAXPATHLEN-2}"     npath(writes)
    ======== ========================= ======================
     0        a                         0 <- a
     1        a                         1 <- a
     n        a                         n <- a
     MPL-2    a                         MPL-2 <- a
     MPL-1    "                         MPL-1 <- ", MPL <- "
     MPL+1                              MPL+1 <- 0
    ======== ========================= ======================

.. class:: handout instructor

 Here we are desk checking somewhat symbolically.  If we wait until we are at
 the end of a MAXPATHLEN string before we introduce the control character, in
 this case a quote, the *extra* work that happens down that path will take the
 loop control variables past where they should go.  The final write to
 ``npath`` will therefore be out of bounds by 1.

Pretest/Posttest Example 
========================

.. .. external

.. code-block:: c
   :number-lines:

   char *cp = get_user_data();
   
   ...
   
   do {
       ++cp;
   } while (*cp && *cp != ',');

.. class:: handout instructor

 Really this is just a normal case of a use-before-check problem.  It is the
 same as it would be in an uninitialized memory situation.  The only novelty
 here is that it is somewhat hidden in the loop construct.  Whenever you see
 a posttest, you should just lookout for this possibility.

.. class:: tiny

   TAOSSA Listing 7-21, pg 334

Flow Transfer Statements
========================

.. class:: handout instructor

 Now how many times in your programming life have you confused ``break`` vs
 ``continue`` vs ``next`` in other languages.  This happens all the time
 although it rarely makes it into production.  Then there the **spooky**
 keyword we were taught to never use called ``goto``.  Turns out it is used a
 lot in some important code.  All of these have potential problems that you
 can look out for though.

What can go wrong with ``break``, ``continue``, or ``goto``?

* They are forgotten.
* They are confused between each other
* Nested loops obscure what you are breaking out of
* ``switch`` statement fall-through
* Generic ``goto`` insanity

Silly Yet Famous ``goto`` Example 
=================================

.. class:: handout instructor

 Here is a famous bug that was so bad it has its own place in hacker history.
 It is called **goto fail** which has kind of a double meaning in this case.

.. .. external

.. class:: scrollable

 .. code-block:: c
    :number-lines:

    static OSStatus
    SSLVerifySignedServerKeyExchange(SSLContext *ctx, bool isRsa, SSLBuffer signedParams,
                                     uint8_t *signature, UInt16 signatureLen)
    {
        OSStatus        err;
        ...

        if ((err = SSLHashSHA1.update(&hashCtx, &serverRandom)) != 0)
            goto fail;
        if ((err = SSLHashSHA1.update(&hashCtx, &signedParams)) != 0)
            goto fail;
            goto fail;
        if ((err = SSLHashSHA1.final(&hashCtx, &hashOut)) != 0)
            goto fail;
        ...

    fail:
        SSLFreeBuffer(&signedHashes);
        SSLFreeBuffer(&hashCtx);
        return err;
    }

.. class:: tiny

   See the module reading for more details.

.. class:: handout instructor

 More is said about this bug in the reading but at first glance, this just
 looks like an accidentally copy paste bug that ended up in production.  As it
 turns out though, that second ``goto fail`` is not bound in the second if
 check so it is **not** harmless.  It means that unconditionally, the code will
 perform the goto before doing the final part of the hash check.  The fail case
 will return the error code but it was set to success.  So this code was just
 simply always skipping the validation checks necessary to open a secure SSL
 connection!


Learning Objectives
===================

.. class:: handout instructor

 With all that, our goals for this week are:

#. Learn common ways control-flow constructs fail.
#. Practice tactics for untangling control-flow.
#. Reinforce hypothesis generation and using bottom-up methodology.

.. class:: handout instructor

 Traditionally this week is where we jump from finding known bugs, to doing
 some open ended VR.  So there is no longer that enticing carrot of a bug to
 find but you have a new motivation in that you might be finding a zero-day!
 We have found them in the past during this module so it can be done!  Let that
 motivate you but don't hold yourself to that standard.  Focus on good process
 and adding in these things to look out for.  Call out loops and their control
 values in annotations.  Reason about complex control flow and leave an
 evidence trail behind that you have considered these things.

 There is nothing akin to a function audit log for loops but you certainly can
 create your own documentation style to help you handle complicated control
 flow.  We will be looking out for that this week during feedback in addition
 to all the things we have been layering on to this point.

 Good luck!
