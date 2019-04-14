from ArgumentError import ArgumentError
from Utils import readWavAndSpeedUp

if __name__ == "__main__":
    try:
        import sys
        if len(sys.argv) < 3:
            raise ArgumentError(0)
        file_path = sys.argv[1].strip()
        if file_path.endswith(".wav"):
            wav_file_path = file_path
        else:
            raise ArgumentError(1)
        
        rate = float(sys.argv[2])
        
        readWavAndSpeedUp(wav_file_path, rate)
    except ArgumentError as e:
        print( e )