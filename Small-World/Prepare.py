#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: lockheed
Information and Electronics Engineering
Huazhong University of science and technology
E-mail:lockheedphoenix@gmail.com
Created on: 4/29/14 3:21 PM

Copyright (C)  lockheedphoenix
This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or  any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
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

