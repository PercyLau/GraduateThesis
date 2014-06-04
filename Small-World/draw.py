#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: lockheed
Information and Electronics Engineering
Huazhong University of science and technology
E-mail:lockheedphoenix@gmail.com
Created on: 4/30/14 9:58 AM

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
g = gt.load_graph('RG.xml.gz')
pos = g.vertex_properties['pos']
gt.graph_draw(g, pos=pos,output_size=[1024,800],output='RG.png')

gt.random_rewire(g,model='erdos')
gt.graph_draw(g, pos=pos,output_size=[1024,800],output='ER.png')

