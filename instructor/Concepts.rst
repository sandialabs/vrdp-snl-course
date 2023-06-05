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

.. _Concepts:

Key Concepts To Teach
=====================

It is important to emphasis as a whole, the collection of concepts that the
course is intended to teach because of the fact that the modules designed to
specifically teach these concepts can change.  If you are adapting VRDP for a
different technology area, consider the arc of the entire course and make sure
that as modules are replaced, you are aware of the coverage of concepts in
your adapted course.

Demystification of VR
---------------------

Sometimes students start VRDP with some unjustified presumptions about what
it takes to be good at VR.  There is sometimes a mystique around that practice
that makes people think that only individuals predisposed to VR talent can
really succeed.  Part of your job as an instructor of the course is to hammer
home how harmful these presumptions are.  Emphasize that process and hard work
count for more than *hacker skills*.  People who are continuous learners,
dedicated to the craft, and enthusiastic can and have overcome a perceived lack
of raw talent and do find bugs!


Elements of Process
-------------------

A big part of VRDP is talking about and improving the process that you
apply to a VR problem.  While they are some key truths that have been
discovered by those with experience, the more important meta-point is that
a deliberate process tailored to the problem is the first step in being a good
vulnerability researcher.  In class we often talk about avoiding a "random
walk" of the problem.  Teach that you should never rely on luck to solve
the problem.  Plan your approach to the problem and execute it in a way
that you have a sense of where you are and how much progress you are making.
Much of this is also adapted from :ref:`TAOSSA <TAOSSA>` Chapter 4 although
some things are cherry-picked or augmented based on experience.

Active auditing
+++++++++++++++

Active auditing is the first key process element taught in VRDP and should be
emphasized throughout the course. We often describe the act of code auditing or
reverse engineering as, "reading the code" but it is important to emphasize
that the act of auditing is not a passive process.  Auditing is an analysis of
the code and just like a hypothetical system that might analyze code for you,
you should produce some kind of output as an artifact of that analysis.  For a
human, that output needs to be something that captures the depth, breadth,
and completeness of the expertise of the auditor.  This is important not only
for other people, but for themselves to refer to later.  Auditing is an active
process that should be thought of as building something, not just consuming
information.

There are multiple benefits to active auditing, all of which you should
continuously emphasize.

* Writing things down keeps you attentive.  Reading can get boring.  It can be
  hard to maintain the level of focus that you need to find bugs if you are only
  a spectator of the process.
* Putting things in your own words helps your memory of what you are reading.
  This is true not only when learning in a classroom setting, but for when you
  are *learning about the code* that you are auditing.
* Good analysis or summaries of things helps teammates, or your "future self",
  when visiting the same code.  You never know if you will revisit a portion of
  code later because it is involved in the path or setup of another issue.
* From the student's perspective, for the purposes of this class, they will get
  better feedback from your evaluation of their skill if they can put their
  thoughts plainly so the instructor knows what they were thinking.  The first
  feedback they can expect from the instructors if the output is sparse should
  be, "increase your output so I have something to go on to help you learn!"

Like any new skill, it is far better to start practicing it correctly early
on to form good habits.  For that reason, pay careful attention to the frequency
at which the students are producing data early on in the course.  If you are
using Snippet, you can check the time stamps on the annotation entries in the
inbox.  If you know the students are working yet there is a lack of activity in
the annotation log, address that with the student early on and encourage them
to "over do it" at the beginning.  If the students aren't recording their
thoughts, you can't tell the difference between poor reasoning about the code
with poor effort or rigor.


**Function Audit Logs**

Function Audit Logs are not mentioned until later in :ref:`TAOSSA <TAOSSA>`
but after the first year of VRDP we found them to be such an essential element
in active auditing that as instructors we mandate them early on in the course.
While students can decide what other elements they feel are important to add
to a function audit block, require them to at least have:

