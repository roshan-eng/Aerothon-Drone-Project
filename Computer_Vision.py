import argparse
import imutils
import cv2

# Loading the video
camera = cv2.VideoCapture("/home/roshan/Desktop/20220514_113409.mp4") # Add the file path for your video

# Keeping checking through the whole video
while True:

    # Checks to perform in current frame
    (grabbed, frame) = camera.read()
    status = "No Targets"

    # Check at end of the video
    if not grabbed:
        break

    # Convert the video to grayscale, blur it, and detect edges
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    edges = cv2.Canny(blurred, 50 , 150)

    # Create a contour map
    cnt = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = imutils.grab_contours(cnt)

    # Looping through the contours
    for c in contour:

        # Approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)

        # Select only approximately rectangular contours
        if 4 <= len(approx) <= 6:

            # Compute the bounding box and use find out the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            aspectRatio = w / float(h)

            # Compute the solidity of original contour
            area = cv2.contourArea(c)
            hullArea = cv2.contourArea(cv2.convexHull(c))
            solidity = area / float(hullArea)

            # Compute weather all fall for the condition to a near flat square target
            keepDims = w > 25 and h > 25
            keepSolidity = solidity > 0.9
            keepAspectRatio = 0.8 <= aspectRatio <= 1.2

            if keepDims and keepSolidity and keepAspectRatio:

                # Draw a bounding box and update the status
                cv2.drawContours(frame, [approx], -1, (0, 255, 0), 4)
                status = "Target found"

                # Find the center of the Target Region
                M = cv2.moments(approx)
                (cX, cY) = ( int (M["m10"] // M["m00"]), int (M["m01"] // M["m00"]) )
                (startX, endX) = ( int (cX - (w * 0.15)), int (cX + (w * 0.15)) )
                (startY, endY) = ( int (cY - (h * 0.15)), int (cY + (h * 0.15)) )
                cv2.line(frame, (startX, cY), (endX, cY), (0, 255, 0), 3)
                cv2.line(frame, (cX, startY), (cX, endY), (0, 255, 0), 3)

    # Show the status
    cv2.putText(frame, status, (20, 30), cv2.FONT_HERSHEY_PLAIN,
                2, (0, 255, 0), 2)

    # Show the frame and record if a key is pressed
    cv2.imshow("Frame", frame)
    key  = cv2.waitKey(1) & 0xFF

    # if Quit then stop the looping
    if key == ord("q"):
        break

# Clean up the Camera and close all windows
camera.release()
cv2.destroyAllWindows()
