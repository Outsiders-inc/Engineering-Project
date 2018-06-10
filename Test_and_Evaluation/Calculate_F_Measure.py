from datetime import datetime

# CRF+ result-file locations:
from builtins import print

GOLD_STANDARD_TAG = -2
OUR_CRF_TAG = -1

TAG_TYPES = {'PERS' : 0, 'ORG' : 1, 'LOC' : 2, 'DATE' : 3, 'PERCENT' : 4, 'MONEY' : 5, 'TIME' : 6,
             'MISC_AFF' : 7, 'MISC_EVENT' : 8, 'MISC_ENT' : 9, 'MISC_MODEL' : 10}
NOT_A_NAME = 'O'
CONTINUE_SUFFIX = '_C'
END_OF_SENTENCE = ""

_F_by_type = []
_recall_by_type = []
_precision__by_type = []
_total_recall = 0
_total_precision = 0
_total_F_measure = 0

tag_counts_file_name = "output/tags_counts_file.txt"

# Takes the tag_origin'th element in each word in the sentence and return a list comprised only of those elements.
def create_tag_list_by(sentence, tag_origin):
    tag_list = []
    for word in sentence:
        tag_list.append(word[tag_origin])
    return tag_list


# Returns a 2D list, 1st row is the word's index (for each name), 2nd row is the tag_type.
def get_name_list_from(sentence, tag_type):
    # Run on sentence and return a list containing only name expressions
    phrase_length = 0
    name_list = []
    if tag_type == 'ALL':
        print("Running 'get_name_list_from' for ALL")  # TODO DELETE !!!!!!!!11--------------------- !!!!!!!!
        current_phrase = []
        current_tag = 'O'
        for i,tag in enumerate(sentence):
            # If we found a regular tag - start of a name phrase
            if tag in TAG_TYPES:
                if len(current_phrase) > 0:
                    name_list.append([current_phrase.copy(), current_tag])
                current_phrase.clear()
                current_tag = tag
                current_phrase.append(i)
                phrase_length = 1
            # If it's not a name at all
            elif tag == NOT_A_NAME or tag == END_OF_SENTENCE:
                if len(current_phrase) > 0:
                    name_list.append([current_phrase.copy(), current_tag])
                current_phrase.clear()
                phrase_length = 0
                current_tag = 'O'
            # If we found a continue tag - adding to the existing name phrase
            elif i > 0:
                if CONTINUE_SUFFIX in sentence[i - 1]:
                    continue_tag = sentence[i - 1]
                else:
                    continue_tag = sentence[i-1] + CONTINUE_SUFFIX
                if tag == continue_tag and phrase_length > 0:
                    current_phrase.append(i)
                    phrase_length += 1
                else:
                    if len(current_phrase) > 0:
                        name_list.append([current_phrase.copy(), current_tag])
                        #name_list.append([current_phrase.copy(), tag_type])
                    current_phrase.clear()
                    phrase_length = 0
        if len(current_phrase) > 0:
            name_list.append([current_phrase.copy(), current_tag])
        return name_list

    elif tag_type in TAG_TYPES.keys():
        print("Running 'get_name_list_from' for " + tag_type)  # TODO DELETE !!!!!!!!11--------------------- !!!!!!!!
        current_phrase = []
        for i, tag in enumerate(sentence):
            # If we found a regular tag - start of a name phrase
            if tag == tag_type:
                if len(current_phrase) > 0:
                    name_list.append([current_phrase.copy(), tag_type])
                current_phrase.clear()
                current_phrase.append(i)
                phrase_length = 1

            # If it's not a name at all
            elif tag == NOT_A_NAME or tag == END_OF_SENTENCE:
                if len(current_phrase) > 0:
                    name_list.append([current_phrase.copy(), tag_type])
                current_phrase.clear()
                phrase_length = 0

            # If we found a continue tag - adding to the existing name phrase
            elif i > 0:
                if sentence[i - 1] == tag_type + CONTINUE_SUFFIX:
                    continue_tag = sentence[i - 1]
                else:
                    continue_tag = tag_type + CONTINUE_SUFFIX
                if tag == continue_tag and phrase_length > 0:
                    current_phrase.append(i)
                    phrase_length += 1
                else:
                    if len(current_phrase) > 0:
                        name_list.append([current_phrase.copy(), tag_type])
                    current_phrase.clear()
                    phrase_length = 0
        if len(current_phrase) > 0:
            name_list.append([current_phrase.copy(), tag_type])
        return name_list
    else:
        # nothing
        return [[[-1, -1]]]


