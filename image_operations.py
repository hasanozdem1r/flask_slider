from os import path
from pathlib import Path
from PIL import Image
from shutil import move


def convert_to_webp(source):
    """
    Convert jpg, png image to WebP format.
    :param: source <(pathlib.Path)> <str> Path to source image
    :return: <pathlib.Path>  path to new image
    """
    destination = source.with_suffix(".webp")
    # Open image
    image = Image.open(source)
    # Convert image to webp
    image.save(destination, format="webp")

    return destination


# source : any
# target : D:\\my_works\\Not_Important\\INTERVIEW-TASKS\\APSS_POC\\static\\img\\img_upload
def move_converted_file(source: str, target_folder: str):
    # separate folder and file name
    head, file_name = path.split(source)
    target = f"{target_folder}/{file_name}"
    move(source, target)
    return file_name


if __name__ == '__main__':
    source="D:/ART/ART20201024_131103.jpg"
    move_converted_file(source,"D:/ART/")
