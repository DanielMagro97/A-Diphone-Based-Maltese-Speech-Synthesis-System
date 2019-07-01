writeFileLine: "./pitch_list.txt", "time,pitch"
selectObject: 1
To Pitch: 0, 75, 600
no_of_frames = Get number of frames

for frame from 1 to no_of_frames
    time = Get time from frame number: frame
    pitch = Get value in frame: frame, "Hertz"
    appendFileLine: "pitch_list.txt", "'time','pitch'"
endfor