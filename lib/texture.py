import os, sys, json, re
import shutil
import requests, urllib
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import imageio 
import scipy.ndimage
import scipy.misc
import numpy as np


class Tex():

    def __init__(self, default_textures='./data/texture.json', data_path='./data'):
        print(f"DEBUG: loaded a texture object, dont forget to run self.warmup() to properly setup your texture directory")
        #load the default texture json file
        with open(default_textures) as f:
            self.textures = json.load(f)

    def getattr(self, texname, textype):
        item = self.textures[texname][textype]
        return item

    def setattr(self, texname, textype, value):
        self.textures[texname][textype] = value
        return self


    @classmethod
    def is_url(cls, item):
        res = urllib.parse.urlparse(item)
        rgx = re.compile(r"^http(s)?")
        return True if rgx.match(res.scheme) else False 
        #if rgx.match(res.scheme):
        #    return True 
        #else:
        #    return False
    @classmethod
    def is_local(cls, item):
        res = urllib.parse.urlparse(item)
        rgx = re.compile(r"^http(s)?")
        return False if rgx.match(res.scheme) else True
        #if  rgx.match(res.scheme):
        #    return False 
        #else: 
        #    return True
    @classmethod 
    def imageread(cls, path):
        img = imageio.imread(path)
        return img

    @classmethod
    def smooth_gaussian(cls, img, sigma: float = 0.):
        if sigma == 0:
            return img
        img_smooth = img.astype(float)
        kernel_x = np.arange(-3*sigma,3*sigma+1).astype(float)
        kernel_x = np.exp((-(kernel_x**2))/(2*(sigma**2)))
        img_smooth = scipy.ndimage.convolve(img_smooth, kernel_x[np.newaxis])
        img_smooth = scipy.ndimage.convolve(img_smooth, kernel_x[np.newaxis].T)
        return img_smooth 
    
    @classmethod
    def gradient(cls, img_smooth):
        gradient_x = img_smooth.astype(float)
        gradient_y = img_smooth.astype(float)
        kernel = np.arange(-1,2).astype(float)
        kernel = - kernel / 2
        gradient_x = scipy.ndimage.convolve(gradient_x, kernel[np.newaxis])
        gradient_y = scipy.ndimage.convolve(gradient_y, kernel[np.newaxis].T)
        return gradient_x,gradient_y

    @classmethod    
    def sobel(cls, img_smooth):
        gradient_x = img_smooth.astype(float)
        gradient_y = img_smooth.astype(float)
        kernel = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
        gradient_x = scipy.ndimage.convolve(gradient_x, kernel)
        gradient_y = scipy.ndimage.convolve(gradient_y, kernel.T)
        return gradient_x,gradient_y

    @classmethod 
    def compute_normal_map(cls, gradient_x, gradient_y, intensity: float = 1.):
        width = gradient_x.shape[1]
        height = gradient_x.shape[0]
        max_x = np.max(gradient_x)
        max_y = np.max(gradient_y)
        max_value = max_x
        if max_y > max_x:
            max_value = max_y
        normal_map = np.zeros((height, width, 3), dtype=np.float32)
        intensity = 1 / intensity
        strength = max_value / (max_value * intensity)
        normal_map[..., 0] = gradient_x / max_value
        normal_map[..., 1] = gradient_y / max_value
        normal_map[..., 2] = 1 / strength
        norm = np.sqrt(np.power(normal_map[..., 0], 2) + np.power(normal_map[..., 1], 2) + np.power(normal_map[..., 2], 2))
        normal_map[..., 0] /= norm
        normal_map[..., 1] /= norm
        normal_map[..., 2] /= norm
        normal_map *= 0.5
        normal_map += 0.5
        return normal_map

    @classmethod 
    def normalmap(cls, img, path, smooth=0., intensity=1.):
        im = cls.imageread(img)
        filename = f"normal_{os.path.basename(img)}"
        print(filename)
        filepath = os.path.join(path, filename)
        print(filepath)
        #convert to gray scale if not gray already
        if im.ndim == 3:
            im_grey = np.zeros((im.shape[0],im.shape[1])).astype(float)
            im_grey = (im[...,0] * 0.3 + im[...,1] * 0.6 + im[...,2] * 0.1)
            im = im_grey
        
        im_smooth = cls.smooth_gaussian(im, smooth)
        sobel_x, sobel_y = cls.sobel(im_smooth)
        normal_map = cls.compute_normal_map(sobel_x, sobel_y, intensity)
        imageio.imsave(filepath, normal_map)
        return filepath

    @classmethod
    def depthmap(cls, img, path, shadows=88, midpoints=1, highlights=255):
        im = Image.open(img)
        im_gray = im.convert('L')
        im_depth = ImageOps.colorize(im_gray, black='black', white='white', blackpoint=shadows, whitepoint=highlights, midpoint=midpoints ) 
        im_depth.save(os.path.join(path, f"height_{os.path.basename(im.filename)}" )) 
        return os.path.join(path, f"height_{os.path.basename(im.filename)}" )

    @classmethod
    def specularmap(cls, img, path, shadows=108, midpoints=1, highlights=135):
        im = Image.open(img)
        im_gray = im.convert('L')
        im_spec = ImageOps.colorize(im_gray, black='black', white='white', blackpoint=shadows, whitepoint=highlights, midpoint=midpoints ) 
        im_spec.save(os.path.join(path, f"specular_{os.path.basename(im.filename)}" )) 
        return os.path.join(path, f"specular_{os.path.basename(im.filename)}" )

    @classmethod
    def emboss(cls, img, path, invert=True): 
        im = Image.open(img)
        im_gray = im.convert('L')
        if invert:
            im_emboss = ImageOps.invert(im_gray.filter(ImageFilter.EMBOSS))
        else:
            im_emboss = im_gray.filter(ImageFilter.EMBOSS)
        im_emboss.save(os.path.join(path, f"embossed_{os.path.basename(im.filename)}" ))
        return im_emboss 

    @classmethod
    def save_normal_map(cls, normal_map, path):
        imageio.save(path, normal_map)

    def fetchitem(self, itemname, itemtype, path):
        item = self.textures[itemname][itemtype]
        if self.__class__.is_local(item):
            if os.path.exists(item):
                fname = os.path.join(path, os.path.basename(item))
                if fname == item: 
                    print(f"WARNING: we have already copied {fname}, moving along..")
                    return True
                shutil.copyfile(item, fname)
                self.textures[itemname][itemtype] = fname
            else: 
                print(f"WARNING: the file {item} does not exist") 
        if self.__class__.is_url(item):
            r = requests.get(item, allow_redirects=True)
            fname = os.path.basename(r.url)
            with open(f"{path}/{fname}", "wb") as f:
                f.write(r.content)
            self.textures[itemname][itemtype] = f.name

    # organizes the various images user selects into one folder
    def fetchitems(self, path, itemnames=['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune'], itemtypes=['albedo']):
        for itemname in itemnames:
            for itemtype in itemtypes:
                item = self.textures[itemname][itemtype]
                print(f"item value is: {item}")
                if item == 'auto':
                    #we need to generate a texture for the user. this will be done from the items albedo key 
                    # we should ensure the albedo key has a usable value also.. and the file exists first. 
                    albedo = self.textures[itemname]['albedo']
                    #depending on the itemtype, determines what type of map we need to generate 
                    if itemtype == 'height':
                        self.textures[itemname][itemtype] = self.__class__.depthmap(albedo, path)
                        continue
                    if itemtype == 'specular':
                        self.textures[itemname][itemtype] = self.__class__.specularmap(albedo, path)
                        continue
                    if itemtype == 'normal':
                        self.textures[itemname][itemtype] = self.__class__.normalmap(albedo, path)
                        continue
                if self.__class__.is_local(item):
                    if os.path.exists(item):
                        fname = os.path.join(path, os.path.basename(item))
                        if fname == item:
                            print(f"WARNING: we already copied {fname}, moving along..")
                            continue
                        print(f"INFO: creating {fname}")
                        shutil.copyfile(item, fname)
                        self.textures[itemname][itemtype] = fname
                    else:
                        print(f"WARNING: the file {item} does not exist")
                if self.__class__.is_url(item):
                    r = requests.get(item, allow_redirects=True)
                    fname = os.path.basename(r.url)
                    with open(f"{path}/{fname}", "wb") as f:
                        f.write(r.content)
                    self.textures[itemname][itemtype] = f.name