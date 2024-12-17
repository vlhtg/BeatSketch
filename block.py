import numpy as np
import pyaudio
import threading

class Block:
    def __init__ (self, bid, present, x, y, angle, audioObj):
        self.bid = bid
        self.present = present
        self.x = x
        self.y = y
        
        self.angle = angle
        self.audioObj = audioObj

    def getID(self):
        return self.bid
    
    def setLocation(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def setPresent(self, present):
        self.present = present

    def getPresent(self):
        return self.present

    def getRect(self):
        power = 1024*(2**(self.angle*4/360))/16
        return (self.x, self.y, power, 15)
    
    def getX(self):
        return self.x
    
    def getColor(self):
        if (self.bid < 10):
            return (255, 0, 0)
        if (self.bid >= 10 and self.bid < 20):
            return (0, 255, 0)
        if (self.bid >= 20):
            return (0, 0, 255)
    
    def __slider_to_frequency(self, slider_position, f_min=523, f_max=523*2, slider_range=570):
        slider_position = slider_range - slider_position
        octaves = np.log2(f_max / f_min)
        r = slider_range / octaves
        return f_min * (2 ** (slider_position / r))
    
    
    def getWave(self, bps):
        
        sample_rate = 44100
        amplitude = 0.5
        power = (2**(self.angle*4/360))/16
        maxPower = (1024-self.x)/float(1024)
        power = min(power, maxPower)
        duration = power/bps
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

    def play(self, bps):

        def play_wave():
            stream = self.audioObj.open(format=pyaudio.paFloat32,
                                        channels=1,
                                        rate=44100,
                                        output=True)
            stream.write(self.getWave(bps).astype(np.float32).tobytes())
            stream.stop_stream()
            stream.close()

        play_thread = threading.Thread(target=play_wave)
        play_thread.start()