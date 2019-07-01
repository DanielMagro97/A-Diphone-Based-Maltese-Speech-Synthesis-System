from typing import List         # for type annotation
from pandas import DataFrame    # for DataFrames
import numpy as np              # for numpy Arrays
import scipy.io.wavfile         # for using .wav files
import re                       # for RE to remove special characters from file names

import TextNormalisation        # for normalising any NSWs
import MalteseG2P               # for converting graphemes to phonemes
import IPAtoArpabetv3           # for converting strings of IPA symbols to Lists of ARPABET symbols
import DiphoneConcatenation     # for joining a list of diphones together using TD-PSOLA


# function which, given a list of arpabet symbols, returns a list of diphones
def arpabet_list_to_diphones(arpabet_list: List[str], silence_symbol: str = '#') -> List[str]:
    # if no phonemes are present => probably punctuation
    if len(arpabet_list) == 0:
        # insert a silence-silence diphone
        silence_diphone: str = silence_symbol + '-' + silence_symbol
        return [silence_diphone]

    diphones_list: List[str] = list()

    # add the first diphone as a transition from silence to the first phoneme
    # diphones_list.append(silence_symbol + '-' + arpabet_list[0])  # TODO fine tune

    # add the rest of the diphones as a transition from one phoneme to the next
    for i, arpabet_symbol in enumerate(arpabet_list):
        if i+1 < len(arpabet_list):
            diphone: str = arpabet_symbol + '-' + arpabet_list[i+1]
            diphones_list.append(diphone)

    # add the last diphone as a transition from the last phoneme to silence
    diphones_list.append(arpabet_list[-1] + '-' + silence_symbol)

    return diphones_list


if __name__ == '__main__':
    # take as input the text the user would like synthesised
    text: str = input("Jekk jogħġbok ikteb it-test hawn\nPlease enter text here\n")
    print("Input text:")
    print(text)

    ###
    # Front End
    ###

    # split this text by spaces into individual words
    tokens: List[str] = text.split()
    print(tokens)

    # Perform Text Normalisation on the user's input, to handle any NSWs
    tokens = TextNormalisation.normalise_sentence(tokens)

    # Convert the text tokens (graphemes) into a List of phonemes (IPA)
    tokens_phonemes_ipa: List[str] = list()
    for token in tokens:
        # tokens_arpabet.append(IPAtoArpabet.findArpabetOfWord(token))
        # tokens_arpabet.append(ipa_file.loc[token]['arpabetList'])
        tokens_phonemes_ipa.append(MalteseG2P.graphemes_to_phonemes_Crimsonwing_MalteseG2P(token).strip())
    print(tokens_phonemes_ipa)

    # Convert the list of phonemes (IPA) into a List of Lists. Where each inner List contains individual arpabet symbols
    tokens_phonemes_arpabet: List[List[str]] = list()
    for phonemes in tokens_phonemes_ipa:
        tokens_phonemes_arpabet.append(IPAtoArpabetv3.ipa_string_to_arpabet_list(phonemes))
    print(tokens_phonemes_arpabet)

    # Convert the list of lists of arpabet symbols into a list of lists of diphones
    tokens_arpabet_diphones: List[List[str]] = list()
    for phonemes in tokens_phonemes_arpabet:
        tokens_arpabet_diphones.append(arpabet_list_to_diphones(phonemes))
    print(tokens_arpabet_diphones)

    ###
    # Back End
    ###
    print()
    text_arpabet_diphones: List[str] = list()
    # iterate over all the lists of diphones for individual words
    for word_diphones in tokens_arpabet_diphones:
        # iterate over each diphone in the list of diphones for a word
        for diphone in word_diphones:
            # add that diphone to the final phonemic transcription
            text_arpabet_diphones.append(diphone)
        # append a #-# diphone to create space between two words
        text_arpabet_diphones.append('#-#')
    print(text_arpabet_diphones)

    # remove the ː symbol for looking up files in the diphone database
    for i, diphone in enumerate(text_arpabet_diphones):
        text_arpabet_diphones[i] = diphone.replace('ː', '')

    # add the path to the diphone set to the beginning of each diphone, such that they become file paths
    diphone_set: str = r'diphones\\DMagroDiphonesMT\\' # TODO
    # diphone_set: str = r'diphones\\DMagroDiphonesMT_DTW\\'
    # add .wav to the end of each diphone, such that they become file names
    file_extension: str = '.wav'

    text_diphones_filenames: List[str] = [(diphone_set + diphone.lower() + file_extension) for diphone in text_arpabet_diphones]
    print(text_diphones_filenames)

    speech: np.ndarray = DiphoneConcatenation.concatenate_diphones(text_diphones_filenames)
    scipy.io.wavfile.write(r'outputs\\'+re.sub('[~#%&*()\\\:<>?/|"]','',text)+'.wav', 16000, np.int16(speech))