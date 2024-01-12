import cv2
import numpy as np
import json

f = open("color_HSV.json")
color_dict = json.load(f)
#print(color_dict)

def get_image_pixels(image_name):   
    im = cv2.imread(image_name)
    h, w, _ = im.shape
    #print(h*w)
    return h*w

def get_contours(image_dir, color, save):
    if save.lower() == "true":
        store = True
    else:
        store = False

    # Read the image
    image = cv2.imread(image_dir)

   
    if image is None:
        print("Error: Unable to load the image.")
    else:
        # Convert BGR to HSV
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        if color=="red":
            lower = np.array(color_dict["red_low"], dtype=np.uint8)
            upper = np.array(color_dict["red_high"], dtype=np.uint8)
        if color=="green":
            lower = np.array(color_dict["green_low"], dtype=np.uint8)
            upper = np.array(color_dict["green_high"], dtype=np.uint8)
        if color=="blue":
            lower = np.array(color_dict["blue_low"], dtype=np.uint8)
            upper = np.array(color_dict["blue_high"], dtype=np.uint8)

        # Create a binary mask based on the red color threshold
        mask = cv2.inRange(hsv_image, lower, upper)

        # Optionally, apply morphological operations to clean up the mask
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Find contours in the binary mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Calculate the total area covered by contours
        total_contour_area = 0
        for contour in contours:
            total_contour_area += cv2.contourArea(contour)
        
        # Draw contours on a black background
        contours_image = np.zeros_like(image)
        cv2.drawContours(contours_image, contours, -1, (255, 255, 255), thickness=cv2.FILLED)

        # Save the image with contours to a new file
        if store:
            if color == "red":
                cv2.imwrite('image_with_red_contours.jpg', contours_image)
            if color == "green":
                cv2.imwrite('image_with_green_contours.jpg', contours_image)
            if color == "blue":
                cv2.imwrite('image_with_blue_contours.jpg', contours_image)

        return total_contour_area

def get_ratio(image, color, save):
    return (get_contours(image, color, save) / get_image_pixels(image))*100

def process_RGB(image, save):
    red_ratio = get_ratio(image, "red", save)
    green_ratio = get_ratio(image, "green", save)
    blue_ratio = get_ratio(image, "blue", save)
    return f"Red %: {red_ratio} - Green %: {green_ratio} - Blue %: {blue_ratio}"
    

