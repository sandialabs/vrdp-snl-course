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

.. Module 5 - C Language Issues

.. include:: <s5defs.txt>
.. include:: custom.txt

.. header::

 UNCLASSIFIED

.. footer::

 UNCLASSIFIED

.. class:: title-slide

 Vulnerability Research Development Program
   :small:`Module 5`

   :small:`C Language Issues`

.. class:: handout instructor

 These instructor call outs are a basic script for an example lecture.  They
 will oftentimes be specific to Sandia but can be a good guide for giving the
 lecture anywhere.

Last Module In Review
=====================

.. class:: incremental

  * Functions!
  * Argument relationships, meanings, types
  * Side effects
  * Function relationships

.. class:: handout instructor

 Last time we got into functions and how they can go wrong.  We talked
 about arguments, returns, side effects, and relationships. This week
 we are going to essentially finish the C/C++ stuff.  Not to say we
 won't continue to look at C/C++ code, but rather this should round
 out your "traditional" hacker knowledge. At least as much as we can
 pack into this course.


This Module - Overview
======================

What are all the things that can go wrong with C?

.. class:: tight-list

 * Properties of C types
 * Type conversion
 * Arithmetic properties
 * Operator precedence
 * Macros
 * General C spec weirdness

.. class:: handout instructor

 This is the deep dive on C.  Keep an eye out however for the meta knowledge
 that is to be gained by the experience you are about to go through for the
 next two weeks.  Understanding the deep and technical nuances of a system you
 are evaluating or safety is crucial for being good at vulnerability research.
 We are going to do this for C but this same point can be made for any system.

\
====================

We are about to get into the obscure, the arcane, and sometimes
the downright weird.  But that is where some of the best things to look
for are.  Nuances in language means that programmers are more likely to
make errors.  **Embrace areas where complexity and nuance reign.**

Properties of Types
===================

.. class:: handout instructor

 Let's get into the meat of this.  We are going to start out with types.
 This is basically going to follow the chapter and you are going to be
 spending a lot of time with the book this module.

* signed vs unsigned

.. class:: incremental

   * What is the signedness of a char?
   * It depends!

.. class:: handout instructor

 Signedness is going to be an important thing to focus on when type are mixed
 in source code.  We will get to it here in a minute but there is a large
 amount of effort in the C spec on figuring out how to map domains of integers
 onto what is sometimes called the "bitvector" domain of computers.  You
 probably remember from your CS college courses that most computers implement
 signedness using twos compliment arithmetic.  That introduces some subtleties
 in how operations happen that sometimes programmers don't understand.

Digression
==========

.. class:: handout instructor

 Before we get into that though, let's talk about this weirdness regarding
 the signedness of a char.  What does it really mean that implementations
 can "decide" what to do sometimes.  Well, there is terminology for that
 which you will run into in the reading or if you peruse the C spec.

Implementation defined behavior

Undefined behavior

.. class:: handout instructor

 Implementation defined behavior are places that the C language specifically
 lets the compiler be flexible with how it will behave.  The signedness of a
 char is one of those choices.  It means literally, there is space in the C
 spec that allows the exact same program to run differently in two different
 implementations.  That is on purpose and it is sometimes maddening.
 Thankfully, most popular compilers have settled on certain things that
 most people expect.  I don't think I know of a compiler that treats a
 char as unsigned.  Another good example of implementation defined behavior is
 the presence of a call stack.  Everything having to do with what you might
 recognize with respect to how memory laid out is an artifact of convention,
 compiler, and runtime.  In theory, your local variables could exist in some
 key/value store behind the scenes.  The C language doesn't care.

 The next phrase to consider is this thing called "undefined behavior".  The
 canonical example of this is a division by zero.  Of course the processor is
 going to freak out if you do this but what if the compiler can detect this
 ahead of time.  The C spec says this is undefined and in some compilers, the
 program actually will not crash if you try to divide by zero! These situations
 are very literally the C spec throwing its hands up in the air and saying, "I
 don't know, do whatever you want!"  There are so many corner cases, the spec
 tries its best to define what it can but for some things, maybe even some
 surprising things, the choice is left up to the compiler with strange
 consequences.  Another well known example of this is the buffer overflow!
 Indexing into an array past its defined bounds is considered undefined
 behavior.  The fact that this can sometimes lead to vulnerabilities it
 an artifact of the implementation.

