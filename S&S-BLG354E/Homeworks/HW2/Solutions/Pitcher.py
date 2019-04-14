class Pitcher:
    def __init__(self, audio = None):
        if audio is not None:
            self.audio = audio
            print("Pitcher object is initialized with given audio.")
        else:
            print("""Pitcher object is not initialized with an audio. \
                Audio should be set later.""")
    def setAudio(self, audio):
        self.audio = audio
        print("Audio is set to given argument.")