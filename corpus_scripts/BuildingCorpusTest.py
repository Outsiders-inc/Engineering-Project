import sys
import random
import copy

TRAINING_SET_PERCENT = 0.75
OPENING_ARTICLE_TAG = "DOCSTART"


def initialize():
        # open corpus & divide to articales
        numberOfWords = 0
        with open(sys.argv[1], encoding="utf8") as corpus:
            corp = corpus.readlines()
        # Divide to articles
        articles = []
        articCounter = -1
        for line in corp:
            if OPENING_ARTICLE_TAG in line:
                articCounter += 1
                articles.append([])
            articles[articCounter].append(line)
        #Generate 3 data sets, 75% for training and the rest for testing.
        #one 25% file with tags for comparing tag & one without for each test file.
        for i in range(3):
            res = generate_rand_article(articles, corp.__len__())
            trainingSet = res[0]
            testSet = res[1]
            trainingSet_File = open("trainingSet" + str(i) + ".txt", 'w', encoding= "utf8")
            for line in trainingSet:
                trainingSet_File.write("".join(map(str, line)))
            trainingSet_File.close()
            compareSet_File = open("compareSet" + str(i) + ".txt", 'w', encoding="utf8")
            for line in testSet:
                line[0] = "... O"
                compareSet_File.write("".join(map(str, line)))
            compareSet_File.close()
            testSet_File = open("testSet" + str(i) + ".txt", 'w', encoding="utf8")
            for line in testSet:
                if OPENING_ARTICLE_TAG in line:
                    line[0] = "..."
                for word in line:
                    word = word.strip(" ").split(" ")
                    testSet_File.write(word[0] + " ")


def generate_rand_article(articles, total_len):
    local_articles = copy.deepcopy(articles)
    articNum = local_articles.__len__()
    training_list = list()
    result_len = 0
    for i in range(articNum):
        r = random.randint(0, articNum - 1)
        result_len += local_articles[r].__len__()
        if result_len > TRAINING_SET_PERCENT * total_len:
            print("result_len is: " + str(result_len))
            print("TRAINING_SET_PERCENT * total_len is: " + str(TRAINING_SET_PERCENT * total_len))
            print("len without adding the last article: " + str(result_len - local_articles[r].__len__()))
            break
        training_list.append(local_articles[r])
        local_articles.remove(local_articles[r])
        articNum -= 1
    return training_list, local_articles


if __name__ == '__main__':
    initialize()

