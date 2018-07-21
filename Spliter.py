import random
import copy
DELTA = 2


# Takes a data file organized as CRF++ requires and splits it into
# train and data files.
# Args:
# data_filename - the name of the file that should be sliced.
# percent - the percentage of train data out of total data (range 1-100).
# delta - range allowed to be different from given percentage. (range 0-100 , a too small/big delta is on user
# responsibility).
# unique_str -  to add to the file name, defaults to none.
# Creates train_data + index + _filename and test + index + _data_filename
# Returns a list of the new files created: test, train.
def create_split(data_filename, percent, delta, unique_str=""):
    percent = float(percent) / 100
    delta = float(delta) / 100
    # A 0/1 flag to indicate where the data goes now.
    flag_train_test = which_now(percent)
    train_file_name = "train_" + unique_str+ data_filename
    test_file_name = "test_" + unique_str + data_filename
    train = open(train_file_name, 'w+', encoding="utf-8")
    test = open(test_file_name , 'w+',  encoding="utf-8")
    files = [train, test]
    lengths = [0, 0]
    with open(data_filename, 'r', encoding="utf-8") as data:
        for line in data:
            files[flag_train_test].write(line)
            lengths[flag_train_test] += 1
            if not line.strip("\n").strip(" "):
                flag_train_test = which_now(percent)
    for i in range(2):
        files[i].seek(0)
    # Variables for sentences transfer, assuming only one file to another transfer and no back and forth
    number_of_lines_transfer = 0
    file_transfer = 0
    # Computing how many lines should be transferred
    number_of_lines_transfer = 0
    while True:
        flag = is_unbalanced(lengths, percent, delta) # Flag that indicate if data is sliced correct
        # and if not which is bigger.
        if not flag:
            break
        else:  # Transfer from one file to another, flag indicates which is the bigger file.
            flag -= 1
            file_transfer = flag
            line = files[flag].readline()
            number_of_lines_transfer += 1
            while line.strip("\n").strip(" ") != "":
                number_of_lines_transfer += 1
                line = files[flag].readline()
            lengths[flag] -= number_of_lines_transfer
            lengths[int(not flag)] += number_of_lines_transfer
    # Transfer lines if needed
    print("Lengthes of files are: " + str(lengths[0]) + " test- " + str(lengths[1]))  # todo
    print("Number of line to trans: " + str(number_of_lines_transfer))  # todo
    if number_of_lines_transfer != 0:
        to_transfer_file = int(not file_transfer)
        files[to_transfer_file].seek(0, 2)  # seek end of file
        files[file_transfer].seek(0)
        for i in range(number_of_lines_transfer):
            line = files[file_transfer].readline()
            files[to_transfer_file].write(line)
        files[file_transfer].seek(0)
        for i in range(number_of_lines_transfer):
            files[file_transfer].write("\n")
    for i in range(2):
        files[i].close()
    return [train_file_name, test_file_name]


# Appends sec file to first file
def append_files(first_file, sec_file):
    f = open(first_file, 'a', encoding="utf-8")
    with open(sec_file, 'r', encoding="utf-8") as s:
        f.write(s.read())
    f.close()


