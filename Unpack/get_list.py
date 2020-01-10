import os
import sys


def main(apks_path):
    for fpath, dirs, fs in os.walk(apks_path):
        for f in fs:
            with open('list', 'a') as fff:
                fff.write(str(os.path.join(fpath, f) + '\n'))
                
                
if __name__ == '__main__':
    apks_path = sys.argv[1]
    apks_path = '/Users/smart_liu/Desktop/dpi_download/apks'
    main(apks_path)
