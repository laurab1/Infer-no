from contextlib import contextmanager
from parser import cd
from parser import parse_results, fill_csv
from config import *
import os
import subprocess
import logging


def main():
    with cd(os.getcwd() + "/benchmark"):
        try:
            subprocess.call("mvn clean && infer --quandary-only -- mvn install", shell=True)
        except Exception:
            print("cannot enter dir")
            return
    results = parse_results(TEST_PROJECT_INFER_FOLDER)
    fill_csv(CSV_ACTUAL_FOLDER_PATH, results)
    return


if __name__ == '__main__':
    main()
