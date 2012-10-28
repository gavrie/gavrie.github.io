---
layout: post
title: "The YAGNI/NIH Conundrum"
date: 2012-06-15 10:38
comments: true
categories: code
---

*Disclaimer:* This post is about software development, but it is more about the human side of it than about the technical side. This means you may enjoy it even if you're not a software developer (or a technical person at all).

One of the recurring issues that I encounter as a software developer is that of having to decide where on the scale between YAGNI and NIH I want to be. You are probably wondering what the hell I am talking about (unless you're one of those people who are nodding your head now and smiling), so I'll explain.

[YAGNI](http://en.wikipedia.org/wiki/YAGNI) stands for "You ain't gonna need it", and refers to a software development principle according to which you don't want to start writing a huge bunch of code up front until you know exactly what you are going to need. Since software requirements change all the time, and one of the common maladies of many code bases is superfluous complexity due to over-engineering and over-abstraction, it makes a lot of sense to implement only what you know you are going to need right now, and leave the rest for later.

[NIH](http://en.wikipedia.org/wiki/Not_invented_here) stands for "Not Invented Here", and refers to a reluctance among some software developers to base their work on code written by someone else: "Hey, I can do this myself, so why should I use this existing project"? This leads people to reinvent the wheel time and again, creating a proliferation of half-baked solutions to problems that have been solved fairly well at other times and places. In addition to the waste of resources in the creating the solution in the first place, it also creates yet another maintainability headache.

<!-- more -->

The Conundrum
-------------

I consider myself a firm believer in the YAGNI principle, and a staunch opponent of the NIH syndrome: I try to avoid writing code that could stay unwritten, since I consider a large codebase a liability rather than an asset. Writing more code means having to expend more resources on maintaining it. In many corporate cultures, it also decreases the ability to respond to change, due to a reluctance to throw away existing code (which is often due to sentimental reasons rather than objective ones).

Now, as software developers, many of us would much rather write new code than maintain a bunch of old code.

One reason for this is that old code bases tend to have accumulated a lot of baggage over the years, and we love the idea of getting rid of all that and starting with a fresh, blank page: All those old bugs can be forgotten, all those workarounds and little tricks can be left behind.

Another reason is that good developers love to learn new ideas and techniques and are itching to try them out. Seeing our own old code after a few months or years make us cringe with the feeling, "who was the idiot that wrote this?!". We are sure that the code we're going to write now, with our new and shiny tools, will be better by leaps and bounds. And then the cycle starts all over again.

Coding in the Corporate World
-----------------------------

I'd like to argue that in the corporate world, as opposed to the Open Source world, writing new code can be an irresponsible thing to do. In the corporate world, we write code not just to scratch our own itches. We're creating something that may very well continue to exist long after we have moved on to greener pastures. Other people will have to maintain what we created. Adhering to good software engineering principles means that not only our own lives will be easier down the road, but also those of other people. 

Now, those who profess not to care about the experience of other people, or who think that at the very least it is less important that their own experience, may want to consider a few points: 

First of all, those "other people" may be yourselves a few months or years from now, trying to adapt your own code to new requirements. Suddenly, all this code is no longer new nor fun, and you'll have to dig in to adapt it to the required changes.

Second, those other people may be your future co-workers, managers or employees. They will remember what you left them with.

Third, people will appreciate your efforts to make their lives easier (or at least won't hate you for making it harder). This increases the likelihood that they will want to work with you in the future. 

So all this makes sense even from a perfectly selfish point of view.

Conclusion
----------

When faced with a new software problem to solve, I always spend a significant amount of energy in investigating existing solutions and see if they can work for me. I will resort to writing code only if I fail to find a solution that has enough similarity or has a good enough quality. Of course, as my friend Eli claims, this may very well mean that I often pass on the chance to be creative by deferring to existing solutions. But that's something I can live with: I feel the need to reach the right balance between creativity and responsibility. 

I can find creativity in ways other than writing a lot of new code: I'd rather leverage existing code that I like and that is maintained by a third party (which becomes more and more commong with the huge Open Source ecosystem). It is more important to me to feel happy with a solution than it is to prove to myself that I can solve a problem that has been solved before by others. That just seems so wasteful.

In an upcoming post, I will analyze a specific case that I encountered in light of the above thoughts.

