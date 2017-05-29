# -*- coding: utf-8 -*-
#
from . import fvm_problem
from . import linear_fvm_problem

from .discretize_linear import *
from .discretize import *
from .nonlinear_methods import *
from .fvm_matrix import *

from pyfvm.__about__ import (
    __version__,
    __author__,
    __author_email__,
    )

__all__ = [
    'fvm_problem',
    'linear_fvm_problem'
    ]