* A description of what the function's intent is in their own words.
* What if anything could go wrong under any assumptions they can think of.

This requirement is often referred to as the `What` and `What Could Go Wrong`
(often abbreviated in practice as `WCGW`) aspects of the function audit block.
Doing this seems to kick start the hypothesis generation activity that you hope to
see in mature vulnerability researchers.  It is also a very easy thing to
look for when providing feedback.  If they did not put the function audit block
on each function, you can explore with the student why the felt the need to
shun the process.  It is especially potent if you can do it in the context of
a missed bug as it drives home the lesson that process is important.


Deliberately Applying Tactics
+++++++++++++++++++++++++++++

See :ref:`TAOSSA <TAOSSA>` Chapter 4 *(Code-Auditing Tactics)*

The list of tactics from the book is introduced early in the course but it
is something that is also emphasized throughout.  Tactics end up becoming the
vocabulary in which you can subtly steer students if they fall off the beaten
path.  For example, if a student has too quickly glossed over a section of the
code, during feedback you can recommend rereading the code and segmenting what
they are looking for on each pass.

Of the list of tactics in the book, heavy emphasis on desk checking should
be drilled throughout the course.  This is particularly beneficial in a
learning environment because desk checking produces artifacts that you can
critique as an instructor.  Depending on your teaching style, you can be a
little bit stern by making desk checking a requirement for getting credit for
finding a bug.  You can tell the students, "if you come to me to tell me you
have found a bug, the first question I am going to ask you is if you have desk
checked it yet."  This sets up an expectation that rigor will be rewarded and
it helps make sure that desk checking is well practiced.  Humans have a
tendency to be lazy and thinking that you have checked things well enough in
your own head is one of the pitfalls that can cause someone to miss a bug.

By labeling which tactics you apply as you talk about code, such as during a
review, spot-the-bug, or feedback, you start to make the practice of applying
tactics something that is a deliberate choice of the students.  This is a
mature mindset that you should be looking to instill throughout the course.


Cognitive Self Awareness
++++++++++++++++++++++++

See :ref:`TAOSSA <TAOSSA>` Chapter 4 *(Avoid Drowning/Auditing Strategies)*

Building a mature VR mindset also means that students should be self aware of
their own cognitive states as they engage in bug hunting.  Remember that we are
human beings and we are affected by the time of day, our health, or even our own
personal cycles which might dictate when we are more alert or not.  Different
strategies to make continual progress on an auditing task might be used
depending on one's own assessment of their current capability.  Everyone's
personal situation might differ and it is important to recognize that the point
of teaching this idea is to make people intentionally aware of their various
cognitive states and to adjust their strategy accordingly.  Below is an example
of situations and how they might apply to an average person.

* **Top-Down Auditing** - Save this for times you have the most energy and
  are most alert.  Top-down auditing requires you to maintain path information,
  either control and/or data flow state in your short term memory, and have
  some amount of a depth/breadth strategy in place to be effective.  Some
  amount of structure in your auditing process can make up for a lack of focus
  (e.g. a good breadcrumb system, taint tracking, etc) but you will still
  probably perform better using a top-down technique if you engage when you
  feel most at the top of your game.  Also, top-down analysis may be more
  fatiguing because it tends to be more open ended and lead to more "wild goose
  chases."

* **Bottom-Up Auditing** - Because you can generally portion out bottom-up
  tasks as you go, this auditing strategy is generally good for anytime or
  simply when your mental condition is "unremarkable".  You don't generally
  need a whole lot of external state to keep around in your memory to make
  substantial progress when doing bottom-up analysis.  You can even sometimes
  "power through" a single function or class if you feel yourself fatiguing.
  Success in bottom-up does rely a bit more on hypothesis generation since you
  don't necessarily know what you can control as an attacker.  The downside of
  this is that you can sometimes get stuck exploring a plethora of boundary
  conditions that can never be realized in practice.

