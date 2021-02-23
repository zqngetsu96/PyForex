import os
import glob


if os.getcwd().endswith('PyForex'):
    os.chdir('./data_utils')

paths = ['../data/chart_npy',
         '../data/gasf_npy',
         '../data/series_npy'
        ]

for path in paths:
    files = glob.glob(path+'/*.npy')
    for f in files:
        os.remove(f)

print('All data directories (chart + GASF train test) Cleaned')