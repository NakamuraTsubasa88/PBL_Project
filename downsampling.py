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

def voxcel_down(pcd,v_size):
    print("Downsample the point cloud with a voxel of %s"%v_size)
    downpcd = pcd.voxel_down_sample(voxel_size=v_size)
    return downpcd

def remove_wall(downpcd,t):
    #壁の削除
    points = np.asarray(downpcd.points)
    # 平面モデルを定義
    plano1 = pyrsc.Plane()
    # RANSACによる平面推定。平面の式とインライア(inlier)を計算。しきい値は0.01
    best_eq, best_inliers = plano1.fit(points, t)
    # 元のデータにおけるインライアの点の色を変更
    plane = downpcd.select_by_index(best_inliers).paint_uniform_color([1, 0, 0])
    # 平面以外の点を抽出
    not_plane = downpcd.select_by_index(best_inliers, invert=True)
    return not_plane, plane

def remove_desk(not_plane,t):
    #机の削除
    desk_points = np.asarray(not_plane.points)
    # 平面モデルを定義
    plano1 = pyrsc.Plane()
    # RANSACによる平面推定。平面の式とインライア(inlier)を計算。しきい値は0.01
    # 机の部分を削除（多分閾値でいけるはず）
    best_eq, desk_inliers = plano1.fit(desk_points, t)
    # 元のデータにおけるインライアの点の色を変更（赤色に変更）
    desk_place = not_plane.select_by_index(desk_inliers).paint_uniform_color([1, 0, 0])
    # 平面以外の点を抽出
    desk_not_plane = not_plane.select_by_index(desk_inliers, invert=True)
    return desk_not_plane, desk_place

def farthest_point_sample(point, npoint):
    """
    Input:
        xyz: pointcloud data, [N, D]
        npoint: number of samples
    Return:
        centroids: sampled pointcloud index, [npoint, D]
    """
    N, D = point.shape
    xyz = point[:,:3]
    centroids = np.zeros((npoint,))
    distance = np.ones((N,)) * 1e10
    farthest = np.random.randint(0, N)
    for i in range(npoint):
        centroids[i] = farthest
        centroid = xyz[farthest, :]
        dist = np.sum((xyz - centroid) ** 2, -1)
        mask = dist < distance
        distance[mask] = dist[mask]
        farthest = np.argmax(distance, -1)
    point = point[centroids.astype(np.int32)]
    return point

if __name__ == "__main__":
    #ファイル名指定（plyファイル）
    pcd = o3d.io.read_point_cloud("test1-5.ply")
    #voxel_sizeを指定
    v_size = 0.01
    #voxcel_downsampling
    downpcd = voxcel_down(pcd, v_size)

    #閾値設定
    threshold = 0.02
    #remove wall
    not_plane, plane = remove_wall(downpcd, threshold)
    pp.pprint(not_plane)
    #3次元座標上の値を出力
    # pp.pprint(np.asarray(not_plane.points))
    #可視化
    # o3d.visualization.draw_geometries([not_plane, plane])

    #外れ値除去をやる
    #statistical
    print("Radius oulier removal")
    cl, ind = not_plane.remove_statistical_outlier(nb_neighbors=30,std_ratio=2.0)
    processed_point = display_inlier_outlier(not_plane, ind)

    #閾値設定
    desk_threshold = 0.02
    #机の削除
    desk_not_plane, desk_plane = remove_desk(processed_point, desk_threshold)
    pp.pprint(desk_not_plane)

    #外れ値除去をやる
    #radisu
    print("Radius oulier removal")
    cl, ind = desk_not_plane.remove_radius_outlier(nb_points=20, radius=0.05)
    processed_point = display_inlier_outlier(desk_not_plane, ind)
    # o3d.visualization.draw_geometries([processed_point])

    # pp.pprint(np.asarray(processed_point.points))
    #FPSを実施
    human_point = np.asarray(processed_point.points)
    #array形式に変更されている
    fps = farthest_point_sample(human_point, len(human_point)//30)
    #numpy→open3d型に変更
    main_pcd = o3d.geometry.PointCloud()
    main_pcd.points = o3d.utility.Vector3dVector(fps)
    pp.pprint(main_pcd)

    # 可視化
    o3d.visualization.draw_geometries([main_pcd])











