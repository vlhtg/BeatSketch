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

        pygame.init()
        clock = pygame.time.Clock()
        fps = 80
        bpm = 120
        sweep = 0
        mute = False

        audio = pyaudio.PyAudio()

        vt = VisionThread(audio)

        canvas = pygame.display.set_mode((1024, 570))

        pygame.display.set_caption("BeatSketch") 
        exit = False
        
        playedIds = []

        try:
            while not exit:
                for event in pygame.event.get(): 
                    if event.type == pygame.QUIT: 
                        exit = True

                sweep += 1024/((60/bpm)*fps);
                if sweep >= 1024:
                    sweep = 0
                    playedIds = []
                            
                # draw sweep line
                if not mute:
                    pygame.draw.rect(canvas, (255, 255, 255), (sweep, 0, 2, 600))

                blocks = vt.getBlocks()
                print("screenUpdate")
                # draw blocks
                if blocks is None:
                    print("No blocks")
                for block in blocks:
                    if block.getPresent():
                        print(f"Block ID: {block.getID()}")
                        pygame.draw.rect(canvas, block.getColor(), block.getRect())
                        # play sound using pyaudio
                        if sweep >= int(block.getX()) and block.getID() not in playedIds and not mute:
                            bps = bpm/60
                            block.play(bps)
                            playedIds.append(block.getID())
                        
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
                
                # events = pygame.event.get()
                # for event in events:
                #     if event.type == pygame.KEYDOWN:
                #         if event.key == pygame.K_d:
                #             if bpm > 50:
                #                 bpm -= 1
                #         if event.key == pygame.K_c:
                #             if bpm < 200:
                #                 bpm += 1

                keys=pygame.key.get_pressed()
                if keys[pygame.K_d]:
                    if bpm > 50:
                        bpm -= 1
                        sleep(0.3)
                if keys[pygame.K_c]:
                    if bpm < 200:
                        bpm += 1
                        sleep(0.3)
                if keys[pygame.K_a]:
                    mute = not mute
                    sleep(0.3)
                if keys[pygame.K_ESCAPE]:
                    vt.exit = True
                    sleep(0.2)
                    exit = True
                                
                clock.tick(fps)

        except KeyboardInterrupt:
            pass

    if __name__ == "__main__":
        main()