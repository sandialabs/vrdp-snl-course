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

.. Module 2 - Auditing Variables

.. include:: <s5defs.txt>
.. include:: custom.txt

.. header::

 UNCLASSIFIED

.. footer::

 UNCLASSIFIED

.. class:: title-slide

 Vulnerability Research Development Program
   :small:`Module 2`

   :small:`Auditing Variables`

.. class:: handout instructor

 These instructor call outs are a basic script for an example lecture.  They
 will oftentimes be specific to Sandia but can be a good guide for giving the
 lecture anywhere.

Last Module In Review
=====================

.. class:: handout instructor

 Last time, we talked about and started practicing these things.

.. class:: incremental

  * Strategies: bottom-up, top-down, candidate-points
  * Tactics: desk checking, testing, re-reading
  * Active Auditing: building knowledge

.. class:: handout instructor

 Before we move on though, let's take a step back for some perspective.

\
=========

Even this early on, you should start to see that being good
at VR isn't all about intuition, elite knowledge, special talent, etc.
Quite a bit can be accomplished by steady and deliberate work, good
process, and a growth mindset.

.. class:: handout instructor

 Everybody made progress last week.  We might not be saving the world yet, but
 you might have taken the first steps.  That is only kind of a joke.  Sometimes
 what we do at Sandia is pretty darn important.

This Module - Overview
======================

.. class:: handout instructor

 Next up we are going to start adding in some specific things to look for!
 Unlike last week where all you had was whatever background knowledge you came
 into the course with and your C development experience, this week we are going
 to add some specific concepts that will help you detect certain categories of
 bugs.

 To start with ...

What are all the things that can go wrong with variables?

* Variable initialization
* Variable relationships
* Nuances with structures and objects

.. class:: handout instructor

 Variables need to be initialized, they can be bound up in relationships that
 are important, and they can be bound up in structures and objects that add
 complexity that isn't always obvious.


Variable Initialization
=======================

What happens when a programmer uses a variable that has not been initialized? (Discuss)

