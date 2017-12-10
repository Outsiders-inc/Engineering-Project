import os
import argparse
from argparse import RawDescriptionHelpFormatter
from unittest.mock import _MockIter
from enum import Enum

_F_by_sent = []
_recall_by_sent = []
_precision__by_sent = []
_total_recall = 0
_total_precision = 0
_total_F_measure = 0

# CRF+ result-file locations:
GOLD_STANDARD_TAG = -2
OUR_CRF_TAG = -1

# Types of tags:
NOT_A_NAME = 'O'
CONTINUE_SUFFIX = '_C'
END_OF_SENTENCE = ""
# BEGINNING_SUFFIX = '_I'

correct = "correct"
incorrect = "incorrect"
missing = "missing"
spurious = "spurious"

_correct_list = []
_incorrect_list = []
_missing_list = []
_spurious_list = []
_O_positive_list = []

# For searching specific tags:
person_str = "PERS"
organization_str = "ORG"
location_str = "LOC"
date_str = "DATE"
percent_str = "PERCENT"
misc_str = "MISC"

#tagType = Enum(PERSON = 0, ORGANIZATION = 2, LOCATION = 2, DATE = 3, PERCENT = 4, MISC = 5)
tagTypeMap = {'PERSON' : 0, 'ORGANIZATION' : 1, 'LOCATION' : 2, 'DATE' : 3, 'PERCENT' : 4, 'MISC' : 5}
currentType = tagTypeMap['PERSON']

# Returns the total number of names and phrases (the name + the non_names) in the sentence
def analyze_sentence(sent):

    print("......Started 'analyze_sentence'...")

    total_names_in_sentence = 0
    total_phrases_in_sentence = 0
    continuing_length = 0
    continue_correct = correct
    _correct, _incorrect, _missing, _spurious, _O_positive = 0, 0, 0, 0, 0

    for i, word in enumerate(sent):

        word = word.split("\t")

        # If gold == "O":
        # ---------------
        if word[GOLD_STANDARD_TAG] == NOT_A_NAME:
            if continuing_length >= 1:
                if continue_correct == correct:
                    _correct += 1
                elif continue_correct == incorrect:
                    _incorrect += 1
                elif continue_correct == missing:
                    _missing += 1
                total_names_in_sentence += 1
                total_phrases_in_sentence += 1

            # Initialize the variable for a new phrase
            continuing_length = 0
            continue_correct = correct

            if word[OUR_CRF_TAG] == NOT_A_NAME: # or word[OUR_CRF_TAG] == END_OF_SENTENCE:
                _O_positive += 1
            else:
                _spurious += 1
            total_phrases_in_sentence += 1

        # if END_OF_SENTENCE:
        # -------------------
        elif word[GOLD_STANDARD_TAG] == END_OF_SENTENCE:
            if continuing_length >= 1:
                if continue_correct == correct:
                    _correct += 1
                elif continue_correct == incorrect:
                    _incorrect += 1
                elif continue_correct == missing:
                    _missing += 1
                total_names_in_sentence += 1
                total_phrases_in_sentence += 1

            # Initialize the variable for a new phrase
            continuing_length = 0
            continue_correct = correct

            if word[OUR_CRF_TAG] == "END_OF_SENTENCE": # What to do if it's crf == "O" ??)
                _O_positive += 1
            elif word[OUR_CRF_TAG] != NOT_A_NAME:
                _spurious += 1

        # If gold == "*_C":
        # -----------------
        elif word[GOLD_STANDARD_TAG][-2:] == CONTINUE_SUFFIX:
            if continuing_length >= 1:
                if continue_correct == correct:
                    if word[OUR_CRF_TAG] != word[GOLD_STANDARD_TAG] and \
                            (word[OUR_CRF_TAG] != NOT_A_NAME and word[OUR_CRF_TAG] != END_OF_SENTENCE):
                        continue_correct = incorrect
                    elif word[OUR_CRF_TAG] == NOT_A_NAME or word[OUR_CRF_TAG] == END_OF_SENTENCE:
                        continue_correct = missing
                elif continue_correct == incorrect and \
                                word[OUR_CRF_TAG] == NOT_A_NAME or word[OUR_CRF_TAG] == END_OF_SENTENCE:
                    continue_correct = missing

                # Increase length of phrase
                continuing_length += 1

            else:
                continuing_length += 1
                continue_correct = missing

        # else (a "regular" name tag):
        # -----------------------------
        else:
            if continuing_length >= 1:
                if continue_correct == correct:
                    _correct += 1
                elif continue_correct == incorrect:
                    _incorrect += 1
                elif continue_correct == missing:
                    _missing += 1
                total_names_in_sentence += 1
                total_phrases_in_sentence += 1

            # Initialize the variable for a new phrase - this time a phrase that might be long
            continuing_length = 1
            continue_correct = correct

            if word[OUR_CRF_TAG] == NOT_A_NAME or word[OUR_CRF_TAG] == END_OF_SENTENCE:
                continue_correct = missing
            elif word[OUR_CRF_TAG] != word[GOLD_STANDARD_TAG]: # A "regular" name tag
                continue_correct = incorrect

    _correct_list.append(_correct)
    _incorrect_list.append(_incorrect)
    _missing_list.append(_missing)
    _spurious_list.append(_spurious)
    _O_positive_list.append(_O_positive)
    return [total_phrases_in_sentence, total_names_in_sentence]


