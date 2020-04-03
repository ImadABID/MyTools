from os import walk
from os import system

compress_folder_name="./777 Compressed Files"

Img_extention=[".jpg",".png",".bmp"]
Vid_extention=[".mp4",".wav",".3gp"]

def files_to_compresse_as_path_name_extention():
    Files_path=[]
    for dir_path,dir_name,files_name in walk("."):
        system("mkdir \""+compress_folder_name+dir_path[1:]+"\"")
        for f in files_name:
            n,e=split_name_from_extension(f)
            Files_path+=[(dir_path+'/',n,e)]
    return Files_path

def compresse(vid_attributs,img_attributs) :
    if vid_attributs!="":
        vid_attributs+=" "
    if img_attributs!="":
        img_attributs+=" "

    Files = files_to_compresse_as_path_name_extention()

    for input_f in Files:
        input_path, input_name, input_extention = input_f
        output_path=compress_folder_name+input_path[1:]
        
        if input_extention in Img_extention :
            system("ffmpeg -i \""+input_path+input_name+input_extention+"\" "+img_attributs+"\""+output_path+input_name+".jpg\"")
        elif input_extention in Vid_extention :
            print("ffmpeg -i \""+input_path+input_name+input_extention+"\" "+vid_attributs+"\""+output_path+input_name+".mp4\"")
            system("ffmpeg -i \""+input_path+input_name+input_extention+"\" "+vid_attributs+"\""+output_path+input_name+".mp4\"")
        else :
            system("cp \""+input_path+input_name+input_extention+"\" \""+output_path+"\"")

def split_name_from_extension(f):
    extention=""
    for i in range(len(f)-1,-1,-1):
        c=f[i]
        if c=='.':
            return f[:i],'.'+extention
        else :
            extention=c+extention
    return f,""

compresse("","")