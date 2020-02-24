
from PIL import Image as im
import matplotlib.pyplot as plt

def clip(postdict):
    # Open image
    # TODO: Fix the json conversion to avoid doing castings
    img = im.open(postdict['url'][1:])
    x = int(postdict['x'])
    y = int(postdict['y'])
    width = int(postdict['width'])
    height = int(postdict['height'])
    area = (x, y, x + width, y + height)
    trim = img.crop(area)
    dir = f"/static/clips/{width * height}.jpg"
    postdict['clip'] = dir
    trim.save(dir[1:])
