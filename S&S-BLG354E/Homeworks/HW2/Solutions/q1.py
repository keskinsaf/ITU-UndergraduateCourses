from ArgumentError import ArgumentError
from Utils import convert2Wav, readAndProcessWavUsingRftt

if __name__ == "__main__":
    try:
        import sys
        if len(sys.argv) == 1:
            raise ArgumentError(0)
        file_path = sys.argv[1].strip()
        if file_path.endswith(".mp3"):
            wav_file_path = convert2Wav(file_path)
        elif file_path.endswith(".wav"):
            wav_file_path = file_path
        else:
            raise ArgumentError(1)
        readAndProcessWavUsingRftt(wav_file_path)
    except ArgumentError as e:
        print( e )