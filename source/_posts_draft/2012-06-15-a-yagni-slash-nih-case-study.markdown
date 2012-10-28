---
layout: post
title: "A YAGNI/NIH Case Study"
date: 2012-06-15 12:09
comments: true
categories: 
---

This post is an actual example of the dilemma that I described in [my previous post](/blog/2012/06/15/the-yagni-slash-nih-conundrum/).


<!-- more -->

Prior Art
---------

As I am wont to do, I started looking around for existing solutions that could help with this project. This means tools for creating distributed architectures, with a major aspect being the communication among the components.

One tool that enjoys incredible popularity these days is [ZeroMQ](http://www.zeromq.org/). It is being mentioned in countless places and generally gets rave reviews. It looks like it is quickly becoming an ubiquitous replacements for plain old BSD sockets. It also has very nice [Python bindings](https://github.com/zeromq/pyzmq).

Having found a hammer, I now went looking for nails. One thing I needed was a replacement for using raw SSH for remote execution, and another was a replacement for RPyC. I'll explain why.

Using SSH for remote execution of shell commands may seem like a logical thing to do, but suffers from several drawbacks. One of them is the authentication process. In our scenario, all hosts are trusted and we use common SSH private keys for authentication. Having SSH authenticate for each remote command is a time consuming process, and slows down execution quite a bit. We did get around this by using OpenSSH's `ControlMaster` functionality, but it's still a bit messy, since that requires manually managing the lifecycle of the ControlMaster process. I would much prefer to have a cleaner solution for this.

Looking at Existing Solutions
-----------------------------

At PyCon 2012, I attended [a nice lecture](http://pyvideo.org/video/639/build-reliable-traceable-distributed-systems-wi) about [ZeroRPC](https://github.com/dotcloud/zerorpc-python), which is an RPC implementation using ZeroMQ and MessagePack supporting Python. However, it has a large bunch of dependencies (including gevent), and seems a bit too much for what I need anyway.

So I said, "how hard can this be"? 

