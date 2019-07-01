import sys                  # for program exit
from typing import List     # for type annotation
import scipy.io.wavfile     # for using .wav files
import numpy as np          # for numpy arrays
import TDPSOLA              # for TDPSOLA


def concatenate_diphones(all_audio_file_paths: List[str], method: str = 'TD-PSOLA') -> np.ndarray:
    if method == 'naive-concatenation':
        all_audio_samples: List[np.ndarray] = list()
        for audio_file_path in all_audio_file_paths:
            fs, audio_samples = scipy.io.wavfile.read(audio_file_path)
            all_audio_samples.append(audio_samples)
        return np.concatenate(all_audio_samples)
    elif method == 'TD-PSOLA':
        return TDPSOLA.combine_all_audio_tdpsola(all_audio_file_paths)
    else:
        sys.exit('Invalid Concatenation Algorithm Chosen!')