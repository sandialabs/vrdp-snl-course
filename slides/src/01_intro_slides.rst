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

.. Module 1 - Introduction & Methodologies

.. include:: <s5defs.txt>
.. include:: custom.txt

.. header::

 UNCLASSIFIED

.. footer::

 UNCLASSIFIED

.. class:: title-slide

 Vulnerability Research Development Program
   :small:`Module 1`

   :small:`Introduction & Methodologies`

.. class:: handout instructor

 These instructor call outs are a basic script for an example lecture.  They
 will oftentimes be specific to Sandia but can be a good guide for giving the
 lecture anywhere.

What to Expect (Goals)
======================

.. class:: handout instructor

 Welcome to the vulnerability research development program.  I will be your
 instructor.  Let's get right into it.

.. class:: small

 * This course is designed to be an accelerator as part of your journey
   in becoming an expert vulnerability researcher.

 * Even though this course is expansive, it will not teach you everything.

 * At the end of the course, you should have a strong foundation to
   build on, a good sense of how to further improve.

 * Being good at vulnerability research means you commit to being a
   lifelong learner.

.. class:: handout instructor

 In general, having a growth mentality is somewhat of a prerequisite for
 success in this class and in vulnerability research.  Some people who take
 this course have reported being immediately hit with a bunch of stuff they
 didn't know before or otherwise felt like they weren't prepared.  That is
 probably going to be true to some extent for everyone.  Don't worry though, we
 will get you through it.  The course starts fast but you won't be left behind.
 Also, the things you will be learning will transcend your individual ability.
 You will get better at certain skills even when you apply the same process we
 are about to discuss.

What to Expect (Schedule)
=========================


.. class:: handout instructor

 The course has gone through many iterations.  It used to be a year long but we
 realized that if you have a healthy VR system to start working in right
 afterward, you don't really need the tons of practice that we were getting in
 that year.  Plus times and budgets change.  The course now is more modular and
 laid out as such.

.. class:: small

 * 4 weeks now (Beginner)
 * 4 weeks later (Intermediate)
 * 6-8 weeks even later (Advanced)
 * Opportunities to do VR in the meantime. (As they arise)
 * If something comes up, I will do whatever I can to make it work.
   **Babies** have been born during VRDP in the past.  If you have the drive,
   I will go to bat for you.

What to Expect (Average Week)
=============================

.. class:: handout instructor

 The basic structure for many of the modules is as follows.

.. class:: small

 * **Monday** - Lecture/Discussion/Class Exercises
 * **Tuesday** - Reading/Auditing/Feedback
 * **Wednesday** - Reading/Auditing/Feedback
 * **Thursday** - Group Feedback
 * **Friday** - Reflections/Reading/Independent Exploration/Read Ahead

.. class:: tiny

 You are expected to spend 20 hours per week on class activities.
 If you have an alternate schedule (e.g. 9/80) you need to spend an extra
 hour M-Th to make up for the missed Friday.  Reflections are still due
 on Friday.

.. class:: handout instructor

 Some of the intermediate and advanced modules will deviate from this but a lot
 of the basic structure is similar with the week being book-ended by a lecture
 and some kind of closing activity with lots of work and interaction in the
 middle.

 Feedback is one of the main benefits of this course.  We will iterate on your
 skills and progress so you can make course corrections.  This is why this
 course is here instead of me just handing you TAOSSA and letting you figure it
 out on your own.  Early on, I will get on your case about it but later on in
 the course it will be more and more on you to make sure you are reaching out
 to instructors for feedback.

 You should also have time during class to do the reading. Some people like to
 have the reading done before.  While I respect that, I try to make sure that
 you have something to do other than the main exercise because you may need a
 change of pace.  You are going to be looking at a **lot** of code and after a
 while, its nice to take a break.

 We'll talk more about reflections here in a minute.

What to Expect (Difficulty)
===========================

.. class:: handout instructor

 I highly recommend this book as reading at any point.  It is one I wish I had
 read as a student.  It really opens your eyes as to how terrible the science
 of learning is in our world.  Basically, our institutions operate the way they
 do because of tradition, not because those methods are the best way to learn.

.. .. external

.. image:: static/make_it_stick.jpg
   :height: 300px
   :align: center

