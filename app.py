import os
import pytesseract
from PIL import Image

def createFolders(folder_path):
    print("Creating folders...")
    for root, _, _ in os.walk(folder_path, topdown=False):
        #Creates filepath for OCR and cropped folders
        file_path = os.path.join(root,"OCR")
        #Checks if file paths already exists, if not then creates them
        if not root.endswith("OCR") and not root.endswith("cropped"):
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            file_path = os.path.join(root, "cropped")
            if not os.path.exists(file_path):
                os.makedirs(file_path)
        else:
            print("No need to!")
    print("Done folder check!")

def walkDirCrop(folder_path):
    for root, _, files in os.walk(folder_path, topdown=False):
        for file_name in files:
            crop(root,file_name)

def walkDirOCR(folder_path):
    for root, _, files in os.walk(folder_path, topdown=False):
        if root.endswith("cropped"):
            for file_name in files:
                file_path = os.path.join(root,file_name)
                text = printOCR(file_path)
                writeToFile(file_name,text,root)

def printOCR(folder_path):
    print("OCR-ing...")
    print("Done!")
    return pytesseract.image_to_string(folder_path)

def writeToFile(file_name,text,root):
    print("Writing to file...")

    #'file.txt' becomes 'file'
    truncated_file_name = file_name[:-4]
    #No idea what this does?
    truncated_folder_name = root[:-8]
    print(truncated_file_name)
    print(truncated_folder_name)

    with open(os.path.join(truncated_folder_name, "OCR", truncated_file_name + ".txt"), "w") as text_file:
        print(f"{text}", file=text_file)
    print("Done writing!")

def crop(root, file_name):
    if file_name.endswith(".jpg"):
        print("Cropping " + file_name)
        
        full_path = os.path.join(root,file_name)
        #Opens image
        image = Image.open(full_path)
        
        width, height = image.size

        #The cropping points
        left = 0
        top = width / 1000
        right = height / 1.55
        bottom = 2.99 * height / 3.85

        new_image = image.crop((left,top,right,bottom))

        file_path = os.path.join(root,"cropped",file_name)
        new_image.save(file_path)
        print("Done cropping!")

path = r"path\goes\here"
createFolders(path)
walkDirCrop(path)
walkDirOCR(path)