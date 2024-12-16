import cv2
import numpy as np
import pygame
import pyaudio
from block import Block

class Main:

    def main():

        pygame.init()
        clock = pygame.time.Clock()
        fps = 60
        bpm = 120
        sweep = 0

        audio = pyaudio.PyAudio()

        capture = cv2.VideoCapture(0)
        canvas = pygame.display.set_mode((1024, 600))

        width = capture.get(cv2.CAP_PROP_FRAME_WIDTH )
        height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT )
        print("Size: ", width, height)

        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        parameters = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

        pygame.display.set_caption("BeatSketch") 
        exit = False
        
        try:
            while not exit:
                for event in pygame.event.get(): 
                    if event.type == pygame.QUIT: 
                        exit = True

                sweep += 1024/((60/bpm)*fps);
                if sweep >= 1024:
                    sweep = 0
                
                ret, frame = capture.read()
                if not ret:
                    print("error capturing frame")
                    break
                grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                corners, ids, _ = detector.detectMarkers(grayscale)
                blocks = []
                for i in range(0, 30):
                    block = Block(i, False, 0, 0, 0)
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

                        cX = int(1024-((topLeft[0] + bottomRight[0])*1024/width/2))
                        cY = int((topLeft[1] + bottomRight[1])*600/height/2)

                        vector = np.array(topRight) - np.array(topLeft)
                        angle = np.arctan2(vector[1], vector[0])

                        angle_degrees = np.degrees(angle)
                        if angle_degrees < 0:
                            angle_degrees += 360

                        print("Marker ID: ", marker_id)
                        print(blocks)
                        for block in blocks:
                            print(f"Block ID: {block.getID()}")
                            if np.int32(block.getID()) == np.int32(marker_id):
                                block.setLocation(cX, cY, angle_degrees)
                                block.setPresent(True)
                                print("BLOCKus")
                                if sweep > cX and sweep < cX+power:
                                    block.enable()

                        print(f"Marker ID: {marker_id}")
                        print(f"Location: X={cX}, Y={cY}")
                        print(f"Z Rotation: {angle_degrees:.2f} degrees")
                        print('---')
                        power = 1024*(2**(angle_degrees*4/360))/16
                            
                pygame.draw.rect(canvas, (255, 255, 255), (sweep, 0, 2, 600))
                for block in blocks:
                    if block.getPresent():
                        pygame.draw.rect(canvas, block.getColor(), block.getRect())
                        print("BLOCK")
                        # play sound using pyaudio
                        if block.getEnabled():
                            stream = audio.open(format=pyaudio.paFloat32,
                                                channels=1,
                                                rate=44100,
                                                output=True)
                            stream.write(block.getWave().astype(np.float32).tobytes())
                            stream.stop_stream()
                            stream.close()
                            block.disable()


                font = pygame.font.SysFont(None, 24)
                bpm_text = "BPM: " + str(bpm)
                img = font.render(bpm_text, True, (125,125,125))
                canvas.blit(img, (20, 20))

                pygame.display.update()
                #print(sweep)
                canvas.fill((0, 0, 0))
                blocks.clear()
                clock.tick(fps)

        except KeyboardInterrupt:
            pass

    if __name__ == "__main__":
        main()