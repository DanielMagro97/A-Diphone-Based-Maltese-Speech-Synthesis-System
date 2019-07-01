from typing import List # for type annotation
import scipy.io.wavfile # for using .wav files

if __name__ == '__main__':
    diphone_list: List[str] = list()
    # open the diphone dictionary which details which .wav file contains each diphone, and during what time it occurs
    with open('cmu_us_kal\kaldiph.est', 'r', encoding='utf-8') as diphone_dictionary:
        # iterate over every diphone entry in the diphone dictionary
        for entry in diphone_dictionary:
            line_list = entry.split()
            # if it is a meta-data line
            if len(line_list) < 5:
                # ignore it
                continue
            else:
                # extract details about the current diphone
                diphone_name: str = line_list[0]
                diphone_wav_file: str = line_list[1]
                diphone_wav_start_time: float = float(line_list[2])
                diphone_wav_end_time: float = float(line_list[4])

                # load the current diphone's carrier word
                fs, carrier_word_samples = scipy.io.wavfile.read('cmu_us_kal\\' + diphone_wav_file + '.wav')

                # convert the start and end times of the diphone within the wav file to samples
                diphone_start_sample: int = int(diphone_wav_start_time * fs)
                diphone_end_sample: int = int(diphone_wav_end_time * fs)

                # trim the carrier word to the part of the wave containing the diphone
                diphone_samples = carrier_word_samples[diphone_start_sample:diphone_end_sample]

                scipy.io.wavfile.write(r'diphones\cmu_us_kal\\'+diphone_name+'.wav' , fs, diphone_samples)
