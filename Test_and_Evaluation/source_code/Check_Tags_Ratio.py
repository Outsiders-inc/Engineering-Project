
TAG_TYPES = {'PERS' : 0, 'ORG' : 1, 'LOC' : 2, 'DATE' : 3, 'PERCENT' : 4, 'MONEY' : 5, 'TIME' : 6,
             'MISC_AFF' : 7, 'MISC_EVENT' : 8, 'MISC_ENT' : 9, 'MISC_MODEL' : 10}

originalCorpusName = "../../corpus_scripts/organized_corp_ORIGINAL_fixed.txt"
tag_ratio_file_name = "../output/tags_ratio_file.txt"
tag_counts_file_name = "../output/tags_counts_file.txt"
GOLD_STANDARD_TAG = -2

# Takes the GOLD_STANDARD_TAG of each word and return a list comprised only of the tags.
def create_tag_list(corpus_file_name):
    tag_list = []
    i = 1   # DELETE
    with open(corpus_file_name, "r", encoding="utf-8") as corp:
        lines = corp.readlines()

    for line in lines:
        i += 1  # DELETE
        # word = line.strip("\n").strip("")
        word = line.split("\t")
        if len(word) < 17:
            continue
        tag_list.append(word[GOLD_STANDARD_TAG])
    return tag_list


# Receives a list of tags and return a list of tags where each tags represent an entire expression (or entity),
#   and not a single word.
# For example: input of ['O', 'PERS', 'PERS_C', 'DATE'] will become an output of ['O', 'PERS', 'DATE'].
def convert_tag_list_to_expressions_list(tag_list):
    print(len(tag_list))
    expressions_list = []
    current_tag = 'O'
    for tag in tag_list:
        if tag == 'O':
            continue
        if tag == current_tag + '_C':
            continue
        current_tag = tag
        expressions_list.append(tag)
    return expressions_list


# returns:
#   tag_to_tags_ratio - The ratio of each tag type in relation to number of NEs in the input list.
#   tag_to_words_ratio - The ratio of each tag type in relation to total number of WORDS in the input list.
def check_tags_ratio(tag_list, expressions_list):
    tags_counter_list = [0] * len(TAG_TYPES)
    num_of_words = len(tag_list)
    num_of_NE = 0

    for expr in expressions_list:
        num_of_NE += 1
        if expr in TAG_TYPES:
            # print (expr) # DELETE
            tags_counter_list[TAG_TYPES[expr]] += 1

    tag_to_tags_ratio = [x / num_of_NE for x in tags_counter_list]
    # tag_to_words_ratio = [x / num_of_words for x in tags_counter_list]

    return [tag_to_tags_ratio, tags_counter_list]


# A variation of the original function - meant to be used in real time in order for the ratios
#   to go in the results files.
# returns:
#   tag_to_tags_ratio - The ratio of each tag type in relation to number of NEs in the input list.
#   tag_to_words_ratio - The ratio of each tag type in relation to total number of WORDS in the input list.
def check_tags_ratio_for_resut_file(corpus_file_name):
    tag_list = create_tag_list(corpus_file_name)
    expressions_list = convert_tag_list_to_expressions_list(tag_list)

    tags_counter_list = [0] * len(TAG_TYPES)
    num_of_words = len(tag_list)
    num_of_NE = 0

    for expr in expressions_list:
        num_of_NE += 1
        if expr in TAG_TYPES:
            # print (expr) # DELETE
            tags_counter_list[TAG_TYPES[expr]] += 1

    tag_to_tags_ratio = [x / num_of_NE for x in tags_counter_list]
    # tag_to_words_ratio = [x / num_of_words for x in tags_counter_list]

    tags_counter = []
    for i, tagType in enumerate(tag_type_list):
            tags_counter.append(str(tags_counter_list[i]))

    return tags_counter



#

#     new_corp = []
#     for i, line in enumerate(lines):
#         new_line = NEW_LINE
#         if line != NEW_LINE:
#             words = line.split(SEP)
#             words.insert(len(words) - NEW_SPOT, feature_values[i])
#             new_line = SEP.join(words)
#         new_corp.append(new_line)
#     with open(corpus_name + NEW_NAME_SUF, "w", encoding="utf-8") as corp:
#         corp.writelines(new_corp)


if __name__ == '__main__':
    tag_list_2 = create_tag_list(originalCorpusName)
    print (tag_list_2)
    expressions_list = convert_tag_list_to_expressions_list(tag_list_2)
    print (expressions_list)
    tag_to_tags_ratio, tags_counter = check_tags_ratio(tag_list_2, expressions_list)
    print (TAG_TYPES)
    print (tag_to_tags_ratio)
    print(tags_counter)
    print ("Total num of NEs: " + str(len(expressions_list)))

    res = open(tag_ratio_file_name, 'w', encoding="utf-8")
    res.write(">>> Total num of NEs: " + str(len(expressions_list)) + " <<< \n")
    res.write("    -----------------------------------------      \n")
    res.write("\n")
    res.write("     Tag-types    )   # Occurrences  /    Tag-NE Ratio  \n")
    res.write("    ------------------------------------------------------     \n")
    tag_type_list = list(TAG_TYPES)
    for i, tagType in enumerate(tag_type_list):
        res.write(tagType + "  ) " + str(tags_counter[i]) + " ,  " + str(tag_to_tags_ratio[i])
                  + "\n")
    # for type in TAG_TYPES.keys():
    #     res.write(type + "  ) " + str(tags_counter[TAG_TYPES[type]]) + " ,  " + str(tag_to_tags_ratio[TAG_TYPES[type]])
    #                + "\n")
    res.close()

    counts = open(tag_counts_file_name, 'w', encoding="utf-8")
    for i, tagType in enumerate(tag_type_list):
        if i == 0:
            counts.write(str(tags_counter[i]))
        else:
            counts.write("\n" + str(tags_counter[i]))
    # for type in TAG_TYPES.keys():
    #     if TAG_TYPES[type] == 0:
    #         counts.write(str(tags_counter[TAG_TYPES[type]]))
    #     else:
    #         counts.write("\n" + str(tags_counter[TAG_TYPES[type]]))
    counts.close()





