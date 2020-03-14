
from PIL import Image as im


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
