import os
import sys
# ATTENZIONE, PRIMA DI ESEGUIRE CAMBIARE IL PATH
sys.path.insert(0, r"D:\programmiUniversita\PyCharm 2022.1\progetti\best\empirical")
from empirical import CoCoS

# esecuzione della combinazione di concetti su tutti i prototipi della cartella prototipi

if __name__ == '__main__':
    file_list = os.listdir('./prototipi')
    max_prop = 10
    for file in file_list:
      CoCoS("./prototipi/"+file, max_prop, write_to_file=True)