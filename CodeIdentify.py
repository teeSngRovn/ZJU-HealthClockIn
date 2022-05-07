import os
import sys
import ddddocr
import cv

class imgobj(object):
    def __init__(self, filename):
        self.filename = filename
        self.img_bytes = self.loadfile()
        self.res = self.CodeVerify()

    def loadfile(self):
        picpath = os.path.dirname(__file__)+"\\Pics\\"+ self.filename
        with open(picpath,"rb") as f:
            img_bytes = f.read()
        return img_bytes

    def CodeVerify(self, *img_bytes):
        ocr = ddddocr.DdddOcr()
        return ocr.classification(self.img_bytes) if (len(img_bytes)==0) else ocr.classification(img_bytes)
