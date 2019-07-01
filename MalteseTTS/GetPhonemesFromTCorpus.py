from typing import List, Set # for typing
import re   # for RegEx

stage2File: str = "B:\\Users\\danqu\\Desktop\\T-Corpus from Speech Synthesis Project\\stage2final"
stage4File: str = "B:\\Users\\danqu\\Desktop\\T-Corpus from Speech Synthesis Project\\stage4final"

file: str = '\\Gazzetti\\cid=6_aid=351.html.txt'

with open(stage2File+file, encoding="utf-8-sig") as file2, open(stage4File + file, encoding="utf-8-sig") as file4:
    # for line1, line2 in zip(file1, file2):
    #     print(line1 + '\n' + line2 + '\n')

    # TODO ts etc are missing
    acceptableSymbols: Set[str] = {'p', 'e', 'm', 'j', 'l', 'ʒ', 'ɪ', 'ʧ', 'b', 's', 'k', 'y', ' ', 'ʤ', 'h', 'z', 'ʔ',
                                   '.', 'ɛ', 'à', 'ː', 'c', 'w', 'I', "'", '!', 'i', 'd', 'ʃ', 'n', 'ɔ', 'f', 'v', 'ɐ',
                                   'g', 'ì', 'è', 'ù', ':', 'ʊ', '(', ')', 'a', 'ɑ', 'r', 't'}
    # convert the entire text file into a single string by converting new lines into spaces
    stage2FileText: str = file2.read().replace('\n', ' ')
    # split the string by spaces and store it as a list
    stage2FileList: List[str] = stage2FileText.split()
    print(stage2FileList)
    # convert all symbols which aren't letters into spaces
    # TODO just remove the special symbols, not anything not a char (- or ! can probably stay? ' can stay for sure)
    stage2FileTextClean = re.sub('[\W+]', ' ', stage2FileText)
    #stage2FileTextClean = re.sub('\[\W+|\\\'|-]', ' ',stage2FileText)
    #stage2FileTextClean = re.sub('Ⓐ|▲', ' ', stage2FileText)
    stage2FileCleanList: str = stage2FileTextClean.split()
    print(stage2FileTextClean)
    print(stage2FileCleanList)

    print()

    # convert the entire text file into a single string by converting new lines into spaces
    stage4FileText: str = file4.read().replace('\n', ' ')
    # split the string by spaces and store it as a list
    stage4FileList: List[str] = stage4FileText.split('·')
    i: int = 0
    while i < len(stage4FileList):
        # TODO remove symbols before splitting
        # TODO maybe instead strip the ending ' or - here?
        stage4FileList[i] = stage4FileList[i].strip()
        # if (stage4FileList[i].__contains__('●')):
        #     stage4FileList.remove(stage4FileList[i])
        #     i -= 1
        print(stage2FileCleanList[i] + ' - pronounced as - ' + stage4FileList[i])
        i += 1
    # print(stage4FileList)
    # convert all symbols which aren't letters into spaces
    # stage4FileTextClean = re.sub('\W+', ' ', stage4FileText)
    stage4FileTextClean = re.sub('[^\spemjlʒɪʧbskyʤhzʔɛàːcwI!idʃnɔfvɐgìèù:ʊaɑrt·]', '', stage4FileText)
    print(stage4FileTextClean)
    stage4FileCleanList: List[str] = stage4FileTextClean.split('·')
    # print(stage4FileTextClean)
    # print(stage4FileCleanList)

    for stage2Entry,stage4Entry in zip(stage2FileCleanList, stage4FileCleanList):
        print(stage2Entry + 'is pronounced as' + stage4Entry)