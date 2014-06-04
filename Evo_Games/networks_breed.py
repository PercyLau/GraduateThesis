#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: lockheed
Information and Electronics Engineering
Huazhong University of science and technology
E-mail:lockheedphoenix@gmail.com
Created on: 3/13/14 9:06 PM

Copyright (C)  lockheedphoenix

"""

import graph_tool.all as gt

"""
20140320 nig
g = gt.load_graph('BA_networks.xml.gz')
pos = gt.arf_layout(g)
g.vertex_properties['pos'] = pos
g.save('BA_networks_2.xml.gz')
"""

g = gt.lattice([40, 40], True)
pos = gt.sfdp_layout(g, cooling_step=0.99, epsilon=1e-3)
g.vertex_properties['pos'] = pos
g.save('3Dlattice.xml.gz')
gt.graph_draw(g, pos)

