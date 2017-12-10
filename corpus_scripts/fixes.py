
def fix_percent():
    temp_lines = []
    with open("organized_corp.txt", 'r', encoding="utf-8") as corp:
        for line in corp:
            line = line.strip("\t").strip(" ")
            if "%" in line:
                words = line.split("\t")
                words[0] = words[0].replace(" ", "")
                line = "\t".join(words)
            temp_lines.append(line)
    with open("organized_corp.txt", 'w', encoding="utf-8") as corp:
        for line in temp_lines:
            corp.write(line)


def check_column_number():
    with open("organized_corp.txt", 'r', encoding="utf-8") as corp:
        corp.readline()
        for line in corp:
            words = line.strip("\n").split("\t")
            words = list(filter(lambda a: a != '', words))
            for word in words:
                if " " in word:
                    print(word)
            if len(words) > 18:
                print(words)
                print(len(words))


def fix_labels():
    temp_lines = []
    prev_label = ""
    with open("organized_corp.txt", 'r', encoding="utf-8") as corp:
        corp.readline()
        for line in corp:
            temp_line = line.strip("\t")
            words = temp_line.split("\t")
            label = words[len(words) - 2]
            if "_" in label:
                new_label = ""
                if label == prev_label:
                    new_label = prev_label.split("_", 1)[1] + "_C"
                else:
                    new_label = label.split("_", 1)[1]
                words[len(words) - 2] = new_label
            else:
                print(label)
            temp_line = "\t".join(words)
            prev_label = label
            temp_lines.append(temp_line)
    with open("organized_corp.txt", 'w', encoding="utf-8") as corp:
        for line in temp_lines:
            corp.write(line)
    # with open("organized_corp.txt", 'w', encoding="utf-8") as corp:
    #     for line in temp_lines:
    #         corp.write(line)
fix_percent()
fix_labels()

