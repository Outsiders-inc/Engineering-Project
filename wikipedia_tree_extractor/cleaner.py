def clean_blank_lines(file_name):
    with open(file_name, "r", encoding="utf8") as dict:
        new_dict = dict.readlines()
    new_dict_file = open(file_name + "_clean", "w", encoding="utf8")
    for line in new_dict:
        if line.strip("\t") != "\n":
            new_dict_file.write(line.strip("\t"))
    new_dict_file.close()

clean_blank_lines("wikiTreePerson.txt")