* **Candidate Points Analysis** - With candidate points you are usually
  looking for something specific.  For example, if via bottom-up auditing you
  found a potential defect if a particular function is called the wrong way,
  there may be thousands of places to check to see if it is possible to invoke
  the buggy behavior.  While this might be a very tedious task, it is also quite
  a low investment cognitively.  Many call sites might be capable of being
  dismissed with a casual inspection.  If only a few are actually difficult to
  analyze, you could also simply mark them for a more careful analysis later with
  a fresh mind.  The danger of candidate points analysis is that you might
  accidentally blow by something else important but it is a similar risk that you
  would be taking if you attempted a top-down strategy while tired or
  inattentive.

..  note::

    Something that we subtly disagree with TAOSSA on is the degree to
    which one strategy is more cognitively difficult than another.  TAOSSA
    labels the difficulty of top-down strategies as lower than that of the
    various bottom-up strategies.  The more important point is to teach
    students to be self aware, judge for themselves, and make sure to plan
    their strategies in accordance with their own assessment.

For some people, those first few early morning hours tend to be their most
productive.  So a person who is paying attention to their mental states might
do open ended exploring in the morning, and save the results of candidate
points generated from a static analysis or their own bottom-up auditing for the
end of the day when they know they are usually more tired.  Other people might
be the exact opposite.  The late-night culture of young tech infused
researchers might mean that they are groggy and unfit for much in the mornings
while their afternoons is when they are picking up steam.  The point is,
encourage students to introspect and use different strategies to maximize their
effectiveness in the time they have.  Success with auditing goes up with more
time spent with eyes on code and so they can either improve their chances with
more hours or more effective hours because you have taught them to be smart and
self-introspective researchers.

Iterative Process Design
++++++++++++++++++++++++

See :ref:`TAOSSA <TAOSSA>` Chapter 4 *(Iterative Process)*

See `The Tao of Boyd: How to Master the OODA Loop <https://www.artofmanliness.com/articles/ooda-loop>`_
[`cached version <../ref/OODA_Loop_A_Comprehensive_Guide_The_Art_of_Manliness.html>`_]

Vulnerability research is an activity that relies on making good
judgments based on continually updated information about a program.  For that
reason having an **iterative** process is an important component to succeeding
where others might get stuck.

TAOSSA's take on an iterative process is pretty basic and easy to understand.  It is
a bare minimum of obtaining some sort of meta-cognition about the cyclical nature of 
vulnerability research.  The view in TAOSSA is also a personal process but in VRDP
we stress the importance of having an overall iterative and team process that
has been useful in solving problems.

.. .. external

The Observe-Orient-Decide-Act loop is another way to think about process looping
but goes into more depth about each phase.  According to the linked article above:

 *The OODA Loop makes explicit our implicit decision-making process. By making
 it explicit, Boyd offered an incomparable strategic tool to everyone from
 soldiers and militaries to businesses and sports teams to social movement
 leaders and political campaigners to better manage their own decision-making
 processes.*

Cast in terms of vulnerability research, an OODA loop can be thought of in 
the following way:


