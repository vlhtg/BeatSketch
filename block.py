import numpy as np

class Block:
    def __init__ (self, bid, present, x, y, angle, enabled=False):
        self.bid = bid
        self.present = present
        self.x = x
        self.y = y
        self.angle = angle
        self.enabled = enabled

    def getID(self):
        return self.bid
    
    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def getEnabled(self):
        return self.enabled
    
    def setLocation(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def setPresent(self, present):
        self.present = present

    def getPresent(self):
        return self.present

    def getRect(self):
        return (self.x, self.y, 100, 100)
    
    def getColor(self):
        if (self.bid < 10):
            return (255, 0, 0)
        if (self.bid >= 10 and self.bid < 20):
            return (0, 255, 0)
        if (self.bid >= 20):
            return (0, 0, 255)
    
    def __slider_to_frequency(self, slider_position, f_min=20, f_max=20000, slider_range=600):
        octaves = np.log2(f_max / f_min)
        r = slider_range / octaves
        return f_min * (2 ** (slider_position / r))
    
    def getDuration(self, bpm, fps):
        return self.x
    
    def getWave(self):
        
        sample_rate = 44100
        amplitude = 0.5
        duration = self.getDuration
        frequency = self.__slider_to_frequency(self.y)

        # generate sine wave
        if (self.bid < 10):
            t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
            wave = amplitude * np.sin(2 * np.pi * frequency * t)
        # generate sawtooth wave
        if (self.bid >= 10 and self.bid < 20):
            t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
            wave = amplitude * 2 * (t * frequency % 1) - amplitude
        # generate square wave
        if (self.bid >= 20):
            t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
            wave = amplitude * np.sign(np.sin(2 * np.pi * frequency * t))

        return wave

        def play(self):
            #play sound using pyaudio in separate thread
            stream = audio.open(format=pyaudio.paFloat32,
                                channels=1,
                                rate=44100,
                                output=True)
            stream.write(self.getWave().astype(np.float32).tobytes())
            stream.stop_stream()
            stream.close()
            self.disable()
