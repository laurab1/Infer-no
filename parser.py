from contextlib import contextmanager
import os
import json

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

def parse_results(path):
    results = {}
    with cd(os.getcwd() + path):
        try:
            with open("report.txt", 'r') as f:
                for line in f:
                    try:
                        strs = line.split('/')
                        if strs[0] == "src":
                            mystr = strs[7]
                            filename = mystr.split(':')
                            results[filename[0]] = True
                        else:
                            continue
                    except Exception:
                        print("error while reading")
            f.close()
        except Exception:
            print("cannot access the report file")
    for item in results.items():
        print(item)
    return results