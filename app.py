import os
import pytesseract
import tkinter as tk
from PIL import Image

def main():
    while True:
        print(
        """
        [C]ustom Folder Names
        [F]older Path Set
        [P]icture Dimension Set
        [S]tart Program
        [E]xit Program""")
        key = input()
        key = key.upper()
        if (key == 'C'):
            #Custom name for folders where cropped images and OCR text files will be placed
            custom_folders = setCustomFolders()
        elif (key == 'F'):
            #The folder path you wish to traverse
            path = setFolderPath()
        elif (key == 'P'):
            #Whatever values are entered will be ignored in the cropping process in this version
            dimensions = setPictureDimesions()
        elif (key == 'S'):
            runProgram(custom_folders, path, dimensions)
        elif (key == 'E'):
            break
        else:
            print("Invalid input. Please enter a recognized character.")
            input("Press Enter to continue.")

def setCustomFolders():
    cropped_folder = input("Enter a name you would like to name the folder housing the cropped images: ")
    text_folder = input("Enter a name you would like to name the folder housing the OCR text: ")
    return (cropped_folder, text_folder)

def setFolderPath():
    return input("Enter the ABSOLUTE PATH of the root folder you would like to traverse: ")

def setPictureDimesions():
    left = input("Enter left dimension: ")
    top = input("Enter top dimension: ")
    right = input("Enter right dimension: ")
    bottom = input("Enter bottom dimension: ")
    return (left,top,right,bottom)

def runProgram(custom_folder, path, dimensions):
    print("Running...")
    createFolders(path, custom_folder)
    walkDirCrop(path,dimensions)
    walkDirOCR(path,custom_folder)


def createFolders(folder_path, custom_folder):
    print("Creating folders...")
    OCR = custom_folder[1]
    cropped_folder = custom_folder[0]

    for root, _, _ in os.walk(folder_path, topdown=False):
        #Creates filepath for OCR (custom_folder[1]) and cropped folders (custom_folder[0])
        file_path = os.path.join(root,OCR)
        #Checks if file paths already exists, if not then creates them
        if not root.endswith(custom_folder[1]) and not root.endswith(cropped_folder):
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            file_path = os.path.join(root, cropped_folder)
            if not os.path.exists(file_path):
                os.makedirs(file_path)
        else:
            print("No need to!")
    print("Done folder check!")

def walkDirCrop(folder_path,dimensions):
    for root, _, files in os.walk(folder_path, topdown=False):
        for file_name in files:
            crop(root,file_name,dimensions)

def walkDirOCR(folder_path, custom_folder):
    for root, _, files in os.walk(folder_path, topdown=False):
        if root.endswith(custom_folder[0]):
            for file_name in files:
                file_path = os.path.join(root,file_name)
                text = printOCR(file_path)
                writeToFile(file_name,text,root,custom_folder)

def printOCR(folder_path):
    print("OCR-ing...")
    print("Done!")
    return pytesseract.image_to_string(folder_path)

def writeToFile(file_name,text,root,custom_folder):
    print("Writing to file...")

    #'file.txt' becomes 'file'
    truncated_file_name = file_name[:-4]
    #No idea what this does?
    truncated_folder_name = root[:-8]
    print(truncated_file_name)
    print(truncated_folder_name)

    with open(os.path.join(truncated_folder_name, custom_folder[1], truncated_file_name + ".txt"), "w") as text_file:
        print(f"{text}", file=text_file)
    print("Done writing!")

def crop(root, file_name, dimensions):
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

# path = r"path\goes\here"
# createFolders(path)
# walkDirCrop(path)
# walkDirOCR(path)

if __name__ == "__main__":
    main()