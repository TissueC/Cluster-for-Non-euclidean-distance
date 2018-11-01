import numpy as np
import random
import matplotlib.pyplot as plt

def kMedoids(D, k, tmax=100):
    # determine dimensions of distance matrix D
    m, n = D.shape
    #print (m,n)

    if k > n:
        raise Exception('too many medoids')

    # find a set of valid initial cluster medoid indices since we
    # can't seed different clusters with two points at the same location
    valid_medoid_inds = set(range(n))
    
    #print ('haha',valid_medoid_inds)
    
    invalid_medoid_inds = set([])
    rs,cs = np.where(D==0)
    #print (rs,cs)
    # the rows, cols must be shuffled because we will keep the first duplicate below
    index_shuf = list(range(len(rs)))
    np.random.shuffle(index_shuf)
    rs = rs[index_shuf]
    cs = cs[index_shuf]
    #print (rs,cs)
    for r,c in zip(rs,cs):
        # if there are two points with a distance of 0...
        # keep the first one for cluster init
        if r < c and r not in invalid_medoid_inds:
            invalid_medoid_inds.add(c)
    valid_medoid_inds = list(valid_medoid_inds - invalid_medoid_inds)

    if k > len(valid_medoid_inds):
        raise Exception('too many medoids (after removing {} duplicate points)'.format(
            len(invalid_medoid_inds)))

    # randomly initialize an array of k medoid indices
    M = np.array(valid_medoid_inds)
    np.random.shuffle(M)
    M = np.sort(M[:k])

    # create a copy of the array of medoid indices
    Mnew = np.copy(M)

    # initialize a dictionary to represent clusters
    C = {}
    for t in range(tmax):
        # determine clusters, i. e. arrays of data indices
        J = np.argmin(D[:,M], axis=1)
        for kappa in range(k):
            C[kappa] = np.where(J==kappa)[0]
        # update cluster medoids
        for kappa in range(k):
            J = np.mean(D[np.ix_(C[kappa],C[kappa])],axis=1)
            j = np.argmin(J)
            Mnew[kappa] = C[kappa][j]
        np.sort(Mnew)
        # check for convergence
        if np.array_equal(M, Mnew):
            break
        M = np.copy(Mnew)
    else:
        # final update of cluster memberships
        J = np.argmin(D[:,M], axis=1)
        for kappa in range(k):
            C[kappa] = np.where(J==kappa)[0]

    # return results
    return M, C





#input file is csv format
input_file='05.csv'
D=np.loadtxt(input_file, delimiter=',')
m,n=D.shape
number_of_team=4

'''
the result is not stable because of the different choosing center point in the beginning
so you may run several times to get a more accurate result
the default running time is set 1.
'''
running_time=1
for times in range(running_time):
    #doc is the output file
    doc=open('kmedoids_result_'+str(times)+'.txt','w')
    x1=[]
    y1=[]
    M, C = kMedoids(D,number_of_team,1000)
    for label in C:
        print('center point:', M[label],file=doc)
        for point_idx in C[label]:
            print('label {0}:　{1}'.format(label, point_idx),file=doc)
            x1.append(point_idx)
            y1.append(label)
        print('',file=doc)
    '''
    if you wanna see the distribution of the data in a figure, uncomment the
    following three-line code. the x-axis is the no. of the data, and the y-axis
    is the label no. of each data.
    '''
    #plt.scatter(x1, y1, c='black', alpha=1, marker='+')     
    #plt.savefig("kmedoids_image_result_"+str(times)+".png")
    #plt.figure()
    doc.close()




