CORP_NAME = "organized_corp"
CURRENT_CORP = CORP_NAME + ".txt"
NEW_NAME_SUF = "_new_feature.txt"
NEW_LINE = "\n"
NEW_SPOT = 2
SEP = "\t\t"

PUNCT_OR_WORD = 2

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


# Dictionary feature - number of occurrences as a name in Wikipedia's person list
def appearances_wikipedia_person_feature(corpus_file_name, wiki_persons_file_name):
    with open(corpus_file_name, "r", encoding="utf-8") as corp:
        lines = corp.readlines()
    words = list(map(lambda s: s.split("\t")[0], lines))

    # for word in words: # TODO Delete
    #     print(word) # TODO Delete

    with open(wiki_persons_file_name, "r", encoding="utf-8") as wiki:
        wikiLines = wiki.readlines()
    wikiLinesStripped = list(map(lambda s: s.strip("\n").strip("\t"), wikiLines))
    wikiWordsList = []
    for line in wikiLinesStripped:
        wikiWordsList += line.split(" ")
    # for word in wikiWordsList: # TODO Delete
    #     print(word) # TODO Delete

    occurrences = ["0"] * len(lines)
    for index, word in enumerate(words):
        counter = 0
        for wiki_word in wikiWordsList:
            if word == wiki_word:
                counter += 1
        occurrences[index] = str(counter)
        # print(word + " - " + str(counter)) # TODO Delete

    add_feature(corpus_file_name, corpus_file_name, occurrences)


# Dictionary feature - is name in Wikipedia's person list (as unigram)
def is_wikipedia_location_unigram_feature(corpus_file_name, wiki_location_file_name):
    with open(corpus_file_name, "r", encoding="utf-8") as corp:
        lines = corp.readlines()
    words = list(map(lambda s: s.split("\t")[0], lines))

    with open(wiki_location_file_name, "r", encoding="utf-8") as wiki:
        wikiLines = wiki.readlines()
    wikiLinesStripped = list(map(lambda s: s.strip("\n").strip("\t"), wikiLines))
    wikiWordsList = []
    for line in wikiLinesStripped:
        wikiWordsList += line.split(" ")

    is_wiki_loc = ["0"] * len(lines)
    for index, word in enumerate(words):
        counter = 0
        for wiki_word in wikiWordsList:
            if word == wiki_word:
                is_wiki_loc[index] = "1"
                break

    add_feature(corpus_file_name, corpus_file_name, is_wiki_loc)


# Dictionary feature - is word and next word in Wikipedia's person list (as Bigram)
def is_wikipedia_location_bigram_feature(corpus_file_name, wiki_location_file_name):
    with open(corpus_file_name, "r", encoding="utf-8") as corp:
        lines = corp.readlines()
    # Creating a list of lists where each element is [word, PUNCT_OR_WORD]:
    for i,line in enumerate(lines):
        if line == "\n":
            print("--empty line ---")  # TODO - DELETE
            lines[i] = "EMPTY_LINE" + SEP + "_" + SEP + "P"
        else:
            # print (line)  # TODO - DELETE
            pass
    # for line in lines: # TODO - DELETE
    #     line = line.split(SEP)    # TODO - DELETE
    #     print("0 -> " + line[0] + " 1 -> " + line[1]+ " 2 -> " + line[2])     # TODO - DELETE
    words = list(map(lambda s: s.split(SEP)[0 : (PUNCT_OR_WORD + 1) : PUNCT_OR_WORD], lines))

    print("words:") # TODO - DELETE
    print (words)   # TODO - DELETE

    with open(wiki_location_file_name, "r", encoding="utf-8") as wiki:
        wikiLines = wiki.readlines()
    wikiLinesStripped = list(map(lambda s: s.strip("\n").strip("\t"), wikiLines))
    # Creating a list of lists, in which for each expression - we save tuples of all consecutive words:
    wikiWordsList = []
    for line in wikiLinesStripped:
        temp = line.split(" ")
        wikiWordsList += ([temp[i], temp[i + 1]] for i in range(len(temp) - 1))

    print("wikiWordsList:")  # TODO - DELETE
    print(wikiWordsList)  # TODO - DELETE

    is_wiki_loc = ["0"] * len(lines)
    for index, word in enumerate(words):
        counter = 0
        print(word)   # TODO - DELETE
        if word[1] == "P":
            continue
        word_tuple = word[0]
        i = 1
        second_word = ""
        while words[index + i][1] == "P":
            if words[index + i][0] == "EMPTY_LINE":
                i = -1
                break
            i += 1
        if i != -1:
            second_word = words[index + i][0]
            if second_word != "":
                word_tuple += " " + second_word
                print(word_tuple)  # TODO - DELETE

                for wiki_word in wikiWordsList:
                    if word_tuple == wiki_word:
                        is_wiki_loc[index] = "1"
                        print(word_tuple + " - 1")  # TODO - DELETE
                        break


if __name__ == '__main__':

    # # Adding a wiki-person feature
    # appearances_wikipedia_person_feature("organized_corp_test.txt", "wikiTreePerson_filtered.txt")

    # # Adding a wiki-location Unigram feature
    # is_wikipedia_location_unigram_feature("organized_corp_test.txt", "wikiTreeConstructions_filtered.txt")

    # Adding a wiki-location Bigram feature
    is_wikipedia_location_bigram_feature("‏‏organized_corp_test_small.txt", "‏‏wikiTreeConstructions_test_small.txt") # TODO - UNFINISHED FUNCTION!!!!