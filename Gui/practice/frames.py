import os
import time
import uuid
from itertools import cycle

import cv2

# Name and path of the video
vid_name = input("Enter the path and the name of video : ")

## Check if video exist

if (os.path.exists(vid_name)):

    # OpenCv tries to open the video 
    vidcap = cv2.VideoCapture(vid_name)

    # detects the rate
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    total_frame = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = float(total_frame) / float(fps)

    print('Frame rate per second = ' + str(fps))
    print('Total Number of frames = ' + str(total_frame))
    print('Total duration of Video in Seconds = ' + str(duration))

    Permit_capture = input("Would you like to capture frames ? Enter Y for Yes and N to exit the program .")

    if (Permit_capture == 'Y' or Permit_capture == 'y'):
        # unique name for a folder
        unique_directory_name = str(uuid.uuid4())

        # Creating a directory with unique name
        os.mkdir(unique_directory_name)
        print("Created a new directory :" + unique_directory_name)

        # Changed the directory so that all Captures
        # frames will be made

        os.chdir(unique_directory_name)

        print("Changed the file directory. ")

        # This creates the main window of an application

        start_time = time.time()

        count = 0
        success = True
        frame_num = 0

        images = []
        while success:
            success, image = vidcap.read()
            frame_num += 1
            if count % (1 * fps) == 0:
                cv2.imwrite('frame%d.png' % count, image)
                print("Frame number " + str(frame_num) + ' has been written Successfully ')
                picture = 'frame%d.png' % count
                images.append(picture)

            count += 1
            if ((frame_num == total_frame)):
                print("This Video has ended on frame number ", str(frame_num))
                break
            print("Reading Frame number: " + str(frame_num), success)
        vidcap.release()

        ## Loop through Images
        ## Display it in a window
        for image in cycle(images):
            image = cv2.imread(image)
            blue = (255, 0, 0)
            cv2.line(image, (200, 0), (200, 800), blue)
            cv2.line(image, (0, 125), (354, 125), blue)
            cv2.imshow('dark', image)

            # Pause here 1 seconds.
            w = cv2.waitKey(1000)
            if w == 27:  # escape to exit
                cv2.destroyAllWindows()
                break

        print("--- %s seconds ---" % (time.time() - start_time))

        ## Close if choose not to capture frames
    else:
        print("Closing the program. Goodbye !")
        exit()


## Exception for Incorrect video name/path
else:
    print("Video does not exist.")
