import numpy as np
from scipy import special

import voropy
# ==============================================================================
def _main():

    args = _parse_options()

    n_phi = 200
    # lengths of major and minor axes
    a = 15.0
    b = 15.0

    # Choose the maximum area of a triangle equal to the area of
    # an equilateral triangle on the boundary.
    # For circumference of an ellipse, see
    # http://en.wikipedia.org/wiki/Ellipse#Circumference
    eccentricity = np.sqrt( 1.0 - (b/a)**2 )
    length_boundary = float(4 * a * special.ellipe(eccentricity))
    a_boundary = length_boundary / n_phi
    max_area = a_boundary**2 * np.sqrt(3) / 4

    # generate points on the circle
    Phi = np.linspace(0, 2*np.pi, n_phi, endpoint = False)
    num_boundary_points = len(Phi)
    boundary_points = np.empty(num_boundary_points, dtype=((float,2)))
    for k, phi in enumerate(Phi):
        boundary_points[k] = [a * np.cos(phi),
                              b * np.sin(phi)]

    import meshpy.triangle
    info = meshpy.triangle.MeshInfo()
    info.set_points( boundary_points )
    def _round_trip_connect(start, end):
        result = []
        for i in xrange(start, end):
            result.append((i, i+1))
        result.append((end, start))
        return result
    info.set_facets(_round_trip_connect(0, len(boundary_points)-1))
    def _needs_refinement(vertices, area):
        return bool(area > max_area)
    meshpy_mesh = meshpy.triangle.build(info,
                                        refinement_func = _needs_refinement
                                        )
    mesh = voropy.mesh2d(meshpy_mesh.points, meshpy_mesh.elements)

    # create values
    X = np.empty(len(mesh.nodes), dtype=complex)
    for k, x in enumerate(mesh.nodes):
        X[k] = complex(1.0, 0.0)

    # Add values for thickness:
    thickness = np.empty(len(mesh.nodes), dtype = float)
    alpha = 0.5 # thickness at the center of the tube
    beta = 2.0 # thickness at the boundary
    t = (beta-alpha) / b**2
    for k, x in enumerate(mesh.nodes):
        thickness[k] = alpha + t * x[1]**2

    mesh.write(args.filename, {'psi': X, 'thickness': thickness})

    return
# ==============================================================================
def _parse_options():
    '''Parse input options.'''
    import argparse

    parser = argparse.ArgumentParser( description = 'Construct a triangulation of an ellipse.' )


    parser.add_argument( 'filename',
                         metavar = 'FILE',
                         type    = str,
                         help    = 'file to be written to'
                       )

    return parser.parse_args()
# ==============================================================================
if __name__ == "__main__":
    _main()
# ==============================================================================
