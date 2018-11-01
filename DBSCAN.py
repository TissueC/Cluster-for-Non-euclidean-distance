import numpy as np
import math as m

import matplotlib.pyplot as plt
import queue



data_path = "MDistance.csv"

# for removing those useless and unlabeled points
NOISE = 0
UNASSIGNED = -1


def load_data():
    """
    导入数据
    :return: 数据
    """
    points = np.loadtxt(data_path, delimiter=',')
    return points


def dist(a, b):
    """
    计算两个向量的距离
    :param a: 向量1
    :param b: 向量2
    :return: 距离
    """
    return m.sqrt(np.power(a-b, 2).sum())


def neighbor_points(data, pointId, radius):
    """
    得到邻域内所有样本点的Id
    :param data: 样本点
    :param pointId: 核心点
    :param radius: 半径
    :return: 邻域内所用样本Id
    """
    points = []
    for i in range (min(data.shape)):
        if data[pointId,i] < radius:
            points.append(i)
    return np.asarray(points)


def to_cluster(data, clusterRes, pointId, clusterId, radius, minPts):
    """
    判断一个点是否是核心点，若是则将它和它邻域内的所用未分配的样本点分配给一个新类
    若邻域内有其他核心点，重复上一个步骤，但只处理邻域内未分配的点，并且仍然是上一个步骤的类。
    :param data: 样本集合
    :param clusterRes: 聚类结果
    :param pointId:  样本Id
    :param clusterId: 类Id
    :param radius: 半径
    :param minPts: 最小局部密度
    :return:  返回是否能将点PointId分配给一个类
    """
    points = neighbor_points(data, pointId, radius)
    points = points.tolist()

    q = queue.Queue()

    if len(points) < minPts:
        clusterRes[pointId] = NOISE
        return False
    else:
        clusterRes[pointId] = clusterId
    for point in points:
        if clusterRes[point] == UNASSIGNED:
            q.put(point)
            clusterRes[point] = clusterId

    while not q.empty():
        neighborRes = neighbor_points(data, q.get(), radius)
        if len(neighborRes) >= minPts:                      # 核心点
            for i in range(len(neighborRes)):
                resultPoint = neighborRes[i]
                if clusterRes[resultPoint] == UNASSIGNED:
                    q.put(resultPoint)
                    clusterRes[resultPoint] = clusterId
                elif clusterRes[clusterId] == NOISE:
                    clusterRes[resultPoint] = clusterId
    return True


def dbscan(data, radius, minPts):
    """
    扫描整个数据集，为每个数据集打上核心点，边界点和噪声点标签的同时为
    样本集聚类
    :param data: 样本集
    :param radius: 半径
    :param minPts:  最小局部密度
    :return: 返回聚类结果， 类id集合
    """
    clusterId = 1
    nPoints = len(data)
    clusterRes = [UNASSIGNED] * nPoints
    for pointId in range(nPoints):
        if clusterRes[pointId] == UNASSIGNED:
            if to_cluster(data, clusterRes, pointId, clusterId, radius, minPts):
                clusterId = clusterId + 1
    return np.asarray(clusterRes), clusterId


if __name__ == '__main__':
    data = load_data()
    radius=5
    minpoints=2
    '''
    dbscan gets the result in dependence of two parameters: radius and minpoints
    and in most situations we decide both parameters only by experience.
    the following comment code is to filter by ranging two parameters and listing all the results 
    '''
    
    '''
    radius_start=2.0
    radius_end=5.0
    radius_step=0.01
    minpoints_start=2
    minpoints_end=6
    for i in np.arange(radius_start,radius_end,radius_step):
        for j in range(minpoints_start,minpoints_end):
            clusterRes,clusterNum=dbscan(data,i,j)
            if(clusterNum>=10):
                print (clusterNum)
                print(i,j)
    '''    

     
    clusterRes, clusterNum = dbscan(data,radius,minpoints)
    #doc is the output file
    doc=open('DBSCAN_result.txt','w')
    for i in range(clusterNum):
        for j in range(len(clusterRes)):
            if(clusterRes[j]==i):
                print ("label",i,":",j,file=doc)  
    doc.close
    #plt.show()
    