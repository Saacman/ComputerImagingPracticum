
from PIL import Image as im


def clip(postdict):
    img = im.open(postdict['url'][1:])
    x = postdict['x']
    y = postdict['y']
    width = postdict['width']
    height = postdict['height']
    area = (x, y, x + width, y + height)
    trim = img.crop(area)
    dir = f"/static/clips/{width * height}.jpg"
    postdict['clip'] = dir
    trim.save("gigavisor/" + dir[1:])
