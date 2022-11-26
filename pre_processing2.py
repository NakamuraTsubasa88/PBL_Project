import numpy as np
import open3d as o3d
import pprint as pp
import matplotlib.pyplot as plt
import pyransac3d as pyrsc

def display_inlier_outlier(cloud, ind):
    inlier_cloud = cloud.select_by_index(ind)
    outlier_cloud = cloud.select_by_index(ind, invert=True)

    #outが外れ値
    print("Showing outliers (red) and inliers (gray): ")
    # outlier_cloud.paint_uniform_color([1, 0, 0])
    # inlier_cloud.paint_uniform_color([0.8, 0.8, 0.8])
    return inlier_cloud

if __name__ == "__main__":
    #ファイル名指定（plyファイル）
    pcd = o3d.io.read_point_cloud("example_ply.ply")
    #voxel_sizeを指定
    v_size = 0.03
    #Voxel downsampling
    print("Downsample the point cloud with a voxel of %s"%v_size)
    #三島グループのsize分からんから適当
    downpcd = pcd.voxel_down_sample(voxel_size=v_size)
    #現在の点群数を表示
    #sample:PointCloud with 1152 points.
    pp.pprint(downpcd)
    #3次元座標上の値を出力
    # pp.pprint(np.asarray(downpcd.points))
    #可視化
    # o3d.visualization.draw_geometries([downpcd])

    #dbscan
    with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
        labels = np.array(downpcd.cluster_dbscan(eps=0.06, min_points=10, print_progress=True))
    max_label = labels.max()
    #max_label種類のクラスタリングをしている
    print(f"point cloud has {max_label + 1} clusters")
    #1つの点に対して色付けをしてる
    # pp.pprint(labels)
    colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
    #外れ値と背景を黒に設定
    colors[labels < 0] = 0
    colors[labels >= 2] = 0
    downpcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
    o3d.visualization.draw_geometries([downpcd])

    # pp.pprint(np.asarray(downpcd.points))




