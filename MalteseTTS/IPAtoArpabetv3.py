from typing import Dict, List, Set
from pandas import DataFrame
from collections import defaultdict
import pandas   # for CSV files
import csv   # for CSV files
import unicodecsv   # for CSV files


# tʃ = ʧ, dʒ = ʤ,
# Regex to find 4 CSV values; .*, .*, .* (lines 155857)

arpabet1: Dict[str, str] = {'ɑ': 'a', 'æ': '@', 'ʌ': 'A', 'ɔ': 'c', 'aʊ': 'W', 'ə': 'x', 'ɚ': 'N/A', 'aɪ': 'Y',
                            'ɛ': 'E', 'ɝ': 'R', 'eɪ': 'e', 'ɪ': 'I', 'ɨ': 'X', 'i': 'i', 'oʊ': 'o', 'ɔɪ': 'O',
                            'ʊ': 'U', 'u': 'u', 'ʉ': 'N/A',

                            'b': 'b', 'ʧ': 'C', 'd': 'd', 'ð': 'D', 'ɾ': 'F', 'l̩': 'L', 'm̩': 'M', 'n̩': 'N',
                            'f': 'f', 'ɡ': 'g', 'h': 'h', 'ʤ': 'J', 'k': 'k', 'l': 'l', 'm': 'm', 'n': 'n',
                            'ŋ': 'G', 'ɾ̃': 'N/A', 'p': 'p', 'ʔ': 'Q', 'ɹ': 'r', 's': 's', 'ʃ': 'S', 't': 't',
                            'θ': 'T', 'v': 'v', 'w': 'w', 'ʍ': 'H', 'j': 'y', 'z': 'z', 'ʒ': 'Z',

                            'ɐ': 'TBD', 'r': 'TBD', ' ': ' ', 'g': 'g'}

# Converts IPA Symbols to 2-Letter ARPABET Symbols
# arpabet2: Dict[str, str] = {'ɑ': 'AA', 'æ': 'AE', 'ʌ': 'AH', 'ɔ': 'AO', 'aʊ': 'AW', 'ə': 'AX', 'ɚ': 'AXR', 'aɪ': 'AY',
#                             'ɛ': 'EH', 'ɝ': 'ER', 'eɪ': 'EY', 'ɪ': 'IH', 'ɨ': 'IX', 'i': 'IY', 'oʊ': 'OW', 'ɔɪ': 'OY',
#                             'ʊ': 'UH', 'u': 'UW', 'ʉ': 'UX',
#
#                             'b': 'B', 'ʧ': 'CH', 'd': 'D', 'ð': 'DH', 'ɾ': 'DX', 'l̩': 'EL', 'm̩': 'EM', 'n̩': 'EN',
#                             'f': 'F', 'ɡ': 'G', 'h': 'HH or H', 'ʤ': 'JH', 'k': 'K', 'l': 'L', 'm': 'M', 'n': 'N',
#                             'ŋ': 'NX or NG', 'ɾ̃': 'NX', 'p': 'P', 'ʔ': 'Q', 'ɹ': 'R', 's': 'S', 'ʃ': 'SH', 't': 'T',
#                             'θ': 'TH', 'v': 'V', 'w': 'W', 'ʍ': 'WH', 'j': 'Y', 'z': 'Z', 'ʒ': 'ZH',
#
#                             'ɐ': 'AH', 'r': '-', ' ': ' ', 'g': 'G', ':': ':', 'y': '-', 'à': '-', 'c': '-', 'ù': '-', '!': '-', '(': '-', ')': '-', 'ì': '-', 'ej': '-', 'I': '-', '\'': '-', 'è': '-', '.': '-'}
arpabet2: Dict[str, str] = {'ɑ': 'AA', 'ɐ': 'AH', 'ɔ': 'AO', 'ɛ': 'EH', 'ɪ': 'IH', 'i': 'IY', 'ʊ': 'UH', 'u': 'UW',

                            'b': 'B', 'ʧ': 'CH', 'd': 'D', 'f': 'F', 'g': 'G', 'h': 'HH', 'ʤ': 'JH', 'k': 'K', 'l': 'L',
                            'm': 'M', 'n': 'N', 'p': 'P', 'ʔ': 'Q', 'r': 'R', 's': 'S', 'ʃ': 'SH', 't': 'T',
                            'v': 'V', 'w': 'W', 'j': 'Y', 'z': 'Z', 'ʒ': 'ZH'}

                            # 'y': '#', 'à': '#', 'c': '#', 'ù': '#', 'ì': '#', 'a': '#', 'e': '#', 'I': '#', 'è': '#', 'æ': 'AE'}   # TODO
