import cv2
import json
import numpy as np
import os


def get_mask_and_vis(image_path, label_file_path):
    """
    Get the mask and visualize the image.

    This function takes in the path of an image and the path of a label file. 
    
    It reads the image using OpenCV and loads the label data from the JSON file. 
    
    It then creates a mask based on the contours in the label data and draws the contours on the image. 
    
    The function returns the mask and the modified image.

    Args:
        image_path (str): The path of the image file.
        label_file_path (str): The path of the label file.

    Returns:
        tuple: A tuple containing the mask (numpy.ndarray) and the modified image (numpy.ndarray).
            - The mask is a binary image with the same dimensions as the input image. 
              It represents the areas covered by the contours.
            - The modified image is the input image with the contours drawn on it.
    """
    try:
        defect_img = cv2.imread(image_path)
        with open(label_file_path, 'r') as file:
            data = json.load(file)
        mask = np.zeros((defect_img.shape[0], defect_img.shape[1]), dtype=np.uint8)
        defect_data = data["shapes"]
        for defect_cnts in defect_data:
            contours = defect_cnts["points"]
            contours = np.array([contours], dtype=np.int32)
            # Create a mask for the contours
            # Draw contours on the mask
            cv2.drawContours(mask, contours, -1, 255, thickness=cv2.FILLED)
            cv2.drawContours(defect_img, contours, -1, (0, 0, 255), thickness=1)
        return mask, defect_img
    except:
        return None, None
    
if __name__=="__main__":
    defect_img_path="" #Image's path
    defect_label_path="" #Label's path
    save_mask_dir="" #Saving visualize image directory's path
    mask, vis_img = get_mask_and_vis(defect_img_path, defect_label_path)
    cv2.imwrite(os.path.join(save_mask_dir, os.path.basename(defect_img_path)), mask)