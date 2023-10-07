'''
Created on 22.02.2020

@author: santnerp
'''

import os, shutil, re
from PIL import ExifTags, Image
import csv
from datetime import datetime

class ImageMove(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def iter_all_files(self, path):
        for root, _, files in os.walk(path):
            for filename in files:
                yield os.path.join(root, filename)
    
    def image_info(self, bilddatei):
        img = Image.open(bilddatei)
        exif_data = img._getexif()
        print(exif_data)
        for tag_id in exif_data:
            # get the tag name, instead of human unreadable tag id
            tag = ExifTags.TAGS.get(tag_id, tag_id)
            data = exif_data.get(tag_id)
            # decode bytes 
            if isinstance(data, bytes):
                data = data.decode()
            print(f"{tag:25}: {data}")
        
    def move_image_files(self, vonVerzeichnis, nachVerzeichnis, bOnlyTesting=True):
        move_list = []
        print("von: {} nach: {}".format(vonVerzeichnis, nachVerzeichnis))
        bilddateien = self.iter_all_files(vonVerzeichnis)
        for bilddatei in bilddateien:
            aufnahmedatum = self.get_data_by_attribute(bilddatei, "DateTimeOriginal")
            if aufnahmedatum != None:
                t = datetime.strptime(aufnahmedatum, "%Y:%m:%d %H:%M:%S")
                # Beispiel: P:\2022\2022-08\03
                # Jeder Tag wird extra angefuehrt:
                # ziel_verzeichnis = "{}\\{}\\{}_{}\\{}".format(nachVerzeichnis, t.year, t.year, t.strftime("%m"), t.strftime("%d"))
                # Tag wird nicht extra angefuehrt
                # Beispiel: P:\2022\2022-08
                ziel_verzeichnis = "{}\\{}\\{}-{}".format(nachVerzeichnis, t.year, t.year, t.strftime("%m"))
                #ziel_verzeichnis = "{}\\{}".format(nachVerzeichnis, t.strftime("%m"))
                if (not os.path.exists(ziel_verzeichnis)):
                    print("Verzeichnis anlegen: {}".format(ziel_verzeichnis))
                    if(not bOnlyTesting):
                        os.makedirs(ziel_verzeichnis)
                        move_list.append(['makedir', '', ziel_verzeichnis])
                if (os.path.exists(os.path.join(ziel_verzeichnis, os.path.basename(bilddatei)))):
                    print ("existiert;{};{}".format(os.path.basename(bilddatei), ziel_verzeichnis))
                    move_list.append(['exist', bilddatei,ziel_verzeichnis])
                else:
                    #print ("copy; ( {}; {} )".format(bilddatei, ziel_verzeichnis))
                    #shutil.copy(bilddatei, ziel_verzeichnis)
                    print ("move;{};{}".format(bilddatei, ziel_verzeichnis))
                    move_list.append(['move', bilddatei,ziel_verzeichnis])
                    if(not bOnlyTesting):
                        # shutil.copy(bilddatei, ziel_verzeichnis)
                        shutil.move(bilddatei, ziel_verzeichnis)
        return move_list
                
    def get_all_video_file(self, aPath):
        l = self.iter_all_files(aPath)
        videoliste = []
        for dateiname in l:
            matchObj = re.search(r'\.avi|\.AVI|\.mpg|\.mp4|\.dv', dateiname)
            if (matchObj):
                fromDir, toDir = self.analyse_destination(dateiname)
                videoliste.append(['video', fromDir, toDir])       
                # print (os.path.basename(dateiname), os.path.dirname(dateiname))
        return videoliste

    def analyse_destination(self, aFullPathName):
        cmd_list = []
        path_list = aFullPathName.split(os.sep)
        print (path_list)
        matchObj = re.search(r'^(\d\d\d\d)\D(\d\d).*$', path_list[1])
        if (matchObj):
            sub_dir = "{}-{}".format(matchObj.group(1), matchObj.group(2))
            ziel_verzeichnis = "{}\\{}\\{}".format(path_list[0], sub_dir , path_list[2])
            #print(ziel_verzeichnis)
            ziel_root = re.sub("P:", "V:", path_list[0])
            ziel_verzeichnis = "{}\\{}".format(ziel_root, sub_dir)
            if(os.path.exists(ziel_verzeichnis) == False):
                print("Zielverzeichnis nicht verfuegbar: {}".format(ziel_verzeichnis))
            return aFullPathName, ziel_verzeichnis
        else:
            print("{} nicht gefunden".format(path_list))
        return "", ""
                       
    def get_data_by_attribute(self, bilddatei, search_attrib):
        try:
            img = Image.open(bilddatei)
            exif_data = img._getexif()
            for tag_id, tag_value in ExifTags.TAGS.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
                if tag_value == search_attrib:
                    data = exif_data.get(tag_id)
                    if isinstance(data, bytes):
                        data = data.decode()
                    return data 
        except Exception:
            print("{} ist keine Bilddatei".format(bilddatei))
            return None
    
    def write_csv(self, csvfilename, list2write):
        with open(csvfilename, 'w', newline='') as csvfile:
            fieldnames = ['cmd','from', 'to']
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(fieldnames)
            for eintrag in list2write:
                writer.writerow(eintrag)

if __name__ == '__main__':
    print("starting ...")
    a = ImageMove()
    #a.move_image_files("P:\\2020\\2020-05", "C:\\Users\\santnerp\\Documents\\tmp")
    #a.image_info("P:\\2020\\2020-05\\20200515_143229.jpg")
#    a.move_image_files("P:\\Upload Peter", "P:")
#    movelist = a.move_image_files("P:\\Upload Peter\\upload", "C:\\Users\\santnerp\\Documents\\tmp")
#    movelist = a.move_image_files("C:\\Users\\santnerp\\Pictures\\2021_unsorted", "C:\\Users\\santnerp\\Pictures", False)
#    movelist = a.move_image_files("P:\\Upload Peter\\upload", "C:\\Users\\santnerp\\Pictures\\upload", False)
    #movelist = a.move_image_files("P:\\2016\\2016-08-Kalifornien", "C:\\Users\\santnerp\\Pictures\\Kalifornien", False)
    #movelist = a.move_image_files("C:\\Users\\santnerp\\Pictures\\2022\\Kalender_Hanni", "C:\\Users\\santnerp\\Pictures\\2022\\Kalender_Hanni", True)
    movelist = a.move_image_files("C:\\Users\\santnerp\\OneDrive - Magna\\Documents\\Privat\\Sicherung\\handy_20231003", "C:\\Users\\santnerp\\Bilder\\tmp", False)
    a.write_csv("movefiles_upload.csv", movelist)
    
    #myvideos = a.get_all_video_file("P:")
    #a.write_csv("videofiles.csv", myvideos)
    print("end")
       