arpabet2 = defaultdict(lambda: '#', arpabet2)

# Converts an IPA Symbol into a 1 or 2-Letter ARPABET Symbol
def ipa_symbol_to_arpabet_symbol(ipa_symbol: str, arpabet1or2: int = 2) -> str:
    if arpabet1or2 == 1:
        return arpabet1[ipa_symbol]
    elif arpabet1or2 == 2:
        return arpabet2[ipa_symbol]
    else:
        print("Invalid Parameter!")


# Converts a string of IPA Symbols into a string of 1 or 2-Letter ARPABET Symbols
def ipa_string_to_arpabet_string(ipa_string: str, arpabet1or2: int = 2) -> str:
    arpabet_string: str = ""
    ipa_symbol_string: str = ""

    if arpabet1or2 == 1:
        i = 0
        while i < len(ipa_string):
            # if ipa_string[i] == 'a' or ipa_string[i] == 'e' or ipa_string[i] == 'o':
            #     ipa_symbol_string += ipa_string[i]
            # elif ipa_string[i] == 'ɔ' and i+1 < len(ipa_string) and ipa_string[i + 1] == 'ɪ':
            #     ipa_symbol_string += ipa_string[i]
            # else:
            ipa_symbol_string += ipa_string[i]
            arpabet_string += ipa_symbol_to_arpabet_symbol(ipa_symbol_string, 1)
            if i+1 < len(ipa_string) and ipa_string[i + 1] == 'ː':
                arpabet_string += 'ː'
                i += 1
            ipa_symbol_string = ""
            i += 1
    elif arpabet1or2 == 2:
        i = 0
        while i < len(ipa_string):
            # if ipa_string[i] == 'a' or ipa_string[i] == 'e' or ipa_string[i] == 'o':
            #     ipa_symbol_string += ipa_string[i]
            # elif ipa_string[i] == 'ɔ' and i+1 < len(ipa_string) and ipa_string[i + 1] == 'ɪ':
            #     ipa_symbol_string += ipa_string[i]
            # else:
            ipa_symbol_string += ipa_string[i]
            arpabet_string += ipa_symbol_to_arpabet_symbol(ipa_symbol_string, 2)
            ipa_symbol_string = ""
            if i+1 < len(ipa_string) and ipa_string[i + 1] == 'ː':
                arpabet_string += 'ː'
                i += 1
            arpabet_string += ' '
            i += 1
    else:
        print("Invalid Parameter!")

    return arpabet_string


# Converts a string of IPA Symbols into a list of 1 or 2-Letter ARPABET Symbols
def ipa_string_to_arpabet_list(ipa_string: str, arpabet1or2: int = 2) -> List[str]:
    arpabet_list: List[str] = []
    arpabet_symbol_string: str = ""
    ipa_symbol_string: str = ""

    if arpabet1or2 == 1:
        i = 0
        while i < len(ipa_string):
            if ipa_string[i] == 'a' or ipa_string[i] == 'e' or ipa_string[i] == 'o':
                ipa_symbol_string += ipa_string[i]
            elif ipa_string[i] == 'ɔ' and i+1 < len(ipa_string) and ipa_string[i + 1] == 'ɪ':
                ipa_symbol_string += ipa_string[i]
            else:
                ipa_symbol_string += ipa_string[i]
                arpabet_symbol_string += ipa_symbol_to_arpabet_symbol(ipa_symbol_string, 1)
                if i+1 < len(ipa_string) and (ipa_string[i + 1] == 'ː' or ipa_string[i+1] == ':'):
                    arpabet_symbol_string += 'ː'
                    i += 1
                arpabet_list.append(arpabet_symbol_string)
                arpabet_symbol_string = ""
                ipa_symbol_string = ""
            i += 1
    elif arpabet1or2 == 2:
        i = 0
        while i < len(ipa_string):
            # if ipa_string[i] == 'a' or ipa_string[i] == 'e' or ipa_string[i] == 'o':
            #     ipa_symbol_string += ipa_string[i]
            # elif ipa_string[i] == 'ɔ' and i+1 < len(ipa_string) and ipa_string[i + 1] == 'ɪ':
            #     ipa_symbol_string += ipa_string[i]
            if str.isalpha(ipa_string[i]) or ipa_string[i] == 'ː' or ipa_string[i] == ':' :
                ipa_symbol_string += ipa_string[i]
                arpabet_symbol_string += ipa_symbol_to_arpabet_symbol(ipa_symbol_string)
                ipa_symbol_string = ""
                if i+1 < len(ipa_string) and (ipa_string[i + 1] == 'ː' or ipa_string[i+1] == ':'):
                    arpabet_symbol_string += 'ː'
                    i += 1
                arpabet_list.append(arpabet_symbol_string)
                arpabet_symbol_string = ""
            i += 1
    else:
        print("Invalid Parameter!")

    return arpabet_list


