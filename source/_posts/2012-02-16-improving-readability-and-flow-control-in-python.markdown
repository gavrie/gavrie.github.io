---
layout: post
title: "Improving readability and flow control in Python"
date: 2012-02-16 00:31
comments: true
categories: [python, code]
published: true
---

Recently, a colleague and I refactored a piece of existing code that had new
behavior added to it. During the process, we managed to improve the readability of the
code using several techniques that I'll describe below.


Where We Started
----------------

The original code was fairly simple: It decides whether certain "dead"
components need to be "revived", and presents the user with a prompt to choose
from one of several actions. 
Depending on the user's choice, the code then proceeds to take the appropriate action:

{% include_code The original code flow_control/code0.py %}


Adding New Behavior
-------------------

We now wanted to add some new functionality to the above code, namely the ability to
allow the user to select a *subset* of the components that he wants to revive.

To make things more foolproof, in case the user chose to revive selected
components but then neglected to select any components from the list, the code
would not proceed blindly but rather send the user back to the menu so that he could try again.

The first version of the new code looked like this:

{% include_code New behavior, first version flow_control/code1.py %}

To get the required behavior, we used an infinite `while True` loop that terminates with an
explicit `break` when a valid choice is made by the user and reiterates otherwise.
This ensures that we don't continue until a valid choice is made.


Can We Do Better?
-----------------

The problem with the above method is that the flow control is not immediately
apparent when looking at the code: It's not obvious that the infinite loop
should actually terminate in all but one case. A future developer could easily
break this behavior. 

In addition, the `if`/`elif` ladder becomes a bit too long to read
comfortably.

The second iteration was meant to make the flow control clearer:

{% include_code Refactoring, first try flow_control/code2.py %}

We use several techniques here to improve the clarity of the code:

* We used internal functions to encapsulate the possible actions to take. The
  advantage of using internal functions is that it keeps the external namespace
  clean, and the naming of each function makes its purpose quite clear.

* We used a dictionary instead of the `if`/`elif` construct. Since Python
  doesn't have a `switch` or `case` statement, this is a more readable replacement.

* We decided to use an exception to signify, well, *exceptional* flow control: If the user hasn't
  selected any components, this warrants exceptional behavior. This technique is
  much debated, but we felt like it was appropriate in this case.

* The function name to be called is determined dynamically at runtime from the
  user's selection. The idea was to avoid code duplication by needing to specify the names
  of the functions yet again (but see below).


Removing Some Coolness For Readability
--------------------------------------

My colleague pointed out that the `locals().get('choice_%s' % choice)()` trick
is not quite readable. I agreed, and was happy to accept his improved proposal:

{% include_code Refactoring, final version flow_control/code3.py %}

This version has several advantages:

* It doesn't use "magic" to achieve the selection of the function. Duplication
  is better than magic in this case, since it makes the code more readable.

* The dictionary is created using the `dict()` syntax instead of the `{...}`
  syntax, which gets rid of a lot of punctuation and makes the code clearer.


Conclusion
----------

It turns out that even in such a simple piece of code, several programming
techniques can be used to make the code clearer to read and maintain.

See you next time!
