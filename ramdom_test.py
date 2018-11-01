# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 01:45:00 2018

@author: Administrator
"""

import random
'''
the result is not stable because of the different choosing center point in the beginning
so you may run several times to get a more accurate result
the default running time is set 1.
'''
running_time=1
for times in range(running_time):
    doc=open('random_result_'+str(times)+'.txt','w')
    #doc=open('random_result.txt','w')
    C=dict()
    for i in range(22):
        C[i]=[]
    for i in range(398):
        x=random.randint(0,21)
        C[x].append(i)
    
    for label in C:
        #add the following one line code if center point considered
        #print('center point:', C[label][0],file=doc)
        for point_idx in C[label]:
                print('label {0}:　{1}'.format(label, point_idx),file=doc)
        print('',file=doc)
    doc.close()