Digression
==========

.. class:: handout instructor

 Here is an example of how undefined behavior can lean to a major problem.

.. class:: smaller

.. code-block:: c
   :number-lines:

   int foo(struct myobj *o){
      ...
      int var 1 = o->member1;
      ...
      if(!o){
          printf("Error");
          return -1;
      }
      ...
      do_dangerous_things(o);
   }

.. class:: handout instructor

 This code is clearly wrong.  There is a check that ``o`` is null on lines
 after it has been dereferenced.  You might think in the worse case this may be
 a risk for a null pointer dereference.  The situation is actually worse than
 that.  The C spec defines checking a pointer for null after it has been
 dereferenced as undefined behavior. This means that the compiler can do
 whatever it wants.  In fact, some compilers will make the assumption that
 ``o`` in fact cannot be null at the point of the check because clearly it was
 dereferenced.  It will then optimize out the if check! Why not, right?

 This is also an example of an issue that is perhaps harder to see in the
 source code than it would be in the binary.  They are rare but sometimes
 exist especially surrounding this quirk where the implementation is doing
 something fancy that isn't reflected in the source.

Properties of Types
===================

.. class:: handout instructor

 So diversion over.  We now have language to talk about undefined vs
 implementation defined things, though, which will be useful going forward.

 Back to types.  We had signedness and now we have some other properties
 like width and precision.  Width is easy, it is the number of bits you
 need to represent the type in its entirety.  The precision however is
 the number of bits you use for the "value" component of the type.  Why
 precision might be different than width could include things like a
 signed bit, or padding.  Let's see if you can guess the width and
 prevision of some popular types.

* signed vs unsigned
* width vs precision

.. class:: smaller

 .. class:: incremental

    * What is the width of a char, int, unsigned long
    * What is the precision of a char, unsigned char?
    * What is the value of sizeof(char)?
    * What if the width of a char is 16?

.. class:: handout instructor

 Width of a char is implementation defined!  So let's limit it to GCC.  The
 width is of course 8.  An int is 32.  A long is also implementation defined
 but on GCC is 64.
 
 The precision of a char is 7 because on GCC we know it is signed.  An int is
 31.  An unsigned long is 64 because there is no sign or padding bits.

 sizeof(char) is 1 right?

 What about if we are on an implementation where the width of a char is 16.
 What is sizeof(char)?  Turns out it is still 1! Crazy, I know!  As it turns
 out, the C spec both allows you to make the char type be wider than one byte
 but mandates that the expression sizeof(char) be equal to 1!

Properties of Types
===================

* signed vs unsigned
* width vs precision
* wider vs narrower

.. class:: smaller

 .. class:: tight-list

    * long long
    * long
    * int
    * short
    * char

.. class:: handout instructor

 The next thing to cover is this concept of wider vs narrower.  These are
 the words we will use to compare types.  It is exactly as you might expect,
 if you have more bits in your width you are "wider" and the other type is
 "narrower".  The C spec mandates that this ranking of types must go from
 wider to narrower.

Arithmetic Boundary Conditions
==============================

.. class:: handout instructor

 So that is it for the properties of types.  Next we are going to talk
 about arithmetic boundaries.  This is the more technical terminology
 for when we talk about integers "wrapping around" if you increment or
 decrement them too much.

 Of course, this happens as a result of the fact that computers work in
 bits and not in arbitrary integers.  The precision of a type will dictate
 how big or small of a value that type can hold.  If you go beyond that
 size, undefined things can occur but in most systems, when using twos
 complement math, you can predict what is going to happen.

 So what is going on in each of these cases:

