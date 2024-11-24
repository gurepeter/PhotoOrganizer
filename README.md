# PhotoOrganizer
Verwaltung von Photos

## Duplikate finden
***get_all_duplicated_images()*** iteriert rekursiv durch alle Verzeichnisse und schreibt die Bilder in eine Datei (***duplicated_files.csv***), 
falls diese öfter als 1x vorkommen.

Implementiert mit dem Pythonscript [ImageCompare.py](src/ImageCompare.py)

```python
  if __name__ == '__main__':
      a = ImageCompare()
      a.get_all_duplicated_images("C:\\Users\\santnerp\\Bilder")
```
Duplikate findet man dann in einer CSV-Datei:

<img src='img/PhotoOrganizer_src_duplicate_duplicated_files.png'>



## Images verschieben oder kopieren

Bilder werden in ein Verzeichnis mit folgenden Format verschoben:
```
<dir>\JJJJ\JJJJ-MM\
```

```python
if __name__ == '__main__':
    print("starting ...")
    a = ImageMove()
    movelist = a.move_image_files('C:\\Users\\santnerp\\Bilder_local\\Canon\\101CANON', 'C:\\Users\\santnerp\\Bilder_local', False)
    a.write_csv("movefiles_upload.csv", movelist)
```