.. class:: tiny

 Optional but recommended reading outside of class.
 
 * Learning is best when done via a process of recall even when recall fails.
 * Difficulty should be embraced and be motivating.  **You learn best when it is hard.**
 * Reflection is a style of recall that solidifies learning.
 
 If you find this class to be too easy, let me know.  I can fix that.
 

.. class:: handout instructor

 If you do pick this up, you may notice ways in which this course is designed
 around some of these concepts.  You are hopefully going to be constantly using
 the material we discuss in lecture.  Most of the time you spend here is going
 to be on solidifying increases in your knowledge and skill, not just dumping
 more information in front of you.

What to Expect (Integrity)
==========================

.. class:: handout instructor

 This is just some basic expectation setting.

.. class:: small

 .. class:: incremental

  * You are encouraged to discuss the reading material.
  * You are encouraged to discuss cool hacker news.
  * You are highly encouraged to share out-of-class war stories and bond.
  
  * Please do not discuss assignments unless it is explicitly a team assignment.
  * Please do not look for answers on the internet.  You are only robbing
    yourself of the opportunity to hone your skill.

.. class:: handout instructor

 Especially early on, we are going to be focusing on individual growth.  It is
 okay to not succeed in finding bugs. You are not being graded and you
 especially aren't being graded on spotting bugs.  The feedback we give you
 will be much more about your process.  The bugs we have to find in the course
 are there as motivation, not milestones.

 Furthermore, you often learn more from your misses than your hits.  A miss
 will identify a gap we need to work on.  The most notable learning moments
 for me on my journey in VR were the bugs that I failed to see and how I
 changed my workflow and dedication to compensate.

\
===========================

.. class:: title-slide

 Questions so far?

This Module - Overview
======================

.. class:: handout instructor

 Now let's dive into the content for this module.  We are going to be talking
 about some of the big high level concepts that we will take with us for pretty
 much the entire rest of the course.  This is the big foundation laying lecture
 so this is probably the most important one to get.  Here is what we are going
 to cover.

Active Auditing

.. class:: smaller

  *A mental approach to the* **work** *of vulnerability research.*

Auditing Strategies

.. class:: smaller

  *A purposeful, high level approach to attacking a problem. A chosen
  strategy should guide how you work over a large unit of time.*

Auditing Tactics

.. class:: smaller

  *Like tools in a toolbox, tactics are activities that
  you use regularly or constantly to make progress on a task.*

.. class:: handout instructor

 So before you know anything about what a security relevant bug looks like or
 how to use it to hack anything, we are going to be talking about these
 elements of a good review process.  Once you have that internalized, then we
 will start peppering a lot of the security specific things that you might be
 expecting.

Active Auditing
===============

.. class:: incremental

 * If you treat auditing like you are reading a book, **you will miss bugs**.
 * Think about auditing instead as **building** a knowledge base.
 * Building is an **active** and **constructive** process that produces **output**.

.. class:: handout instructor

 Contrast this with what it would mean for this process to be *passive*.  When
 you hear about code auditing you may think about it more in terms of this, as
 if all you are doing is reading the code looking for problems.  That is
 exactly what you should not do.  Instead what you should be thinking about is
 exactly what you would be doing if you were building the software itself.
 Everyone here has built software and when you do, you clearly leave behind
 important things other than the code itself.  You may create tests,
 documentation, notes, etc.

 This is the first big potential expectation I want to break right away.  Bug
 hunting is about making things.  In particular, you are making knowledge in
 ways that the original programmer probably wasn't considering.

Active Auditing Pro/Con
=======================

.. class:: handout instructor

 There are a lot of benefits to thinking about bug hunting in this way.  A lot
 of this shares similarities to being a good student where smart teachers tried
 to encourage you to take notes.  The act of writing things down helps you
 remember.

 Just reading, can be tiring and your mind can quickly wander.

 The amount you do write down is a sign of progress that you can both share
 with other people, and prove to sponsors/managers/project leads that you have
 actually done something instead of just relying on trust.

 Finally, even if you don't believe me about any of this; maybe for example you
 have a photographic memory and don't care what other people think; at the very
 least writing things down for this course will allow me inside your head to
 give you feedback so I can help you on your journey to become a vulnerability
 researcher.  There are more things to notice in code than there are bugs, by a
 **lot**.  If you write them down, I can tell that you are grasping both the
 process and the knowledge of bugs to help you succeed.

