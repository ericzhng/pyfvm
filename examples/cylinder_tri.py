#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Creates a simplisitc mesh on a cylinder strip.
'''
import numpy as np

import voropy
# ------------------------------------------------------------------------------
def _main():
    # The width of the strip
    width = 1.0

    # Mesh parameters
    # Number of nodes along the length of the strip
    nl = 100
    # Number of nodes along the width of the strip (>= 2)
    nw = 10

    # Generate suitable ranges for parametrization
    u_range = np.arange( nl, dtype='d' ) \
            * 2 * np.pi \
            / nl
    v_range = np.arange( nw, dtype='d' ) \
            / (nw - 1.0)*width \
            - 0.5 * width

    # Create the vertices. This is based on the parameterization
    # of the M\"obius strip as given in
    # <http://en.wikipedia.org/wiki/M%C3%B6bius_strip#Geometry_and_topology>
    num_nodes = nl * nw
    nodes = np.empty(num_nodes, dtype=np.dtype((float, 3)))
    k = 0
    for u in u_range:
        for v in v_range:
            nodes[k] = np.array([np.cos(u), np.sin(u), v ])
            k += 1

    # create the elements (cells)
    numelems = 2 * nl * (nw-1)
    elems = np.zeros( [numelems, 3], dtype=int )
    elem_types = np.zeros( numelems, dtype=int )
    k = 0
    for i in range(nl - 1):
        for j in range(nw - 1):
            elems[k]   = [ i*nw + j, (i + 1)*nw + j + 1,  i     *nw + j + 1 ]
            elems[k+1] = [ i*nw + j, (i + 1)*nw + j    , (i + 1)*nw + j + 1 ]
            k += 2

    # close the geometry    
    for j in range(nw - 1):
        elems[k]   = [ (nl - 1)*nw + j, j + 1 , (nl - 1)*nw + j + 1 ]
        elems[k+1] = [ (nl - 1)*nw + j, j     , j + 1  ]
        k += 2

    mesh = voropy.mesh2d_shell(nodes, elems)

    # write the mesh
    mesh.write( 'cylinder.e' )

    return
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    _main()
# ------------------------------------------------------------------------------