# Calculates the total_recall, total_precision, and total_F_measure (saves them in the global variables).
# Also calculates it for each sentence and puts the results in the global arrays
def make_statistics(res_file, _total_phrases, _total_names):

    print("...___Started 'make_statistics' for file: " + res_file)

    # Calculating the overall Recall and Precision (and F-measure):
    total_correct = sum(_correct_list)
    total_incorrect = sum(_incorrect_list)
    total_missing = sum(_missing_list)
    total_spurious = sum(_spurious_list)
    global _total_F_measure, _total_precision, _total_recall
    div_r = total_correct + total_incorrect + total_missing
    if div_r == 0:
        _total_recall = 0
    else:
        _total_recall = total_correct / div_r
    div_p = total_correct + total_incorrect + total_spurious
    if div_p == 0:
        _total_precision = 0
    else:
        _total_precision = total_correct / div_p
    div_f = _total_recall + _total_precision
    if div_f == 0:
        _total_F_measure = 0
    else:
        _total_F_measure = (2 * _total_recall * _total_precision) / div_f

    print("_correct_list: " + str(_correct_list))
    print("_incorrect_list: " + str(_incorrect_list))
    print("_missing_list: " + str(_missing_list))
    print("_spurious_list: " + str(_spurious_list))

    # Calculating the Recall and Precision (and F-measure) for each sentence:
    for i in range(len(_correct_list)):
        div_r = _correct_list[i] + _incorrect_list[i] + _missing_list[i]
        if div_r == 0:
            recall = 0
        else:
            recall = _correct_list[i] / div_r
        div_p = _correct_list[i] + _incorrect_list[i] + _spurious_list[i]
        if div_p == 0:
            precision = 0
        else:
            precision = _correct_list[i] / div_p
        div_f = recall + precision
        if div_f == 0:
            f_measure = 0
        else:
            f_measure = (2 * recall * precision) / div_f

        _recall_by_sent.append(recall)
        _precision__by_sent.append(precision)
        _F_by_sent.append(f_measure)


def run_analysis(res_file):
    print("...Started 'run_analysis' for file: " + res_file)

    end_of_file = False
    sentence = []
    sentence_counter = 0
    _total_names = 0
    _total_phrases = 0
    # word_counter = 0
    data = open(res_file, 'r', encoding="utf-8")
    # data = open(res_file, 'r')
    while not end_of_file:
        # word_counter += 1
        line = data.readline()
        if not line:
            end_of_file = True
            break
        # # TODO - Just because it adds empty lines after each line:
        # if (word_counter % 2 == 0):
        #     continue
        line = line.strip("\n").strip("\t").strip(" ")
        if len(line):
            print("found regular line. starting with: " + line.split("\t")[0]) # TODO - Just a print
            print("line-length: " + str(len(line)))
            print("FULL LINE:" + line)
            sentence.append(line)
        # if we've reached the end of the sentence - en empty line.
        else:
            print("empty line")  # TODO - Just a print
            sentence_counter += 1
            analysis_res = analyze_sentence(sentence)
            sentence = []
            _total_phrases += analysis_res[0]
            _total_names += analysis_res[1]
    # TODO Check if end_of_file is True, to know if we've scanned all of the file!!!
    if not end_of_file:
        exit("ERROR!! DID NOT REACH END OF FILE!")
    make_statistics(res_file, _total_phrases, _total_names)

    # Write to file
    file_name_short = res_file.split("/")[1]
    res_file_name = "output/" + file_name_short + "_analysis" + ".txt"
    res = open(res_file_name, 'w', encoding="utf-8")
    res.write(">>> TOTAL : <<< \n")
    res.write("    ------      \n")
    res.write("F_measure , Recall , Presicion \n")
    res.write(str(_total_F_measure) + " , " + str(_total_recall) + " , " + str(_total_precision) + "\n\n")
    res.write(">>> By Sentence : <<< \n")
    res.write("    ------------      \n")
    res.write("F_measure , Recall , Precision \n")
    for i in range(len(_F_by_sent)):
        res.write(str(i) + ") " + str(_F_by_sent[i]) + " , " + str(_recall_by_sent[i]) + " , "
                  + str(_precision__by_sent[i]) + "\n")
    res.close()
    return res_file_name
if __name__ == '__main__':
    files_to_test = []
    files_to_test.append("input/input_test_all_correct.txt")
    files_to_test.append("input/input_test_2_missing.txt")
    files_to_test.append("input/input_test_3_incorrect.txt")
    files_to_test.append("input/input_test_4_spurious.txt")
    files_to_test.append("input/input_test_5_misc.txt")
    files_to_test.append("input/input_test_6_misc.txt")
    for file in files_to_test:
        print("Starting the program for file: " + file)
        run_analysis(file)

        # Initializing the global variables after each run
        _F_by_sent = []
        _recall_by_sent = []
        _precision__by_sent = []
        _total_recall = 0
        _total_precision = 0
        _total_F_measure = 0
        _correct_list = []
        _incorrect_list = []
        _missing_list = []
        _spurious_list = []
        _O_positive_list = []
