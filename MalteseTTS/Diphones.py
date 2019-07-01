from typing import List # for type annotation
import pyaudio          # for recording audio
import wave             # for recording audio
import scipy.io.wavfile # for reading audio
# import mlpy             # for Dynamic Time Warping (DTW)
import fastdtw          # for Dynamic Time Warping (DTW)
import numpy as np
import TDPSOLA
import random           # for list shuffling
import pandas           # for Data Frames
import ast              # for converting string list into actual list
import os               # for folder directories

def record_wav_audio(fs: int = 16000, duration: float = 10, output_filename = "sound.wav"):
    """
    Record mono wav data from system microphone
    :param fs: Sampling frequency (Hz)
    :param duration: Duration of recording (seconds)
    :param output_filename: Absolute path of wav file to be written
    :return:
    """
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = fs
    RECORD_SECONDS = duration

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK)

    print("Recording...")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Done!")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open("diphones\\" + output_filename, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


def get_all_maltese_diphones(phonemes: List[str]) -> List[str]:
    diphones: List[str] = list()

    for phoneme1 in phonemes:
        for phoneme2 in phonemes:
            diphone: str = phoneme1 + '-' + phoneme2
            diphones.append(diphone)

    return diphones


def find_carrier_word_for_diphone(arpabet_file: pandas.DataFrame, diphone: str) -> str:

    # extract the two phonemes that need to be found consecutively in the carrier word
    phoneme1: str = diphone.split('-')[0]
    phoneme2: str = diphone.split('-')[1]    # TODO remove '-'s from phonemes list

    # initially declare the carrier word as an empty string
    carrier_word: str = ""
    # iterate over all word,phoneme pairs in the arpabet_file DataFrame
    for word_phoneme_pair in arpabet_file.itertuples():
        word: str = word_phoneme_pair[0]
        arpabet: List[str] = ast.literal_eval(word_phoneme_pair[2])

        # boolean value which tracks whether the current word is a suitable carrier word for the current diphone
        word_contains_diphone: bool = False

        # check if the word contains the current diphone by looking at every pair of consecutive diphones
        # from the middle of the word

        # if the first phoneme of the diphone is a # (silence), look for the diphone at the beginning of the word
        if phoneme1 == '#':
            if arpabet[0] == phoneme2:
                word_contains_diphone = True
        # if the second phoneme of the diphone is a # (silence), look for the diphone at the end of the word
        elif phoneme2 == '#':
            if arpabet[-1] == phoneme1:
                word_contains_diphone = True
        # if the diphone does not contain a #, look for the diphone anywhere in the centre of the word
        else:
            word_contains_diphone = (phoneme1, phoneme2) in zip(arpabet[1:-1], arpabet[2:-1])

        if word_contains_diphone:
            carrier_word = word
            print('carrier word for ' + diphone + ' is ' + carrier_word)
            break

    # if the carrier word remains an empty string, then no carrier word was found for it
    if carrier_word == "":
        print('A carrier word for ' + diphone + ' was not found')

    return carrier_word


