import subprocess

def execute(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.stdout.read()
    err = p.stderr.read()
    retval = p.wait()
    return retval, out, err

retval, out, err = execute("git ls-remote")
