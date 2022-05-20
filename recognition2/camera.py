# import os
# import cv2
# import face_recognition
# import numpy as np
# from myfunctions import findEncodings


# class VideoCamera(object):
#     def __init__(self):
#         self.video = cv2.VideoCapture(0)

#     def __del__(self):
#         self.video.release()        

#     def get_frame(self):
#         success, frame = self.video.read()

#         # DO WHAT YOU WANT WITH TENSORFLOW / KERAS AND OPENCV
#         path = 'knownfaces'

        
#         imageNames = os.listdir(path)[1:]
#         images = []
#         knownNames = []
#         print(f"Names of images: {imageNames}")

#         # Add element in above lists
#         for imageName in imageNames:
#             curImg = cv2.imread(f'{path}/{imageName}')
#             images.append(curImg)
#             knownNames.append(os.path.splitext(imageName)[0])
#         print(f"Known people: {knownNames}")

#         # Create a list of encoded images
#         encoded_images = findEncodings(images)
#         print("Encoding Complete!")


#         # ----------

#         imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
#         imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

#         facesCurFrame = face_recognition.face_locations(imgS)
#         encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

#         for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
#             matches = face_recognition.compare_faces(encoded_images, encodeFace)
#             faceDis = face_recognition.face_distance(encoded_images, encodeFace)
#             print(f"FaceDis: {faceDis}")

#             if min(faceDis) < 0.5:
#                 matchIndex = np.argmin(faceDis)
#                 if matches[matchIndex]:
#                     name = knownNames[matchIndex].upper()
#                     print(name)

#                     # To get the location of the face in a webcam
#                     y1, x2, y2, x1 = faceLoc
#                     y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

#                     # To draw a rectangle on the image with a green color
#                     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                     cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
#                     cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
#                     # markAttendance(name)

#             else:
#                 matchIndex = np.argmin(faceDis)
#                 if matches[matchIndex]:
#                     name = "Not Found"
#                     print(name)

#                     # To get the location of the face in a webcam
#                     y1, x2, y2, x1 = faceLoc
#                     y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

#                     # To draw a rectangle on the image with a green color
#                     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                     cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
#                     cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
#                     # markAttendance(name)

#         ret, jpeg = cv2.imencode('.jpg', frame)

#         return jpeg.tobytes()