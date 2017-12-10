# Macros
NUMBER_OF_ATT = 18  # Range 0 to 17
WINDOW_SIZE = 2  # A window of 5, -2 to 2


def make_feature(row, col):
    return "%x[" + str(row) + "," + str(col) + "]"


def make_uni(feature_num, row, col):
    return "U" + str(feature_num) + ":" + make_feature(row, col)


# Word level Bigram
def make_short_bigram(feature_num, rows, cols):
    bigram = "U" + str(feature_num) + ":"
    for i, row in enumerate(rows):
        bigram += make_feature(row, cols[i])
    return bigram


# Word and tag level bigram
def make_bigram(feature_num, row, col):
    return "B" + feature_num + ":" + make_feature(row, col)


# Class Template will open a file with a given name and enables features insert
# using "add_unigram_features"
# Use "close" in the end of use.
class Template:
    def __init__(self, file_name):
        self.template_file = open(file_name, 'w', encoding="utf-8")
        self.feature_counter = 0

    # Add a word level bigram or a uni
    def add_unigram_features(self, rows, cols):
        feature = "";
        if isinstance(rows, int):
            feature = make_uni(self.feature_counter, rows, cols)
        else:
            feature = make_short_bigram(self.feature_counter, rows, cols)
        self.template_file.write(feature + "\n")
        self.feature_counter += 1

    def close(self):
        self.template_file.close()