.. class:: handout instructor

 (Some leading questions if you don't get any bites on discussion)

 What value might a variable or memory have before you assign anything to it?

 Could that value ever be under the control of an attacker?


Variable Initialization
=======================

.. class:: small

 Why does this happen?

 .. class:: incremental

    * The programmer forgot
    * A path exists where the variable is not initialized.
    * The programmer assumed the calling function did it.


Example of an initialization error
==================================

.. class:: handout instructor

 Here is a sinister example that involves some C++.  You may have seen
 this already if you did the reading first.

.. .. external

.. class:: scrollable

 .. code-block:: c
    :number-lines:

    class netobj {
        private:
            char *data;
            size_t datalen;
        public:
            netobj(){ datalen = 0; }
            ~netobj(){ free(data); }
            getdata(){ return data; }
            int setdata(char *d, int n){
                if(!(data = (char*)malloc(n)))
                    return -1;
                memcpy(data, d, n);
            }
            ...
    }
    ...
    int get_object(int fd){
        char buf[1024];
        netobj obj;
        int n;

        if((n = read(fd, buf, sizeof(buf))) < 0)
            return -1;

        obj.setdata(buf, n);
        ...
        return 0;
    }

.. class:: tiny

   TAOSSA Listing 7-8, pg 314

.. class:: handout instructor

 (scroll through / highlight the code as you describe)

 * Here we have this ``netobj`` class which has two data members.  The important
   thing to point out is that in the constructor, only one of the two data
   members is initialized.
 * Then after the destructor, you have a getter and setter for that ``data`` member.
 * There may be a type in TAOSSA because there is another issue in this code in
   that the setter doesn't update the ``datalen`` variable.
 * The consequences of that object being kind of primitive and seemingly
   incomplete are seen here when it is used. What is tricky about this
   are the calls you don't see because of C++.  When ``obj`` is created,
   the constructor fires and initializes ``datalen`` but not ``data``.
 * Everything is actually fine except for the error case.  If the call
   to ``read`` fails, this function will return an error code but there
   is one more unseen thing.  The destructor of the ``netobj`` will fire
   which unconditionally deletes ``data``.
 * What is in data then?
 * It will contain whatever value happened to be on the stack when this
   function was called and the runtime created a new stack frame over the top
   of whatever was previously there.
 * Turns out, this is "quasi-controllable".  Imagine a different call stack
   where you might get to write arbitrary data into a buffer on the stack for
   another reason.  If that is just hanging around, you could control the value
   of that pointer and cause what is called an *arbitrary free*.  This could
   then turn into a class of vulnerability called a *use after free*, where
   an object can have its internal memory replaced because the system re-used
   the memory after it had been inadvertently freed.  There are many different
   ways to exploit something in this situation.  For example, if that object
   that was freed contains a function pointer, the new data could contain a
   replacement value for that function pointer causing the program to execute
   something else.  If you can control that, you have wedged your foot into the
   door of an exploitable vulnerability.

Information Leaks
=================

.. class:: handout instructor

 We have seen out not initializing something can be the start of a problem.  It
 can also be the entire problem in and of itself.  It all depends on the data
 that happens to be there when the uninitialized issue is manifest.

.. class:: small

 Useful things in uninitialized memory:

 .. class:: incremental

  * Code pointers -> Break ASLR
  * Heap pointers -> Break heap randomization
  * Stack pointers -> Locate the stack
  * Stack canaries -> Allow traditional stack smashing
  * Crypt material -> Authentication bypass
  * App specific information

.. class:: handout instructor

 An information leak can assist other aspects of exploitation, or can be a fully
 fledged vulnerability in and of itself.  There was a famous bug called "Heartbleed"
 where the problem was **only** an information leak.  In this case, an attacker
 was enable to leak enough information to totally compromise the integrity of a
 secure system.

Defined in the negative...
==========================

.. class:: handout instructor

 The previous example had its own challenges related to C++ but initialization
 bugs have something in common that make them harder to spot.

Uninitialized value bugs are often defined by what code **isn't** present
which sometimes makes them unnatural to spot.  Therefore, try to make looking
for them an explicit part of of your process.  *(e.g. "I am going to use a
re-reading tactic and make a pass of this code explicitly checking for
initialization")*

Variable Relationships
======================

.. .. external

*"Variables are related to each other if their values depend on each other
in some fashion, or they are used together to represent some sort of
application state.  For example, a function might have one variable that points
to a writable location in a buffer and one variable that keeps track of the
amount of space left in that buffer."* -TAOSSA


Variable Relationships
======================

.. .. external

*"As a code auditor, you must search for variables that are related to
each other, determine their intended relationships, and then determine whether
there's a way to desynchronize these variables from each other."* -TAOSSA

.. class:: handout instructor

 So the name of the game here is to #1, identify relationships, and #2 figure
 out if you can desynchronize that relationship.  "Desynchronization" of a
 variable relationship can happen in many ways but it often is just because one
 variable bound in a relationship is changed without deference to the other
 one.

Example of a relationship error
===============================


.. class:: handout instructor

 The best way to see this perhaps is with an example.

.. .. external

.. class:: scrollable

 .. code-block:: c
    :number-lines:

    cdata = s = apr_palloc(pool, len + 1);

    for (scan = elem->first_cdata.first; scan != NULL;
         scan = scan->next) {
        tlen = strlen(scan->text);
        memcpy(s, scan->text, tlen);
        s += tlen;
    }

    for (child = elem->first_child; child != NULL;
         child = child->next) {
        for (scan = child->following_cdata.first;
             scan != NULL;
             scan = scan->next) {
            tlen = strlen(scan->text);
            memcpy(s, scan->text, tlen);
            s += tlen;
        }
    }

    *s = '\0';
    ...
    if (strip_white) {
        /* trim leading whitespace */
        while (apr_isspace(*cdata)) /* assume: return false
                                     * for '\0' */
            ++cdata;

        /* trim trailing whitespace */
        while (len-- > 0 && apr_isspace(cdata[len]))
            continue;
        cdata[len + 1] = '\0';
    }

    return cdata;

.. class:: tiny

   TAOSSA Listing 7-1, pg 298

.. class:: handout instructor

 (scroll through / highlight the code as you describe)

 * A relationship is born between ``cdata``, ``s``, and ``len``.  Hopefully
   that is obvious but in case it is not, any time two variables are involved
   in the same expression, it has the potential to create a relationship with
   important implications.  In this case, it is not safe to either increment
   either pointer value past ``len+1`` number of bytes, or index using those
   pointers as a base past ``len+1`` number of bytes.
 * It is not the bug that TAOSSA talks about, but I also take issues with
   both of these for loops which happen to modify ``s``.  Both of them are
   doing so without checking if ``s`` ever goes beyond ``len+1`` You could
   justifiably write a hypothesis for this code for a potential buffer overflow
   just for that.  In this case it would be a type 1 hypothesis because it
   would depend on if the ``elem`` structures were independently controlled.
 * However the actual problem occurs in the basic block control by the
   ``strip_white`` variable.  The issue is the same, however in this case it is
   clearly dangerous because ``cdata`` is modified without a corresponding check
   or modification of ``len``.
 * After whitespace is removed from the front of the buffer, it will attempt to
   remove it from the back part of the buffer starting at ``cdata+len+1``.  This
   could be out of bounds by the number of whitespace characters that were
   removed in the first step.  All you have to do to prove this to yourself is
   to desk check this considering a string of only whitespace characters.  A
   null byte will be written out of bounds exactly as far away as the number of
   whitespace characters in that string.  Programs have been exploited with far
   less control than this.

Structure and Object Management
===============================

Identifying relationships between members of a struct or object works the same
way as normal variables.  The complication lies in the fact that issues like
desynchronization might happen across function calls over the object's
lifetime.

.. class:: handout instructor

 If anyone was wondering what you should document when you run into a struct,
 this is one possibility.  The hard part about this is it takes you a bit out
 of your "function in isolation" paradigm.  It is however a useful thing to
 note about an object once you see its constituent parts being used in other
 part of the code.

Structure and Padding
=====================

.. .. external

.. class: tiny

   This is something that is a little bit difficult to see from the source, but
   nevertheless is relevant.

.. class:: scrollable

 .. code-block:: c
    :number-lines:

    struct sh
    {
        void *base;
        unsigned char code;
        void *descptr;
    };

    void free_sechdrs(struct sh *a, struct sh *b)
    {
        if (!memcmp(a, b, sizeof(a)))
        {
            /* they are equivalent */
            free(a->descptr);
            free(a->base);
            free(a);
            return;
        }

        free(a->descptr);
        free(a->base);
        free(a);
        free(b->descptr);
        free(b->base);
        free(b);
        return;
    }

.. class:: tiny

   TAOSSA Listing 6-33, pg 286

.. class:: handout instructor

 (scroll through / highlight the code as you describe)

 * What this code is attempting to do is **avoid** a situation called
   a *double free*.  Think about a double free as a special case of a use after
   free that we previously discussed.  In this case, if you free the same
   memory twice, in the intervening time, a new object could have been
   allocated in that space, for example in another thread.  That object is
   going to expect to own its memory but like in the use after free case,
   it could have its innards be replaced with something else.
 * The way this function attempts to avoid that is to only free the
   insides of this ``sh`` structure once if the pointers are the same.
 * Instead of comparing the pointers directly however, it just uses
   ``memcmp`` to compare all the bytes of the whole structure.
 * Now, who can tell me what is the ``sizeof(struct sh)``?
 * The two pointer values either take 4 or 8 bytes depending on the
   architecture and the char takes 1 byte.  So it should be 9 or 17 right?
 * As it turns out, the size is either 12 or 24!  Why?  Because the one
   character member of the struct throws off the alignment.  Pointers have to
   be either 4 or or 8 byte aligned so there actually exists 3 or 7 bytes of
   padding between the char and the last pointer!
 * What values do those invisible bytes contain?
 * Just like uninitialized data, they could contain garbage and if they
   do, that ``memcmp`` could fail stopping this function from protecting
   against the double free.

Random Walking
==============

.. class:: handout instructor

 I also wanted to take the opportunity to introduce one more
 concept that will come up many times during the course.  That
 is "random walking".  By that I mean doing this without intent
 or purpose.  That is a good way to not make progress.

By now you have the tools to avoid "random walking".

If you feel lost, make a plan, or ask for help.

.. class:: handout instructor

 You have a process to follow.  You have tactics to employ.
 You have things to look for.  You are officially bootstrapped!
 If you don't feel that way, now is the time for us to have a
 discussion about that so we can address any gaps we missed
 last week and this week.
   
Learning Objectives
===================

.. class:: handout instructor

 Our goals for this week are:

#. Understand basic vulnerability patterns around variable usage.
#. Practice auditing with variable usage in mind.
#. Reinforce hypothesis generation and using bottom-up methodology.

.. class:: handout instructor

 We are really trying to build upon what you have been doing by adding in
 these concepts.  You should still be doing function audit logs.  You should
 still practice active auditing.  What might go into those logs now should
 increase.  You also may have some more reasons to use certain tactics like
 re-reading.  For example, plan a re-reading pass around simply identify
 relationships and adding those to your annotations.  Then perform another
 pass looking for opportunities to desynchronize those relationships.