.. class:: small

 .. code-block:: c
 
    unsigned char c = 255;
    c++;
 
 .. code-block:: c
 
    signed char c = 0;
    c--;
 
 .. code-block:: c
 
    signed char c = -128;
    c--;

What happens to ``c``?

.. class:: handout instructor

 It really is that simple.  You just have to be on the lookout for it.
 Clearly, if these boundaries are capable of being hit in code, it is probably
 not intentional.  Your job will be to see if you can spin that into something
 vulnerable.  As we have already seen, desk checking is a way to do this
 without necessarily even knowing about these boundaries. You must be
 reflecting what the machine would do, perhaps by sprinkling in some testing to
 be sure.

Type Conversions
================

.. class:: handout instructor

 (Consider a break at this point.)

 Now we are going to get into the deep dark world of C type conversion rules!
 This is like a rite of passage in this class.  We all look back on the pain
 of this week with a little bit of nostalgia.  There was the you that was in
 the before time, then there is you that is after the C language module and
 this stuff is a big part of it.

 Let's dig in.  There are two main kinds of conversion: *"value-preserving"*
 and *"value-changing"*.  There are also a set of operations that may be
 involved in each kind of conversion as listed here.

**value-preserving** vs **value-changing**

Conversion operations:

* widening
* narrowing (also called truncation)
* sign extending
* zero extending

.. class:: handout instructor

 Widening, of course, just increases the number of bits in the width of
 the type from one to the other.

 Narrowing is of course the opposite, removing bits from one type into
 another.

 Then you have two operations that changes the values in the new bits
 when you perform widening.  You can either take the sign bit and copy
 it into all the other bits which is called sign extension or you make
 all the new bits zero which is called zero extension.

 This seems simple, but it gets complicated.

Type Conversion Examples
========================

.. class:: handout instructor

 Let's go over what is going to happen to various types under
 conversion.  So for each one, we are going to reason if the
 conversion is value preserving, value changing, and which operations
 are going to occur.

.. class:: tight-list

 .. class:: incremental

  * char -> int

    * `(widening, sign-extending, value-preserving)`

  * int -> char

    * `(narrowing, value-changing)`

  * int -> unsigned int

    * `(value-changing)`

  * unsigned short -> int

    * `(widening, zero-extending, value-preserving)`

  * short -> unsigned int

    * `(widening, sign-extending, value-changing)`

.. class:: handout instructor

 (talk as you slowly uncover the incremental items)
 (ask questions and wait for responses)

 From int to char we are going to widen, and sign extend because both types
 have the same signedness.  This change is value preserving.

 From int to char however, we have to lose bits.  This means that for certain
 values that can fit into an int, they won't fit into a char.  Therefore this is
 a value changing operation.

 At first glance, when you go from int to unsigned int you might think that
 this is value preserving.  You don't have to do any type conversion
 operations.  However, one bit of an int is now re-purposed as a value bit in
 the unsigned case.  That means that this is still a value changing operation.

 Going from an unsigned short to an int will mean we need to widen and
 because there is no sign bit to extend, we will just zero extend and that
 means we can be value preserving.

 Finally, going from a short to unsigned int, we get to some weirdness.  Of
 course we need to widen but then what do you think should happen to the bit
 that previously represented the sign of the short?  Well we only have two
 operations, sign or zero extend.  In this case, you may be somewhat surprised
 to know that this actually does a sign extension!  It is therefore a value
 changing operation!  Most people don't know this.

When Does Type Conversion Happen?
=================================

.. class:: handout instructor

 Okay, so when do you have to worry about this?

.. class:: incremental

 * Assignment
 * Explicit Casts
 * Arguments
 * Returns
 * Expressions
 * ... basically everywhere ...

.. class:: handout instructor

 Type conversions are happening constantly.  You mostly don't notice it
 because it mostly doesn't matter. But when it does, it can be crucial
 to the safety of a program.