# Calculates the recall of a text, separated to sentences (a list of lists) , returns integer
def calculate_recall(gold_names, pred_names):     #TODO - IMPLEMENT !!!!!!!!!!!!!!!!!!!!
    correct = 0
    total_gold_length = 0
    print("pred_names " + str(pred_names))
    for i, gold_sentence in enumerate(gold_names):
        print("gold_sentence " + str(gold_sentence))
        print("i = " + str(i))  # TODO - DELETE
        for name in gold_sentence:
            if name in pred_names[i]:
                correct += 1
        total_gold_length += len(gold_sentence)
    if total_gold_length == 0:
        return 0
    return correct / total_gold_length


# Calculates the precision of a text, separated to sentences (a list of lists) , returns integer
def calculate_precision(gold_names, pred_names):     #TODO - IMPLEMENT !!!!!!!!!!!!!!!!!!!!
    correct = 0
    total_pred_length = 0
    for i, pred_sentence in enumerate(pred_names):
        for name in pred_sentence:
            if name in gold_names[i]:
                correct += 1
        total_pred_length += len(pred_sentence)
    if total_pred_length == 0:
        return 0
    return correct / total_pred_length


# Calculates the F-Measure of a text, separated to sentences (a list of lists).
# Returns a list of integers: [f_measure_res, recall_res, precision_res]
# Input:
#   gold_sentences - List of Gold-standard tags, separated to sentences (a list of lists).
#   pred_sentences - List of our Predicted tags, separated to sentences (a list of lists).
def calculate_F_measure(gold_sentences, pred_sentences):
    # Creating name lists from all sentences in both pred and gold:
    gold_sentences_list = list()
    pred_sentences_list = list()

    for i, gold_sent in enumerate(gold_sentences):
        pred_sent = pred_sentences[i]
        gold_names_list = get_name_list_from(gold_sent, 'ALL')
        pred_names_list = get_name_list_from(pred_sent, 'ALL')

        gold_sentences_list.append(gold_names_list)
        pred_sentences_list.append(pred_names_list)

    # Calculating Reccall and Precision for all sentences:
    recall_res = calculate_recall(gold_sentences_list, pred_sentences_list)
    precision_res = calculate_precision(gold_sentences_list, pred_sentences_list)

    # Calculating the F-Measure:
    div_f = recall_res + precision_res
    if div_f == 0:
        f_measure_res = 0
    else:
        f_measure_res = (2 * recall_res * precision_res) / div_f

    return [f_measure_res, recall_res, precision_res]


