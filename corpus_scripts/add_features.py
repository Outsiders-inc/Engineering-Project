import copy
import re

CORP_NAME = "organized_corp"
NEW_NAME_SUF = "_new_feature.txt"
FILE_SUF = ".txt"
CURRENT_CORP = CORP_NAME + FILE_SUF
NEW_LINE = "\n"
NEW_SPOT = 1
SEP = "\t\t"

# Threshold for appearances in wiki-dictionary:
THRESHOLD = 3

PERSON_FUNCTION_WORDS = "dictionaries/Preson_Function_Words.txt"
CONSTRUCT_FUNCTION_WORDS = "dictionaries/Construction_Function_Words.txt"
COMPANY_FUNCTION_WORDS = "dictionaries/‏‏Company_Function_Words.txt"
DATE_FUNCTION_WORDS = "dictionaries/Date_Function_Words.txt"

PERSON_THRESHOLD = 3
CONSTRUCT_THRESHOLD = 1
COMPANY_THRESHOLD = 1
DATE_THRESHOLD = 0

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

# In case we want to edit a feature we can remove it first using feature coulomb number
def remove_feature(corpus_file_name, new_name, feature_number):
    with open(corpus_file_name, "r", encoding="utf-8") as corp:
        lines = corp.readlines()
    new_corp = []
    for i, line in enumerate(lines):
        new_line = NEW_LINE
        if line != NEW_LINE:
            words = line.split(SEP)
            # words.remove()
            # print(words)
            del words[feature_number]
            # print(words)
            new_line = SEP.join(words)
        new_corp.append(new_line)
    with open(new_name + FILE_SUF, "w", encoding="utf-8") as corp:
        corp.writelines(new_corp)


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


# Dictionary feature - number of occurrences in Wikipedia's list given as parameter 'wiki_file_name'
# The function uses a threshold, where no' of appearances that is smaller then it - is regarded as 0.
def appearances_wikipedia_feature_by_base_word(corpus_file_name, wiki_file_name, func_words_file_name, threshold):
    print("appearances_wikipedia_person_feature...") # TODO - DELETE
    words_variations = []
    # Creating lists of all possible base words for each word in the corpus:
    with open(corpus_file_name, "r", encoding="utf-8") as corp:
        for line in corp:
            if line != NEW_LINE:
                words = line.split(SEP)
                variations = create_words_from_delimiter(words[1])
                words_variations.append(variations)
                # words_variations.append([words[0]] + variations)
            else:
                words_variations.append([line])
        # lines = corp.readlines()
    # words = list(map(lambda s: s.split(SEP)[0], lines))

    # Creating lists of all words in the wikipedia tree:
    with open(wiki_file_name, "r", encoding="utf-8") as wiki:
        wiki_lines = wiki.readlines()
    wiki_lines_stripped = list(map(lambda s: s.strip("\n").strip("\t"), wiki_lines))
    wiki_words_list = []
    for line in wiki_lines_stripped:
        wiki_words_list += line.split(" ")

    # Creating lists of function words:
    with open(func_words_file_name, "r", encoding="utf-8") as functions_words_file:
        functions_words = functions_words_file.readlines()
        functions_words = list(map(lambda s: s.strip("\n").strip("\t"), functions_words))

    # Searching if either of the base-words appear in the wikipedia tree (and is not a function word):
    occurrences = ["0"] * len(words_variations)
    for index, word_arr in enumerate(words_variations):
        counter = 0
        for wiki_word in wiki_words_list:
            if wiki_word in word_arr and wiki_word not in functions_words:
                counter += 1
        occurrences[index] = str(counter)
        # if index % 200 == 0:                             # TODO - DELETE
        #     print(str("{0:.2f}".format(index / len(words_variations)* 100)) + "%")  # TODO - DELETE
    occurrences = [x if (int(x) > threshold) else "0" for x in occurrences]

    # Checking which words got a positive counter:
    words_set = []
    for i, occ in enumerate(occurrences):
        if occ != "0":
            if words_variations[i] not in words_set:
                words_set.append(words_variations[i])
                print(str(words_variations[i]) + " " + str(occ))

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
# Building a Node list out of the Wiki dictionary
class SetList:
    def __init__(self, word="root"):
        self.word = word
        self.children = []

    def __repr__(self):
        return self.word

    def search(self, word):
        for child in self.children:
            if word == child.word:
                return child
        return False

    def search_arr(self, word_array):
        for word in word_array:
            child = self.search(word)
            if child:
                return child
        return False

    def add_child(self, name):
        child = self.search(name)
        if not child:
            node = SetList(name)
            self.children.append(node)
            return node
        return child

    def is_leaf(self):
        return len(self.children) == 0

    def print_tree(self, tab_number=0):
        print("\t" * tab_number + self.__repr__())
        for child in self.children:
            child.print_tree(tab_number + 1)