.. class:: small

  Pros
    * Helps you learn about the code base and remember nuances.
    * Keeps you attentive and engaged with the problem.
    * Gives you a sense of progress.
    * Allows you to collaborate with other auditors.
    * Proves to others that you have done something other than think in your own head.
    * Give **me** a mechanism to give you feedback!


 
Active Auditing Pro/Con
=======================

.. class:: small

  Cons
    *  ... there are no cons ...

.. class:: handout instructor

 This is one of the primary points in this course.  Its about flipping the
 script on the expectations of what it means to be a vulnerability researcher.
 Its not about passively seeing through the matrix.  You are constantly
 engaging in a process of learning about something, and you need to be capable
 of learning about it better than the people who built it.

How to Actively Audit?
======================

Build Something!
 * A Snippet database
 * A OneNote store
 * A Wiki
 * A notebook

.. class:: handout instructor

 Really the medium doesn't matter although there probably are better ways to do
 it depending on your goals.  In a pinch, I will take a git repo, fork it, and
 add annotations directly to the source.  Because that disturbs the source, it
 is perhaps better to use something meant for the job.  This is an area of
 active research and development for which Snippet is one solution.  More are
 on their way.  I have however been part of workshops and other VR efforts
 where there was not much in the way of specific support for building artifacts
 and yet artifacts were made aplenty.  Something as simple as a wiki is a
 great way to create artifacts.

The Demystification of VR
=========================

.. class:: handout instructor

 What I really hope you get out of this course, and especially this first week
 is some destruction of myths about what makes a good vulnerability
 researcher.

.. class:: incremental

 * Engaging in active auditing makes VR accessible.
 * Hard work can count just as much as cleverness or talent.
 * This is probably the most important takeaway of this course.

.. class:: handout instructor

 Maybe you have been or seen some videos from hacker-cons where someone gets on
 stage and shows off some amazing exploitation of something important.  If not,
 you should go seek some of those out, they can be inspiring and highly
 educational.  The important point to make though is that you are seeing in
 that moment the highly curated version of events for the purposes of a 1-hour
 talk. What is very often happening behind the scenes with that person on stage
 is months to years of hard work becoming an expert at the technology they
 are able to twist to their whims.

 Is what they are able to do impressive?  Yes of course.  But there is also
 nothing magical or mystical about **how** they were able to do it.  It took
 practice.  It took hard work.  It took them having a plan of attack and it
 took them being motivated to get the job done.

 Good old work ethic, can count for as much if not more than raw talent
 when it comes to being good at this skill.  My hope is that by the end
 of the course, or maybe even by the end of this beginner session,
 you will start to see evidence that this is true.

Auditing Strategy Taxonomy
==========================

.. class:: handout instructor

 Now we are going to talk about strategies.  These are high level approaches
 you might take to tackle a VR problem.  These are also a simplified version
 that what you will see in the reading.  We are really only going to go over
 the following three generalizations.

 * Top-Down
 * Bottom-Up
 * Candidate Points

.. class:: handout instructor

 TAOSSA has a much more detailed taxonomy of these which I encourage you to
 read although there are some key points where we disagree with their
 assessment on how difficult these strategies can be.

Top-Down Strategy
=================

.. class:: handout instructor

 Let's start with the top-down strategy because oftentimes, this is considered
 the "obvious" place to start examining something.  We'll see in a minute why
 that not always true.

.. class:: incremental

 Also known in TAOSSA as *"trace malicious input"*.

 You start at an entry point, trace the flow of code and data forward
 keeping track of "bad" inputs in your mind until you hit vulnerable code.

 This is **very hard**, especially when you first start.
 :tiny:`*(heavily disagree with TAOSSA that suggests this method is easier than others)*`

 There is a time and place for it and we will be exploring it later in the course.