# Calculates the F-Measure of a text by EACH tag separately, separated to sentences (a list of lists).
# Returns 3 lists of integers: [f_measure_res, recall_res, precision_res], containing the results for each tag
#   from the 'TAG_TYPES' list in the order it appears on the list.
# Input:
#   gold_sentences - List of Gold-standard tags, separated to sentences (a list of lists).
#   pred_sentences - List of our Predicted tags, separated to sentences (a list of lists).
def calculte_F_measure_by_tag(gold_sentences, pred_sentences):
    # global recall_res
    # global precision_res
    # global f_measure_res
    recall_res = []
    precision_res = []
    f_measure_res = []
    print("TAG_TYPES.keys(): " + str(TAG_TYPES.keys()))  # TODO DELETE !!!!------------------
    print("gold_sentences: " + str(gold_sentences))  # TODO DELETE !!!!------------------
    print("pred_sentences: " + str(pred_sentences))  # TODO DELETE !!!!------------------
    # gold_names_list = []
    # pred_names_list = []
    # Calculating Recall and Precision for each tag type:
    for tag_type in TAG_TYPES.keys():
        gold_names_list = []
        pred_names_list = []
        print("for loop, now on " + tag_type)  # TODO DELETE !!!!-----------------
        for i, gold_sent in enumerate(gold_sentences):
            # if len(gold_sent) == 0:
            #     break
            pred_sent = pred_sentences[i]
            gold_names_list.append(get_name_list_from(gold_sent, tag_type))
            pred_names_list.append(get_name_list_from(pred_sent, tag_type))
        print("gold_names_list: " + str(gold_names_list))  # TODO DELETE !!!!------------------
        print("pred_names_list: " + str(pred_names_list))  # TODO DELETE !!!!------------------
        recall_res.append(calculate_recall(gold_names_list, pred_names_list))
        precision_res.append(calculate_precision(gold_names_list, pred_names_list))


    # Calculating the F masure for each tag type:
    for rec, prec in zip(recall_res, precision_res):
        div_f = rec + prec
        if div_f == 0:
            f_measure_res.append(0)
        else:
            f_measure_res.append((2 * rec * prec) / div_f)
    return [f_measure_res, recall_res, precision_res]


    # for tag_type in TAG_TYPES.keys():
    #     print ("for loop, now on " + tag_type)          # TODO DELETE !!!!-----------------
    #     gold_names_list = get_name_list_from(gold_sent, tag_type)
    #     pred_names_list = get_name_list_from(pred_sent, tag_type)
    #     recall_res.append(calculate_recall_sentence(gold_names_list, pred_names_list))
    #     precision_res.append(calculate_precision_sentece(gold_names_list, pred_names_list))
    # f_measure_res = []
    # print("recall_res: " + str(recall_res))             # TODO DELETE !!!!-----------------
    # print("pred_names_list: " + str(pred_names_list))   # TODO DELETE !!!!-----------------
    # for i in range(len(recall_res)):
    #     div_f = recall_res[i] + precision_res[i]
    #     if div_f == 0:
    #         f_measure_res.append(0)
    #     else:
    #         f_measure_res.append((2 * recall_res[i] * precision_res[i]) / div_f)
    # return f_measure_res


def run_analysis(file_to_analyze):
    print("...Started 'run_analysis' for file: " + file_to_analyze)

    # global _F_by_type
    # global _recall_by_type
    # global _precision__by_type

    end_of_file = False
    sentence = []
    gold_sentences, pred_sentences = [], []
    sentence_counter = 0
    data = open(file_to_analyze, 'r', encoding="utf-8")
    # data = open(res_file, 'r')
    while not end_of_file:
        line = data.readline()
        if not line:
            end_of_file = True
            break

        line = line.strip("\n").strip("\t").strip(" ")
        if len(line):
            print("found regular line. starting with: " + line.split("\t")[0])  # TODO - Just a print
            print("line-length: " + str(len(line)))
            line = line.split("\t")
            print("FULL LINE:" + str(line))
            sentence.append(line)
        # if we've reached the end of the sentence - en empty line.
        else:
            print("empty line")  # TODO - Just a print
            sentence_counter += 1
            gold_sentence = create_tag_list_by(sentence, GOLD_STANDARD_TAG)
            pred_sentence = create_tag_list_by(sentence, OUR_CRF_TAG)
            # Putting all sentences in one big list
            gold_sentences.append(gold_sentence)
            pred_sentences.append(pred_sentence)
            sentence = []
    if not end_of_file:
        exit("ERROR!! DID NOT REACH END OF FILE!")

    # Delete the following:
    print("gold sentences:")    # TODO - Delete all of these prints
    print(gold_sentences)
    print("pres sentences:")
    print(pred_sentences)

    F_measure, recall, precision = calculate_F_measure(gold_sentences, pred_sentences)
    _F_by_type, _recall_by_type, _precision__by_type = calculte_F_measure_by_tag(gold_sentences, pred_sentences)

    # Opening the tag count file, to add this information to our results file:
    tag_count_file = open(tag_counts_file_name, 'r', encoding="utf-8")
    tag_count_list = tag_count_file.readlines()

    # Write to file
    # current_time = str(datetime.now())
    current_time = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
    file_name_short = file_to_analyze.split("/")[1]
    # res_file_name = "Test_and_Evaluation/output/" + file_name_short + "_analysis_" + current_time + ".txt"
    res_file_name = "output/" + file_name_short + "_analysis_" + current_time + ".txt"
    res = open(res_file_name, 'w', encoding="utf-8")
    res.write(">>> TOTAL : <<< \n")
    res.write("    ------      \n")
    res.write("F_measure , Recall , Presicion \n")
    res.write(str(F_measure) + " , " + str(recall) + " , " + str(precision) + "\n\n")
    res.write(">>> By Type : <<< \n")
    res.write("    ---------      \n")
    res.write("F_measure , Recall , Precision \n")
    for type in TAG_TYPES.keys():
        res.write(type + ") " + str(_F_by_type[TAG_TYPES[type]]) + " , " + str(_recall_by_type[TAG_TYPES[type]])
                  + " , " + str(_precision__by_type[TAG_TYPES[type]]) + " out of " + tag_count_list[TAG_TYPES[type]]
                  + " " + type + " that exist in the corpus" "\n")
    res.close()
    return res_file_name

