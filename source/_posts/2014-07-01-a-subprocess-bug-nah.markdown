---
layout: post
title: "A subprocess bug? Nah."
date: 2014-07-01 16:57
comments: true
categories: [python, code]
---

A few weeks ago, a colleague came to me with an interesting bug: When running a child process with Python's `subprocess` module, no exception is thrown when the child process fails. In essence, what happened was the following (typed at the interactive Python prompt):

    >>> import subprocess
    >>> subprocess.check_call("false")
    0

The `false` command always exits with a nonzero exit code. The expected behavior, as confirmed on another machine, would be as follows:

    >>> subprocess.check_call("false")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/subprocess.py", line 542, in check_call
        raise CalledProcessError(retcode, cmd)
    subprocess.CalledProcessError: Command 'false' returned non-zero exit status 1

So, what happens is that `subprocess` thinks that the child process exited successfully, even though it did not.

This behavior, of course, wreaks total havoc with the application. Instead of an exception being thrown due to the failed child process, the application goes on and fails at a later point when it tries to do something based on the data received from the child process. This goes against the good design principle of [failing early](http://en.wikipedia.org/wiki/Fail-fast), as embodied by the way Python uses exceptions instead of error codes.

So, what is going on here? You may want to think it through and see if you can find the problem.

<!-- more -->

Diving In
---------

At first sight, this looks like a problem with either Python itself or with the OS (Linux, in our case). How could this happen?  The colleague who first encountered this issue looked at it through the Python debugger, and got as far as the `wait()` function of `subprocess`:


``` python
def wait(self):
    """Wait for child process to terminate.  Returns returncode attribute."""
    while self.returncode is None:
        try:
            pid, sts = _eintr_retry_call(os.waitpid, self.pid, 0)
        except OSError as e:
            if e.errno != errno.ECHILD:
                raise
            # This happens if SIGCLD is set to be ignored or waiting
            # for child processes has otherwise been disabled for our
            # process.  This child is dead, we can't get the status.
            pid = self.pid
            sts = 0
        # Check the pid and loop as waitpid has been known to return
        # 0 even without WNOHANG in odd situations.  issue14396.
        if pid == self.pid:
            self._handle_exitstatus(sts)
    return self.returncode
```

As seen in the code, if `os.waitpid` on a child process fails with `ECHILD`, an exception is not raised. The reason for this is that `ECHILD` is returned in cases where there is no child process to be waited for. Normally, when a process terminates, the kernel keeps information such as its exit code until the parent calls `wait()` on it. In the interim, the process is a so-called "zombie". If there is no child process (even not a zombie), we cannot know if it succeeded or failed.

The above piece of code went into Python's `subprocess` module as part of a fix for another problem, as documented in [this Python bug report](http://bugs.python.org/issue1731717). 

Python chooses to assume that the child process exited successfully. Is this a correct assumption? Well, it's as good as any other. In the legitimate use case, namely when a process explicitly ignores `SIGCHLD` since it isn't interested in the exit code of its child processes, it makes sense for `waitpid()` to always complete successfully. Of course this can be argued against, but it is not a senseless assumption.


Back to the Code
----------------

Do we by any chance ignore `SIGCHLD` in our application? The chance we do is very small, since we run a lot of child processes and depend on their state all their time, and this fails only occasionally. A quick `git grep` on the code shows that we *do* ignore `SIGCHLD` in one specific standalone Python script, but that script is not part of the application and is run on a remote machine on which we indeed *should* ignore this signal.

At this point, I suspected (wrongly, as we shall see) that this was a problem with the specific host on which it happened, and resolved the issue as "Can't reproduce". Since this happened more than once, this was not ideal, so I asked other team members to keep an eye open in case this happened again.


A Week Later
------------

Of course, a week later it happened again. Fortunately, this time it was caught as it happened and we could look at the live process in the debugger. My colleague [Erez Horev](https://plus.google.com/107274679081446769903/) called me over and we started looking at it together.

We easily reproduced the issue in the debugger. After a lot of dead ends, we concluded that the only logical way of this happening was indeed if the application ignored `SIGCHLD`. To check if this was the case, we ran the following in the debugger:

```
>>> signal.getsignal(signal.SIGCHLD)
1
>>> signal.SIG_IGN
1
```

Indeed -- `SIGCHLD` is being ignored by our application. How can this be? Nowhere in the code do we ignore `SIGCHLD`, except for that standalone script, which runs only on the remote machine. Or does it?


Checking our Assumptions
------------------------

At this point, the only thing left to do was to look at that script. It includes the following line, right at the top.

``` python
signal.signal(signal.SIGCHLD, signal.SIG_IGN)
```

Could we, by any chance, have `imported` this script as a module in our application, therefore running the above code as a side effect?

It turns out we were doing exactly that. In recently added code, under specific circumstances, our application imports the module in order to get its filename and to deploy it to the remote machine. While normally `import` should be clean of side effects, the above `signal` code appears at the module level and not inside a function, and is therefore run when imported. This contaminates our application and causes it to ignore `SIGCHLD` with the described consequences.

Moving this line fixed the problem.


Question Everything
-------------------

[Mark Dalrymple](http://www.bignerdranch.com/about-us/nerds/mark-dalrymple.html), in his [Thoughts on Debugging, Part 1](http://www.bignerdranch.com/blog/thoughts-on-debugging-part-1/), talks about the hierarchy of potential blame when debugging. In short, new code is the first suspect, after which come old code, library code etc. The point here is that the chance of there being a bug in Python is much smaller than that of there being a bug in your own code. Not only that, but the chance of the bug being in new code is the highest.

The idea of there being a bug in Python or an OS issue might have been valid, but it was not likely. The assumption that this *could not happen* since the relevant code does not run turned out to be false. The bug was indeed in our code, and in new code at that.


Conclusion
----------

As a lesson from this, aside from some debugging ideas, please remember: Don't run any code that may have side effects at the module top level! Somehow, some day, your module will be imported by other code that may be hurt by this side effect. Put all code in functions, or use the Python `if __name__ == '__main__'` construct.
