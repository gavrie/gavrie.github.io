import subprocess

def execute(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    retval = p.wait()
    return retval, p.stdout.read(), p.stderr.read()

retval, out, err = execute("git ls-remote")
