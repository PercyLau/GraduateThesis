#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: lockheed
Information and Electronics Engineering
Huazhong University of science and technology
E-mail:lockheedphoenix@gmail.com
Created on: 4/3/14 3:26 PM

Copyright (C)  lockheedphoenix
"""

import graph_tool.all as gt
N = 99
'''
g = gt.lattice([15, 15])
Pin = g.new_vertex_property('bool')
Pin.a = False
Pin[g.vertex(1)] = True
Pin[g.vertex(0)] = True
assert isinstance(Pin, object)
pos = gt.sfdp_layout(g, epsilon=0.2)
pos[g.vertex(1)][0] = pos[g.vertex(0)][0]
pos = gt.sfdp_layout(g)
g.vertex_properties['pos'] = pos
g.save('S2Dlattice.xml.gz')
'''
g = gt.lattice([N, N])
Pin = g.new_vertex_property('bool')
Pin.a = False
Pin[g.vertex(1)] = True
Pin[g.vertex(0)] = True
assert isinstance(Pin, object)
pos = gt.sfdp_layout(g, epsilon=0.2)
pos[g.vertex(1)][0] = pos[g.vertex(0)][0]
pos = gt.sfdp_layout(g)
g.vertex_properties['pos'] = pos
g.save('2Dlattice.xml.gz')

'''

g = gt.lattice([N, N])
pos = gt.sfdp_layout(g, epsilon=0.000000001, C=1)
#pos = gt.sfdp_layout(g)
g.vertex_properties['pos'] = pos

for i in range(0, N-1):
    for j in range(0, N-1):
        g.add_edge(i*N+j, i*N+j+N+1)

for i in range(0, N-1):
    for j in range(1, N):
        g.add_edge(i*N+j, i*N+j+N-1)

g.save('haurt_lattice.xml.gz')
'''
#gt.graph_draw(g, pos, vertex_text=g.vertex_index)


