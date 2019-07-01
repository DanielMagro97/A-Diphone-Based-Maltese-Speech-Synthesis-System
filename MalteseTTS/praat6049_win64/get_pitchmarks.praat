# get the path of the wav file as a command line argument
form Path command line calls
	sentence wav_file_path example_path
endform

# print the path of the wav file passed as a parameter
#writeInfoLine: "You chose the wav file at path: ", wav_file_path$

# read the wav file at the specified apth
wav = Read from file: wav_file_path$

To Pitch: 0, 75, 600
no_of_frames = Get number of frames

writeFileLine: "./pitch_list.txt", "time,pitch"

for frame from 1 to no_of_frames
    time = Get time from frame number: frame
    pitch = Get value in frame: frame, "Hertz"
    appendFileLine: "pitch_list.txt", "'time','pitch'"
endfor