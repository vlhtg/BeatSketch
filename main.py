import cv2
import numpy as np
import pygame
import pyaudio
from block import Block
from helpers import Helpers as h
from visionThread import VisionThread
from time import sleep

class Main:

    def main():

        # constants
        fps = 80
        bpm = 120
        sweep = 0

        # flags and variables
        mute = False
        hold = False
        adjusting = False
        exit = False

        playedIds = []
        audioBlocks = []

        # init various objects
        pygame.init()
        clock = pygame.time.Clock()
        audio = pyaudio.PyAudio()
        vt = VisionThread(audio)
        canvas = pygame.display.set_mode((1024, 570))
        pygame.display.set_caption("BeatSketch") 
        
        # gameplay loop
        try:
            while not exit:

                # exit handling
                for event in pygame.event.get(): 
                    if event.type == pygame.QUIT: 
                        vt.finish()
                        exit = True

                # move sweep line and reset played blocks
                sweep += 1024/((60/bpm)*fps)
                if sweep >= 1024:
                    sweep = 0
                    playedIds = []
                            
                # draw sweep line
                if not mute and not adjusting:
                    pygame.draw.rect(canvas, (255, 255, 255), (sweep, 0, 2, 600))

                # get blocks
                blocks = vt.getBlocks()
                #print("screenUpdate")
                # draw blocks
                if blocks is None:
                    #print("No blocks")
                    pass

                # if we are holding, then audioBlocks do not change
                if not hold:
                    audioBlocks = blocks.copy()

                # play music blocks and draw shadow blocks
                for block in audioBlocks:
                    if block.getPresent():
                        if hold:
                            pygame.draw.rect(canvas, block.getShadowColor(), block.getRect())
                        if sweep >= int(block.getX()) and block.getID() not in playedIds and not mute and not adjusting:
                            bps = bpm/60
                            block.play(bps)
                            playedIds.append(block.getID())

                # draw music blocks
                for block in blocks:
                    if block.getPresent():
                        print(f"Block ID: {block.getID()}")
                        pygame.draw.rect(canvas, block.getColor(), block.getRect())
                        
                # draw bpm text
                font = pygame.font.SysFont(None, 24)
                bpm_text = "BPM: " + str(bpm)
                img = font.render(bpm_text, True, (125,125,125))
                canvas.blit(img, (20, 20))

                # update display
                pygame.display.update()
                # clear canvas
                canvas.fill((0, 0, 0))

                # draw quarter lines
                for i in range(1, 4):
                    pygame.draw.line(canvas, (50, 50, 50), (i*256, 0), (i*256, 570), 2)

                # key events
                hold = False
                adjusting = False
                keys=pygame.key.get_pressed()
                if keys[pygame.K_d]: # decrease bpm
                    if bpm > 50:
                        bpm -= 1
                        adjusting = True
                        sleep(0.15)
                if keys[pygame.K_c]: # increase bpm
                    if bpm < 200:
                        bpm += 1
                        adjusting = True
                        sleep(0.15)
                if keys[pygame.K_a]: # mute
                    mute = not mute
                    sleep(0.2)
                if keys[pygame.K_b]: # hold
                    hold = True
                if keys[pygame.K_ESCAPE]: # exit
                    vt.exit = True
                    sleep(0.2)
                    exit = True

                #make sure we are running at the correct fps   
                clock.tick(fps)

        except KeyboardInterrupt:
            pass

    if __name__ == "__main__":
        main()