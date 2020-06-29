class ConfusionMatrix:
    # Confusion matrix generated from expected behaviour csv and actual behaviour csv
    # csv format: test name, category, real vulnerability, cwe, Benchmark version: 1.2, 2016-06-1

    def __init__(self, actual_csv, expected_csv):
        self.TP = 0
        self.TN = 0
        self.FP = 0
        self.FN = 0
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
                expected = row_expected[2]
                actual = row_actual[2]

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

    def pretty_print(self):
        # print the confusion matrix on std_out
        print('Results: \n')
        print('True Positive: ' + str(self.TP))
        print('True Negative: ' + str(self.TN))
        print('False Positive: ' + str(self.FP))
        print('False Negative: ' + str(self.FN))
