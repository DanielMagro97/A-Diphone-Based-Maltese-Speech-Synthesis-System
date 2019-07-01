import os
from typing import List, Set  # for type annotation
from pandas import DataFrame
import IPAtoArpabetv3
from MalteseG2P import graphemes_to_phonemes_Crimsonwing_MalteseG2P


if __name__ == '__main__':
    words: Set[str] = set()
    for i, file in enumerate(os.listdir('D:\Daniel\Full MLRS Corpus')):
        print(str(i+1) + '/' + str(len(os.listdir('D:\Daniel\Full MLRS Corpus'))))
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            with open('D:\Daniel\Full MLRS Corpus\\' + filename, 'r', encoding='utf-8') as text_file:
                for line in text_file:
                # for line, next_line in zip(text_file, iter(text_file[1:])):
                # for i, line in enumerate(text_file):
                #     print(line)
                #     print(text_file)
                    line_list: List[str] = line.split()
                    word: str = str.lower(line_list[0])
                    if line[0] != '<':
                        pos_tag: str = line_list[1]
                    # if the line is meta data (starts with <)
                    # or the 'word' is punctuation
                    # or the word contains any digits
                    # or the word is marked as foreign, and so is the one after it
                    # TODO or line[:3] == 'www'
                    if line[0] == '<' or pos_tag == 'X-PUN' or pos_tag == 'X-DIG': # TODO or ((pos_tag == 'X-ENG' or pos_tag == 'X-FOR') and next_line.split()[1] == pos_tag):
                        # ignore it
                        continue
                    else:
                        words.add(word)

    with open('D:\Daniel\Full MLRS Corpus\\MalteseWords.csv', 'w', encoding='utf-8') as output:
        output.write('word,phonetic' + '\n')
        for i, word in enumerate(words):
            if (i % 2500) == 0:
                print(str(i) + '/' + str(len(words)))
            phonemes: str = graphemes_to_phonemes_Crimsonwing_MalteseG2P(word).strip()
            output.write(word + ',' + phonemes + '\n')

    ipa_file: DataFrame = IPAtoArpabetv3.read_csv('D:\Daniel\Full MLRS Corpus\\MalteseWords.csv')
    ipa_file['arpabetList'] = IPAtoArpabetv3.ipa_file_to_arpabet_lists(ipa_file)
    ipa_file.to_csv('D:\Daniel\Full MLRS Corpus\ARPABET Output.csv')