* **Observe** - Take in or update the information you have about the program.  Be
  aware that you will be unable to collect all the information you might like.  Remember
  that you will be repeating this process.  (e.g. *"It looks like the UI, model, and util
  components are separated out into different directories in this source."*)
* **Orient** - Try to make sense of what you are seeing and form a list of hypotheses
  about the best way to move forward.  For example, you might try to align which components
  of the program might be amenable to a particular VR strategy. (e.g. *"It seems like this
  parser is a good place to start a top-down strategy while the whole backend could use the
  bottom-up treatment.  I don't know if fuzzing will be effective on this program until I
  understand it more."*)
* **Decide** - Choose a path forward based on the best information you have and your
  experience. In other words, pick one of your hypotheses to try and test.  (e.g. *"This
  is a short term project so the best chance for success will be using a top-down
  approach on the elements I identified as potentially aligning with that strategy."*)
* **Act** - Perform in a way that improves the situation for the next iteration.
  Capture information and give yourself a goal or time limit to refresh your perspective.
  (e.g. *"I am going to audit this interface until our next team sync and see if I
  learned enough by then, or my team has learned enough to justify continuing."*)

Just like we teach students to be aware of their mental states, teach them also
to make explicit planning decisions about how to attack a VR problem.  If students
get stuck, you can encourage them to "loop" and take a different approach based on
what they have learned so far.  For group projects, align an OODA cycle with the
schedule so that meetings designed to sync knowledge among the team are also
points where you update each element and **act** anew.

Mitigations
-----------

Exploit mitigations are an important concept for vulnerability researchers
to understand but they are best understood in context.  For that reason, we
don't associate talking about things like DEP, or ASLR with any particular
module because it may be more impactful to introduce these concepts alongside
a bug where they are relevant.  Look at the arc of the course and plan times to
talk about at least the basic common mitigations when they seem to be most
relevant to what the students are learning.

By the end of the course, students should have a basic familiarity with the
following, all of which are general and usually exist on modern platforms:

 * Data Execution Prevention (DEP)
 * Stack Canaries
 * NULL Page Protection
 * Address Space Layout Randomization (ASLR)

There are a LOT of other mitigations that may be relevant based on the
circumstances.  Some mitigations are platform specific so may not be as general
as the above.  Nevertheless, if you find opportunity to talk about other
mitigations, you are helping to build the student's understanding of state of
the *"arms race"* between attackers and defenders.

Other mitigations worth talking about if the opportunity arises:

 * Control Flow Guard (CFG) *Microsoft*
 * Control Enforcement Technology (CET) *Intel*
 * Pointer Authentication Codes (PAC) *ARM-Apple*
 * Memory Tagging Extension (MTE) *ARM-Google*

Students should be familiar at a conceptual level with what the
mitigations prevent, historical work arounds for the mitigations (e.g. ROP),
and how the presence of mitigations might affect their auditing strategy.  For
example, if it is known that in the real world the executables don't have ASLR,
there is no need to spend time looking for information leaks unless the leaks
are useful in and of themselves (e.g. authentication bypass).

What About Fuzzing?
-------------------

Fuzzing can be a great way to find vulnerabilities but there are some 
reason why we don't focus on it in VRDP.

* Fuzzing in and of itself generally doesn't lead to better understanding of the program.
* The experience of setting up a fuzzer doesn't always generalize in a way that improves
  the experience of the students.
* Setting up a fuzzer can sometimes take too long and there is already a lot of material
  to cover just in the realm of auditing.

What you should teach is that fuzzing is a valid **strategy** that can be chosen
as part of a real world VR process. There are some pitfalls that we historically have
warned VRDP students about though.  There is a pervasive myth that it is efficient to
spend time setting up fuzzing at the beginning of a new VR task so that the fuzzer can
be running while you are doing other things.  Setting up a fuzzer while you know the least
about a program is often times the worst way to fuzz.  Do encourage students to play with
fuzzers along with any other VR tools they want to explore as part of their independent
exploration.  Sometimes having class discussions about, "would you fuzz this" or, "could a
fuzzer find this bug" can be fun and spark lighthearted controversies.


The Future of VR
----------------

This course is currently focused on *"old-school"* memory corruption vulnerability
hunting but it is important to make sure that students come away from the course
with more nuanced understanding of what vulnerability research is.  Some of the
most critical bugs that affect our society have been so-called *"logic"* bugs that
don't involve twisting the computer architecture in clever ways.

New memory safety mitigations that are becoming more pervasive means that
vulnerabilities are going to be more subtle, more application specific, and harder
to find.  The process that students have learned though is general and the attitude
and dedication necessary to be a good vulnerability researcher is what the course
intends to instill in the students.

