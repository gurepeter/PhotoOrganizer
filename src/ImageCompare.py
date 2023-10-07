'''
Iteriert rekursiv durch alle Verzeichnisse und schreibt die Bilder in eine Datei (duplicated_files.csv), 
falls diese oefter als 1x vorkommen

@author: Peter Santner
'''

import hashlib
import os
from collections import defaultdict
import csv

class ImageCompare(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass

    def hash_md5(self, path, blocksize=65536):
        hasher = hashlib.md5()
        with open(path, 'rb') as data:
            while True:
                buf = data.read(blocksize)
                if not buf:
                    break
                hasher.update(buf)
        return hasher.hexdigest()
    
    def generate_hashes(self, filenames):
        hashes2filenames = defaultdict(list)
        for filename in filenames:
            myhash = self.hash_md5(filename)
            hashes2filenames[myhash].append(filename)
            print(myhash, filename)
        return hashes2filenames
    
    def print_duplicates(self, hashes2filenames, CsvFile="duplicated_files.csv"):
        print("------------------ duplicates -------------------------------------------------------------------------------------------------")
        csvfilename = (CsvFile)
        with open(csvfilename, 'w', newline='') as csvfile:
            fieldnames = ['hash', 'filename', 'dir']
            writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
            writer.writeheader()
            for myhash, filenames in hashes2filenames.items():
                if len(filenames) > 1:
                    for filename in filenames:
                        print("{0:<32} {1:>1}".format(myhash, filename))
                        writer.writerow({'hash' : myhash, 'filename': os.path.basename(filename), 'dir':os.path.dirname(filename)})
    
    def iter_all_files(self, path):
        for root, _, files in os.walk(path):
            for filename in files:
                yield os.path.join(root, filename)
    
    def get_all_duplicated_images(self, aImagePath):
        hashes2filenames = self.generate_hashes(self.iter_all_files(aImagePath))
        self.print_duplicates(hashes2filenames)
             
        
if __name__ == '__main__':
    a = ImageCompare()
    a.get_all_duplicated_images("C:\\Users\\santnerp\\OneDrive - Magna\\Documents\\Privat\\Sicherung\\handy_20231003")

