from typing import List, Dict  # for type annotation

import csv                      # for reading from .csv fiels

import os                       # for file paths
import subprocess               # for running commands over command line


# Method for reading a CSV file
def read_csv(file_name: str) -> Dict:
    # index_col argument can be left out so that an index is generated for each entry -
    # this would be handy for having multiple phonemes for the same word (eg: 'sur')
    # na_filter=False was used so that the word 'nan' is read as a string, not as the NotANumber symbol
    # return pandas.read_csv(filename, index_col='word', encoding='utf-8-sig', na_filter=False)
    word_phoneme_dictionary: Dict[str, str] = dict()    # TODO default dict with default to UNK?
    with open(file_name, 'r', encoding='utf-8-sig') as word_phoneme_file:
    # with open(file_name, 'rb') as word_phoneme_file:
    #     file = word_phoneme_file.read().decode
        reader = csv.reader(word_phoneme_file, delimiter=',')
    #     reader = unicodecsv.reader(word_phoneme_file, delimiter=',', encoding='utf-8-sig')
        # ignoring the first row (header row - word,phonetic)
        next(reader)
        for word_phoneme_pair in reader:
            # word_phoneme_dictionary[word_phoneme_pair[0].decode('utf-8-sig')] = word_phoneme_pair[1].decode('utf-8-sig')
            # print(word_phoneme_pair[0].decode('utf-8-sig') + ' ' + word_phoneme_pair[1].decode('utf-8-sig'))
            word_phoneme_dictionary[word_phoneme_pair[0]] = word_phoneme_pair[1]
            print(word_phoneme_pair[0] + ' ' + word_phoneme_pair[1])

    # TODO instead of returning just save to disk as a .pkl file

    return word_phoneme_dictionary


def graphemes_to_phonemes_Phonemes_csv(graphemes: str) -> str:
    # load the word->phoneme dictionary from disk
    dictionary: Dict[str, str] = dict()# TODO use pickle or so

    # split the graphemes into tokens, in case there are multiple words
    tokens: List[str] = graphemes.split()

    phonemes_list: List[str] = list()
    for token in tokens:
        phonemes_list.append(dictionary[token])

    phonemes_string: str = ""
    for phonemes in phonemes_list:
        phonemes_string += phonemes + ' '
    phonemes_string.strip()

    return phonemes_string


def graphemes_to_phonemes_Crimsonwing_MalteseG2P(graphemes: str) -> str:
    malteseg2p_executable_file_path = os.path.abspath(r"MalteseG2P\MalteseG2P.exe")
    graphemes_file_path = os.path.abspath(r"MalteseG2P\graphemes.txt")
    phonemes_file_path = os.path.abspath(r"MalteseG2P\phonemes.txt")

    # write the graphemes to be converted to phonemes to a text file
    with open(graphemes_file_path, 'w', encoding='utf-8') as input_graphemes:
        input_graphemes.write(graphemes)

    # run the Crimsonwing MalteseG2P program which will convert the graphemes in graphemes_file_path
    # to phonemes in phonemes_file_path
    subprocess.run('"' + malteseg2p_executable_file_path + '" "' + graphemes_file_path + '" "' + phonemes_file_path + '"',
                   stdout=subprocess.DEVNULL)

    # read the phonemes in from phonemes_file_path
    with open(phonemes_file_path, 'r', encoding='utf-8-sig') as output_phonemes:
        return output_phonemes.read()


if __name__ == '__main__':
    print(graphemes_to_phonemes_Crimsonwing_MalteseG2P("jien jisimni Daniel!."))
    print(graphemes_to_phonemes_Crimsonwing_MalteseG2P("sur"))
    print(graphemes_to_phonemes_Crimsonwing_MalteseG2P("Jien għandi 21 sena'."))
    print(graphemes_to_phonemes_Crimsonwing_MalteseG2P("għandi"))
    print(graphemes_to_phonemes_Crimsonwing_MalteseG2P("għandek"))
    print(graphemes_to_phonemes_Crimsonwing_MalteseG2P("għaliex"))

    print(graphemes_to_phonemes_Crimsonwing_MalteseG2P("sar"))
    print(graphemes_to_phonemes_Crimsonwing_MalteseG2P("sur"))