def find_carrier_words_for_diphones(diphones: List[str]) -> List[List[str]]:
    # declare a list of lists of diphones, that corresponds to the list of carrier phrases
    diphones_in_carrier_phrases: List[List[str]] = list()
    # declare a list of sentences of carrier words. Each sentence is a list of carrier words.
    carrier_phrases: List[List[str]] = list()
    #
    arpabet_file = pandas.read_csv("ARPABET Output.csv", index_col='word', encoding='utf-8-sig', na_filter=False)
    # declare a list of diphones for which a carrier word was not found
    diphones_no_carrier: List[str] = list()
    # shuffle the list of diphones
    random.shuffle(diphones)

    #TODO
    found = 0
    not_found = 0
    orig_no_diph = len(diphones)
    #TODO

    counter: int = 1
    while len(diphones) > 0:
        diphones_in_carrier_phrase: List[str] = list()
        carrier_phrase: List[str] = list()

        # adding a random pad word to the beggining of the carrier phrase so articulation can start
        diphones_in_carrier_phrase.append('pad')
        carrier_phrase.append(arpabet_file.sample().index[0])

        # calculate how many diphones are left for which a carrier word needs to be calculated
        diphones_left: int = len(diphones)
        # iterate over 10 diphones, or the remaining diphones if there are less than 10 left
        for i in range(min(10, diphones_left)):
            # pop a diphone from the list
            diphone: str = diphones.pop()
            # call the find_carrier_word_for_diphone function to find a carrier word for the diphone
            carrier_word: str = find_carrier_word_for_diphone(arpabet_file, diphone)
            # add the diphone to the diphones_in_carrier_phrase list
            diphones_in_carrier_phrase.append(diphone)
            # add the carrier_word to the carrier_phrase
            carrier_phrase.append(carrier_word)

            counter += 1

            #TODO
            if carrier_word == "":
                not_found += 1
            else:
                found += 1
            #TODO

        # adding a random pad word to the end of the carrier phrase so articulation can stop
        diphones_in_carrier_phrase.append('pad')
        carrier_phrase.append(arpabet_file.sample().index[0])

        diphones_in_carrier_phrases.append(diphones_in_carrier_phrase)
        carrier_phrases.append(carrier_phrase)

    print('found: ' + str(found) + '/' + str(orig_no_diph))           # TODO
    print('not found: ' + str(not_found) + '/' + str(orig_no_diph))   # TODO

    # Write a file with the entire transcript of what will be recorded
    with open('DMagroCarrierPhrasesMT\\CarrierPhrases.txt', 'w', encoding='utf-8') as carrier_phrases_text_file:
        for i, diphones_in_carrier_phrase, carrier_phrase in zip(range(len(carrier_phrases)), diphones_in_carrier_phrases, carrier_phrases):
            carrier_phrases_text_file.write(str(i) + '\n')
            carrier_phrases_text_file.write(str(diphones_in_carrier_phrase) + '\n')
            carrier_phrases_text_file.write(str(carrier_phrase) + '\n\n')

    # Write a file for each carrier phrase so that extraction can be easily done
    # (for easier linking of audio files with transcripts when using WebMAUS)
    for i, carrier_phrase in zip(range(len(carrier_phrases)), carrier_phrases):
        with open('DMagroCarrierPhrasesMT\\transcripts\\'+str(i)+'.txt', 'w', encoding='utf-8') as carrier_phrases_text_file:
            for carrier_word in carrier_phrase:
                carrier_phrases_text_file.write(carrier_word + ' ')

    return carrier_phrases


def extract_diphone_from_carrierword_dtw(carrierword_path: str, diphone_path: str, diphone_name: str):
    fs, long_sine = scipy.io.wavfile.read(carrierword_path)
    fs, sub_sine = scipy.io.wavfile.read(diphone_path)

    distance, path = fastdtw.fastdtw(sub_sine, long_sine)

    extracted_diphone_wave = np.empty(len(path))
    for point in path:
        extracted_diphone_wave[point[0]] = long_sine[point[1]]

    scipy.io.wavfile.write(r'diphones\\DMagroDiphonesMT_DTW\\'+diphone_name+'.wav',
                           fs, np.int16(extracted_diphone_wave[:len(sub_sine)]))


