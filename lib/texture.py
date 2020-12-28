import os, sys, json, re
import shutil
import requests, urllib
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import imageio 
import scipy.ndimage
import scipy.misc
import numpy as np
import logging
import tempfile

class Tex():
    """

    A container class for Textures. 
    Additionally exposes capabilities
        - fetch or download image files from the internet based on a user provided JSON file 
        - defaults for major solar system objects 
        - image processing functions for auto-generation of height (bump) maps, normal maps, and specular maps for realistic rendering of solar system objects 
            - height maps are used for surface displacement 
            - normal maps & specular maps are used for proper lighting/reflection of object surfaces for more realistic lighting effects 

    Class Attributes
    ------------------

    Instance Attributes
    --------------------
    default_textures: str
        An absolute (or relative with respect to APP_HOME) path pointing to a JSON format file, of structure ...
        {
            'englishName': {
                'albedo': 'url|filepath',
                'height': 'url|filepath|auto',
                'specular': 'url|filepath|auto'
                },
                ...
        }
    default_path: str 
    
    Class Methods
    --------------
    @mkdir(path: str)
        Creates a directory (used for storing texture data, this is run by default when a Tex object is created)
    @show(item: str)
        Opens the image in the default system application
    @is_url(item)
        Returns True if provided value is web URL like
    @is_local(item)
        Returns True if the provided value is a local file
    @imageread(path)
        Reads path to image and returns image data (np array)
    @smooth_gaussian(img, sigma: float = 0.)
        Applies smooth Gaussian filter to image , `sigma` determines the amount of smoothing
    @gradient(img_smooth)
        Calculates image gradient 
    @sobel(img_smooth)
        Applies sobel filter to image gradient 
    @compute_normal_map(gradient_x, gradient_y, intensity: float = 1.)
        Compute normal map from image gradient with intensity levels defined by `intensity`
    @normalmap(cls, img, path, smooth=0., intensity=1.)
        Top level function for deriving normal map from diffuse map (base color, or albedo)
    @depthmap(cls, img, path, shadows=88, midpoints=1, highlights=255)
        Top level function for deriving depth (height/bump) map from diffuse map (base color, or albedo)
    @specularmap(img, path, shadows=108, midpoints=1, highlights=135)
        Top level function for deriving specular map from diffuse map (base color, or albedo)

    Instance Methods
    -----------------
    getattr(texname: str, textype: str) -> str 
        Queries the texture dictionary for requested texture name, and texture type
    setattr(texname: str, textype: str,value: str)
        Update the dictionary value of requested texture name, and texture type
    ...

    """

    tempfile.mkdtemp()
    def __init__(self, default_textures: str ='./data/texture.json', default_path: str = tempfile.mkdtemp()):
        """
        Parameters
        -----------
        default_textures: str
            Provide absolute or relative path to texture.json file 
        default_path: str 
            Provide absolute or relative path to default output directory 
        """
        print(f"DEBUG: a Tex instance, dont forget to run self.fetchimages(imagetypes=['albedo']) to properly setup your texture directory")
        #load the default texture json file
        try:
            if not os.path.exists(default_path):
                os.mkdir(default_path)
            self.default_path = default_path
        except FileExistsError:
            print(f"WARNING: {default_path} already exist")

        try:
            with open(default_textures) as f:
                self.textures = json.load(f)
        except FileNotFoundError:
            print(f"WARNING: {default_textures} does not exist")

            
    def getattr(self, texname: str, textype: str) -> str:
        """
        Queries the texture dictionary for requested texture name, and texture type

        Parameters 
        -----------
        texname: str
            Texture name, eg: 'Earth', 'Moon', ...
        textype: str
            Texture type, eg: ['albedo', 'height', 'normal', 'specular']
        """
        item = self.textures[texname][textype]
        return item

    def setattr(self, texname: str, textype: str, value: str):
        """
        Update the dictionary value of requested texture name, and texture type

        Parameters 
        -----------
        texname: str
            Texture name, eg: 'Earth', 'Moon', ...
        textype: str
            Texture type, eg: ['albedo', 'height', 'normal', 'specular']
        """
        self.textures[texname][textype] = value
        return self

    @classmethod 
    def mkdir(cls, path):
        """
        Create project output directory 

        Parameters
        -----------
        path: str
            Absolute or relative path for to be created project directory
        """
        if not os.path.exists(path):
            os.mkdir(path)        

    @classmethod
    def show(cls, item):
        """
        Display local image using system default application 

        Parameters
        -----------
        item: str
            Absolute or relative path to image file
        """
        Image.open(item).show 

    @classmethod
    def is_url(cls, item):
        """
        Determines if item is internet/web URL

        Parameters
        -----------
        item: str
            Absolute or relative path to image file
        """
        res = urllib.parse.urlparse(item)
        rgx = re.compile(r"^http(s)?")
        return True if rgx.match(res.scheme) else False 
        #if rgx.match(res.scheme):
        #    return True 
        #else:
        #    return False
    @classmethod
    def is_local(cls, item):
        """
        Determines if item is local file

        Parameters
        -----------
        item: str
            Absolute or relative path to image file
        """
        res = urllib.parse.urlparse(item)
        rgx = re.compile(r"^http(s)?")
        return False if rgx.match(res.scheme) else True
        #if  rgx.match(res.scheme):
        #    return False 
        #else: 
        #    return True
    @classmethod 
    def imageread(cls, path):
        """
        Reads path to image file and returns image data

        Parameters
        -----------
        path: str
            Absolute or relative path to image file
        """
        img = imageio.imread(path)
        return img

    @classmethod
    def smooth_gaussian(cls, img, sigma: float = 0.):
        """
        Applies smooth gaussian filter to image data

        Parameters
        -----------
        img: str
            Absolute or relative path to image file
        sigma: float
            Smoothness applied to gaussian filter
        """
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
        """
        Calculates image gradient

        Parameters
        -----------
        img_smooth: str
            Reference to image data with a smooth gaussian filter applied
        sigma: float
            Smoothness applied to gaussian filter

        Returns
        -----------
        tuple(gradient_x, gradient_y)
        """
        gradient_x = img_smooth.astype(float)
        gradient_y = img_smooth.astype(float)
        kernel = np.arange(-1,2).astype(float)
        kernel = - kernel / 2
        gradient_x = scipy.ndimage.convolve(gradient_x, kernel[np.newaxis])
        gradient_y = scipy.ndimage.convolve(gradient_y, kernel[np.newaxis].T)
        return gradient_x,gradient_y

    @classmethod    
    def sobel(cls, img_smooth):
        """
        Applies sobel across image data gradient

        Parameters
        -----------
        img_smooth: str
            Reference to image data with a smooth gaussian filter applied
        sigma: float
            Smoothness applied to gaussian filter

        Returns
        -----------
        tuple(gradient_x, gradient_y)
        """
        gradient_x = img_smooth.astype(float)
        gradient_y = img_smooth.astype(float)
        kernel = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
        gradient_x = scipy.ndimage.convolve(gradient_x, kernel)
        gradient_y = scipy.ndimage.convolve(gradient_y, kernel.T)
        return gradient_x,gradient_y

    @classmethod 
    def compute_normal_map(cls, gradient_x, gradient_y, intensity: float = 1.):
        """
        Calculate normal map for image

        Parameters
        -----------
        gradient_x: str
            Reference to image data gradient(x) component
        gradient_y: str
            Reference to image data gradient(y) component
        intensity: float
            Intensity of normal map

        Returns
        -----------
        img data (normal map)
        """
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
        """
        Top level function for deriving a normal map from base texture

        Parameters
        -----------
        img: str
            Absolute or relative path to image file
        path: str
            Absolute or relative path to output directory
        smooth: str
            Smoothness of gaussian filter
        intensity: float
            Intensity of normal map

        Returns
        -----------
        img data (normal map)
        """
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
        """
        Top level function for deriving a depth map from base texture

        Parameters
        -----------
        img: str
            Absolute or relative path to image file
        path: str
            Absolute or relative path to output directory

        Returns
        -----------
        img data (depth map)
        """
        im = Image.open(img)
        im_gray = im.convert('L')
        im_depth = ImageOps.colorize(im_gray, black='black', white='white', blackpoint=shadows, whitepoint=highlights, midpoint=midpoints ) 
        im_depth.save(os.path.join(path, f"height_{os.path.basename(im.filename)}" )) 
        return os.path.join(path, f"height_{os.path.basename(im.filename)}" )

    @classmethod
    def specularmap(cls, img, path, shadows=108, midpoints=1, highlights=135):
        """
        Top level function for deriving a specular map from base texture

        Parameters
        -----------
        img: str
            Absolute or relative path to image file
        path: str
            Absolute or relative path to output directory

        Returns
        -----------
        img data (specular map)
        """
        im = Image.open(img)
        im_gray = im.convert('L')
        im_spec = ImageOps.colorize(im_gray, black='black', white='white', blackpoint=shadows, whitepoint=highlights, midpoint=midpoints ) 
        im_spec.save(os.path.join(path, f"specular_{os.path.basename(im.filename)}" )) 
        return os.path.join(path, f"specular_{os.path.basename(im.filename)}" )

    @classmethod
    def emboss(cls, img, path, invert=True): 
        """
        Top level function for deriving a specular map from base texture

        Parameters
        -----------
        img: str
            Absolute or relative path to image file
        path: str
            Absolute or relative path to output directory
        invert: bool
            If True, return inverted emboss (default: True)

        Returns
        -----------
        img data (embossed image)
        """
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
        """
        TO BE REMOVED
        """
        imageio.save(path, normal_map)

    def fetchitem(self, itemname, itemtype, path):
        """
        Collects image file defined in Texture dictionary json, (from URLs or arbitrary file paths) into the project directory
            - any itemname.itemtype can be a URL (eg: http://domain.com/path/to/file.jpg)
            - any itemname.itemtype can be an absolute or relative file path (eg: /Users/photon/Downloads/earth.jpg)
            - files are collected into a singular destination (Tex.default_path), regargless of their source location
            
        Parameters
        -----------
        img: str
            Absolute or relative path to image file
        path: str
            Absolute or relative path to output directory
        invert: bool
            If True, return inverted emboss (default: True)

        Returns
        -----------
        img data (embossed image)
        """
        item = self.textures[itemname][itemtype]
        if item == 'auto':
            albedo = self.textures[itemname]['albedo']
            if itemtype == 'height':
               self.textures[itemname][itemtype] = self.__class__.depthmap(albedo, path)
               return self.textures[itemname][itemtype] 
            if itemtype == 'specular':
                self.textures[itemname][itemtype] = self.__class__.specularmap(albedo, path)
                return self.textures[itemname][itemtype] 
            if itemtype == 'normal':
                self.textures[itemname][itemtype] = self.__class__.normalmap(albedo, path)
                return self.textures[itemname][itemtype] 

        if self.__class__.is_local(item):
            if os.path.exists(item):
                fname = os.path.join(path, os.path.basename(item))
                if fname == item: 
                    print(f"WARNING: we have already copied {fname}, moving along..")
                    return True
                shutil.copyfile(item, fname)
                self.textures[itemname][itemtype] = fname
                return self.textures[itemname][itemtype]
            else: 
                print(f"WARNING: the file {item} does not exist") 
        if self.__class__.is_url(item):
            r = requests.get(item, allow_redirects=True)
            fname = os.path.basename(r.url)
            with open(f"{path}/{fname}", "wb") as f:
                f.write(r.content)
            self.textures[itemname][itemtype] = f.name
            return self.textures[itemname][itemtype]

    # organizes the various images user selects into one folder
    def fetchitems(self, path, itemnames=[], itemtypes=['albedo']):
        """
        Collects image files defined in Texture dictionary json, (from URLs or arbitrary file paths) into the project directory
            - any itemname.itemtype can be a URL (eg: http://domain.com/path/to/file.jpg)
            - any itemname.itemtype can be an absolute or relative file path (eg: /Users/photon/Downloads/earth.jpg)
            - files are collected into a singular destination (Tex.default_path), regargless of their source location
            
        Parameters
        -----------
        img: str
            Absolute or relative path to image file
        path: str
            Absolute or relative path to output directory
        invert: bool
            If True, return inverted emboss (default: True)

        Returns
        -----------
        img data (embossed image)
        """
        items = itemnames if len(itemnames) > 0 else self.textures.keys()
        for itemname in items:
            types = itemtypes if len(itemtypes) > 0 else self.textures[itemname].keys()
            for itemtype in types:
                item = self.textures[itemname][itemtype]
                print(f"INFO: the item value is: {item}")
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