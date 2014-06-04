#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: lockheed
Information and Electronics Engineering
Huazhong University of science and technology
E-mail:lockheedphoenix@gmail.com
Created on: 3/31/14 9:50 PM

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
import numpy as np
import os
import sys
import os.path
#import matplotlib.pyplot as mplt

#from gi.repository import Gtk, Gdk, GdkPixbuf, GObject
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject

# TODO: some parameters
Cooperator = [0, 0, 1, 1]# Cooperator vertex with blue color
New_Coop = [1, 0.9, 0.1, 1]   # New cooperator with yellow color
New_Defc = [0, 1, 0, 1] # New_Defc Green color
Defector = [1, 0.1, 0, 1]  # Defector color

'''
this is a strategic game
this is payoff matrix
        Column Player
            C       D
Row     C   R,R     S,T
Player  D   T,S     P,P
some literature also use A stands for cooperator and B stands for defector

Many Classical Games can be unified in the form above

Prisoners' dilemma:S<P<R<T": only NE is BB
Stag-Hunt:S<P<T<R: two NEs: AA or BB
Hawk-Dove:P<S<R<T:ESS
Leader:P<R<S<T
Battle of the Sexes:P<R<T<S
'''
# the first example is Prisoner' Dilemma, we can also change T and S to construct different games
T = 1.9
R = 1.000
P = 0.000
S = 0.000
# construct payoffs matrix here
PM = [[[R, R], [S, T]], [[T, S], [P, P]]]

File = '2DlatticeV2.xml.gz'
h = file(File+'.txt', 'a')

def Initial_Networks(filename='2Dlattice.xml.gz'):
    graph = gt.load_graph(filename)
    '''
    each node stands for a player, he can choose to always cooperate with its immediate neighbour or always defect in
    every round of the game. Our game are synchronous. Synchronization Games is easy to study theoretically.
    each edge stands for a game. The source always plays a game with the target.
    '''
    pos = graph.vertex_properties['pos']

    '''
    old cooperator is Cooperator
    new cooperator is New_Coop
    old defector is Defector
    new defector is New_Defc
    '''
    Charactor = graph.new_vertex_property('vector<double>')
    Utility = graph.new_vertex_property('long double')
    for v in graph.vertices():
        Charactor[v] = Cooperator

    Utility.a = 0.0

    was_Coop = graph.new_vertex_property('bool')
    was_Coop.a = True
    Center = graph.vertex(int(graph.num_vertices()/2))
    Charactor[Center] = Defector
    was_Coop[Center] = False
    graph.vertex_properties['was_cha'] = was_Coop
    graph.vertex_properties['Utility'] = Utility
    graph.vertex_properties['is_cha'] = Charactor

    return graph, pos

# play an evolutionary games
def Play_EG(graph, Cooperator, New_Coop, Defector, New_Defc):
    Charactor = graph.vertex_properties['is_cha']
    was_Coop = graph.vertex_properties['was_cha']
    Utility = graph.vertex_properties['Utility']
    # clear memory
    Utility.a = 0.0

    # every edge represents a game
    for e in g.edges():
        assert isinstance(e, object)
        P1 = e.source()
        P2 = e.target()
        assert isinstance(Charactor, object)
        if was_Coop[P1]:
            if was_Coop[P2]:
                Utility[P1] += PM[0][0][0]
                Utility[P2] += PM[0][0][1]
            else:
                Utility[P1] += PM[0][1][0]
                Utility[P2] += PM[0][1][1]
        else:
            if was_Coop[P2]:
                Utility[P1] += PM[1][0][0]
                Utility[P2] += PM[1][0][1]
            else:
                Utility[P1] += PM[1][1][0]
                Utility[P2] += PM[1][1][1]

    for v in graph.vertices():
        if was_Coop[v]:
            Utility[v] += R
    # rational players will imitate his best performance immediate neighbour or stay the same.

    for v in graph.vertices():
        best = v
        for n in v.all_neighbours():
            if Utility[n] > Utility[best]:
                best = n

        if Charactor[best] == Defector or Charactor[best] == New_Defc:
            was_Coop[v] = False
        else:
            was_Coop[v] = True
    i = 0.0
    for v in graph.vertices():
        if was_Coop[v]:
            i += 1
            if Charactor[v] == New_Coop:
                Charactor[v] = Cooperator
            elif Charactor[v] == Defector or Charactor[v] == New_Defc:
                Charactor[v] = New_Coop
        else:
            if Charactor[v] == New_Defc:
                Charactor[v] = Defector
            elif Charactor[v] == Cooperator or Charactor[v] == New_Coop:
                Charactor[v] = New_Defc
    global h
    h.write(str(i/graph.num_vertices())+',')
    return True


def Update_GTK_State():
    global g
    was_Coop = g.vertex_properties['was_cha']
    #  update whole graph states with the definition of GTK
    Play_EG(g, Cooperator, New_Coop, Defector, New_Defc)

    # The following will force the re-drawing of the graph and issue a re-drawing of the GTK window
    win.graph.regenerate_surface(lazy=False)
    win.graph.queue_draw()
    # if doing an offscreen animation, dump frame to disk
    if offscreen:
        global count
        pixbuf = win.get_pixbuf()
        pixbuf.savev(r'./frames/' + File + '%06d.png' % count, 'png', [], [])
        if count > max_count:
            sys.exit(0)
        count += 1

    # We need to return True so that the main loop will call this function more
    # than once.
    return True

#  network initialization and position acquisition
g, pos = Initial_Networks(File)
Cha = g.vertex_properties['is_cha']
#  Gtk window initialization
offscreen = sys.argv[1] == 'offscreen' if len(sys.argv) > 1 else False
offscreen = True
max_count = 220  # refresh screen internal time
if offscreen and not os.path.exists('./frames'):
    os.mkdir('./frames')

if not offscreen:
    # TODO: modify the graph to squares and no edges
    win = gt.GraphWindow(g, pos, geometry=(1024, 800),
                         vertex_shape = 'hexagon',
                         vertex_size = 10,
                         vertex_anchor = 0,
                         vertex_pen_width = 0,
                         edge_color=[1, 1, 1, 1],
                         vertex_fill_color=Cha)
else:
    count = 0
    win = Gtk.OffscreenWindow()
    win.set_default_size(1024, 1024)
    win.graph = gt.GraphWidget(g, pos,
                               vertex_shape='hexagon',
                               vertex_size=10,
                               vertex_anchor=0,
                               vertex_pen_width=0,
                               edge_color=[1, 1, 1, 1],
                               vertex_fill_color=Cha)
    win.add(win.graph)

# TODO: main loop function is starting from here

# TODO: Gtk window end process is here
# Bind the function above as an 'idle' callback.
cid = GObject.idle_add(Update_GTK_State)
# We will give the user the ability to stop the program by closing the window.
win.connect("delete_event", Gtk.main_quit)


# Actually show the window, and start the main loop.
win.show_all()
Gtk.main()
h.close()