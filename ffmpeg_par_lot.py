import os
class Media_file:

    def __init__(self,file_path):

        info_txt=os.popen("ffprobe "+file_path+" -show_streams")
        #info_txt=os.popen('ls')
        info_txt=info_txt.read()
        txt=info_txt.split('\n')
        self.codec=txt[2][11:]
        self.width=int(txt[9][6:])
        self.hieght=int(txt[10][7:])
        d=txt[15][21:].split(':')
        self.display_aspect_ratio=(int(d[0]),int(d[1]))
        f=txt[30][15:].split('/')
        self.fps=int(int(f[0])/int(f[1]))+1
        print(self.codec)
        print(self.width)
        print(self.hieght)
        print(self.display_aspect_ratio)
        print(self.fps)

    def get_fps(self):
        pass

    def get_hieght(self):
        pass

    def get_with(self):
        pass

    def get_encoding(self):
        pass

compress_folder_name="./777 Compressed Files"

Img_extention=[".jpg",".png",".bmp"]
Vid_extention=[".mp4",".wav",".3gp"]

def files_to_compresse_as_path_name_extention():
    Files_path=[]
    for dir_path,dir_name,files_name in os.walk("."):
        os.system("mkdir \""+compress_folder_name+dir_path[1:]+"\"")
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
            os.system("ffmpeg -i \""+input_path+input_name+input_extention+"\" "+img_attributs+"\""+output_path+input_name+".jpg\"")
        elif input_extention in Vid_extention :
            print("ffmpeg -i \""+input_path+input_name+input_extention+"\" "+vid_attributs+"\""+output_path+input_name+".mp4\"")
            os.system("ffmpeg -i \""+input_path+input_name+input_extention+"\" "+vid_attributs+"\""+output_path+input_name+".mp4\"")
        else :
            os.system("cp \""+input_path+input_name+input_extention+"\" \""+output_path+"\"")

def split_name_from_extension(f):
    extention=""
    for i in range(len(f)-1,-1,-1):
        c=f[i]
        if c=='.':
            return f[:i],'.'+extention
        else :
            extention=c+extention
    return f,""

#compresse("","")
#f1=Media_file("Flock.mp4")