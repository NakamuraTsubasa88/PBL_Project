import h5py
import numpy as np
from plyfile import PlyData, PlyElement
import glob


# 参考(github URL)
# https://github.com/IsaacGuan/PointNet-Plane-Detection/blob/master/data/write_hdf5.py

#ファイル名指定
filenames = glob.glob('ply/*.ply')

#h5ファイルを作成する
for i in range(len(filenames)):
    f = h5py.File("h5/frame-output-%s.h5"%i, 'w')

#plyファイルをh5形式に変換する
a_data = np.zeros((len(filenames), 2048, 3))

for i in range(0, len(filenames)):
    plydata = PlyData.read(filenames[i])
    for j in range(0, 2048):
        a_data[i, j] = [plydata['vertex']['x'][j], plydata['vertex']['y'][j], plydata['vertex']['z'][j]]

#h5ファイルに書き込み
data = f.create_dataset("data", data = a_data)

