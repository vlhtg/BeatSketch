import numpy as np

class Block:
    def __init__ (self, bid, present, x, y, angle):
        self.bid = bid
        self.present = present
        self.x = x
        self.y = y
        self.angle = angle
    
    def setLocation(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def setPresent(self, present):
        self.present = present

    def getRect(self):
        return (self.x, self.y, 100, 100)
    
    def getColor(self):
        if (self.id < 10):
            return (255, 0, 0)
        if (self.id >= 10 and self.id < 20):
            return (0, 255, 0)
        if (self.id >= 20):
            return (0, 0, 255)
    
    def slider_to_frequency(self, slider_position, f_min=20, f_max=20000, slider_range=600):
        octaves = np.log2(f_max / f_min)
        r = slider_range / octaves
        return f_min * (2 ** (slider_position / r))
    
    def getWave(self):
        
        sample_rate = 44100
        amplitude = 0.5
        duration = self.bid
        frequency = self.slider_to_frequency(self.y)

        # generate sine wave
        if (id < 10):
            t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
            wave = amplitude * np.sin(2 * np.pi * frequency * t)
        # generate sawtooth wave
        if (id >= 10 and id < 20):
            t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
            wave = amplitude * 2 * (t * frequency % 1) - amplitude
        # generate square wave
        if (id >= 20):
            t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
            wave = amplitude * np.sign(np.sin(2 * np.pi * frequency * t))

        return wave
