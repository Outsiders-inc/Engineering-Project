from Template_scripts import prepare_template
import subprocess
from Runner import Spliter
import time
import threading
import os.path
from Runner import Statistics
PATH = r"CRF++-0.58"
LABEL_COLUMN = 17
WINDOW_SIZE = 2
PARTITION = ["a", "b", "c"]


# Creates a simple template and invokes a simple crf run
def simple_test():
    template_maker = prepare_template.Template("template.txt")
    template_maker.add_unigram_features(0, 0)
    template_maker.close()
    Spliter.create_split("organized_corp.txt", 80, 2)
    subprocess.call([PATH + "\crf_learn.exe", "template.txt", "train_organized_corp.txt", PATH + "\model_file",
                            "> train_output"], shell=True)
    subprocess.call([PATH + "\crf_test.exe","-m", PATH + "\model_file", "test_organized_corp.txt", "> output"]
                    , shell=True)


# Will run CRF on all unigram options in a window of 2.
def uni_test_all():
    for i in range((WINDOW_SIZE * 2) + 1):
        current = i - WINDOW_SIZE
        for j in range(LABEL_COLUMN):
            feature_string = "_" + str(current) + str(j)
            template_maker = prepare_template.Template(r"templates\template" + feature_string)
            template_maker.add_unigram_features(current, j)
            template_maker.close()
            for part in PARTITION:
                single_uni_test(current, j, part)


# Runs a test on a single unigram.
# Does not create a template.
# Param:
# Word - number of word to refer relative to current word.
# Feature- the feature number to refer.
# Part - since every test is run at least once it is requires to mention which part of testing is this. Can be a letter
# from a-z
# If a result file of this specific unigram and part exists will return without computation.
def single_uni_test(word, feature, part):
    feature_string = "_" + str(word) + str(feature) + part
    result_filename = r"results\output" + feature_string
    if os.path.isfile(result_filename):
        return
    train_filename = r"train_results\train_output" + feature_string
    template_filename = r"templates\template" + "_" + str(word) + str(feature)
    single_run(train_filename, template_filename, result_filename)


# One call to CRF++. Train then test.
# Receives the following file names: train output, template, result.

def single_run(train_output_file, template_file, result_file):
    s = time.clock()
    open(train_output_file, "w").close()
    open(result_file, "w").close()
    Spliter.create_split("organized_corp.txt", 80, 2)
    crf_args = [PATH + "\crf_learn.exe " + template_file + " train_organized_corp.txt " + PATH + "\model_file" +\
                ">" + train_output_file]
    c_thread = threading.Thread(target=subprocess.call, args=crf_args, kwargs={'shell': True})
    c_thread.start()
    while c_thread.isAlive():
        time.sleep(1)
    crf_args = [PATH + "\crf_test.exe " + "-m " + PATH + "\model_file " + "test_organized_corp.txt " + ">" + result_file]
    c_thread = threading.Thread(target=subprocess.call, args=crf_args, kwargs={'shell': True})
    c_thread.start()
    while c_thread.isAlive():
        time.sleep(1)
    times = open("time.txt", 'a')
    times.write("Time for template: " + template_file + " is " + str(time.clock() - s) + "\n")
    times.close()
    return


# Analyze all uni-gram results and insert into one file.
def uni_sum():
        res = open("uni_results.txt", 'w')
        for i in range((WINDOW_SIZE * 2) + 1):
            current = i - WINDOW_SIZE
            for j in range(LABEL_COLUMN):
                feature = str(current) + "_" + str(j)
                current_f = 0.0
                for part in PARTITION:
                    result_filename = r"results\output" + "_" + str(current) + str(j) + part
                    result_filename = Statistics.run_analysis(result_filename)
                    current_f += f_from_file(result_filename)
                current_f /= len(PARTITION)
                res.write(feature + ": " + str(current_f) + "\n")
        res.close()


# Reads result file and returns the F-measure as float
def f_from_file(result_filename):
    res_file = open(result_filename, "r", encoding="utf-8")
    # f-measure is in forth row
    for z in range(3):
        res_file.readline()
    f = float(res_file.readline().strip("\n"))
    res_file.close()
    return f


# Gets a template and runs a full test on it.
# Runs # of PARTITION length times and outputs a score.
# Time is registered through 'single_run'
def manual_run(template_file):
    res_score = 0.0
    # A unique name attempt for each manual run
    temp  = template_file.split(".")[0]
    unique_str = temp[-8:len(temp)]
    for part in PARTITION:
        result_filename = r"results\manual_output" + "_" + unique_str + "_" + part
        train_filename = r"train_results\manual_train_output" + "_" + unique_str + "_" + part
        single_run(train_filename, template_file, result_filename)
        result_filename = Statistics.run_analysis(result_filename)
        res_score += f_from_file(result_filename)
    res_score /= len(PARTITION)
    print(res_score)


# Greedy attempt to get the best results.
# Uses up to N features
# Takes features from best to worse and checks effect.
# Prints the best result found.
def greedy_unigram(n):
    uni_res = open("uni_results.txt", 'r')
    used_features = []
    per_feat_res = []
    for line in uni_res:
        feature, score = line.split(": ")
        temp = (score, feature)
        per_feat_res.append(temp)
    # Sort by score
    per_feat_res.sort(key=lambda tup: tup[0], reverse=True)
    # Throw scores
    features = []
    for tupe in per_feat_res:
        features.append(tupe[1])
    used_features.append(features[0])
    feature_index = 0
    prev_result = float(per_feat_res[0][0])
    while len(used_features) < n:
        feature_index += 1
        if feature_index >= len(features):
            break
        used_features.append(features[feature_index])
        template_filename = r"templates\template_" + str(feature_index)
        template_maker = prepare_template.Template(template_filename)
        for feat in used_features:
            word, col = feat.split("_")
            template_maker.add_unigram_features(int(word), int(col))
        template_maker.close()
        current_result = 0.0
        for part in PARTITION:
            result_filename = r"results\uni_output" + "_" + str(feature_index) + part
            train_filename = r"train_results\uni_train_output" + "_" + str(feature_index) + part
            single_run(train_filename, template_filename, result_filename)
            result_filename = Statistics.run_analysis(result_filename)
            current_result += f_from_file(result_filename)
        current_result /= len(PARTITION)
        if current_result <= prev_result:
            used_features.pop(-1)
        else:
            prev_result = current_result
    best_found_file = open("best_uni_found.txt", "w")
    for feat in used_features:
        best_found_file.write(feat + "\n")
    print(prev_result)

# uni_sum()
# greedy_unigram(11)
# Statistics.run_analysis("input/input_test_all_correct.txt")
# Statistics.run_analysis("input/input_test_2_missing.txt")
manual_run(r"templates\best_with_some_bigram_4.txt")