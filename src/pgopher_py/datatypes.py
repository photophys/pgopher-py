from dataclasses import dataclass, field
import numpy as np
import numpy.typing as npt
from enum import Enum
from typing import Optional
from .utils import Frank_Cordon_Matrix
import re


class PgopherError(RuntimeError):
    """Base exception for PGOPHER-related failures."""


class Parity(Enum):
    """
    Inversion parity.

    Attributes:
        gerade: Even parity ("g").
        ungerade: Odd parity ("u").
    """

    gerade = "g"
    ungerade = "u"


class Lambda(Enum):
    """
    Projection (Λ) of the electronic orbital angular momentum onto
    the molecular axis.

    Attributes:
        SIGMA_PLUS: Σ⁺ state.
        SIGMA_MINUS: Σ⁻ state.
        PI: Π state.
        DELTA: Δ state.
        PHI: Φ state.
    """

    SIGMA_PLUS = "Sigma+"
    SIGMA_MINUS = "Sigma-"
    PI = "Pi"
    DELTA = "Delta"
    PHI = "Phi"


@dataclass(frozen=True, slots=True, kw_only=True)
class LinearState:
    """
    Base class representing a rovibronic state of a linear molecule.

    Energetic parameters are in wavenumbers (cm⁻¹), consistent with PGOPHER conventions.

    Attributes:
        spin_multiplicity (int): Spin multiplicity S = 2S + 1.
        lambda_symmetry (Lambda): Projection Λ of electronic orbital angular momentum.
        parity (Parity, optional): Inversion symmetry of the state (gerade or ungerade).
        rotational_constant (float): Rotational constant B (cm⁻¹).
        lambda_ss (float): Spin-spin coupling constant (cm⁻¹), currently unused.
        vibrations (list): list of exited vibrational states included in simulation default [0,1,2,3,4]
        alpha (float): rotational constant - first term (cm-1)
        vibrational constants (list): vibrational constants [ω_e, ω_ex_e, ω_ey_e, ω_ez_e] only ω_e required others optional
    """

    spin_multiplicity: int
    lambda_symmetry: Lambda
    parity: Optional[Parity] = None
    rotational_constant: float
    # lambda_ss: float  # LambdaSS
    vibrational_constants: tuple[float, ...]
    vibrations: tuple[int, ...] = (0, 1, 2, 3, 4)
    alpha: float = 0


@dataclass(frozen=True, slots=True, kw_only=True)
class LinearGroundState(LinearState):
    """
    Ground electronic and vibrational state of a linear molecule.

    This state defines the zero of energy for the spectrum and does not
    have an electronic origin or parity.

    Inherits all attributes from LinearState:
        spin_multiplicity (int)
        lambda_symmetry (Lambda)
        parity (Parity, optional): Inversion symmetry of the state (gerade or ungerade).
        rotational_constant (float)
        lambda_ss (float)
        vibrations (list)
        oritin (float)
    """

    origin: float = 0


@dataclass(frozen=True, slots=True, kw_only=True)
class LinearExcitedState(LinearState):
    """
    Excited electronic and/or vibrational state of a linear molecule.

    Additional attributes beyond the base LinearState:

    Attributes:
        origin (float): Electronic or vibronic origin energy relative to the ground state (cm⁻¹).

    Inherits all attributes from LinearState:
        spin_multiplicity (int)
        lambda_symmetry (Lambda)
        parity (Parity, optional): Inversion symmetry of the state (gerade or ungerade).
        rotational_constant (float)
        lambda_ss (float)
        vibrations(list)
        origin (float)
    """

    origin: float


@dataclass(frozen=True)
class SimulationParams:
    """
    Parameters defining a linear molecule spectrum simulation.

    Attributes:
        ground (LinearGroundState): Ground state parameters.
        excited (LinearExcitedState): Excited state parameters.
        temperature (float): Simulation temperature in Kelvin.
        j_max (int): Maximum rotational quantum number to include (defaults 100).
        symmetric (bool): Optional symmetry flag for asymmetric top (currently unused).
        asym_weight (int): Optional asymmetry weight (currently unused).
    """

    ground: LinearGroundState
    excited: LinearExcitedState
    temperature: float
    franck_condon_matrix: np.ndarray
    j_max: int = 100
    symmetric: bool = True
    asym_weight: int = 0
    threshold: float = 1e-15

    def __post_init__(self):
        pass


@dataclass(slots=True, frozen=True)
class StateInformation:
    """
    Information on a state of a specific transition extracted from pgopher
    Taken straight from pgopher Output see https://pgopher.chm.bris.ac.uk/Help/lineform.htm
    or https://pgopher.chm.bris.ac.uk/Help/linearmolecules.htm for more detail



    Attributes:
        v(int): vibrational quantum number only thing taken from definition in Linearsate vibrations
        J(float): The J quantum number
        parity(string): e/f according to PGOPHER definition
        F(string): F component
    """

    v: int
    J: float
    parity: str
    F: str


@dataclass(slots=True, frozen=True)
class TransitionInformation:
    """ "
    Information on a specific transitional line

    Attributes:
        position(float): Position of transition line
        intensity(float): Intensity of transition line
        branch (string): Branch label from PGOPHER (https://pgopher.chm.bris.ac.uk/Help/linearmolecules.htm)
        ground(StateInformation): Information on the lower (ground) state
        excited(StateInformation): Information on the upper (excited) state
    """

    position: float
    intensity: float
    branch: str
    ground: StateInformation
    excited: StateInformation
