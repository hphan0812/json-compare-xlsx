import os
import pandas as pd
import glob

def filter_images(img_folder):
    """
    Filter images based on their labels.

    This function takes an image folder path as input and filters the images based on their corresponding labels.
    It returns two lists: ok_images_list and ng_images_list.
    - ok_images_list contains the names of images that have no corresponding label.
    - ng_images_list contains the names of images that have a corresponding label.

    Args:
        img_folder (str): The path to the image folder.

    Returns:
        tuple: A tuple containing two lists: ok_images_list and ng_images_list.
    """
    ref_dir = img_folder
    image_path_list = glob.glob(os.path.join(ref_dir, "**/*.bmp"), recursive=True)
    label_path_list = glob.glob(os.path.join(ref_dir, "**/*.json"), recursive=True)
    image_name_list = [os.path.splitext(os.path.basename(image_path))[0] for image_path in image_path_list]
    label_name_list = [os.path.splitext(os.path.basename(label_path))[0] for label_path in label_path_list]
    ok_images_list = [x for x in image_name_list if x not in label_name_list]
    ng_images_list = [x for x in image_name_list if x in label_name_list]
    return ok_images_list, ng_images_list


def compare_image_folders(folders):
    """
    Compare the images in the given folders and generate a comparison result in an Excel file.

    Parameters:
    folders (list): A list of folder paths containing the images to be compared.
    """
    data = []
    
    for folder in folders:
        if not os.path.isdir(folder):
            print(f"Directory does not exist: {folder}")
            continue

        ok_images, ng_images = filter_images(folder)
        
        for file in ok_images + ng_images:
            status = "ng" if file in ng_images else "ok"
            data.append([file, folder, status])
    
    df = pd.DataFrame(data, columns=["Image", "Folder", "Status"])
    
    # Pivot the DataFrame to have folders as columns and fill missing values with "Missing"
    df_pivot = df.pivot(index="Image", columns="Folder", values="Status").fillna("Missing")
    
    # Add a "Result" column that shows "Match" if all statuses are the same, "Conflict" otherwise
    df_pivot["Result"] = df_pivot.apply(lambda row: "Conflict" if len(set(row)) > 1 else "", axis=1)
    
    # Filter the DataFrame to keep only rows with "Conflict" in the "Result" column
    df_pivot_conflict = df_pivot[df_pivot["Result"] == "Conflict"]
    
    df_pivot_conflict.to_excel("comparison_result.xlsx")
    
if __name__=="__main__":
    folder1 = os.path.abspath("Label")
    folder2 = os.path.abspath("Label_2")
    folder3 = os.path.abspath("Label_3")
    folders = [folder1, folder2, folder3]
    compare_image_folders(folders)