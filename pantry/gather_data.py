import os
import sys
import time
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, help='Class name')
    args = parser.parse_args()

    args.name = os.path.join('data', args.name)
    os.makedirs(args.name, exist_ok=True)

    count = 0
    while count < 3:
        save_file = os.path.join(args.name, 'image_'+str(count).zfill(5)+'.png')
        os.system('fswebcam -q -r 1000x1000 --no-banner '+save_file)
        print('Captured image',count)
        a = input('>')
        count += 1