.. class:: handout instructor

 For example, if you are heavily time limited in your review, a top-down
 strategy might make a lot of sense because you will only be able to evaluate
 low hanging fruit kinds of bugs.

 Top-down is perhaps the common sense strategy and is in fact advocated as the
 better strategy by other authors.  See *A Bug Hunter's Diary* for a great
 example of someone who uses this strategy to great effect.

Top-Down Pro/Con 
================

.. class:: handout instructor

 There are some natural pros to this strategy and some perhaps unexpected cons
 if you aren't experienced.

.. class:: small

 .. class:: incremental
 
  Pros
    * You know you can direct execution to the code you are reading.
    * You can start in places that you are know are security relevant.
    * Is often a *natural* place to start understanding an application.
 
 .. class:: incremental
 
  Cons
    * You don't understand or may make invalid assumptions about the
      building blocks of the program. This can cause you to miss subtle bugs.
    * Can lead to path explosion and difficulty tracking where you are.
    * DFS versus BFS can be an arbitrary choice without experience.

.. class:: handout instructor

 You might not expect the downsides listed here to be that big of a deal and
 to some extent you will just have to trust me that they are.  Are they worth
 losing some of the advantages of this strategy?  Well that is a debate for
 a different day.

 So we go over this strategy now but aren't going to talk about it again for a
 long time.  That is because my job is to get you to fall in love with the next
 strategy so that you can appreciate some of these things.  We will however get
 to this and eventually, you can have this as part of your toolbox and
 hopefully be able to use it more purposefully instead of it just being the
 default choice.


Bottom-Up Strategy
==================

.. class:: handout instructor

 This is the strategy you are going to be experiencing a lot of in the
 beginning of this course and for good reasons as you will see.

.. class:: incremental

 Corresponds to a collection of strategies in TAOSSA such as *"analyze a module"*
 or *"analyze a class"*.

 Instead of drilling down into functions or back-tracking to see how
 things are called, you examine and note what **could** go wrong.

 You consider code in isolation and makes heavy use of hypothesis generation in
 order to tease out subtle issues.

.. class:: handout instructor

 We are going to talk a lot about hypothesis generation over the next few weeks.
 Your hypotheses are going to be the main focus of your reasoning as we improve
 over time.  Hypothesis generation has a huge advantage especially for learning
 in that you can generate **way more** hypotheses than you are likely to find
 bugs. So you will have much more opportunities to evaluate how you are doing
 on your journey.  In the past, vulnerability researchers who lacked confidence
 had to potentially wait a long time until they found their first bug to
 validate that they were, "doing it right."  A hypothesis however, can be
 examined in isolation and we can speculate about what could happen if you were
 to hit code where you have a hypothesis of a bug.  That is going to be very
 important.
 

Bottom-Up Pro/Con 
=================

.. class:: handout instructor

 Some of the pros and cons of bottom-up are of course a reflection of the ones
 we saw for top-down.

.. class:: small

 .. class:: incremental
 
  Pros
    * You gain an understanding of key building blocks of the program which is
      useful in other strategies or to determine exploitability.
    * You are not burdened by elements of context such as how a module is used.
    * Is often the source of subtle or *deep* bugs.
 
.. class:: handout instructor

 Now you are probably going to **feel** like this lack of context is a huge con
 when you start to use this strategy in the lab later.  Trust me that this
 notion will pass in time as you get used to it.  You are going to have to
 practice telling that part of your brain that wants to know why some code
 exists or what the code is good for to be patient. When in doubt, just pretend
 anything you want about the code if you have questions that can only be
 answered by going down rabbit holes.  If you don't know what input looks like,
 just imagine it can be anything you want.  Consider any open questions in the
 most favorable light possible to find bugs.

.. class:: small

 .. class:: incremental
 
  Cons
    * Many hypotheses prove false in the presence of context or conditions
      for a bug are simply not met. (e.g. reachability)
    * It is difficult to know when you should be "done" understanding fundamentals.

.. class:: handout instructor

 The big down side is that **most** bug hypotheses are not bugs.  You just need
 to expect that.  There are going to be hundreds of little let-downs before the
 first real issue materializes.
 
 By the time you are "done" doing bottom-up, you also will know quite a bit
 about the building blocks of the program which is going to make your job of
 being effective at top-down much easier.  All of the custom allocators, data
 structures, and other "bottom" code will no longer be foreign to you as you
 are going top-down.

