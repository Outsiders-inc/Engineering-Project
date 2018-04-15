
CORP_NAME = "organized_corp"
CURRENT_CORP = CORP_NAME + ".txt"
NEW_NAME_SUF = "_new_feature.txt"
NEW_LINE = "\n"
NEW_SPOT = 2
SEP = "\t"


# Push to corpus with corpus_file_name a feature with values feature_values before tag.
# Saves as a new file with the name:
# corpus_name + "_new_feature.txt"
def add_feature(corpus_file_name, corpus_name, feature_values):
    with open(corpus_file_name, "r", encoding="utf-8") as corp:
        lines = corp.readlines()
    if len(feature_values) != len(lines):
        print("ERROR: number of feature values is not the number of lines")
        return 1
    new_corp = []
    for i, line in enumerate(lines):
        new_line = NEW_LINE
        if line != NEW_LINE:
            words = line.split(SEP)
            words.insert(len(words) - NEW_SPOT, feature_values[i])
            new_line = SEP.join(words)
        new_corp.append(new_line)
    with open(corpus_name + NEW_NAME_SUF, "w", encoding="utf-8") as corp:
        corp.writelines(new_corp)
# That works:
# feature = []
# with open(CURRENT_CORP, encoding="utf-8") as corp:
#     feature = ["1" for i in corp.readlines()]
# add_feature(CURRENT_CORP, CORP_NAME, feature)


# Structure features- begin of sentence
def is_begin_feat(corpus_file_name):
    with open(corpus_file_name, "r", encoding="utf-8") as corp:
        lines = corp.readlines()
    is_begin = list()
    is_end = list()
    prev_line = "\n"
    for line in lines:
        if prev_line == "\n":
            is_begin.append("1")
        else:
            is_begin.append("0")
        prev_line = line
    add_feature(corpus_file_name, corpus_file_name, is_begin)


# Structure features- end of sentence
def is_end_feat(corpus_file_name):
    with open(corpus_file_name, "r", encoding="utf-8") as corp:
        lines = corp.readlines()
    is_end = ["0"] * len(lines)
    for index,line in enumerate(lines):
        if line == "\n":
            is_end[index - 2] = "1"
    add_feature(corpus_file_name, corpus_file_name, is_end)
