import numpy as np
from scipy.spatial import distance_matrix
from autode import geom
from autode.atoms import Atom


def test_are_coords_reasonable():

    good_coords = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    assert geom.are_coords_reasonable(coords=good_coords) is True

    bad_coords1 = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.5]])
    assert geom.are_coords_reasonable(coords=bad_coords1) is False

    bad_coords2 = np.array([[0.0, 0.0, 0.0],
                            [1.0, 0.0, 0.0],
                            [0.0, 1.0, 0.0],
                            [0.0, 2.0, 0.0],
                            [2.0, 0.0, 0.0]])
    assert geom.are_coords_reasonable(coords=bad_coords2) is False


def test_length():
    assert geom.length(np.array([1.0, 1.0, 1.0])) == np.linalg.norm(np.array([1.0, 1.0, 1.0]))


def test_shifted_atoms():

    atoms = [Atom('H', 0.0, 0.0, 0.0), Atom('H', 0.0, 0.0, 2.0)]

    new_atoms = geom.get_atoms_linear_interp(atoms, bonds=[(0, 1)], final_distances=[1.0])

    # Linear interpolation of the coordinates should move the atom either end of the bond half way
    assert np.linalg.norm(new_atoms[0].coord - np.array([0.0, 0.0, 0.5])) < 1E-6
    assert np.linalg.norm(new_atoms[1].coord - np.array([0.0, 0.0, 1.5])) < 1E-6


def test_points_on_sphere():

    points = geom.get_points_on_sphere(n_points=4)

    # 4 points on a sphere equally spaced should be roughly √2 apart
    assert len(points) == 4
    assert np.abs(np.linalg.norm(points[0] - points[1]) - np.sqrt(2)) < 1E-6

    points = geom.get_points_on_sphere(n_points=2)
    # The algorithm isn't great at generated small numbers of points so 2 -> 3

    # 3 points on a sphere equally spaced should be roughly the diameter
    assert len(points) == 3
    assert np.abs(np.linalg.norm(points[0] - points[1]) - np.sqrt(3)) < 1E-6
