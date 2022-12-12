import h5py
import numpy as np
from plyfile import PlyData, PlyElement
import glob
# import pprint as pp


# 参考(github URL)
# https://github.com/IsaacGuan/PointNet-Plane-Detection/blob/master/data/write_hdf5.py
# https://isaacguan.github.io/2018/05/04/Prepare-Your-Own-Data-for-PointNet/

# #ファイル名指定
filenames = glob.glob('ply/wash_output/*.ply')

for i in range(0,len(filenames)):
    #データの読込み
    plydata = PlyData.read(filenames[i])
    #点群の個数で配列を作成([x軸の値,x軸の値,x軸の値]*点群の個数分)
    a_data = np.empty((1, plydata.elements[0].count, 3))
    #ply→h5変換
    for j in range(0, plydata.elements[0].count):
        a_data[0, j] = [plydata['vertex']['x'][j], plydata['vertex']['y'][j], plydata['vertex']['z'][j]]
    #h5ファイルを作成する
    f = h5py.File("h5/wash_h5/wash-frame-output-%s.h5"%i, 'w')
    #h5にデータを書き込む
    data = f.create_dataset("data", data = a_data)
    # pp.pprint(data)