# # Unused
# def run_analysis_old(file_to_analyze):
#     print("...Started 'run_analysis' for file: " + file_to_analyze)
#
#     end_of_file = False
#     sentence = []
#     # gold_sentence, pred_sentence = [], []
#     sentence_counter = 0
#     _total_names = 0
#     _total_phrases = 0
#     data = open(file_to_analyze, 'r', encoding="utf-8")
#     # data = open(res_file, 'r')
#     while not end_of_file:
#         line = data.readline()
#         if not line:
#             end_of_file = True
#             break
#
#         line = line.strip("\n").strip("\t").strip(" ")
#         if len(line):
#             print("found regular line. starting with: " + line.split("\t")[0]) # TODO - Just a print
#             print("line-length: " + str(len(line)))
#             print("FULL LINE:" + line)
#             sentence.append(line)
#         # if we've reached the end of the sentence - en empty line.
#         else:
#             print("empty line")  # TODO - Just a print
#             sentence_counter += 1
#             gold_sentence = create_tag_list_by(sentence, GOLD_STANDARD_TAG)
#             pred_sentence = create_tag_list_by(sentence, OUR_CRF_TAG)
#             # send each sentence to:
#             total_f_measure_res = calculate_F_measure_sentence(gold_sentence, pred_sentence)
#             f_measure_res_by_name = calculte_F_measure_by_tag(gold_sentence, pred_sentence)
#
#             # _total_phrases += total_f_measure_res[0]
#             # _total_names += total_f_measure_res[1]
#
#             # TODO: ADD ALL THE REST THAT IS MISSING !!!!!!!
#
#     if not end_of_file:
#         exit("ERROR!! DID NOT REACH END OF FILE!")
#     # make_statistics(file_to_analyze, _total_phrases, _total_names)
#
#     # Write to file
#     # current_time = str(datetime.now())
#     current_time = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
#     file_name_short = file_to_analyze.split("/")[1]
#     res_file_name = "output/" + file_name_short + "_analysis_" + current_time + ".txt"
#     res = open(res_file_name, 'w', encoding="utf-8")
#     res.write(">>> TOTAL : <<< \n")
#     res.write("    ------      \n")
#     res.write("F_measure , Recall , Presicion \n")
#     res.write(str(_total_F_measure) + " , " + str(_total_recall) + " , " + str(_total_precision) + "\n\n")
#     res.write(">>> By Type : <<< \n")
#     res.write("    ---------      \n")
#     res.write("F_measure , Recall , Precision \n")
#     for type in TAG_TYPES.keys():
#         res.write(type + ") " + str(_F_by_type[TAG_TYPES[type]]) + " , " + str(_recall_by_type[TAG_TYPES[type]])
#             + " , " + str(_precision__by_type[TAG_TYPES[type]]) + "\n")
#     res.close()
#     return res_file_name


