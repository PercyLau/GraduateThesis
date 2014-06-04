#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: lockheed
Information and Electronics Engineering
Huazhong University of science and technology
E-mail:lockheedphoenix@gmail.com
Created on: 3/14/14 10:10 AM

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
'''

# TODO: add precise descriptions to this program
# force compiler to use true division
from __future__ import division

# We need some Gtk and gobject functions
# from gi.repository import Gtk, Gdk, GdkPixbuf, GObject
import graph_tool.all as gt
import scipy as sp
import numpy as np
import os
import sys
import os.path

# We need some Gtk and gobject functions
# from gi.repository import Gtk, Gdk, GdkPixbuf, GObject
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject

# TODO: get a new directed network named 'g' from outfile or produce by a function, cal positions if necessary

# TODO: define 4 sorts of edge map, directed or undirected, define two vertex property

# TODO: list all dynamic parameters here

Red = [0.7, 0.2, 0, 1]  # Type A vertex with Red color
Green = [0, 1, 0, 1]  # Type B vertex with Green color
Yellow = [0, 0, 0.7, 1]  # Yellow color
Mutation_likely = 0  # TODO: need to be specified
alpha = 0.7  # indicate network A's attraction
beta = 0.35  # indicate network B's attraction
partition = 0.179
# steady state a o.7 b 0.35 p = 0.205
initial_total_rounds = 1000000000
Community_Gain = 1.0
Non_Community_Gain = 0
Num_A = 0
N = 0
File = '0.63SW.xml.gz'

'''
# BA_networks_2 alpha = 0.500, beta = 0.501 initial_partition = 0.745, initial_total_round = 10000 Community_Gain = 2
this will boost chaos in SF and mutation will trigger cascading failure
# for 2Dlattice 60*60, seems alpha = 0.500 beta = 0.501, initial_partition = 0.745, initial_total_round = 10000 Community_Gain = 2
is the Pc
'''


def Initial_Networks(filename='2Dlattice.xml.gz'):
    """

    :param Networks:
    :return:
    """
    global mutate_tag
    global VertexState
    global Num_A
    global N

    graph = gt.load_graph(filename)
    print(graph.num_vertices())
    mutate_tag = graph.new_vertex_property('bool')
    mutate_tag.a = False
    VertexState = graph.new_vertex_property('vector<double>')

    pos = graph.vertex_properties['pos']
    is_VTA = graph.new_vertex_property('bool')  # whether it is vertex type A
    was_VTA = graph.new_vertex_property('bool')  # whether it was vertex type A last time
    graph.vertex_properties['is_VTA'] = is_VTA  # force it into internal property map
    graph.vertex_properties['was_VTA'] = was_VTA  # force it into internal property map
    #  Initialization each vertex a state with each state (equal probability 1/2)?
    Vertex_Mem = graph.new_vertex_property('vector<int>')  # to record neighbours' behavior history
    graph.vertex_properties['vertex_mem'] = Vertex_Mem  # force into internal map
    Neighbour_Trust = graph.new_vertex_property('vector<double>')
    graph.vertex_properties['neighbour_trust'] = Neighbour_Trust  # force into internal map
    Total_Rounds = graph.new_graph_property('double', initial_total_rounds)
    graph.graph_properties['total_rounds'] = Total_Rounds
    N = graph.num_vertices()
    #  random initialization?
    for v in graph.vertices():
        Vertex_Mem[v] = [1] * len(list(v.all_neighbours()))
        Neighbour_Trust[v] = [1.0] * len(list(v.all_neighbours()))
        if np.random.random() < partition:  # the A's amount is equal to B's
            is_VTA[v] = True
            was_VTA[v] = True
            Num_A += 1
            VertexState[v] = Red
        else:
            is_VTA[v] = False
            was_VTA[v] = False
            VertexState[v] = Green

    for v in graph.vertices():
        i = 0
        for n in v.all_neighbours():
            if was_VTA[n]:
                Vertex_Mem[v][i] = 1  # tag 1 shows n was type A last round
            else:
                Vertex_Mem[v][i] = 0  # tag 0 shows n was type B last round
            i += 1

    Edge_Type = graph.new_edge_property('int')  # indicate edges type
    graph.edge_properties['edge_type'] = Edge_Type
    #  1 is A to A edge, 2 is A to B edge, 3 is B to B edge, can be modified
    for e in graph.edges():
        if is_VTA[e.source()] and is_VTA[e.target()]:
            Edge_Type[e] = 1
        elif (not is_VTA[e.source()]) and (not is_VTA[e.target()]):
            Edge_Type[e] = 3
        else:
            Edge_Type[e] = 2
    # TODO: specified edges' properties
    fhandle = file(filename + '.txt', 'a')

    return graph, pos, fhandle


def Update_VE(graph):
    """

    :param graph:
    :return:
    """
    is_VTA = graph.vertex_properties['is_VTA']  # vertex type A tag map
    was_VTA = graph.vertex_properties['was_VTA']
    Edge_Type = graph.edge_properties['edge_type']  # edge_type map
    Vertex_Mem = graph.vertex_properties['vertex_mem']  # vertex mem map
    Neighbour_Trust = graph.vertex_properties['neighbour_trust']

    for v in graph.vertices():
        i = 0
        # update vertices' neighbour trust
        for n in v.all_neighbours():
            if was_VTA[n]:
                if Vertex_Mem[v][i] is 1:
                    Neighbour_Trust[v][i] = (Neighbour_Trust[v][i] * (graph.graph_properties['total_rounds']) + 1.0) / (
                        graph.graph_properties['total_rounds'] + 1)
                else:
                    Neighbour_Trust[v][i] = (Neighbour_Trust[v][i] * (graph.graph_properties['total_rounds'])) / (
                        graph.graph_properties['total_rounds'] + 1.0)
            else:
                if Vertex_Mem[v][i] is 0:
                    Neighbour_Trust[v][i] = (Neighbour_Trust[v][i] * (graph.graph_properties['total_rounds']) + 1.0) / (
                        graph.graph_properties['total_rounds'] + 1.0)
                else:
                    Neighbour_Trust[v][i] = (Neighbour_Trust[v][i] * (graph.graph_properties['total_rounds'])) / (
                        graph.graph_properties['total_rounds'] + 1.0)
            # pay attention to index!
            i += 1
        #update vertex
        was_VTA[v] = is_VTA[v]

    graph.graph_properties['total_rounds'] = graph.graph_properties['total_rounds'] + 1.0

    '''
    for e in graph.edges():
        if is_VTA[e.source()] and is_VTA[e.target()]:
            Edge_Type[e] = 1
        elif (not is_VTA[e.source()]) and (not is_VTA[e.target()]):
            Edge_Type[e] = 3
        else:
            Edge_Type[e] = 2
    '''

    return True


def Vertex_A_Utility(graph, vertex, Alpha, Beta):
    # TODO: map A's vertex action functions to utility, it's supposed to be a repeat public-goods game
    # TODO: supposed the vertex tend to be A type, cal its utility
    """

    :param Networks:
    :param vertex:
    :return:
    """
    A = 0
    was_VTA = graph.vertex_properties['was_VTA']
    Neighbour_Trust = graph.vertex_properties['neighbour_trust']
    #case A
    i = 0
    for n in vertex.all_neighbours():
        if was_VTA[n]:
            A += Community_Gain * Alpha * Neighbour_Trust[vertex][i]
        else:
            A += Non_Community_Gain * Beta * Neighbour_Trust[vertex][i]
        i += 1
    return A


def Vertex_B_Utility(graph, vertex, Alpha, Beta):
    # ??TODO: map B's vertex action functions to utility, it's supposed to be a repeat public-goods game
    # TODO: supposed the vertex tend to be A type, cal its utility
    """

    :param Networks:
    :param vertex:
    :return:
    """
    B = 0
    was_VTA = graph.vertex_properties['was_VTA']
    Neighbour_Trust = graph.vertex_properties['neighbour_trust']
    #case A
    i = 0
    for n in vertex.all_neighbours():
        if not was_VTA[n]:
            B += Community_Gain * Beta * Neighbour_Trust[vertex][i]
        else:
            B += Non_Community_Gain * Alpha * Neighbour_Trust[vertex][i]
        i += 1
    return B


def Vertexes_Mumate(graph, genetic_mutation_likely=Mutation_likely):
    """

    :param vertex:
    :return:
    """
    global Num_A
    global N
    mutate_tag.a = False
    is_VTA = graph.vertex_properties['is_VTA']
    for vertex in graph.vertices():
        if np.random.random() < genetic_mutation_likely:
            if is_VTA[vertex]:
                Num_A -= 1
            else:
                Num_A += 1
            mutate_tag[vertex] = True
            is_VTA[vertex] = not is_VTA[vertex]
            if is_VTA[vertex]:
                VertexState[vertex] = Red
            else:
                VertexState[vertex] = Green

    Update_VE(graph)

    return True


def Vertexes_Inherit(graph):
    """

    :param graph:
    :param vertex:
    :return:
    """
    global Num_A
    global N
    is_VTA = graph.vertex_properties['is_VTA']
    vs = list(graph.vertices())
    np.random.shuffle(vs)
    for vertex in vs:
        if Vertex_A_Utility(graph=graph, vertex=vertex, Alpha=alpha, Beta=beta) > Vertex_B_Utility(graph=graph,
                                                                                                   vertex=vertex,
                                                                                                   Alpha=alpha,
                                                                                                   Beta=beta):
            if not is_VTA[vertex]:
                assert isinstance(Num_A, object)
                Num_A += 1
            is_VTA[vertex] = True
            VertexState[vertex] = Red
        elif Vertex_A_Utility(graph=graph, vertex=vertex, Alpha=alpha, Beta=beta) < Vertex_B_Utility(graph=graph,
                                                                                                     vertex=vertex,
                                                                                                     Alpha=alpha,
                                                                                                     Beta=beta):
            if is_VTA[vertex]:
                assert isinstance(Num_A, object)
                Num_A -= 1
            is_VTA[vertex] = False
            VertexState[vertex] = Green

    return True


def Update_GTK_State():
    """

    :param max_count:
    :param win:
    :param offscreen:
    :return:
    """
    global alpha
    global beta
    global Num_A
    global N
#    if (Num_A/N) > partition:
#        alpha = np.power(alpha, 2)
#        beta = np.sqrt(beta)
#    else:
#        alpha = np.sqrt(alpha)
#        beta = np.power(beta, 2)


    print('A conquers about '+str(Num_A / N)+' while alpha is '+str(alpha)+' beta is '+str(beta))
    global h
    global filename

    h.write(',' + str(Num_A / N))
    # TODO: update whole graph states with the definition of GTK
    Vertexes_Inherit(g)
    Vertexes_Mumate(g)
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

# TODO: network initialization and position acquisition
g, pos, h = Initial_Networks(File)



# TODO: Gtk window initialization
offscreen = sys.argv[1] == 'offscreen' if len(sys.argv) > 1 else False
#offscreen = True
max_count = 40  # refresh screen internal time
if offscreen and not os.path.exists('./frames'):
    os.mkdir('./frames')

if not offscreen:
    win = gt.GraphWindow(g, pos, geometry=(1024, 800),
                         edge_color=[0.6, 0.6, 0.6, 1],
                         vertex_fill_color=VertexState,
                         vertex_halo=mutate_tag,
                         vertex_halo_size=2,
                         vertex_halo_color=Yellow)
else:
    count = 0
    win = Gtk.OffscreenWindow()
    win.set_default_size(1024, 800)
    win.graph = gt.GraphWidget(g, pos,
                               edge_color=[0.6, 0.6, 0.6, 1],
                               vertex_fill_color=VertexState,
                               vertex_halo=mutate_tag,
                               vertex_halo_size=2,
                               vertex_halo_color=Yellow)
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

