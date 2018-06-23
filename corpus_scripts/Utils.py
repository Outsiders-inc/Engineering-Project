import re

# Receives a word, that might contain a delimiter (for example '&'), which comes after a letter that is optional.
# Returns a list of all the possible ways to write the word, with or without each delimiter.
# For example: for input 'main', the uotput should be ['main', 'man'].
import math

## My version - had a small calculation defect:
# def create_words_from_delimiter(word, delimiter):
#     bad_inputs = ["\n", " ", "", ".", ",", "-", ":"]
#     if len(word) == 0 or word in bad_inputs:
#         return [word]
#
#     # Finding all the occurrences of the delimiter in the word
#     delim_indices = list(map(int, [m.start() for m in re.finditer(delimiter, word)]))
#     num_of_delims = len(delim_indices)
#     power_set_delim = int(math.pow(2, num_of_delims))
#     result = [""] * power_set_delim
#
#     start_index = 0
#     n = power_set_delim
#     for i in range(num_of_delims):
#         current_sub_str = word[start_index:delim_indices[i]]
#         print(current_sub_str)   # TODO DELETE
#         print("n = " + str(n))   # TODO DELETE
#         # while n >= 1:
#         for m in range(0,int(power_set_delim / n)):
#             m = m  * (n // 2)   # A PROBLEM WITH THE CONSTANT WE MULTIPLY BY
#             for k in range(0, n // 2):
#                 print("(i) * m + k = " + str((i) * m + k))
#                 result[(i ) * m + k] += current_sub_str
#                 print("(i ) * m + k + (n // 2) = " + str((i) * m + k + (n // 2)))
#                 result[(i ) * m + k + (n // 2)] += current_sub_str[0:-1]
#                 # result[i * m + k] += current_sub_str
#                 # result[i * m + k + int(n / 2)] += current_sub_str[0:-1]
#         n //= 2
#         start_index = delim_indices[i] + 1
#         print(result)   # TODO DELETE
#     for i in range(power_set_delim):
#         result[i] += word[start_index:]
#
#     return result


# dIFFERENT VERSION:
import copy

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

    # EXAMPLES:
    # ---------
    del1 = create_words_from_delimiter("mai&n", "&")
    print(del1)
    del2 = create_words_from_delimiter("mas&t&er", "&")
    print(del2)
    del3 = create_words_from_delimiter("mas&t&er&ant", "&")
    print(del3)
    del4 = create_words_from_delimiter("mas&t&er&ant&ing", "&")
    print(del4)