# This function uses the generated CarrierPhrases.txt file, the recorded audio, and the CMU US KAL diphone set
# to automatically extract the diphones using Dynamic Time Warping (DTW)
def extract_diphones_dtw():
    # open the generated CarrierPhrases.txt file so as to extract which recordings contain which diphones
    with open('DMagroCarrierPhrasesMT\\CarrierPhrases.txt', 'r', encoding='utf-8') as carrier_phrases_text_file:
        carrier_phrases: List[str] = carrier_phrases_text_file.readlines()
    carrier_phrases = [line.strip() for line in carrier_phrases]

    print(carrier_phrases)

    # iterate until all carrier phrases have been dealt with
    while len(carrier_phrases) > 0:
        # the name of the audio file containing the diphones is the first line in the set of 4
        carrier_phrase_recording: str = carrier_phrases.pop(0)

        # the list of diphones contained in the audio file is on the second line in the set of 4
        diphones_in_carrier_phrase: List[str] = ast.literal_eval(carrier_phrases.pop(0))
        # the first and last diphones are popped as these are pad words
        diphones_in_carrier_phrase.pop(0)
        diphones_in_carrier_phrase.pop(-1)

        # the third and fourth line are irrelevant here, and thus ignored
        carrier_phrases.pop(0)
        carrier_phrases.pop(0)

        # generate the path of the carrier phrase
        carrier_phrase_path: str = 'DMagroCarrierPhrasesMT\\recordings\\' + carrier_phrase_recording + '.wav'
        # iterate over each diphone
        for diphone in diphones_in_carrier_phrase:
            # generate the path of the current diphone, and change it to the format used by CMU
            cmu_diphone: str = diphone.lower().replace('#', 'pau')
            diphone_path: str = 'diphones\\cmu_us_kal\\' + cmu_diphone + '.wav'
            # call the extract_diphone_from_carrierword_dtw function
            extract_diphone_from_carrierword_dtw(carrier_phrase_path, diphone_path, diphone)


if __name__ == '__main__':
    maltese_phonemes: List[str] = ['AA', 'AH', 'AO', 'EH', 'IH', 'IY', 'UH', 'UW',

                                   'B', 'CH', 'D', 'F', 'G', 'HH', 'JH', 'K', 'L',
                                   'M',  'N', 'P', 'Q', 'R', 'S', 'SH', 'T',
                                   'V', 'W', 'Y',  'Z',  'ZH',
                                   '#']
    print(maltese_phonemes)

    diphones: List[str] = get_all_maltese_diphones(maltese_phonemes)
    print(diphones)

    # A statement such as the following can be used to only look for a specific list of diphones
    # This is particularly handy for, say, rerecording any diphones which are deemed to currently be of poor quality
    diphones: List[str] = ['IH-L', 'L-K', 'K-AO', 'AO-M', 'M-P', 'P-Y', 'Y-UH', 'UH-T', 'T-EH', 'EH-R', 'R-#', 'Y-AH', 'AH-F', 'F-#', 'Y-IH', 'IH-T', 'T-K', 'K-EH', 'EH-L', 'L-L', 'L-EH', 'EH-M', 'M-#', 'IH-N', 'N-#', 'K-HH', 'HH-AH', 'AH-N', 'N-D', 'D-IH', 'IH-#', 'W-IH', 'IH-HH', 'HH-EH', 'EH-T', 'T-UH', 'UH-AO', 'AO-SH', 'SH-R', 'R-IH', 'S-EH', 'EH-N', 'N-AH', 'AH-#', 'IH-S', 'S-IH', 'IH-M', 'M-N', 'N-IH', 'D-AH', 'L-#', 'N-T', 'T-#', 'SH-Y', 'S-M', 'M-EH', 'EH-K', 'K-#']

    carrier_phrases: List[List[str]] = find_carrier_words_for_diphones(diphones)
    print(carrier_phrases)

    # The following command can be run to use DTW and the CMU US KAL diphone set to automatically extract the diphones
    # from the recorded carrier phrases
    extract_diphones_dtw()

    # testing:
    fs, long_sine = scipy.io.wavfile.read(r"DMagroCarrierPhrasesMT\recordings\0.wav")
    fs, sub_sine = scipy.io.wavfile.read(r"diphones\cmu_us_kal\ah-n.wav")

    distance, path = fastdtw.fastdtw(sub_sine, long_sine)
    # distance, path = fastdtw.dtw(sub_sine, long_sine)

    test_output = np.empty(len(path))
    for point in path:
        test_output[point[0]] = long_sine[point[1]]

    TDPSOLA.plot_wave_samples(long_sine)
    TDPSOLA.plot_wave_samples(sub_sine)
    TDPSOLA.plot_wave_samples(test_output[:len(sub_sine)])

    print(len(long_sine))
    print(len(sub_sine))
    print(len(test_output))
    print(len(test_output[:len(sub_sine)]))

    scipy.io.wavfile.write(r'outputs\DTW_test_extract.wav', 16000, np.int16(test_output[:len(sub_sine)]))
