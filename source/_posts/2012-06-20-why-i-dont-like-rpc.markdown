---
layout: post
title: "Why I don't like RPC"
date: 2012-06-20 09:47
comments: true
categories: [code, rpc, python]
---

Lately I've been working on modifying an architectural aspect of an existing software project. This project makes heavy use of remote execution of code on several hosts. To accomplish this feat, it uses several different methods for remote execution: SSH for running general shell commands, RPyC for executing arbitrary Python code remotely, as well as a couple of proprietary interfaces.

One issue I encountered with the current design is that it is quite difficult to make a clean separation between code running locally and code running remotely. This turns debugging any problem involving execution of remote code into an incredibly complicated endeavor.

Much clarity could be gained by changing the architecture of this project to be more explicitly distributed. This would involve several agents running on multiple hosts that communicate amongst themselves to get the work done. The agents would have a clean and documented API, making them usable and testable as standalone components, as well as allowing them to act on behalf of a central process. All remote execution would be explicit, using one single method for any kind of execution -- be it shell commands, Python code or anything else.

<!-- more -->

The Problem With RPC
--------------------

Our existing codebase makes heavy use of [RPyC](http://rpyc.sourceforge.net/), a native Python RPC implementation, for remote execution of arbitrary Python code on remote machines.

Using a variant of RPC sounds like a great solution. RPyC is also a very nice and seamless tool. Code that is running remotely looks just like code that is running locally. Which is the exact reason for why I *don't* like using it: I don't want transparent RPC! I want it to be immediately clear which code runs locally and which code runs remotely. "Seamless" RPC encourages the writing of spaghetti code, because it's so easy to mix local and remote code. This makes it deceptively easy to write distributed code without thinking about the design of the API and about which parts should reside on each side of the connection. Code can quickly become an intermix of RPC calls with local calls, causing it to be an opaque blob that is impossible to test or debug. In addition, its performance can quickly deteriorate: Objects are being serialized back and forth all the time, and tens of implicit network round-trips introduce latency all around the code.

Of course, the tool is not necessarily at blame here. The problem may lie with those developers who use it incorrectly, instead of designing a clean distributed model around it -- which is certainly possible. But I tend to find that the thoughts and practices of developers become molded to the tools they have at hand. A tool that encourages calling remote code without a conscious effort makes it too easy to avoid thinking about the distributed design.

So, yes, I don't like RPC, especially not *stateful RPC* that supports access of remote objects by reference. I can live with simple designs like XML-RPC, supporting value-based RPC with native data types, which are fairly easy to understand and debug: There are no remote objects, just data that is passing back and forth. But I dislike tools that try to hide everything under a shiny exterior, and try to act as if remote code were just the same as local code, and as if remote objects actually exist locally with magic proxies doing all the work behind the scenes.

The above is just one of the issues in the long-standing debate regarding RPC vs. Messaging. If you're at all interested in this debate, I heartily recommend reading some of the [articles by Steve Vinoski](http://steve.vinoski.net/blog/category/rpc/), who is a leading expert on the matter and writes on it very eloquently. [This presentation](http://qconlondon.com/dl/qcon-london-2009/slides/SteveVinoski_RPCAndItsOffspringConvenientYetFundamentallyFlawed.pdf) summarizes his viewpoint quite nicely, and I quite agree with many of his points.

What Now?
---------

So, I'm looking for a good tool to create a distributed architecture that is based on explicit message passing. It should be able to send and receive native Python data types by value. It should be nicely designed, clearly documented, and should make the distinction between local code and remote code crystal clear to the developer.

I am currently investigating and evaluating several solutions. Most of them are based on the excellent ZeroMQ messaging library, along with some kind of serialization tool such as MsgPack. There are several good candidates. I'll write more about it as I make progress.
