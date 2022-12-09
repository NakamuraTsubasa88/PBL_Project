import h5py
import pandas as pd

#input_file name
input_file = "h5/frame.1-4.s303.df1.5_output-test.h5"

h5file = h5py.File(input_file,"r")
#ファイルのタイプを確認
print(h5file.keys())
print(h5file['data'])
#数値を確認する
print(h5file['data'][::])
