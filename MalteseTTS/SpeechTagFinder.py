import os
import pandas

from pandas import DataFrame
from typing import List, Dict


# Method for reading a CSV file
def CSVReader(filename: str) -> DataFrame:
    # index_col can be left blank so that an index is generated for each entry -
    # this would be handy for having multiple phonemes for the same word (eg: 'sur')
    # return pandas.read_csv(filename, index_col='word')
    return pandas.read_csv(filename, index_col='word', encoding='utf-8-sig')


words = {}

from collections import defaultdict
d = defaultdict(set)

counter: int = 1
for file in os.listdir('D:\Daniel\Full MLRS Corpus'):
    print(counter.__str__() + '/' + len(os.listdir('D:\Daniel\Full MLRS Corpus')).__str__())
    filename = os.fsdecode(file)
    if filename.endswith(".txt"):
        with open('D:\Daniel\Full MLRS Corpus\\' + filename, 'r', encoding='utf-8') as textFile:
            for line in textFile:
                if line[0] == '<':
                    continue
                else:
                    lineList: List[str] = line.split()
                    d[lineList[0]].add(lineList[1])
    counter += 1


with open('D:\Daniel\Full MLRS Corpus\\PartsOfSpeech.txt', 'w', encoding='utf-8') as outputAll, open('D:\Daniel\Full MLRS Corpus\\PartsOfSpeechDiff.txt', 'w', encoding='utf-8') as outputDiff:
    for entry in d:
        outputAll.write(entry + ' ' + d[entry].__str__() + '\n')
        if len(d[entry]) > 1:
            print(entry + ' ' + d[entry].__str__())
            outputDiff.write(entry + ' ' + d[entry].__str__() + '\n')