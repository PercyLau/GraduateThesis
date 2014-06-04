#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: lockheed
Information and Electronics Engineering
Huazhong University of science and technology
E-mail:lockheedphoenix@gmail.com
Created on: 4/29/14 3:21 PM

Copyright (C)  lockheedphoenix

"""

import graph_tool.all as gt
g = gt.lattice([60, 60])
pos = gt.sfdp_layout(g)
g.vertex_properties['pos']=pos
K = 2
'''
for k in range(2, K):
    for v in g.vertices():
        g.add_edge(v, g.vertex((g.vertex_index[v]+k)%(g.num_vertices())))
'''

g.save('RG.xml.gz')

