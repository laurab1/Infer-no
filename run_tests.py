from contextlib import contextmanager
import os
import subprocess
import logging

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

def main():
    with cd(os.getcwd() + "/testcode"):
        try:
            files = [f for f in os.listdir('.') if os.path.isfile(f)]
            for f in files:
                name, ext = os.path.splitext(f)
                if ext == '.java':
                    subprocess.call("infer --quandary-only -- javac " + f)
        except Exception:
            print("cannot enter dir")
            return

if __name__ == '__main__':
    main()