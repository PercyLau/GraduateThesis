#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: lockheed
Information and Electronics Engineering
Huazhong University of science and technology
E-mail:lockheedphoenix@gmail.com
Created on: 3/13/14 9:05 PM

Copyright (C)  lockheedphoenix

"""

from graph_tool.all import *
from numpy.random import *
import sys, os, os.path

#seed(42)
#seed_rng(42)

# We need some Gtk and gobject functions
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject

# We will use the network of network scientists, and filter out the largest
# component
#g = load_graph('example.xml.gz')
g = load_graph('BA_networks_2.xml.gz')
#g = load_graph('test_graph_from_g3.xml.gz')
#g = price_network(100000, gamma=4)
#pos = sfdp_layout(g)
pos = g.vertex_properties['pos']
#g = collection.data["netscience"]
#g = price_network(10000,gamma = 0.32,directed = False)
#pos = sfdp_layout(g)
#g = GraphView(g, vfilt=label_largest_component(g), directed=False)
#class Graph(object):
#Definition : Graph(g=None, directed=True, prune=False, vorder=None)
"""
Generic multigraph class.This class encapsulates either a directed multigraph (default or if directed=True) or an undirected multigraph (if directed=False), with optional internal edge, vertex or graph properties.
If g is specified, the graph (and its internal properties) will be copied.
If prune is set to True, and g is specified, only the filtered graph will be copied, and the new graph object will not be filtered. Optionally, a tuple of three booleans can be passed as value to prune, to specify a different behavior to vertex, edge, and reversal filters, respectively.
If vorder is specified, it should correspond to a vertex PropertyMap specifying the ordering of the vertices in the copied graph.
The graph is implemented as an adjacency list, where both vertex and edge lists are C++ STL vectors.#
"""
#g = Graph(g, prune=True)

#pos = g.vp["pos"]  # layout positions

# We will filter out vertices which are in the "Recovered" state, by masking
# them using a property map.
is_moved = g.new_vertex_property("bool")

# The states would usually be represented with simple integers, but here we will
# use directly the color of the vertices in (R,G,B,A) format.

S = [1, 1, 1, 1]           # White color
I = [0, 0, 0, 1]           # Black color
R = [0.5, 0.5, 0.5, 1]     # Grey color

# Initialize all vertices to the S state
state = g.new_vertex_property("vector<double>")
for v in g.vertices():
    state[v] = S
state[g.vertex(0)] = R
# Newly infected nodes will be highlighted in red
energy = g.new_vertex_property("int")
#Initialization
energy.a = 3
is_moved.a = False
is_moved[g.vertex(0)] = True

#set the start point as a trigger with energy - 1 that represents infinit

# If True, the frames will be dumped to disk as images.
offscreen = sys.argv[1] == "offscreen" if len(sys.argv) > 1 else False
max_count = 5
if offscreen and not os.path.exists("./frames"):
    os.mkdir("./frames")

# This creates a GTK+ window with the initial graph layout
if not offscreen:
    win = GraphWindow(g, pos, geometry=(1024, 800),
                      edge_color=[0.6, 0.6, 0.6, 1],
                      vertex_fill_color=state,
                      vertex_halo=is_moved,
                      vertex_halo_color=[0.8, 0, 0, 0.6])
else:
    count = 0
    win = Gtk.OffscreenWindow()
    win.set_default_size(1024, 800)
    win.graph = GraphWidget(g, pos,
                            edge_color=[0.6, 0.6, 0.6, 1],
                            vertex_fill_color=state,
                            vertex_halo=is_moved,
                            vertex_halo_color=[0.8, 0, 0, 0.6])
    win.add(win.graph)

# dynamics parameters:
p = 0.2

# This function will be called repeatedly by the GTK+ main loop, and we use it
# to update the state according to the SIRS dynamics.


def update_state():
    vs = list(g.vertices())
    shuffle(vs)
    for ver in vs:
        if is_moved[ver]:
            state[ver] = I
            is_moved[ver] = False
            if energy[ver] > 0:
                ns = list(ver.all_neighbours())
                shuffle(ns)
                #send ads to its neighbours
                for n in ns:
                    if random() < p:
                        is_moved[n] = True
                    else:
                        is_moved[n] = False
                #reduce energy only if the node is moved
                energy[ver] -= 1

    # The following will force the re-drawing of the graph, and issue a
    # re-drawing of the GTK window.
    win.graph.regenerate_surface(lazy=False)
    win.graph.queue_draw()

    # if doing an offscreen animation, dump frame to disk
    if offscreen:
        global count
        pixbuf = win.get_pixbuf()
        pixbuf.savev(r'./frames/sirs%06d.png' % count, 'png', [], [])
        if count > max_count:
            sys.exit(0)
        count += 1

    # We need to return True so that the main loop will call this function more
    # than once.
    return True


# Bind the function above as an 'idle' callback.
cid = GObject.idle_add(update_state)

# We will give the user the ability to stop the program by closing the window.
win.connect("delete_event", Gtk.main_quit)

# Actually show the window, and start the main loop.
win.show_all()
Gtk.main()

