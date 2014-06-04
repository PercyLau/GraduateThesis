#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: lockheed
Information and Electronics Engineering
Huazhong University of science and technology
E-mail:lockheedphoenix@gmail.com
Created on: 4/30/14 9:58 AM

Copyright (C)  lockheedphoenix

"""
import graph_tool.all as gt
g = gt.load_graph('RG.xml.gz')
pos = g.vertex_properties['pos']
gt.graph_draw(g, pos=pos,output_size=[1024,800],output='RG.png')

gt.random_rewire(g,model='erdos')
gt.graph_draw(g, pos=pos,output_size=[1024,800],output='ER.png')

