import os
import glob


if os.getcwd().endswith('PyForex'):
    os.chdir('./data_utils')

paths = ['../data/chart/test/buy',
    '../data/chart/test/hold',
    '../data/chart/test/sell',
    '../data/chart/train/buy',
    '../data/chart/train/hold',
    '../data/chart/train/sell'
    '../data/gasf/train/buy',
    '../data/gasf/train/hold',
    '../data/gasf/train/sell',
    '../data/gasf/test/buy',
    '../data/gasf/test/hold',
    '../data/gasf/test/sell']

for path in paths:
    files = glob.glob(path+'/*.jpg')
    for f in files:
        os.remove(f)

print('All data directories (chart + GASF train test) Cleaned')