Integer Promotion
=================

.. class:: handout instructor

 So now we know something about conversions, let's talk about promotion.
 Promotion happens when the system needs to resolve types so that an
 expression can be valid.  You cannot perform any operation between two
 elements unless they are of the same type.  So the types will undergo
 promotion in order to resolve this when they are different.

Integer Conversion Rank

 * unsigned long long, long long
 * unsigned long, long
 * unsigned int, int
 * unsigned short, short
 * unsigned char, char

.. class:: handout instructor

 This first think you need to understand is this concept of promotion
 rank.  Each type has a rank relative to the other types and depending
 on that rank something different may occur.  The list of the ranks
 is as you might expect as it follows the same ordering as the wider
 to narrower list.

Usual Arithmetic Conversions
================================

.. class:: handout instructor

 So what happens when we have an expression.  Here are the steps that are
 taken.  TAOSSA goes into much more detail for each of these so please go
 review.

What happens during: ``(arg1 < arg2)``

.. class:: incremental

 #. Floats win
 #. **APPLY INTEGER PROMOTION**
 #. If types are the same, done
 #. If same sign, convert narrower to wider
 #. If unsigned is wider -> convert the other to unsigned
 #. If signed is wider -> convert other to signed if value-preserving is possible
 #. Otherwise use the corresponding unsigned type

.. class:: handout instructor

 (reveal slowly as you explain)

 First up, floats just win.  There are other rules for making floats happy with
 doubles and such but that is out of scope for now.

 The next rule is something that gets lots of people in trouble.  That is that
 everything is promoted to an int no matter what type it had before as long as
 its rank is lower than an int.  That might also be somewhat surprising.  So
 before we know anything about if the types agree or not, we
 **unconditionally** turn everything into an int.  Don't forget that, it will
 mess up your reasoning when you think about these things.

 After that is where the logic starts to try to marry up the types.  If they
 are the same after integer conversion, we are done.

 If they are not the same but their sign is the same, that is also easy, we
 can just sign extend the narrower one into the wider one if it is signed
 or zero extend if they are unsigned.

 The rest of the rules are for when the types are of different signs. If the
 unsigned type is wider, you convert the narrow type up to it. If the signed
 type is wider you convert the unsigned type up to it with a catch, you only do
 so if it possible to do it in a value preserving way.  If not, then you do
 something strange, you convert both of those types up to the unsigned
 equivalent of the widest type.

 Now, that is a lot to remember.  You probably won't.  I don't sometimes and
 I teach this stuff.  The more important thing to remember is when it **might**
 matter that some type is going to undergo a conversion that you think is
 relevant to slow down, find your book, and work it out.  Lots of bugs happen
 in this spaces that are rarely understood by most of us.

Order of Operations
===================

.. class:: handout instructor

 Operator precedence can also get you.  When in doubt, check the
 table!

.. class:: small

 Which of these are equivalent?

 .. code-block:: c

  (a | b == c << d); //1

  ( a | (b == (c << d) ) ); //2

  ( (a | b) == (c << d) ); //3

.. class:: handout instructor

 In this case, #1 and #3 are the same!


Macros
======

.. class:: small

 Macros expansion can be dangerous if you don't understand that it
 is basically a copy/paste operation.

 .. code-block:: c

   #define AORB(a,b) (a?a:b)

   if(AORB(x++,y++)){ ... }

   // becomes
   if(x++?x++:b++){ ... }

.. class:: handout instructor

 Note that the ``x++`` will happen twice!  The macro just copies
 and pasts whatever is in it before the rest of the compiler
 takes over!


What to do today?
=================

.. class:: small

 * We are not getting into auditing straightaway
 * If you haven't read the chapter yet, now is the time
 * If you have, take time to review it and go over
   examples near the end.
 * Get ready for a fun game tomorrow!

Spot-The-Bug in TAOSSA!
============================

