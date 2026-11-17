from PIL import Image

def analyze_image(image_path):
    image= Image.open(image_path)

    return{
        "filename":image.filename,
        "format":image.format,
        "width":image.width,
        "height":image.height
    }