if __name__ == '__main__':
    # for each input file:
    files_to_test = []
    # For a test
    files_to_test.append("input/input_test_all_correct.txt")
    files_to_test.append("input/input_test_2_missing.txt")
    files_to_test.append("input/input_test_3_incorrect.txt")
    files_to_test.append("input/input_test_4_spurious.txt")
    files_to_test.append("input/input_test_5_misc.txt")
    files_to_test.append("input/input_test_6_misc.txt")
    #
    for file in files_to_test:
        print("Starting the program for file: " + file)
        run_analysis(file)
        # run_analysis_old(file)

    # print("Testing 'create_tag_list_by':")
    # print("-----------------------------")
    # word1 = [1, 2, 3, 'bla', 'blabla', 'GOLD_TEST1', 'PRED_TEST1']
    # word2 = [1, 2, 3, 'bla2', 'blabla2', 'GOLD_TEST2', 'PRED_TEST2']
    # word3 = [1, 2, 3, 'bla3', 'blabla3', 'blablabla3', 'GOLD_TEST3', 'PRED_TEST3']
    # word4 = [1, 2, 3, 'bla4', 'GOLD_TEST4', 'PRED_TEST4']
    # word5 = [1, 2, 3, 'bla5', 'blabla5', 'GOLD_TEST5', 'PRED_TEST5']
    # sentence_list_1 = [word1, word2, word3, word4, word5]
    # tag_list = create_tag_list_by(sentence_list_1, GOLD_STANDARD_TAG)
    # print("tag_list for gold: ")
    # print(tag_list)
    # tag_list = create_tag_list_by(sentence_list_1, OUR_CRF_TAG)
    # print("tag_list for pred: ")
    # print(tag_list)
    #
    # print("\n")
    #
    # print("Testing 'get_name_list_from' for 'ALL':")
    # print("---------------------------------------")
    # word0 = [1, 2, 3, 'bla', 'blabla', 'PERS', 'PERS']
    # word1 = [1, 2, 3, 'bla1', 'blabla1', 'PERS', 'O']
    # word2 = [1, 2, 3, 'bla2', 'blabla2', 'blablabla2', 'PERS_C', 'PERS_C']
    # word3 = [1, 2, 3, 'bla3', 'O', 'O']
    # word4 = [1, 2, 3, 'bla4', 'blabla4', 'DATE', 'DATE']
    # word5 = [1, 2, 3, 'bla5', 'blabla5', 'PERS', 'PERS']
    # word6 = [1, 2, 3, 'bla6', 'blabla6', 'PERS_C', 'PERS_C']
    # word7 = [1, 2, 3, 'bla7', 'blabla7', 'PERS', 'PERS_C']
    # word8 = [1, 2, 3, 'bla8', 'blabla8', 'DATE_C', 'DATE']
    # word9 = [1, 2, 3, 'bla9', 'blabla9', 'LOC', 'LOC']
    # word10 = [1, 2, 3, 'bla10', 'blabla10', 'LOC_C', 'LOC_C']
    # word11 = [1, 2, 3, 'bla11', 'LOC_C', 'O']
    # # Expecting for GOLD: [[[0], 'PERS'], [[1,2], 'PERS'], [[4], 'DATE'], [[5,6], 'PERS'], [[7], 'PERS'], [9,10,11], 'LOC']]
    # # Expecting for PRED: [[[0], 'PERS'], [[4], 'DATE'], [[5,6,7], 'PERS'], [[8], 'DATE'], [9,10], 'LOC']]
    # sentence_list = [word0, word1, word2, word3, word4, word5, word6, word7, word8, word9, word10, word11]
    # tag_list_gold = create_tag_list_by(sentence_list, GOLD_STANDARD_TAG)
    # print("tag_list for gold: ")
    # print(tag_list_gold)
    # gold_name_list_all = get_name_list_from(tag_list_gold, 'ALL')
    # print("name_list for gold: ")
    # print("FOUND: " + str(gold_name_list_all))
    # print("EXPECTED: " + str(
    #     [[[0], 'PERS'], [[1, 2], 'PERS'], [[4], 'DATE'], [[5, 6], 'PERS'], [[7], 'PERS'], [[9, 10, 11], 'LOC']]))
    # print()
    # tag_list_pred = create_tag_list_by(sentence_list, OUR_CRF_TAG)
    # print("tag_list for pred: ")
    # print(tag_list_pred)
    # pred_name_list_all = get_name_list_from(tag_list_pred, 'ALL')
    # print("name_list for pred: ")
    # print("FOUND: " + str(pred_name_list_all))
    # print("EXPECTED: " + str([[[0], 'PERS'], [[4], 'DATE'], [[5, 6, 7], 'PERS'], [[8], 'DATE'], [[9, 10], 'LOC']]))

    #
    # # _F_by_type, _recall_by_type, _precision__by_type = calculte_F_measure_by_tag(tag_list_gold, tag_list_pred)
    #
    # print("Testing 'calculate_recall' for 'ALL':")
    # print("-------------------------------------")
    # recall_all = calculate_recall([gold_name_list_all], [pred_name_list_all])
    # print("FOUND: " + str(recall_all))
    # print("EXPECTED: 2/6 = " + str(2 / 6))
    # print()
    # print("Testing 'calculate_precision' for 'ALL':")
    # print("----------------------------------------")
    # prec_all = calculate_precision([gold_name_list_all], [pred_name_list_all])
    # print("FOUND: " + str(prec_all))
    # print("EXPECTED: 2/5 = " + str(2 / 5))
    #
    # print()
    #
    # print("Testing 'calculate_recall' for 'PERS':")
    # print("--------------------------------------")
    # recall_pers = calculate_recall(gold_name_list_pers, pred_name_list_pers)
    # print("FOUND: " + str(recall_pers))
    # print("EXPECTED: 1/4 = " + str(1 / 4))
    # print()
    # print("Testing 'calculate_precision' for 'PERS':")
    # print("-----------------------------------------")
    # prec_pers = calculate_precision(gold_name_list_pers, pred_name_list_pers)
    # print("FOUND: " + str(prec_pers))
    # print("EXPECTED: 1/2 = " + str(1 / 2))
    #
    # print()

    # print("Testing 'calculate_recall' for 'DATE':")
    # print("--------------------------------------")
    # recall_date = calculate_recall(gold_name_list_date, pred_name_list_date)
    # print("FOUND: " + str(recall_date))
    # print("EXPECTED: 1 = " + str(1))
    # print()
    # print("Testing 'calculate_precision' for 'DATE':")
    # print("-----------------------------------------")
    # prec_date = calculate_precision(gold_name_list_date, pred_name_list_date)
    # print("FOUND: " + str(prec_date))
    # print("EXPECTED: 1/2 = " + str(1 / 2))

    # print()
    #
    # print("Testing 'calculate_F_measure':")
    # print("------------------------------")
    # f_measure_all = calculate_F_measure([tag_list_gold], [tag_list_pred])
    # print("FOUND: " + str(f_measure_all))
    # print("EXPECTED: 4/11 = " + str(4 / 11))

    # print()
    #
    # print("Testing 'calculte_F_measure_by_tag':")
    # print("------------------------------------")
    # f_measure_by_tag = calculte_F_measure_by_tag([tag_list_gold], [tag_list_pred])
    # print("FOUND: " + str(f_measure_by_tag))
    # print(
    #     "EXPECTED: 'PERS': 1/3 = " + str(1 / 3) + ", 'ORG': 0 = 0" + ", 'LOC': 0 = 0" + ", 'DATE': 2/3 (= " + str(2 / 3)
    #     + "), 'PERCENT': 0 = 0" + ", 'MISC': 0 = 0")