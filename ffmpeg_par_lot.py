from os import walk
from os import system

Img_extention=["jpg","png","bmp"]
Vid_extention=["mp4","wav","3gp"]

def files_to_compresse():
    Files_path=[]
    for dir_path,dir_name,files_name in walk("."):
        for f in files_name:
            Files_path+=[dir_path+'/'+f]
    return Files_path

def compresse(vid_attributs,img_attributs) :
    if vid_attributs!="":
        vid_attributs+=" "
    if img_attributs!="":
        img_attributs+=" "
        
    Files = files_to_compresse()
    system("mkdir \"compressed files\"")
    for iF in Files:
        name,extention=split_name_from_extension(iF)
        dF_name="./compressed files"+name[1:]
        if extention in Img_extention :
            system("ffmpeg -i \""+iF+"\" "+img_attributs+"\""+dF_name+".jpg\"")
        if extention in Vid_extention :
            system("ffmpeg -i \""+iF+"\" "+vid_attributs+"\""+dF_name+".mp4\"")

def split_name_from_extension(f):
    extention=""
    for i in range(len(f)-1,-1,-1):
        c=f[i]
        if c=='.':
            return f[:i],extention
        else :
            extention=c+extention
    return f,""

compresse("","")