from contextlib import contextmanager
from parser import cd
from parser import parse_results
import os
import subprocess
import logging

def main():
    with cd(os.getcwd() + "/testcode"):
        try:
            subprocess.call("mvn clean && infer --quandary-only -- mvn install", shell=True)
        except Exception:
            print("cannot enter dir")
            return
    results = parse_results("/infer-out")
    return

if __name__ == '__main__':
    main()