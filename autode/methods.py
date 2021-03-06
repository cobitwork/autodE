from autode.wrappers.G09 import G09
from autode.wrappers.MOPAC import MOPAC
from autode.wrappers.NWChem import NWChem
from autode.wrappers.ORCA import ORCA
from autode.wrappers.XTB import XTB
from autode.config import Config
from autode.exceptions import MethodUnavailable
from autode.log import logger

"""
Functions to get the high and low level electronic structure methods to use for example high-level methods would be
orca and Gaussian09 which can perform DFT/WF theory calculations, low level methods are for example xtb and mopac which
are non ab-initio methods and are therefore considerably faster
"""

high_level_method_names = ['orca', 'g09', 'nwchem']
low_level_method_names = ['xtb', 'mopac']


def get_hmethod():
    """Get the high-level electronic structure theory method to use

    Returns:
        (autode.wrappers.base.ElectronicStructureMethod):
    """
    orca = ORCA()
    g09 = G09()
    nwchem = NWChem()

    if Config.hcode is not None:
        if Config.hcode.lower() == 'orca':
            method = orca
        elif Config.hcode.lower() == 'g09':
            method = g09
        elif Config.hcode.lower() == 'nwchem':
            method = nwchem
        else:
            logger.critical('Requested electronic structure code doesn\'t exist')
            raise MethodUnavailable

        method.set_availability()
        if not method.available:
            logger.critical('Requested electronic structure method is not available')
            raise MethodUnavailable

        return method
    else:
        # See if orca available, then Gaussian, then nwchem
        for method in [orca, g09, nwchem]:
            method.set_availability()
            if method.available:
                return method

        logger.critical('No electronic structure methods available')
        raise MethodUnavailable


def get_lmethod():
    """Get the low-level electronic structure theory method to use

    Returns:
        (autode.wrappers.base.ElectronicStructureMethod):
    """
    xtb = XTB()
    mopac = MOPAC()
    orca = ORCA()
    g09 = G09()
    nwchem = NWChem()

    if Config.lcode is not None:

        for method in [xtb, mopac, orca, g09, nwchem]:
            if method.name == Config.lcode.lower():

                method.set_availability()
                if method.available:
                    return method

        logger.critical('Requested electronic structure code doesn\'t exist')
        raise MethodUnavailable

    else:
        # See if xtb available, then mopac
        for method in [xtb, mopac]:
            method.set_availability()
            if method.available:
                return method

        logger.critical('No electronic structure methods available')
        raise MethodUnavailable