TAOSSA Endorsed!
================

.. class:: handout instructor

 If I am not convincing enough, I hope you will temporarily take the word of the
 author of textbook to heart.

.. .. external

.. class:: center

 *"You might not expect this, but many experienced code reviewers settle on this
 technique as a core part of their approach.  In fact, two of your authors typically
 start reviewing a new code base by finding the equivalent of the util/ directory and
 reading the framework and glue code line by line."*

.. class:: handout instructor

 You are also more than welcome to interrogate some of the other experienced VR
 people in our organization.  This is a great way to do VR and especially if
 you have time, is the best way to start.

Candidate Points Strategy
=========================

.. class:: handout instructor

 To round out the discussion of strategies we will be going over in the course,
 last is candidate points.

.. class:: incremental

 Corresponds to a collection of strategies in TAOSSA such as *"general candidate points"*,
 *"automated source analysis"*, *"simple lexical"*, and *"black box generated"*.

 Generate a list of points of interest from an analyzer, grep, fuzzer, or even a back-track
 list of curious issues you found while doing bottom-up.

 Examine each site for the presence of a particular issue or pattern.

 Repeat

.. class:: handout instructor

 This can be a simple strategy to employ depending on the way in which you
 generate candidate points.  If you spend a year figuring out how to fuzz
 something those candidate points might be expensive.  I don't recommend doing
 that.

Candidate Points Pro/Con 
========================

.. class:: handout instructor

 A Candidate points strategy is a very good mix-in kind of strategy.  When you
 finally have all these tools on your tool belt, it is very useful to be able
 to pull this one out occasionally.

.. class:: small

 .. class:: incremental
 
  Pros
    * Very good when you have low mental energy.  You just troll through a list
      looking for something specific.
    * Mechanical, hard to get lost.
 
 .. class:: incremental
 
  Cons
    * Can blind you to other nearby issues. 
    * You end up learning a lot less about the program.

.. class:: handout instructor

 The biggest downsides to the strategy are also why we only touch it in one
 module later.  There are things you need to figure out when it comes to
 candidate points but I hope you can see, if you believed me at the beginning
 that you job is to learn about the program better than the developer, that
 hopping around somewhat arbitrarily is perhaps not the best way to do that.

Tactics
=======

.. class:: small

 Focus your reading mostly on this section of TAOSSA (pg 133-147)
 **Code-Auditing Tactics**.  While you should finish all of the assigned
 reading for this module, do this *before* you start the auditing assignment.
 
 List of Tactics:
  * Internal flow analysis
  * Subsystem and dependency analysis
  * **Re-reading code**
  * **Desk checking**
  * Testing

.. class:: handout instructor

 Most of these are going to stand for themselves in the reading but I want to
 highlight a few of these, namely re-reading and desk checking.

 We are going to talk about re-reading a lot but I want to start off by
 emphasizing that this is the tactic I make deliberate use of the most.
 Re-reading does not simply mean to read the code again.  You can use
 re-reading as part of your planning on how you are going to approach code
 analysis.  For example, I will often read a function or a file once very
 quickly just to get my bearings.  I will then plan to read a complicated
 function more than once to establish certain things that I need to make progress.
 I might read the whole function once not looking for any problems at all but
 just to establish how data flows through the function and what kinds of
 complexity I might expect to have to manage.  Then I can tailor my approach
 based on evidence.  Being a good vulnerability researcher is not about
 gritting your teeth and going through code line by line.  That happens
 sometimes but this tactic in particular, helps you manage your plan, your
 expectations, and your mental capacity to deal with complexity.

 We'll see desk checking more here in a minute but I just want to point
 out that testing is just a special class of desk checking.  If you have
 the ability to run the code and write tests for things, that can be a
 huge advantage but some times it is not worth the effort.  Deciding when
 it is can be hard.

Tactics (continued)
===================

.. class:: handout instructor

 There are also a few documentation processes that we treat as "tactics" in
 that you are expected to be doing them all the time.

.. class:: small

 We Treat as "Tactics":
  * Function Audit Logs
  * Allocate/Copy/Check Logs (later)

Desk Checking Example
=====================

