from config import *
import os
import csv
from Model.confusion_matrix import ConfusionMatrix


def confusion_builder():
    # for each csv result file inside CSV_ACTUAL_FOLDER_PATH, print the confusion matrix

    expected_csv = csv_load(CSV_EXPECTED_FILE_PATH)
    list_result_files = os.listdir(CSV_ACTUAL_FOLDER_PATH)

    for bench_file_name in list_result_files:
        try:
            actual_csv = csv_load(os.path.join(CSV_ACTUAL_FOLDER_PATH, bench_file_name))
            # create the matrix
            matrix = ConfusionMatrix(actual_csv=actual_csv, expected_csv=expected_csv)
            # print the matrix
            print("\n \nBenchmark output file: " + bench_file_name)
            matrix.pretty_print()
        except Exception as e:
            print("File: " + bench_file_name + " ignored " + str(e))


def csv_load(path):
    return list(csv.reader(open(path)))


if __name__ == "__main__":
    confusion_builder()
