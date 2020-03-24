"""
Save on PDF size by downsampling images

These processes are done in this file
"""
from PIL import Image
import os

# Enable large images being processed
Image.MAX_IMAGE_PIXELS = None

def load_image(img_path):
    """
    Reads image and returns a PIL instance

    @param img_path: The path to load the image from
    """
    return Image.open(img_path)

def resize(img, largest_size=(800, 800), dimension_override=-1, sampling=Image.ANTIALIAS):
    """
    Resizes an image to the smaller dimension of largest_size if the same dimension of the image is greater.
    This makes the assumption that usually images have aspect ratios which arent too far from 50%.

    If dimension_override is set to a particular dimension (0 or 1) 
    then that dimension is used instead of the above criteria

    Image is resized, maintaining the aspect ratio.
    
    Antialiasing is by default enabled because this is commonly used for images which are viewed, 
    not algorithmically processed (e.g. segmentation masks)

    @param img: the image to apply resizing too
    @param largest_size: The largest allowed size in pixels, as a 2-tuple: (width, height).
    @param sampling: the sampling to use during resizing. This can be one of PIL.Image.NEAREST (use nearest neighbour),
                                                            PIL.Image.BILINEAR (linear interpolation), 
                                                            PIL.Image.BICUBIC (cubic spline interpolation), or 
                                                            PIL.Image.LANCZOS (a high-quality downsampling filter). 
                                                            If omitted, or if the image has mode “1” or “P”, it is set PIL.Image.NEAREST.
    @param dimension_override: Force the function to be applied to a certain dimension. Default: disabled (-1)
    @return a copy of the image resized
    """
    
    if dimension_override >= 0 and dimension_override <=1:
        resize_idx = dimension_override
    else: # Resize to the smaller of the dimensions
        if largest_size[0] >= largest_size[1]:
            resize_idx = 0
        else:
            resize_idx = 1
    
    img_size = img.size
    if img_size[resize_idx] > largest_size[resize_idx]:
        new_size = [0, 0]
        new_size[resize_idx] = largest_size[resize_idx]
        ratio = float(largest_size[resize_idx]) / float(img_size[resize_idx])
        other_idx = not(resize_idx)
        new_size[other_idx] = round(img_size[other_idx] * ratio)

        resized_img = img.resize(new_size, sampling)
    else:
        # return a copy to maintain that it is a copy not the same object
        resized_img = img.copy()

    return resized_img

def save_compressed(img, img_path, quality=80, optimize=True):
    """
    Saves an image using compression to reduce file size
    Supports: JPG and PNG files. maybe some others?

    @param img the Image to compress
    @param img_path: The path to save the image at
    @param quality: Quality parameter between 0 and 100. Default: 80
    @param optimize: Engage optimisation or not. Default: True
    """
    img.save(img_path, quality=quality,optimize=optimize)

def alpha_to_color(image, color=(255, 255, 255)):
    """Alpha composite an RGBA Image with a specified color.

    Source: http://stackoverflow.com/a/9459208/284318

    Keyword Arguments:
    image -- PIL RGBA Image object
    color -- Tuple r, g, b (default 255, 255, 255)

    """
    image.load()  # needed for split()
    background = Image.new('RGB', image.size, color)
    background.paste(image, mask=image.split()[3])  # 3 is the alpha channel
    return background

def convert_to_jpg(img_path):
    """
    Checks if an image is in the jpg format, if not converts it to jpg to save space

    @param img_path: the path to the image
    @return the new image path
    """
    if not os.path.splitext(img_path)[-1].lower() in ['.jpg', '.jpeg']:
        img = load_image(img_path)
        if len(img.split()) >= 4:
            img = alpha_to_color(img)
        img_path = img_path.replace(os.path.splitext(img_path)[-1], '.jpg')
        img.save(img_path)
    
    return img_path

if __name__ == '__main__':
    img_path = '/home/daniel/random/texTools/synthetic_overView.png'
    # img_path = '/home/daniel/random/texTools/plant00000_label.png'
    s_path = img_path.replace('.png', '-clean.png')


    img = load_image(img_path)
    print(img.size)
    resized_img = resize(img)
    print(resized_img.size)

    save_compressed(resized_img, s_path)