.. class:: handout instructor

 Let's get deeper into desk checking.  Here is some code with a real bug in it,
 but let's pretend that we don't know that for a minute.

.. class:: scrollable

 .. code-block:: c
    :number-lines:

    #define NTLM_BUFSIZE 1024
    CURLcode Curl_auth_create_ntlm_type3_message(...){

      size_t size;
      unsigned char ntlmbuf[NTLM_BUFSIZE];
      unsigned int ntresplen = 24;
      unsigned char ntresp[24];
      unsigned char *ptr_ntresp = &ntresp[0];
      unsigned char *ntlmv2resp = NULL;
      ...
      /* Create the big type-3 message binary blob */
      size = snprintf((char *)ntlmbuf, NTLM_BUFSIZE, ... );
      ...
      /* NTLMv2 response */
      result = Curl_ntlm_core_mk_ntlmv2_resp(ntlmv2hash, entropy,
                                             ntlm, &ntlmv2resp, &ntresplen)
      ...
      if(size < (NTLM_BUFSIZE - ntresplen)) {
        memcpy(&ntlmbuf[size], ptr_ntresp, ntresplen);
        size += ntresplen;
      }


.. class:: handout instructor

 In real life this function is quite big but you might get to the ``memcpy`` call
 and wonder about its safety.  In order to evaluate that, you are going to have to
 follow the dataflow of all the variables or expressions involved in that if
 check and the subsequent copy.

 (demo building this table)

 +------+------+-----------+-------------------+--------------+-------------+
 | line | size | ntresplen | BUFSIZE-ntresplen |  memcpy dst  | memcpy size |
 +------+------+-----------+-------------------+--------------+-------------+
 | 10   | ???  |  24       |                   |              |             |
 +------+------+-----------+-------------------+--------------+-------------+
 | 12   | 1024 |  24       |                   |              |             |
 +------+------+-----------+-------------------+--------------+-------------+
 | 15   | 1024 |  1025     |                   |              |             |
 +------+------+-----------+-------------------+--------------+-------------+ 
 | 18   | 1024 |  1025     | 0xffffffff        | ntlmbuf+1024 |  1025       |
 +------+------+-----------+-------------------+--------------+-------------+

 Here at the last step, we can see that the buffer size minus the response
 length would be negative.  The types of these variables however are unsigned.
 What happens when you do that is that the value "wraps around" the bit width
 of the variable size and in this case, become a very large unsigned integer
 causing the check to pass when it shouldn't.  That leads to a buffer overflow.
 This was a real bug in ``curl`` where a malicious website could potentially
 hack a client!

 Later on in the course we are going to go into a much deeper discussion of
 this issue where the safety check can be bypassed because a number "wraps
 around".  Nevertheless, you can find these issues without even necessarily
 knowing about this particular bug pattern by applying desk checking.  

 Where there is complexity, especially when it also involves safety, don't
 trust your brain to keep the entire computer state coherent.  Write it
 down.  I still use paper but other people have used spreadsheet apps.
 The point here is to offload the computation onto something more reliable
 than your mind.

 The alternative is to of course try to isolate the code and run it (i.e. the
 testing tactic).  That can oftentimes be much harder than desk checking.  You
 will just have to judge for yourself.

Hypothesis Generation
=====================

Especially in the beginning, bug hunting is not about flashes of insight.
Instead focus on creating as many hypothetical scenarios about what could be
problems in the code.

What could go wrong?

What would you **WANT** to go wrong?

As you audit, the list of these hypotheses will grow.
**This is your measure of progress.**

.. class:: handout instructor

 I probably can't emphasize it enough, this is especially true for the "meta"
 of this course.  When you get a chance to see your peers, it is very often
 the case that the students who make the most hypotheses are the ones who
 end up finding real issues.

Types of Hypotheses
===================

.. class:: handout instructor

 We have formalized a nomenclature for kinds of hypotheses that has ended up
 being very useful in previous classes.

.. class:: small

 Not all hypotheses are created equal.
 
 **Type 1** - Something could go wrong if a caller or something else external
 misunderstands the meaning or purpose of this function.
 
 *"WCGW: If the caller interprets the size parameter as the total size instead
 of the remaining size of the buffer, an overflow can occur"*
 
 **Type 2** - Something does go wrong with legal / expected input.
 
 *"WCGW: This function can return success even if the allocation of memory fails."*

.. class:: handout instructor

 Most of the time, these type 2 hypotheses are considered better than type 1.
 There is no other value attached to them though other than this rough
 judgment. It doesn't mean that they are more likely to be a real bug.  Think
 about a type 2 bug as something you would clearly fix if you ran into it as
 the developer.  Whereas a type 1 bug might just be a convention of the
 implementation.  Mind you, conventions being violated are still a source of
 bugs, they just take more work to realize.
 

Function Audit Logs
===================

.. class:: handout instructor

 A function audit block, a collection of which is called a function audit log,
 are the basic unit of artifacts I expect you to begin creating here at the
 beginning of the course and they will remain an important part of your process
 throughout the course.

.. class:: small

 .. class:: incremental
 
  Keep notes about functions that will be useful later.
 
 .. class:: incremental
 
  Mandatory for the course:
    * One function audit block per function definition.
    * Must have a description of the function in your own words.
    * Must have a *What could go wrong?* section. (shortened WCGW)
 
 .. class:: incremental
 
  TAOSSA has other suggestions including some obvious ones.
    * Arguments and their meaning
    * Return values and their meaning

Function Audit Block Example
============================

.. class:: handout instructor

 Here is an example of a function audit block for that buggy ``curl`` function.

.. class:: scrollable

 .. code-block:: c

    // WHAT: Generates a ntlm message based on a previous response
    // WCGW: If using a NTLMv2 response, it is possible to control
    //  the ntresplen such that it will be larger than NTLM_BUFSIZE
    //  causing the check guarding a memcpy to fail.
    #define NTLM_BUFSIZE 1024
    CURLcode Curl_auth_create_ntlm_type3_message(...){

      size_t size;
      unsigned char ntlmbuf[NTLM_BUFSIZE];
      unsigned int ntresplen = 24;
      unsigned char ntresp[24];
      unsigned char *ptr_ntresp = &ntresp[0];
      unsigned char *ntlmv2resp = NULL;
      ...
      /* Create the big type-3 message binary blob */
      size = snprintf((char *)ntlmbuf, NTLM_BUFSIZE, ... );
      ...
      /* NTLMv2 response */
      result = Curl_ntlm_core_mk_ntlmv2_resp(ntlmv2hash, entropy,
                                             ntlm, &ntlmv2resp, &ntresplen)
      ...
      if(size < (NTLM_BUFSIZE - ntresplen)) {
        memcpy(&ntlmbuf[size], ptr_ntresp, ntresplen);
        size += ntresplen;
      }

\
===========================

.. class:: handout instructor

 Snippet is a tool we use because it is designed for auditing.  Unlike the
 function audit block I wrote above which disturbed the line numbers of the
 code, Snippet lets you annotate while keeping the code pristine.  Snippet is a
 little old and we are trying to create a replacement but until then, it is a
 great tool to use to learn auditing skills.

 (Things to cover in your demo):

 * Indexing
 * Adding annotations
 * Editing annotations
 * Show the annotation heat bar
 * Show the inbox
 * Tagging and the annotation info window
 * Outline view
 * Omnibar
 * Results pane
 * Navigation
 * Slicing

.. class:: title-slide

 Snippet Demo

Learning Objectives
===================

#. Understand at a high level, the strategies and tactics you can employ to do VR.
#. Practice active auditing and using function audit logs.
#. Practice applying tactics.
#. Practice using a bottom-up strategy to understand code.

.. class:: handout instructor

 Now we are going to jump right into some auditing.  You might ask, "what are
 we auditing for? You have shown us one bug!" Well, a prerequisite for this
 course was programming in C.  You should all know how to do that.  If you have
 written any C in your life, you have created bugs.  For starters, I just want
 you to focus on the strategy we are using, and the tactics.  What is or is not
 a problem is anything that looks wrong to you as if you were the developer of
 this code.  Imagine that this is something important and your job is to review
 the code to look for anything that will disturb the safety, security, or
 reliability of your product.  You are not necessarily vulnerability hunting yet,
 you are just "problem" hunting and that can be anything.
