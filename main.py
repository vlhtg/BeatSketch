import cv2
import numpy as np
import pygame
import pyaudio
from block import Block
from helpers import Helpers as h

class Main:

    

    def main():

        pygame.init()
        clock = pygame.time.Clock()
        fps = 20
        bpm = 120
        sweep = 0
        seconds_per_pixel = 0.01

        audio = pyaudio.PyAudio()

        capture = cv2.VideoCapture(1)
        # set resolution to 720p
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


        canvas = pygame.display.set_mode((1024, 570))

        width = capture.get(cv2.CAP_PROP_FRAME_WIDTH )
        height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        height = height/2
        width = width/2
        frameNum = int(0)

        print("Size: ", width, height)

        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        parameters = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

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

                ret, frame = capture.read()
                if not ret:
                    print("error capturing frame")
                    break
                grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # quarter resolution
                grayscale = cv2.resize(grayscale, (int(width), int(height)))
                # rotate 180 degrees
                grayscale = cv2.rotate(grayscale, cv2.ROTATE_180)

                corners, ids, _ = detector.detectMarkers(grayscale)
                blocks = []
                for i in range(0, 30):
                    block = Block(i, False, 0, 0, 0, audio)
                    blocks.append(block)

                if ids is not None:
                    ids = ids.flatten()

                    for marker_corners, marker_id in zip(corners, ids):
                        corners = marker_corners.reshape((4, 2))
                        (topLeft, topRight, bottomRight, bottomLeft) = corners

                        topLeft = (int(topLeft[0]), int(topLeft[1]))
                        topRight = (int(topRight[0]), int(topRight[1]))
                        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))

                        cX = int(((topLeft[0] + bottomRight[0])/2))
                        cY = int((topLeft[1] + bottomRight[1])/2)
                        print(f"Real Location: X={cX}, Y={cY}")

                        cX = h.map_range(cX, 55, 948, 1, 1023)
                        cY = h.map_range(cY, 60, 525, 1, 569)

                        vector = np.array(topRight) - np.array(topLeft)
                        angle = np.arctan2(vector[1], vector[0])

                        angle_degrees = np.degrees(angle)
                        if angle_degrees < 0:
                            angle_degrees += 360

                        # print("Marker ID: ", marker_id)
                        # print(blocks)
                        for block in blocks:
                            # print(f"Block ID: {block.getID()}")
                            if np.int32(block.getID()) == np.int32(marker_id):
                                block.setLocation(cX, cY, angle_degrees)
                                block.setPresent(True)

                        # print(f"Marker ID: {marker_id}")
                        # print(f"Location: X={cX}, Y={cY}")
                        # print(f"Z Rotation: {angle_degrees:.2f} degrees")
                        # print('---')
                frameNum = frameNum + 1
                            
                # draw sweep line
                pygame.draw.rect(canvas, (255, 255, 255), (sweep, 0, 2, 600))

                # draw blocks
                if blocks is None:
                    print("No blocks")
                for block in blocks:
                    if block.getPresent():
                        print(f"Block ID: {block.getID()}")
                        print(frameNum)
                        pygame.draw.rect(canvas, block.getColor(), block.getRect())
                        # play sound using pyaudio
                        if sweep >= block.getY() and block.getID() not in playedIds:
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
                blocks.clear()

                # draw quarter lines
                for i in range(1, 4):
                    pygame.draw.line(canvas, (50, 50, 50), (i*256, 0), (i*256, 570), 2)
                clock.tick(fps)

        except KeyboardInterrupt:
            pass

    if __name__ == "__main__":
        main()