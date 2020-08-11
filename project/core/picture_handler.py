import os
from PIL import Image
from flask import url_for, current_app

def addPicture(picture,rename,folder):
    filename=picture.filename
    extType=filename.split('.')[-1]
    storageName=rename+'.'+extType

    filepath=os.path.join(current_app.root_path,'static','images',folder,storageName)
 
    pic=Image.open(picture)
    if folder=='profile_pic':
        pic.thumbnail((200,200))
    
    pic.save(filepath)
    return storageName