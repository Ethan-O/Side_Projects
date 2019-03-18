# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 12:18:08 2019

@author: Ethan Otto
"""

import pandas as pd
import numpy as np

data =pd.read_table('data.txt',sep = ' ')
D= data
def info(D):
    tot_counts = sum(D['count'])
    ans = 0
    for name,grs in D.groupby('status'):
        
        p = sum(grs['count'])/tot_counts
        if p == 0:
            return 0
        ans += -p*np.log2(p)
    return ans
    
def info_a(D,a):
    ans = 0
    for name, grs in D.groupby(a):
        ans +=sum(grs['count'])/sum(D['count'])*info(grs)
    return ans

def gain(D,a):
    return info(D) - info_a(D,a)


def select_a(D):
    atts = list(D.columns.values)
    atts.remove('status')
    atts.remove('count')


    scores= []
    for a in atts:
        scores.append(gain(D,a))

    ind = scores.index(max(scores))
    best = atts[ind]
    return best



class Node:
    def __init__(self,D,parent = None,A_V= ("Root","Root")):
        self.parent = parent
        self.children = None
        self.D = D
        self.A_V = A_V
        
    def divide_on(self):
        N= self
        if(len(N.D.columns.values) <=1):
            return 
        if(len(N.D) ==1):
            return
        
        att = select_a(N.D)
        
        children = []
        for name, grs in N.D.groupby(att):
            
            D = grs.drop(att,axis=1)
            child = Node(D,parent = N,A_V = ( att,name))
            children.append(child)
        
        N.children = children
        for Nc in N.children:
            Nc.divide_on()
        return
    
    def Build_Graph(self,G):
        N = self
        node =pydot.Node(str(N))
        print(N)
        G.add_node(node)
        if N.parent is not None:
            print(str(N.parent))
            print(str(N))
            edge = pydot.Edge(str(N.parent),str(N))
            G.add_edge(edge)
            
        if self.children is None:
            nodeD_name = str(N.D.loc[:,['status','count']])
            nodeD = pydot.Node(nodeD_name)
            G.add_node(nodeD)
            edge = pydot.Edge(str(N),nodeD_name)
            G.add_edge(edge)
        if self.children is not None:
            for n in self.children:
                n.Build_Graph(G)
    
    def __str__(self):
        if self.parent is not None:
            e = 'Parent- ' + self.parent.A_V[1] +'\n'
        else:
            e = ''
            
        return e + 'Node- ' + self.A_V[0] + '- ' + self.A_V[1]
        
            

class Tree:
    def __init__(self,D):
        self.root = Node(D)
    
    
N = Node(D)
N.divide_on()

#Graph Visual code, requires Graphviz2 generates tree3.png

import pydot
from IPython.display import Image, display

import os     
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

open('hello.dot','w').write("digraph G {Hello->World}")
import subprocess
subprocess.call(["dot.exe","-Tpng","hello.dot","-o","graph1.png"]) 
        


G = pydot.Dot(graph_type = 'digraph')

N.Build_Graph(G)
im = Image(G.create_png())
display(im)


