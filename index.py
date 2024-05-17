import cv2
import json
import numpy as np
import os 

def get_mask_and_vis(image_path, label_file_path):
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