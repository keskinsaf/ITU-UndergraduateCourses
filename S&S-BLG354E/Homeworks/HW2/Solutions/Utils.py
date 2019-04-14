def convert2Wav(file_path):
    from pydub import AudioSegment
    file_name = file_path.split("/")[-1]
    file_name_without_extension = file_name[:len(file_name) - 4]

    mp3_audio = AudioSegment.from_mp3(file_path)
    wav_file_path = "./output/" + file_name_without_extension + ".wav"
    mp3_audio.export(wav_file_path, format="wav")
    return wav_file_path

def readAndProcessWavUsingRftt(file_path):
    import wave
    import numpy as np
    wr = wave.open(file_path, 'r')
    splitted_file_path = file_path.split("/")
    directory_path = "/".join(splitted_file_path[:-1]) + "/" if len(splitted_file_path) > 1 else "./"
    # print(directory_path)
    # Set the parameters for the output file.
    par = list(wr.getparams())
    par[3] = 0  # The number of samples will be set by writeframes.
    par = tuple(par)
    ww = wave.open( directory_path + 'p1.wav', 'w')
    ww.setparams(par)
    fr = 20
    sz = wr.getframerate()//fr  # Read and process 1/fr second at a time.
    # A larger number for fr means less reverb.
    c = int(wr.getnframes()/sz)  # count of the whole file
    shift = 100//fr  # shifting 100 Hz
    for num in range(c):
        da = np.fromstring(wr.readframes(sz), dtype=np.int16)
        left, right = da[0::2], da[1::2]  # left and right channel
        lf, rf = np.fft.rfft(left), np.fft.rfft(right)
        lf, rf = np.roll(lf, shift), np.roll(rf, shift)
        lf[0:shift], rf[0:shift] = 0, 0
        nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
        ns = np.column_stack((nl, nr)).ravel().astype(np.int16)
        ww.writeframes(ns.tostring())
    wr.close()
    ww.close()

def readAndProcessWav(file_path):
    from pydub import AudioSegment
    from pydub.playback import play

    sound = AudioSegment.from_file(file_path, format="wav")

    # shift the pitch up by half an octave (speed will increase proportionally)
    octaves = 0.5

    new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))

    # keep the same samples but tell the computer they ought to be played at the 
    # new, higher sample rate. This file sounds like a chipmunk but has a weird sample rate.
    hipitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})

    # now we just convert it to a common sample rate (44.1k - standard audio CD) to 
    # make sure it works in regular audio players. Other than potentially losing audio quality (if
    # you set it too low - 44.1k is plenty) this should now noticeable change how the audio sounds.
    hipitch_sound = hipitch_sound.set_frame_rate(44100)

    #Play pitch changed sound
    play(hipitch_sound)

    
    # take export directory
    splitted_file_path = file_path.split("/")
    directory_path = "/".join(splitted_file_path[:-1]) + "/" if len(splitted_file_path) > 1 else "./"

    #export / save pitch changed sound
    hipitch_sound.export( directory_path + "out.wav", format="wav")

def readWav(file_path):
    # inspired from https://stackoverflow.com/a/42567511/6013366
    from pydub import AudioSegment
    import numpy as np
    audio = AudioSegment.from_file(file_path, format="wav")
    sample_array = audio.get_array_of_samples()
    return np.array(sample_array), audio.frame_rate

def writeToWav(file_path, frame_rate, data, exit_file_name=None):
    import scipy.io.wavfile as wavfile
    output_file_path = file_path.split(".wav")[0] + "_fastened.wav" if exit_file_name is None else exit_file_name
    print(output_file_path)
    wavfile.write(output_file_path, frame_rate, data)
    return output_file_path, frame_rate

def readWavAndSpeedUp(file_path, rate):
    print("File at " + file_path + " will be read and processed.")
    print("Reading part is started...")
    sound, sound_frame_rate = readWav(file_path)
    print("File is read.")
    print("Frame_rate of input file is: ", sound_frame_rate)

    print("Processing part is started...")
    output_path, fast_frame_rate = writeToWav(file_path, int(sound_frame_rate * 2 * rate), sound)
    print("Processing is completed...")
    print("Path of output file is: ", output_path)
    print("Frame_rate of output file is: ", fast_frame_rate / 2)

def convolve2Signals(s1, s2):
    import numpy as np
    l1 = s1.shape[0]
    l2 = s2.shape[0]
    if l1 < l2:
        c1 = s2
        c2 = s1
    else:
        c1 = s1
        c2 = s2
    
    j = 1
    res = []

    for i in range(l1 + l2 - 1):
        if i < c2.shape[0]:
            res.append(np.sum(np.multiply( c1[:i+1], c2[:i+1][::-1] )) )
        elif i < c1.shape[0]:
            res.append(np.sum(np.multiply( c1[i-c2.shape[0]+1:i+1], c2[::-1] )))
        else:
            res.append(np.sum(np.multiply( c1[i-c2.shape[0]+1 : i+1-j], c2[::-1][:c2.shape[0]-j])))
            j += 1
    return np.array(res)