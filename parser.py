from contextlib import contextmanager
import os
from os import listdir
from os.path import isfile, join
from config import *
import csv


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
    with cd(os.path.join(os.getcwd(), path)):
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
    return results


def fill_csv(path, results):
    testpath = os.path.join(os.getcwd(), TEST_SOURCE_FILES)
    out = [f for f in listdir(testpath) if (isfile(join(testpath, f)) and f.split('.')[1] == 'java')]
    out.sort()
    with cd(os.path.join(os.getcwd(), path)):
        try:
            with open('actual.csv', mode='w') as actual_results:
                res_writer = csv.writer(actual_results, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for item in out:
                    found = True if item in results else False
                    res_writer.writerow([item.split('.')[0], "a_string", found, 0])
            return
        except Exception:
            print("cannot access the csv file")
    return