.. class:: handout instructor

 In the meantime, go revisit or when you finally read this part in TAOSSA,
 see if you can spot any problems.

What is wrong with Table 6-4?

Learning Objectives
===================

#. Understand many nuances of the C language and how they contribute to memory safety.
#. Practice deliberately documenting things like boundary conditions, type conversions, promotions, etc.

.. class:: handout instructor

 I know today was a lot of info, which is why we are basically taking
 this first week to absorb as much of it as we can.  I will say, the more
 you can get familiar with, the better you are going to be at the game we
 are going to start tomorrow.  Time to get those competitive juices flowing!

\
=========

*(slide intentionally left mostly blank to remind me to stop here for the day)*

Group Spot-The-Bug
======================

.. class:: handout instructor

 (The next day)

 Let's start off with a warm up group spot-the-bug.

.. class:: scrollable

 .. code-block:: c
    :number-lines:

    struct sval {
        union {
            long lval;
            double dval;
            struct {
                char *val;
                int len;
            } str;
            ...
        }
        int type;
    }
    ...
    #define INTERNAL_FUNC_PARAMS int ht, \
        zval *return_value, zval **return_value_ptr, \
        zval *this_ptr, int return_value_used TSRMLS_DC
    ...
    static void php_html_entities(INTERNAL_FUNC_PARAMS, int all)
    {
        char *str, *hint_charset = NULL;
        int str_len, hint_charset_len = 0;
        size_t new_len;
        long flags = ENT_COMPAT;
        char *replaced;
        zend_bool double_encode = 1;

        if (zend_parse_parameters(ZEND_NUM_ARGS() TSRMLS_CC, "s|ls!b",
            &str, &str_len, &flags, &hint_charset, &hint_charset_len,
            &double_encode) == FAILURE) {
            return;
        }

        if (!hint_charset) {
            hint_charset = get_default_charset(TSRMLS_C);
        }
        replaced = php_escape_html_entities_ex(str, str_len, &new_len,
                    all, (int) flags, hint_charset, double_encode TSRMLS_CC);

        return_value->str.len = new_len;
        return_value->str.val = replaced;
        return_value->type = IS_STRING;
    }

.. class:: handout instructor

 (scroll through / highlight the code as you describe)

 (You should be able to show off the struct and then leave
  the function body on the screen to let the students think)

 * The first thing to note is that there are a lot of types, both
   in the structure being initialized and among the local variables of this
   function.  That is your signal to slow down and be thinking about
   conversions.

 * You don't have the prototypes for the calls to ``zend_parse_parameters``
   or ``php_escape_html_entities_ex`` but that is just for brevity. In real
   life you would go hunt those down and check their types.  For now we can
   assume that they are okay and that the values passed in by reference are
   done so in order to initialize them.

 * If you are tracking types, you should get to the end where ``new_len``
   is being assigned to the structure's ``str.len`` member.  However,
   new_len is a size_t while the structure len is an int!  This will
   undergo conversion resulting in a truncation.  If the 32nd bit of
   new_len happens to be set, it will become the sign but in the new
   value leaving behind a negative length.  That is the root of this
   real world CVE in PHP.

Stump the Students!
===================

.. class:: handout instructor

 Now I am going to introduce a game we have played every year for this
 module.  We are going to start out with "stump the students" and later,
 we will play "stump the teacher"!

* Figure out what will be printed
* No compiling!  Just use your brain
* PM me your answer

Stump the Students! #1
======================

.. class:: handout instructor

 (copy and paste these out to a compiler to show the answers after
  everyone has answered or given up)

Let's play

.. class:: instructor
 
 .. class:: smaller
 
  .. code-block:: c
     :number-lines:
 
     int main(){
 
         int x = -1; 
         unsigned int y = 1;
 
         if(x < y)
             printf("0\n");
         else
             printf("1\n");
 
         return 0;
     }

Stump the Students! #2
===========================

