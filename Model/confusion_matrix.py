from config import CSV_ACTUAL_TN_NUMBER, CSV_ACTUAL_TP_NUMBER
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
        self.fn_error_rank = []
        self.fp_error_rank = []
        self.vulnerability_tested_counter = {}
        self._compute()

    def _compute(self):
        self._confusion_matrix_build()
        self._classification_build()

    def _confusion_matrix_build(self):
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

                vuln_name = row_expected[1]
                if vuln_name in self.vulnerability_tested_counter:
                    self.vulnerability_tested_counter[vuln_name] = self.vulnerability_tested_counter[vuln_name] + 1
                else:
                    self.vulnerability_tested_counter[vuln_name] = 1

                # true=true => TP
                if expected == 'true' and actual == 'true':
                    self.TP = self.TP + 1
                    self.TP_list.append(row_expected)
                # true=false => FN
                elif expected == 'true' and actual == 'false':
                    self.FN = self.FN + 1
                    self.FN_list.append(row_expected)
                # false=true => FP
                elif expected == 'false' and actual == 'true':
                    self.FP = self.FP + 1
                    self.FP_list.append(row_expected)
                # false=false => TN
                elif expected == 'false' and actual == 'false':
                    self.TN = self.TN + 1
                    self.TN_list.append(row_expected)

        self.TPR = self.TP / self.tp_number
        self.FPR = self.FP / self.tn_number

    def _classification_build(self):
        # build misclassification statistics
        fn_ledger = {}
        fp_ledger = {}

        for elem in self.FN_list:
            vuln_name = elem[1]
            if vuln_name in fn_ledger:
                fn_ledger[vuln_name] = fn_ledger[vuln_name] + 1
            else:
                fn_ledger[vuln_name] = 1

        for elem in self.FP_list:
            vuln_name = elem[1]
            if vuln_name in fp_ledger:
                fp_ledger[vuln_name] = fp_ledger[vuln_name] + 1
            else:
                fp_ledger[vuln_name] = 1

        # sort items by value
        def percentage(name, val):
            return val * 100 / self.vulnerability_tested_counter[name]

        self.fn_error_rank = [[k, percentage(k, v), v] for k, v in
                              sorted(fn_ledger.items(), key=lambda item: percentage(item[0], item[1]), reverse=True)]
        self.fp_error_rank = [[k, percentage(k, v), v] for k, v in
                              sorted(fp_ledger.items(), key=lambda item: percentage(item[0], item[1]), reverse=True)]

    def pretty_print(self):
        # print the confusion matrix and statistics on std_out
        print('\nResults: \n')

        print('Top 3 False Negative misclassification by Vulnerability type')
        t = Texttable()
        t.add_rows(
            [['Vulnerability name', 'Relative Incorrect classification %', 'Absolute Incorrect classification %']])
        try:
            for i in range(3):
                k = self.fn_error_rank[i]
                t.add_row([k[0], k[1], k[2] * 100 / self.FN])
        except Exception as e:
            print("There aren't at least 3 false negative, congrats!")
        print(t.draw())

        print('\nTop 3 False Positive misclassification by Vulnerability type')
        t = Texttable()
        t.add_rows([['Vulnerability name', 'Incorrect classification %', 'Absolute Incorrect classification %']])
        try:
            for i in range(3):
                k = self.fp_error_rank[i]
                t.add_row([k[0], k[1], k[2] * 100 / self.FP])
        except Exception as e:
            print("There aren't at least 3 false negative, congrats!")
        print(t.draw())

        print('\nConfusion Matrix')
        t = Texttable()
        t.add_rows([['', 'Positive', 'Negative'],
                    ['Total Population', self.tp_number, self.tn_number]])
        print(t.draw())
        t = Texttable()
        t.add_rows([[' ', 'Condition Positive', 'Condition Negative'],
                    ['Predicted \nCondition \nPositive', self.TP, self.FP],
                    ['Predicted \nCondition \nNegative', self.FN, self.TN]])
        print(t.draw())

        sensitivity = self.TPR
        specificity = 1 - self.FPR
        youden_index = sensitivity + specificity - 1

        # Final score = Youden Index * 100
        t = Texttable()
        t.add_rows([['Final Score: ', youden_index * 100],
                    ['Sensitivity: ', sensitivity],
                    ['Specificity: ', specificity]])
        print(t.draw())
