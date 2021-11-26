from pathlib import Path
from PIL import Image

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

if __name__=='__main__':
    # D:\\my_works\\Not_Important\\INTERVIEW-TASKS\\APSS_POC\\static\\img\\img_upload\\paşam1.jpg
    # D:\\my_works\\Not_Important\\INTERVIEW-TASKS\\APSS_POC\\static\\img\\img_upload\\paşam2.jpg
    webp_path=str(convert_to_webp(Path("D:\\my_works\\Not_Important\\INTERVIEW-TASKS\\APSS_POC\\static\\img\\img_upload\\paşam1.jpg")))
    webp_path=webp_path[webp_path.index('d\\')+2:]
    print(webp_path)