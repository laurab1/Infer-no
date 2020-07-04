from config import CSV_ACTUAL_TN_NUMBER,CSV_ACTUAL_TP_NUMBER
from texttable import Texttable

class ConfusionMatrix:
    # Confusion matrix generated from expected behaviour csv and actual behaviour csv
    # csv format: test name, category, real vulnerability, cwe, Benchmark version: 1.2, 2016-06-1

    def __init__(self, actual_csv, expected_csv, tp_number=CSV_ACTUAL_TP_NUMBER, tn_number=CSV_ACTUAL_TN_NUMBER):
        self.TP = 0
        self.TN = 0
        self.FP = 0
        self.FN = 0
        self.TPR = 0
        self.FPR = 0
        self.tp_number = tp_number
        self.tn_number = tn_number
        self.TP_list = []
        self.TN_list = []
        self.FP_list = []
        self.FN_list = []
        self.actual_csv = actual_csv
        self.expected_csv = expected_csv
        self._compute()

    def _compute(self):
        # cmpute the confusion matrix
        assert len(self.actual_csv) == len(self.expected_csv)
        for i, row_actual in enumerate(self.actual_csv):
            row_expected = self.expected_csv[i]
            test_name_actual = row_actual[0]
            test_name_expected = row_expected[0]

            # if test names are the same
            if test_name_actual == test_name_expected:
                expected = row_expected[2].lower()
                actual = row_actual[2].lower()

                # true=true => TP
                if expected == 'true' and actual == 'true':
                    self.TP = self.TP + 1
                    self.TP_list.append(test_name_expected)
                # true=false => FN
                elif expected == 'true' and actual == 'false':
                    self.FN = self.FN + 1
                    self.FN_list.append(test_name_expected)
                # false=true => FP
                elif expected == 'false' and actual == 'true':
                    self.FP = self.FP + 1
                    self.FP_list.append(test_name_expected)
                # false=false => TN
                elif expected == 'false' and actual == 'false':
                    self.TN = self.TN + 1
                    self.TN_list.append(test_name_expected)
        self.TPR = self.TP/self.tp_number
        self.FPR = self.FP/self.tn_number

    def pretty_print(self):
        # print the confusion matrix on std_out
        print('\n Results: \n')
        t = Texttable()
        t.add_rows([['', 'Positive', 'Negative'],
                    ['Total Population', self.tp_number, self.tn_number]])
        print(t.draw())
        t = Texttable()
        t.add_rows([[' ', 'Condition Positive', 'Condition Negative'],
                    ['Predicted \nCondition \nPositive', self.TP, self.FP],
                    ['Predicted \nCondition \nNegative', self.FN, self.TN]])
        print(t.draw())

        sensitivity=self.TPR
        specificity=1-self.FPR
        youden_index=sensitivity+specificity-1

        # Final score = Youden Index * 100
        t = Texttable()
        t.add_rows([['Final Score: ', youden_index*100],
                    ['Sensitivity: ', sensitivity],
                    ['Specificity: ', specificity]])
        print(t.draw())


