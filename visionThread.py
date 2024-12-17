import cv2
from block import Block
import numpy as np
from helpers import Helpers as h
import threading

class VisionThread:

    blocks = []

    def cvinit(self):
        capture = cv2.VideoCapture(1)
        # set resolution to 720p
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        width = capture.get(cv2.CAP_PROP_FRAME_WIDTH )
        height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        height = height/2
        width = width/2
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        parameters = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
        return capture, detector

    def loop(self, capture, detector):
        ret, frame = capture.read()
        if not ret:
            print("error capturing frame")
        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # quarter resolution
        grayscale = cv2.resize(grayscale, (int(960), int(540)))
        # rotate 180 degrees
        grayscale = cv2.rotate(grayscale, cv2.ROTATE_180)

        corners, ids, _ = detector.detectMarkers(grayscale)
        blocks = []
        for i in range(0, 30):
            block = Block(i, False, 0, 0, 0, self.audio)
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
        self.blocks = blocks


    def action(self):
        capture, detector = self.cvinit()
        while True:
            self.loop(capture, detector)

    def getBlocks(self):
        return self.blocks

    def __init__(self, audio):
        # create a new thread
        self.audio = audio
        self.thread = threading.Thread(target=self.action)
        # start the thread
        self.thread.start()
