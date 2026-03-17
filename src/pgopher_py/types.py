from dataclasses import dataclass
from enum import Enum
from typing import Optional


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
    """

    spin_multiplicity: int
    lambda_symmetry: Lambda
    parity: Optional[Parity] = None
    rotational_constant: float
    # lambda_ss: float  # LambdaSS


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
    """

    pass


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
    """

    origin: float


@dataclass
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
    j_max: int = 100
    # symmetric: bool = True
    # asym_weight: int = 0
