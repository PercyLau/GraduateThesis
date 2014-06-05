# -*- coding: utf-8 -*-
'''
auther: lockheed 
at 6/5/14 3:33 PM
lockheedphoenix@gmail.com
Copy Rights (c)
Electronics and Information Engineering
Huazhong University of science and Technology
Wuhan, China 
'''

import graph_tool.all as gt
from math import *
from pylab import *

#g = gt.collection.data['cond-mat-2005']
#cond-mat-2005 updated network of coauthorships between scientists posting preprints on the Condensed Matter E-Print Archive.
#g = gt.collection.data['email-Enron']
#Enron email communication network covers all the email communication within a dataset of around half million emails.
g = gt.collection.data['pgp-strong-2009']
#Strongly connected component of the PGP web of trust circa November 2009. The full data is available at http://key-server.de/dump/.


# Let's plot its in-degree distribution
in_hist = gt.vertex_hist(g, "total")

y = in_hist[0]
err = sqrt(in_hist[0])
err[err >= y] = y[err >= y] - 1e-3

figure(figsize=(6,4))
errorbar(in_hist[1][:-1], in_hist[0], fmt="o", yerr=err,
        label="all")
gca().set_yscale("log")
gca().set_xscale("log")
gca().set_ylim(1e-1, 1.1*1e4)
gca().set_xlim(1, 1e4)
subplots_adjust(left=0.2, bottom=0.2)
xlabel("$k_{all}$")
ylabel("$N*Pr(k_{all})$")
tight_layout()
savefig("pgp-deg-dist.png")