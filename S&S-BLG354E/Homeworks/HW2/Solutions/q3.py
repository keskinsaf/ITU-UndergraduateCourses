import numpy as np
from Utils import convolve2Signals, readWav, writeToWav
from ArgumentError import ArgumentError

if __name__ == "__main__":
    try:
        import sys
        if len(sys.argv) < 3:
            raise ArgumentError(2)
        first_wav  = sys.argv[1].strip()
        second_wav = sys.argv[2].strip()

        if not first_wav.endswith(".wav") or not second_wav.endswith(".wav"):
            raise ArgumentError(1)
        
        print("File 1 will be read...")
        s1, s1_rate = readWav(first_wav)
        print("File 1 is read!")
        # print(s1.shape)
        
        print("File 2 will be read...")
        s2, s2_rate = readWav(second_wav)
        print("File 2 is read!")
        # print(s2.shape)

        print("Convolution will be calculated...")
        y1 = convolve2Signals(s1, s2).astype("int32")
        print("Convolution is calculated!")

        splitted_file_path = first_wav.split("/")
        directory_path = "/".join(splitted_file_path[:-1]) + "/" if len(splitted_file_path) > 1 else "./"

        output_path = directory_path + "y1.wav"

        answer = "y" #input("Processed data will be save to " + output_path + " at " + str(s1_rate) + " sampling rate [y]/n: ").strip()[0]
        print("\n\n\ndatatype:", end=" ")
        print(y1.dtype)

        if answer != "n":
            writeToWav( "" , s1_rate, y1, output_path)
            print("Successful!")

        # import numpy as np
        # print("Numpy convolution will be calculated...")
        # np_y1 = np.convolve(s1, s2)
        # print("Numpy convolution is calculated!")
        # print("\n\n\nnumpy data type: ", end="")
        # print(np_y1.dtype)

        # print(np.array_equal(y1, np_y1))

    except ArgumentError as e:
        print( e )
    
    except Exception as e:
        print(e)