from urllib.request import urlretrieve
import os

def download(url, file):
  if os.path.isfile(file):
    print(file + " already downloaded. You can see it if you click on the folder icon at the left")
  else:
    print("Downloading file " + file + " ...", end="")
    urlretrieve(url,file)
    print("OK")


download('http://red.smu.edu.sg/resources/colabq2data/sample1.txt', 'sample1.txt')
download('http://red.smu.edu.sg/resources/colabq2data/sample2.txt', 'sample2.txt') 
download('http://red.smu.edu.sg/resources/colabq2data/sample3.txt', 'sample3.txt') 