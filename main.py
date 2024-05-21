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


def compare_image_folders(folder1, folder2):
    """
    Compare two folders containing images and create a result table of their differences.

    Parameters:
        folder1 (str): The path to folder 1 containing images.
        folder2 (str): The path to folder 2 containing images.

    """
    data = []
    
    # Get the parent folder names to use as column headers
    folder1_name = os.path.basename(os.path.normpath(folder1))
    folder2_name = os.path.basename(os.path.normpath(folder2))
    
    # Get the list of subfolders in folder1 and folder2
    subfolders1 = sorted([d for d in os.listdir(folder1) if os.path.isdir(os.path.join(folder1, d))])
    subfolders2 = sorted([d for d in os.listdir(folder2) if os.path.isdir(os.path.join(folder2, d))])

    common_subfolders = set(subfolders1).intersection(set(subfolders2))
    
    for subfolder in common_subfolders:
        path1 = os.path.join(folder1, subfolder)
        path2 = os.path.join(folder2, subfolder)
        
        files1 = sorted(os.listdir(path1))
        files2 = sorted(os.listdir(path2))
        
        all_files = set(files1).union(set(files2))
        
        for file in all_files:
            status1 = "ng" if file in files1 else "ok"
            status2 = "ng" if file in files2 else "ok"
            
            if status1 != status2:
                data.append([file, status1, folder1_name])
                data.append([file, status2, folder2_name])
    
    # Convert data to DataFrame and pivot
    df = pd.DataFrame(data, columns=["Image", "Status", "Folder"])
    df_pivot = df.pivot(index="Image", columns="Folder", values="Status").fillna("Missing")
    
    # Add a "Result" column to determine "Conflict"
    df_pivot["Result"] = df_pivot.apply(lambda row: "Conflict" if len(set(row)) > 1 else "", axis=1)
    
    # Filter rows with "Conflict" in the "Result" column
    df_pivot_conflict = df_pivot[df_pivot["Result"] == "Conflict"]
    
    # Export DataFrame to Excel file
    df_pivot_conflict.to_excel("comparison_result.xlsx", sheet_name="Conflict_Results")

if __name__=="__main__":
    folder1 = os.path.abspath("Labelled_Hanh")
    folder2 = os.path.abspath("Labelled_Minh")
    compare_image_folders(folder1, folder2)