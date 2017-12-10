import xml.etree.ElementTree as et
WEIRD_GAP = " " * 8
IRRELEVANT = "-1"
input_file = open("organized_corp.txt", 'w', encoding="utf-8")
tree = et.parse('corp_untagged.xml')
root = tree.getroot()
text = root.find("Text")
new_corp = open("new_corp.txt", encoding='utf8').readlines()
att_list = ["OrgForm", "basic_form", "type", "sub", "eng", "pref", "pos", "gen", "num", "per",
            "cst", "suff_n", "suff_p", "suff_g", "bin", "voc", "ten", "label"]
prev_string = "."
field_string = "# "
for i, field in enumerate(att_list):
    field_string += field + "\t"
    if i > 1:
        field_string += "\t"
input_file.write(field_string)
prev_label = ""
i = -1
j = 0
broken_set = [i for i in range(30, 35)]
for toAdd in range(41, 48):
    broken_set.append(toAdd)
broken_set.append(80)
broken_set.append(93)
broken_set.append(94)
broken_set.append(95)
broken_set.append(96)
broken_set.append(97)
broken_set.append(98)
broken_set.append(99)
broken_set.append(100)
broken_set.append(101)
broken_set.append(102)
broken_set.append(103)
broken_set.append(104)
broken_set.append(105)
broken_set.append(106)
broken_set.append(107)
broken_set.append(108)
broken_set.append(109)
broken_set.append(110)
broken_set.append(111)
broken_set.append(112)
broken_set.append(114)
for token in text:
    # print(i)
    if "..." in token.text and ("." in prev_string or " " == prev_string or "\n" == prev_string):
        continue
    i += 1
    if token.attrib["type"] == "NL":
        input_file.write("\n")
        continue
    field_dic = {}
    for field in token.attrib:
        field_dic[field] = token.attrib[field]

    for child in token.getchildren():
        for field in child.attrib:
            field_dic[field] = child.attrib[field]
    if token.attrib["type"] == "P":
        field_dic["OrgForm"] = token.text
        field_dic["basic_form"] = token.text

    if " " in new_corp[i].strip("\n"):
        if len(new_corp[i].strip("\n").split(" ")) == 2:
            word, label = new_corp[i].strip("\n").split(" ")
        else:
            print("HERE: " + new_corp[i].strip("\n"))
    else:
        if new_corp[i].strip("\n") == "":
            i += 1
            continue
        # else:
        #     print(str(i) + " Here: " + new_corp[i].strip("\n"))
        #     print("And here: " + token.text)
        #     exit()
    # The 2 corpora are built a bit different, this is one of the differences
    if "%" in token.text:
        word += " %"
        if j not in broken_set:
            i += 1
    if token.text == "-" and not label == "HYPHEN":
        word = token.text
        i -= 1
    if word.strip(" ") != token.text.strip(" "):
        j += 1
        if "%" not in word:
            if j > 170:
                print("Failed sync in:\nCorp: " + word + "\nAnalyzer: " + token.text + "\nLine number: " + str(i)+ "\nj="+ str(j))
                exit()
    if label == "HYPHEN":
        label = prev_label
    field_dic["label"] = label
    prev_label = label
    token_string = ""
    for field in att_list:
        if field == "eng":
            if field in field_dic:
                if field_dic[field] != "":
                    field_dic[field] = "1"
        if field in field_dic:
            # If field has a value
            if not field_dic[field] == "":
                # Need less tabs for orgForm
                if field != "OrgForm":
                        token_string += "\t" + field_dic[field] + "\t"
                else:
                    token_string += field_dic[field] + "\t"
            else:
                token_string += "\t" + IRRELEVANT + "\t"
        else:
            if field != "OrgForm":
                token_string += "\t" + IRRELEVANT + "\t"
            else:
                token_string += "\t" + token.text + "\t"

    token_string += "\n"
    input_file.write(token_string)
    prev_string = token.text

# orgform(word) base_form(word) type(letter) sub(letter) eng(eng word) pref(word) pos(num) gen(num) num(num) per(num)
# cst(num) suff_n(num) suff_p(num) suff_g(num)  bin(num) voc(num) ten(num) label(eng word)
# orgin_corp = open("corp.txt", encoding='utf8').readlines()
# new_corp = open("new_corp.txt", 'w', encoding='utf8')
# for line in orgin_corp:
#     if "DOCSTART" in line:
#         continue
#     line = line.strip("\n").split(" ")
#     if '-' in line[0]:
#         words = line[0].split("-")
#         for i in range(len(words) - 1):
#             if words[i] != "":
#                 new_corp.write(words[i] + " " + line[1] + "\n")
#                 new_corp.write("-" + " " + "HYPHEN" + "\n")
#         if words[-1] != "":
#             new_corp.write(words[-1] + " " + line[1] + "\n")
#     else:
#         if len(line) == 1 and line[0] == "":
#             new_corp.write("\n")
#             continue
#
#         orig_line = ""
#         for el in line:
#             orig_line += el
#             orig_line += " "
#         orig_line = orig_line[:-1]
#         print(orig_line)
#         new_corp.write(orig_line + "\n")
# new_corp.close()

#


# index = 0
# hyphen_pattern = re.compile("(w+\-w+)|(d+\-d+)|(d+\:d+)")
#
# hyphen_hybreed_pattern = "w+\-d+"
# for token in text.findall("Token"):
#     if "DOCSTART" in new_corp[index]:
#         index += 1
#         continue
#     line = "\n"
#     for child in token:
#         print(child.tag)
#     print(new_corp[index])
#     print(index)
#     index += 1
#     input_file.write(line)
#     if index == 100:
#         break
#
# print(new_corp[0])
input_file.close()