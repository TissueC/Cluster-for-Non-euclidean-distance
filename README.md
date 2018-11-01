# Cluster-for-Non-euclidean-distance
K-medoids and DBSCAN to cluster from a distance matrix

# Background
in euclidean space, the cluster is easy to be done because each element can be seen as a point in 2d or 3d coordinate system. K-means has been solved this problem pretty well.
However, in non-euclidean, there is no coordinates for elements, we can only get the non-euclidean distance(such as Mahalanobis distance and Averaged Kullback-Leible) of any two elements， from which we need to cluster them especially in text-clustering.

# input: 
a distance matrix table, the format should be csv.
the example data_input file is added in this repo

# output: 
a txt file that shows the cluster.

# To do:
It seems hard and even impossible to plot a coordinate system to show the distribution of those elements because of no coordinates for elements, but I am trying to show them visually in a figure.