# Creates 5 files for cross validation. Uses create split so names formats of names listed there.
# Receives the corpus file name and unique_str to add to file names
# Returns a list with 2 lists: [[train files names], [test files names]]
def create_cross_valid(data_filename, unique_str):
    train_files = []
    test_files = []
    file_to_split = data_filename
    for i in range(0, 4):
        split = create_split(file_to_split, 100 * (4 - i)/(5 - i), DELTA, str(i + 1) + "_" + unique_str)
        file_to_split = split[0]
        train_files.append(split[0])
        test_files.append(split[1])
    new_train_file = "train_" + "5_" + unique_str + data_filename
    train_files.append(new_train_file)
    open(new_train_file, "w", encoding="utf-8").close()
    new_test_file = "test" + "5_" + unique_str + data_filename
    test_files.append(new_test_file)
    open(new_test_file, "w", encoding="utf-8").close()
    append_files(new_test_file, file_to_split)
    for i in range(2, 6):
        for j in range(1, i-1):
            append_files(train_files[i - 1], test_files[j - 1])
    # first_split = create_split(data_filename, 80, DELTA, "1_" + unique_str)
    # train_files.append(first_split[0])
    # test_files.append(first_split[1])
    # sec_split = create_split(train_files[0], 75, DELTA, "2_" + unique_str)
    # test_files.append(sec_split[1])
    # # append first test set to sec train
    # append_files(sec_split[0], test_files[0])
    # train_files.append(sec_split[0])
    # third_split = create_split(train_files[1], 50, DELTA, "3_" + unique_str)
    # test_files.append(third_split[0])
    # test_files.append(third_split[1])
    # # append three others to both results of the third split
    # new_third = "train_" + "3_" + unique_str + data_filename
    # new_forth = "train_" + "4_" + unique_str + data_filename
    # open(new_third, "w", encoding="utf-8").close()
    # open(new_forth, "w", encoding="utf-8").close()
    # train_files.append(new_third)
    # train_files.append(new_forth)
    # for i, test_file in enumerate(test_files):
    #     if i != 3:
    #         append_files(new_third, test_file)
    #     if i != 4:
    #         append_files(new_forth, test_file)
    return [train_files, test_files]


def which_now(percent):
    if random.random() < percent:
        return 0
    else:
        return 1


# Checks if the train/test data is sliced correctly.
# Returns False is so, and 1 to indicate train file is too big and 2 for too small.
def is_unbalanced(lengths, percent, delta):
    train_percentage = float(lengths[0]) / (lengths[0] + lengths[1])
    print("Train percantge: " + str(train_percentage))
    print("Length 1: " + str(lengths[0]) + " length 2: " + str(lengths[1]))
    if train_percentage > (percent + delta) :
        return 1
    if train_percentage < (percent - delta):
        return 2
    return False


# ---- New version, all togther for cross validation.
# Returns a number between 0-4 to indicate which test file will get next sentence
def which_slice_now(tot_length, test_lengths):
    big_enough_files = []
    zeroes_count = 0
    for i, length in enumerate(test_lengths):
        zeroes_count += int(length == 0)
        if length/tot_length > 0.2:
            big_enough_files.append(i)
    next_slice = random.randint(0, 4)
    while next_slice in big_enough_files:
        next_slice = random.randint(0, 4)
    if zeroes_count == 1:
        return test_lengths.index(0)
    return next_slice


def cross_validate(data_filename, unique_str):
    with open(data_filename, "r", encoding="utf-8") as corp:
        lines = corp.readlines()
    test_content = [[] for i in range(5)]
    tot_len = len(lines)
    test_lengths = [0 for j in range(5)]
    current_slice = which_slice_now(tot_len, test_lengths)
    for line in lines:
        test_content[current_slice].append(line)
        if line == "\n":
            tot_len -= 1
            current_slice = which_slice_now(tot_len, test_lengths)
        else:
            test_lengths[current_slice] += 1
    test_files = []
    train_files = []
    for i in range(5):
        test_name =  "test_" + unique_str + str(i + 1) + "_" + data_filename
        train_name = "train_" + unique_str + str(i + 1) + "_" + data_filename
        test_file = open(test_name, "w", encoding="utf-8")
        test_file.writelines(test_content[i])
        test_file.close()
        train_file = open(train_name, "w", encoding="utf-8")
        for j in range(5):
            if j != i:
                train_file.writelines(test_content[j])
        train_file.close()
        test_files.append(test_name)
        train_files.append(train_name)
    return [train_files, test_files]
t = cross_validate("organized_corp.txt", "fds")

# create_split(, 80, 2)
# t = create_cross_valid("dugma_simple.txt", "gTes_")
# t = create_split("dugma_long.txt", 80, 2,"gTes_")
# print(t)
for file in t[1]:
    print("number of lines in file: " + file + " are: ")
    print(len(open(file, "r", encoding="utf-8").readlines()))
    print("\n")