# Method for reading a CSV file
def read_csv(file_name: str) -> DataFrame:
# def read_csv(file_name: str) -> Dict:
    # index_col argument can be left out so that an index is generated for each entry -
    # this would be handy for having multiple phonemes for the same word (eg: 'sur')
    # na_filter=False was used so that the word 'nan' is read as a string, not as the NotANumber symbol
    return pandas.read_csv(file_name, index_col='word', encoding='utf-8-sig', na_filter=False)

    # TODO
    # word_phoneme_dictionary: Dict[str, str] = dict()    # TODO default dict with default to UNK?
    # with open(file_name, 'r', encoding='utf-8-sig') as word_phoneme_file:
    # # with open(file_name, 'rb') as word_phoneme_file:
    # #     file = word_phoneme_file.read().decode
    #     reader = csv.reader(word_phoneme_file, delimiter=',')
    # #     reader = unicodecsv.reader(word_phoneme_file, delimiter=',', encoding='utf-8-sig')
    #     # ignoring the first row (header row - word,phonetic)
    #     next(reader)
    #     for word_phoneme_pair in reader:
    #         # word_phoneme_dictionary[word_phoneme_pair[0].decode('utf-8-sig')] = word_phoneme_pair[1].decode('utf-8-sig')
    #         # print(word_phoneme_pair[0].decode('utf-8-sig') + ' ' + word_phoneme_pair[1].decode('utf-8-sig'))
    #         word_phoneme_dictionary[word_phoneme_pair[0]] = word_phoneme_pair[1]
    #         print(word_phoneme_pair[0] + ' ' + word_phoneme_pair[1])
    #
    # return word_phoneme_dictionary


# Method which takes a DataFrame representing the input from a 'word, phoneme' CSV file,
# and finds the arpabet 1 or 2 equivalents to each
def ipa_file_to_arpabet_strings(ipa_file: DataFrame, arpabet1or2: int = 2) -> List[str]:
    arpabet_conversions: List[str] = []

    if arpabet1or2 == 1:
        for word_phoneme_pair in ipa_file.itertuples():
            arpabet_conversions.append(ipa_string_to_arpabet_string(word_phoneme_pair[1], 1))
    elif arpabet1or2 == 2:
        for word_phoneme_pair in ipa_file.itertuples():
            arpabet_conversions.append(ipa_string_to_arpabet_string(word_phoneme_pair[1], 2))
    else:
        print("Invalid Parameter!")

    return arpabet_conversions


def ipa_file_to_arpabet_lists(ipa_file: DataFrame, arpabet1or2: int = 2) -> List[List[str]]:
    arpabet_conversions: List[List[str]] = []

    if arpabet1or2 == 1:
        for word in ipa_file.itertuples():
            arpabet_conversions.append(ipa_string_to_arpabet_list(word[1], 1))
    elif arpabet1or2 == 2:
        for word in ipa_file.itertuples():
            arpabet_conversions.append(ipa_string_to_arpabet_list(word[1], 2))
    else:
        print("Invalid Parameter!")

    return arpabet_conversions


def find_unique_symbols(ipaFile: DataFrame):
    uniqueSymbols: set = set()
    for word in ipaFile.itertuples():
        for symbol in word[1]:
            # if not uniqueSymbols.__contains__(symbol):
            #     print(word[0])
            uniqueSymbols.add(symbol)
    print(len(uniqueSymbols))
    print(uniqueSymbols)


def findArpabetOfWord(word: str) -> str:
    return ipa_file.loc[word]['arpabetList']  # TODO change to List in final implementation


