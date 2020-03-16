
from PIL import Image as im
from PIL import ImageFilter

def clip(postdict):
    img = im.open("gigavisor/"+postdict['url'][1:])
    x = postdict['x']
    y = postdict['y']
    width = postdict['width']
    height = postdict['height']
    area = (x, y, x + width, y + height)
    trim = img.crop(area)
    if postdict['filter']:
        trim = trim.convert('L')
    dir = f"/static/clips/{width * height}.jpg"
    postdict['clip'] = dir
    trim.save("gigavisor/" + dir[1:])

def filterIt(filter, img):
    if filter == 'blur':
        img = img.filter(ImageFilter.BLUR)
    elif filter == 'contour':
        img = img.filter(ImageFilter.CONTOUR)
    elif filter == 'detail':
        img = img.filter(ImageFilter.DETAIL)
    return img
