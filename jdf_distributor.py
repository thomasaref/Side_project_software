# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:44:51 2015

@author: thomasaref
"""

Awafer=[                                         (7,1), (8,1),
                                   (5,2), (6,2), (7,2), (8,2),
                            (4,3), (5,3), (6,3), (7,3), (8,3),
                     (3,4), (4,4), (5,4), (6,4), (7,4), (8,4),
              (2,5), (3,5), (4,5), (5,5), (6,5), (7,5), (8,5),
              (2,6), (3,6), (4,6), (5,6), (6,6), (7,6), (8,6),
       (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7), (8,7),
       (1,8), (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8)]

BadCoords=[(7,1), (8,1),
           (5,2), (8,2),
           (4,3), (8,3),
           (3,4), (8,4),
           (2,5), (8,5),
           (2,6), (8,6),
           (1,7), (8,7),
           (1,8), (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8)]

#from numpy import array #flatten
#Awafer=array(Awafer)
print Awafer
print 
print BadCoords

GoodCoords = [x for x in Awafer if x not in BadCoords]

print 
print GoodCoords

AssignArray=[('A(1)+A(2)+A(15)', 'D32080 with two IDTs and Squid connect'),
        ('A(1)+A(3)+A(15)', 'S32080 with two IDTs and Squid connect'),
        ('A(1)+A(4)+A(15)', 'S32050 with two IDTs and Squid connect'),
        ('A(1)+A(5)+A(15)',  'D32050 with two IDTs and Squid connect'),
        ('A(1)+A(6)+A(15)',  'D9050 with two IDTs and Squid connect'),
        ('A(1)+A(7)+A(15)', 'S9050 with two IDTs and Squid connect'),
        ('A(1)+A(8)+A(15)', 'S9080 with two IDTs and Squid connect'),
        ('A(1)+A(9)+A(15)', 'D9080 with two IDTs and Squid connect'),
        ('A(12)+A(10)+A(15)', 'D5080 with two FDTs and Squid connect'),
        ('A(12)+A(11)+A(15)', 'D5096 with two FDTs and Squid connect'),
        ('A(13)+A(15)', 'IDT by itself'),
        ('A(14)+A(15)', 'FDT by itself'),
        ('A(1)+A(15)',  'Two IDTs alone with squid connect'),
        ('A(12)+A(15)', 'two FDTs alone with squid connect')]

numCoords=int(len(Awafer)//len(AssignArray))
numBadCoords=int(len(BadCoords)//len(AssignArray))
numGoodCoords=int(len(GoodCoords)//len(AssignArray))
numSkip=len(AssignArray)

print numBadCoords, numGoodCoords

for i, item in enumerate(AssignArray):
    tempstr=""
    for n in range(numBadCoords):
        tempstr+=str(BadCoords[n*numSkip+i])+", "
    for m in range(numGoodCoords):
        tempstr+=str(GoodCoords[m*numSkip+i])+", "
    leftover=len(BadCoords)-numBadCoords*numSkip
    if numBadCoords*numSkip+i<len(BadCoords):
        tempstr+=str(BadCoords[(n+1)*numSkip+i])+", "
    #offset+=1
    elif numGoodCoords*numSkip-leftover+i<len(GoodCoords):
        tempstr+=str(GoodCoords[numGoodCoords*numSkip-leftover+i])+", "
    if numGoodCoords*numSkip-leftover+numSkip+i<len(GoodCoords):
        tempstr+=str(GoodCoords[(numGoodCoords+1)*numSkip-leftover+i])+", "
        
    #if (m+1)*numSkip+i<len(GoodCoords):
    #    tempstr+=str(GoodCoords[(m+1)*numSkip+i])+", "
    print "ASSIGN {arrays} -> ({nums}{dose}) ;{comment}".format(arrays=item[0], comment=item[1], nums=tempstr[:-2], dose="")
#AssignArray=[('A(1)+A(2)+A(15)',  ->  ((7,1), (6,4), (6,6)) ;D32080 with two IDTs and Squid connect
#        ASSIGN A(1)+A(3)+A(15)  ->  ((8,1), (7,4), (7,6)) ;S32080 with two IDTs and Squid connect
#        ASSIGN A(1)+A(4)+A(15)  ->  ((5,2), (8,4), (8,6), (4,8)) ;S32050 with two IDTs and Squid connect
#        ASSIGN A(1)+A(5)+A(15)  ->  ((6,2), (2,5), (1,7), (5,8))  ;D32050 with two IDTs and Squid connect
#        ASSIGN A(1)+A(6)+A(15)  ->  ((7,2), (3,5), (2,7), (6,8)) ;D9050 with two IDTs and Squid connect
#        ASSIGN A(1)+A(7)+A(15)  ->  ((8,2), (4,5), (3,7), (7,8))  ;S9050 with two IDTs and Squid connect
#        ASSIGN A(1)+A(8)+A(15)  ->  ((4,3), (5,5), (4,7))  ;S9080 with two IDTs and Squid connect
#        ASSIGN A(1)+A(9)+A(15)  ->  ((5,3), (6,5), (5,7))  ;D9080 with two IDTs and Squid connect
#        ASSIGN A(12)+A(10)+A(15) -> ((6,3),  (7,5), (6,7), (8,8)) ;D5080 with two FDTs and Squid connect
#        ASSIGN A(12)+A(11)+A(15) ->  ((7,3), (8,5), (7,7))   ;D5096 with two FDTs and Squid connect
#        ASSIGN A(13)+A(15)       ->  ((8,3), (2,6), (8,7))   ;IDT by itself
#        ASSIGN A(14)+A(15)       ->  ((3,4), (3,6), (1,8))         ;FDT by itself
#        ASSIGN A(1)+A(15)        -> ((4,4), (4,6), (2,8))     ;Two IDTs alone with squid connect
#        ASSIGN A(12)+A(15)       -> ((5,4), (5,6), (3,8))          ;two FDTs alone with squid connect