# Method which finds the ARPABET Phonetics for a DataFrame of words
# def findArpabetList(wordFile: DataFrame) -> List[str]: # change to List[List[str]] TODO
def find_arpabet_list(wordFile: DataFrame) -> List[List[str]]:
    arpabet_phonetics: List[List[str]] = []

    for wordFileRow in wordFile.itertuples():
        word: str = wordFileRow[0]
        # print(word + ' ' + ipa_file.loc[word]['arpabetString'])  # TODO remove
        print(word + ' ' + str(ipa_file.loc[word]['arpabetList']))
        arpabet_phonetics.append(findArpabetOfWord(word))

    return arpabet_phonetics


# Method which looks for words with duplicate entries but different phonetics
def findDuplicateEntries(ipaFile: DataFrame):
    print()
    print('Differences Found:')
    print()
    encountered: set = set()
    foundPairs: List[List[str]] = []
    duplicateCount: int = 0
    for entry in ipaFile.itertuples():
        if encountered.__contains__(entry[0]):
            for pair in foundPairs:
                if entry[0] == pair[0]:
                    if entry[1] != pair[1]:
                        print(entry[0] + ' ' + entry[1])
                        print(pair[0] + ' ' + pair[1])
                        print()
                    else:
                        duplicateCount += 1
        else:
            encountered.add(entry[0])
            foundPairs.append([entry[0], entry[1]])
    print('Duplicates Found: ' + str(duplicateCount))
    print()


def findUniqueWords(ipaFile: DataFrame):
    uniqueWords: Set[str] = set()
    for word in ipaFile.itertuples():
        uniqueWords.add(word[0])

    uniqueWordsDF: DataFrame = DataFrame(columns=["words"])
    uniqueWordsDF["words"] = list(uniqueWords)
    uniqueWordsDF.set_index('words', inplace=True)
    uniqueWordsDF.to_csv("UniqueWords.csv")


def ipa_dictionary_to_arpabet_dictionary(word_ipa_phoneme_dictionary: Dict[str, str], arpabet1or2: int = 2) -> Dict[str, List[str]]:
    word_arpabet_phoneme_dictionary: Dict[str, List[str]] = dict()

    if arpabet1or2 == 1:
        for word, ipa_phoneme in word_ipa_phoneme_dictionary.items():
            word_arpabet_phoneme_dictionary[word] = ipa_string_to_arpabet_list(ipa_phoneme, 1)
    elif arpabet1or2 == 2:
        for word, ipa_phoneme in word_ipa_phoneme_dictionary.items():
            word_arpabet_phoneme_dictionary[word] = ipa_string_to_arpabet_list(ipa_phoneme, 2)
    else:
        print("Invalid Parameter!")

    return word_arpabet_phoneme_dictionary


if __name__ == "__main__":
    # Scan the CSV file containing Maltese words and their IPA pronunciation
    ipa_file: DataFrame = read_csv('Phonemes.csv')
    # word_ipa_phoneme_dictionary: Dict[str, str] = read_csv('Phonemes.csv')
    # print("Input CSV File:")
    # print(word_ipa_phoneme_dictionary)

    # Convert the IPA phonetics of every word in the CSV file, into 2-letter ARPABET equivalents
    # and store them as 2 new columns, one as a string and the other as a list of symbols
    # ipa_file['arpabetString'] = ipa_file_to_arpabet_strings(ipa_file)
    ipa_file['arpabetList'] = ipa_file_to_arpabet_lists(ipa_file)
    # word_arpabet_phoneme_dictionary: Dict[str, str] = ipa_dictionary_to_arpabet_dictionary(word_ipa_phoneme_dictionary, 2)
    # print(word_arpabet_phoneme_dictionary)

    # Write the data frame of words, phonemes (ipa), phonemes (arpabet 2 strings) and phonemes (arpabet 2 lists)
    # to a CSV File
    ipa_file.to_csv('ARPABET Output.csv')
    print("Output CSV File:")
    print(ipa_file)
    print()

    # Get the Arpabet phonetics for a word in the database
    wordPhonetics: str = "stalel"
    # print(ipa_file.loc[wordPhonetics]['arpabetString'])
    print(ipa_file.loc[wordPhonetics]['arpabetList'])

    find_unique_symbols(ipa_file)

    wordFile: DataFrame = read_csv('FindArpabetTest.csv')
    wordFile['arpabet'] = find_arpabet_list(wordFile)
    wordFile.to_csv('FindArpabetTestOutput.csv')

    #findDuplicateEntries(ipaFile)

    findUniqueWords(ipa_file)
