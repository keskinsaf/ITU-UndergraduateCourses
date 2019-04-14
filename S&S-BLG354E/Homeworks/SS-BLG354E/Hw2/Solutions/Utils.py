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
    print(directory_path)
    # Set the parameters for the output file.
    par = list(wr.getparams())
    par[3] = 0  # The number of samples will be set by writeframes.
    par = tuple(par)
    ww = wave.open( directory_path + 'pitch1.wav', 'w')
    ww.setparams(par)
    fr = 20
    sz = wr.getframerate()//fr  # Read and process 1/fr second at a time.
    # A larger number for fr means less reverb.
    c = int(wr.getnframes()/sz)  # count of the whole file
    shift = 1000//fr  # shifting 100 Hz
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