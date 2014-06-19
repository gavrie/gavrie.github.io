---
layout: post
title: "Buffers will fill Up... Eventually"
date: 2014-06-18 18:42
comments: true
categories: [python, code]
published: true
---

A colleague asked me to look into a problem with him, mentioning that "Tlib hangs when we run it". Tlib is a fairly large project that is written in Python. His initial analysis showed that it hangs at a very early phase, during with it tries to fetch the latest version to run from a git server. Various users complained about the same problem, suggesting that it is not a local issue.

Running the code, and interrupting it with `^C` when it hangs, turned up a result similar to the following:

    ^CTraceback (most recent call last):
      File "./execute_wrong.py", line 8, in <module>
        retval, out, err = execute("git ls-remote")
      File "./execute_wrong.py", line 5, in execute
        retval = p.wait()
      File "/usr/lib/python2.7/subprocess.py", line 1376, in wait
        pid, sts = _eintr_retry_call(os.waitpid, self.pid, 0)
      File "/usr/lib/python2.7/subprocess.py", line 476, in _eintr_retry_call
        return func(*args)
    KeyboardInterrupt

Interesting. The code seems to hang while waiting for the `git` child process to terminate. However, running `git ls-remote` from the command line works fine, so why does it hang when run from the code?

<!-- more -->

Investigating the Issue
-----------------------

Let's look at the code history to see if anything has changed recently.

Nope. A quick `git blame` shows that this code is more than 5 years old, and has been performing flawlessly every day since then. So what else has changed?

Let's see what is happening while waiting for the `git` child process to finish, by running `strace` on the process:

    $ strace -p 5774
    Process 5774 attached
    write(1, "pull/624/merge\n2fe9da91f5a4b5ba3"..., 4096

OK. The process is trying to write to `stdout`, but hanging while doing so. It looks like some buffer is getting filled, which blocks the process from writing further.

Let's look at the size of the data returned by the child process:

    $ git ls-remote | wc -c
    From gitserver:/git/qa/tlib
       65572

Aha! This number looks suspiciously like "a bit more than 64k". Which affirms our hypothesis. Let's try to reduce its size by deleting some old remote branches:

    $ git push origin :old_branch1
    $ git push origin :old_branch2
    ...
    $ git ls-remote | wc -c
    From gitserver:/git/qa/tlib
       65368

Now to run the program again... It worked! The program continues to run successfully.

The Code
--------

Here is what the original code looked like (slightly changed to protect the innocent). Can you spot what is wrong?

{% include_code The original code buffers/execute_wrong.py %}

The problem is that we `wait()` for the process to terminate, without reading its output. Only after it terminates do we read its output. This code has worked correctly for years, since the output was by change smaller than 64k and fitted completely in the pipe's buffer. Once it exceeded the buffer's size due to one remote branch too many, it blocked the process on the pipe, while the parent was waiting for it to terminate. A classic deadlock condition.

The Fix
-------

Now that we see the problem, fixing it is simple: First read, then wait.

{% include_code The fixed code buffers/execute_right.py %}

Conclusion
----------

Buffers, filesystems, databases will all fill up sometime in the future. Always take this into account when writing code. Any time you generate some data, be sure to set up a process to prune the data and don't assume that it will be OK -- because it will come back to bite you, or at least some future user of your code.
