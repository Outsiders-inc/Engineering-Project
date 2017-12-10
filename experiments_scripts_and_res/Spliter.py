import random


# Takes a data file organized as CRF++ requires and splits it into
# train and data files.
# Args:
# data_filename - the name of the file that should be sliced.
# percent - the percentage of train data out of total data (range 1-100).
# delta - range allowed to be different from given percentage. (range 0-100 , a too small/big delta is on user
# responsibility).
# Creates data_filename_train and data_filename_test
def create_split(data_filename, percent, delta):
    percent = float(percent) / 100
    delta = float(delta) / 100
    # A 0/1 flag to indicate where the data goes now.
    flag_train_test = which_now(percent)
    train = open("train_" + data_filename, 'w+', encoding="utf-8")
    test = open("test_" + data_filename, 'w+',  encoding="utf-8")
    files = [train, test]
    lengths = [0, 0]
    with open(data_filename, 'r', encoding="utf-8") as data:
        # Discard comment line (first line)
        data.readline()
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
    while True:
        flag = is_unbalanced(lengths, percent, delta) # Flag that indicate if data is sliced correct
        # and if not which is bigger.
        if not flag:
            break
        else:  # Transfer from one file to another, flag indicates which is the bigger file.
            flag -= 1
            file_transfer = flag
            line = files[flag].readline()
            number_of_lines_transfer = 1
            while not line.strip("\n").strip(" "):
                number_of_lines_transfer += 1
                line = files[flag].readline()
            lengths[flag] -= number_of_lines_transfer
            lengths[int(not flag)] += number_of_lines_transfer
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


def which_now(percent):
    if random.random() < percent:
        return 0
    else:
        return 1


# Checks if the train/test data is sliced correctly.
# Returns False is so, and 1 to indicate train file is too big and 2 for too small.
def is_unbalanced(lengths, percent, delta):
    train_percentage = float(lengths[0]) / (lengths[0] + lengths[1])
    if train_percentage > (percent + delta) :
        return 1
    if train_percentage < (percent - delta):
        return 2
    return False

# create_split("organized_corp.txt", 80, 2)