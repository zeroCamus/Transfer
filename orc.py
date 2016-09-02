#!/usr/bin/env python
# coding=utf-8
import subprocess
import os

def readPic(fileName):
    p = subprocess.Popen(["tesseract", fileName+".jpg", "page"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    p.wait()
    with open("page.txt", "r") as file:
        raw_text = file.read()
        text = raw_text.replace("\n", "").replace(" ", "")
        os.rename(fileName+"jpg",text+".jpg")
        print(text)
readPic()
