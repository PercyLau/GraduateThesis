#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: lockheed
Information and Electronics Engineering
Huazhong University of science and technology
E-mail:lockheedphoenix@gmail.com
Created on: 3/13/14 9:06 PM

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