def create_wiki_tree(file_name):
    with open(file_name, "r", encoding="utf8") as doc:
        lines = doc.readlines()
    tree = SetList()
    for line in lines:
        words = line.strip("\n").strip(SEP).split(" ")
        new_node = tree.add_child(words[0])
        words = words[1:]
        for word in words:
            new_node = new_node.add_child(word)
    return tree


def is_in_wiki_tree_feat(corpus_file_name, wiki_dic_name):
    tree = create_wiki_tree(wiki_dic_name)
    feat = []
    current_tree = tree
    tree_length = 0
    found_trees = 0
    with open(corpus_file_name, "r", encoding="utf8") as corp:
        for line in corp:
            if line == NEW_LINE:
                current_tree = tree
                feat.append("0")
                for i in range(tree_length):
                    feat.append("0")
                tree_length = 0
                continue
            words = line.split(SEP)
            current_word = words[1].strip()
            variations = create_words_from_delimiter(current_word)
            variations.append(words[0].strip())
            is_tree = current_tree.search_arr(variations)
            if not is_tree:
                for i in range(tree_length):
                    feat.append("0")
                tree_length = 0
                current_tree = tree
                # Maybe the word is a new root
                is_tree = current_tree.search_arr(variations)
            if is_tree:
                if is_tree.is_leaf():
                    found_trees += 1
                    current_tree = tree
                    feat.append("1")
                    for i in range(tree_length):
                        feat.append("1")
                    tree_length = 0
                else:
                    current_tree = is_tree
                    tree_length += 1
            else:
                feat.append("0")
    print("Found: " + str(found_trees) + " trees total")
    return feat


# TODO - TEMPORARILY HERE:
# ------------------------
# For wiki features we want to search all forms in base form of words
def create_words_from_delimiter(word, delimiter="&"):
    bad_inputs = ["\n", " ", "", ".", ",", "-", ":"]
    if len(word) == 0 or word in bad_inputs:
        return [word]
    # Finding all the occurrences of the delimiter in the word
    delim_indices = list(map(int, [m.start() for m in re.finditer(delimiter, word)]))
    if len(delim_indices) == 0:
        return [word]
    l1 = word.split(delimiter)
    l2 = [x[0:-1] for x in l1]
    l2[-1] = copy.deepcopy(l1[-1])
    if delim_indices[-1] == len(word) - 1:
        l1.pop()
        l2.pop()
    all_lists = []
    for i in range(len(l1)):
        all_lists.append([l1[i], l2[i]])

    r = [[]]
    for x in all_lists:
        t = []
        for y in x:
            for i in r:
                t.append(i + [y])
        r = t
    res = []
    for tup in r:
        res.append("".join(tup))
    return res[0:len(r)//2]


if __name__ == '__main__':

    # # Adding a wiki-person feature
    # appearances_wikipedia_person_feature("organized_corp_test.txt", "wikiTreePerson_filtered.txt")

    # # Adding a wiki-location Unigram feature
    # is_wikipedia_location_unigram_feature("organized_corp_test.txt", "wikiTreeConstructions_filtered.txt")

    # # Adding a wiki-location Bigram feature
    # is_wikipedia_location_bigram_feature("‏‏organized_corp_test_small.txt", "‏‏wikiTreeConstructions_test_small.txt") # TODO - UNFINISHED FUNCTION!!!!


    # Debug - Running it to see which words are distracting:
    is_begin_feat("organized_corp_ORIGINAL_fixed.txt")
    is_end_feat("organized_corp_ORIGINAL_fixed.txt")
    appearances_wikipedia_feature_by_base_word("organized_corp_ORIGINAL_fixed.txt", "../wikipedia_tree_extractor/wikiTreePerson.txt", PERSON_FUNCTION_WORDS, PERSON_THRESHOLD)
    appearances_wikipedia_feature_by_base_word("organized_corp_ORIGINAL_fixed.txt", "../wikipedia_tree_extractor/wikiTreeConstructions.txt", CONSTRUCT_FUNCTION_WORDS, CONSTRUCT_THRESHOLD)
    appearances_wikipedia_feature_by_base_word("organized_corp_ORIGINAL_fixed.txt", "../wikipedia_tree_extractor/wikiTreeCompany.txt", COMPANY_FUNCTION_WORDS, COMPANY_THRESHOLD)
    appearances_wikipedia_feature_by_base_word("organized_corp_ORIGINAL_fixed.txt", "../wikipedia_tree_extractor/Date_Dictionary.txt", DATE_FUNCTION_WORDS, DATE_THRESHOLD)

