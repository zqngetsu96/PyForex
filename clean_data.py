import os
import glob

paths = ['./data/chart/test/buy',
    './data/chart/test/hold',
    './data/chart/test/sell',
    './data/chart/train/buy',
    './data/chart/train/hold',
    './data/chart/train/sell'
    './data/gasf/train/buy',
    './data/gasf/train/hold',
    './data/gasf/train/sell',
    './data/gasf/test/buy',
    './data/gasf/test/hold',
    './data/gasf/test/sell']

for path in paths:
    files = glob.glob(path+'/*.jpg')
    for f in files:
        os.remove(f)

Print('All data directories Cleaned')