.. class:: instructor
 
 .. class:: smaller
 
  .. code-block:: c
     :number-lines:
 
     int main(){
 
         char x = -1;
         unsigned short y = 1;
 
         if(x < y)
             printf("0\n");
         else
             printf("1\n");
 
         return 0;
     }

Stump the Students! #3
===========================

.. class:: instructor
 
 .. class:: smaller
 
  .. code-block:: c
     :number-lines:
 
     int main(){
 
         unsigned short x = -1;
         unsigned short y = -1;
 
         if(x * y > 0)
             printf("0\n");
         else
             printf("1\n");
 
         return 0;
     }

Stump the Students! #4
===========================

.. class:: instructor
 
 .. class:: smaller
 
  .. code-block:: c
     :number-lines:
 
     int main(){
 
         unsigned char x = 255;
         int y = x + 1; 
 
         if(y > 0)
             printf("0\n");
         else
             printf("1\n");
 
         return 0;
     }

Stump the Students! #5
===========================

.. class:: instructor
 
 .. class:: smaller
 
  .. code-block:: c
     :number-lines:
 
     int main(){
 
         unsigned int x = 0xFFFFFFFFU;
         unsigned int y = 0xFFFFFFFFU;
         long long unsigned int z = x * y;
 
         if(z > 0xFFFFFFFFLU)
             printf("0\n");
         else
             printf("1\n");
 
         return 0;
     }

\
=========

.. class:: handout instructor

 (Go over the stump the teacher exercise in the guide)

*(slide intentionally left mostly blank to remind me to stop here for the day)*

Exercise
========

.. class:: handout instructor

 (resume this the following Monday)

 Now we are going to get into some auditing with our new C language skills
 fresh in our mind.  We are however going to audit a little differently.

.. class:: small

 Document in as much detail as possible, every type action happening in a piece of code.
 
 * Any time a type is non-obvious
 * Any promotion
 * Any conversion
 * Issues resulting from the integer manipulation
 * Strange order of operation situations
 * Manually expand macros

.. class:: handout instructor

 This is not something that you are expected to do always, but I want you
 to turn your awareness up to 11 this week.  This is a good auditing mode
 to be able to get into when you confront complexity.  As you get better,
 you may need to use it less but it is nice to know that you can do it.

Exercise
========

.. class:: scrollable

 .. code-block:: c
    :number-lines:

    unsigned short foo(int fd){
        char buf[10];
        size_t a;

        // read returns a size_t
        // b is a short
        // The return value of read is truncated into a short
        // issue: b can be signed in an unexpected way!
        short b = read(fd, buf, 10);

        // b is a signed short value
        // b is promoted to an int and remains signed
        // the > operation is therefore signed
        // issue: this check can be bypassed
        if(b > 8){
            RAISE_ERROR();
        }

        // atoi returns an int
        // a is a size_t
        // size_t is wider than int therefore
        // The assignment will sign extend into a
        a = atoi(buf);

        // The return value of foo is an unsigned short
        // issue: a will be truncated upon return
        return a;
    }

.. class:: handout instructor

 Everyone is allowed to have a different style but this is a basic example of
 what I am expecting.  Call out every time, every conversion, etc.  Put your
 thinking as verbosely as possible into your annotations.  We will go over it
 during feedback to make sure you and I are comfortable with your progress.


Process for C Nuances
=====================

Everybody likes to think they "get-it" when it comes to C nuances until they
miss bugs because of it.  Don't be cocky around complex C code!  You don't
always need to go to extreme lengths to document every conversion but what's
the harm?

Learning Objectives
===================

#. Understand many nuances of the C language and how they contribute to memory safety.
#. Practice deliberately documenting things like boundary conditions, type conversions, promotions, etc.

.. class:: handout instructor

 The difficulty you will encounter this week is that real code isn't as dense
 with issues as the stump challenges.  You have only have pockets of code that
 this is worth doing on, but be on the lookout and be attracted to complexity.
 That is where bugs lie.  Happy hunting!
