import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path

from .types import SimulationParams, Parity
from .utils import format_int, format_float


def write_linear_spectrum_xml(file: Path, params: SimulationParams, print_input: bool):
    """
    Create a PGOPHER XML input file for a linear molecule spectrum simulation.

    This function generates the XML using `create_linear_spectrum_xml` and writes it
    to the specified file. Optionally, the XML can also be printed to stdout.

    Args:
        file (Path): Path to the file where the XML should be saved.
        params (SimulationParams): Parameters defining the simulation.
        print_input (bool): If True, print the generated XML to stdout.

    Notes:
        - Overwrites the file if it already exists.
    """
    with file.open("w", encoding="utf-8") as f:
        input = generate_linear_spectrum_xml(params)
        if print_input:
            print(input)
        f.write(input)


def generate_linear_spectrum_xml(params: SimulationParams) -> str:
    """
    Generate a PGOPHER XML configuration for a linear molecule spectrum simulation.

    Args:
        params (SimulationParams): Parameters defining the molecule, states, and
                                   simulation conditions (temperature, rotational constants, etc.).

    Returns:
        str: Pretty-printed XML document as a UTF-8 string suitable for PGOPHER input.

    Notes:
        - Defines the ground and excited manifolds and their parameters.
        - Includes transition moments and simulation temperature.
        - Designed for linear molecules only.
    """

    # Root element
    mixture = ET.Element(
        "Mixture",
        Units="cm1",
        Version="PGOPHER 10.1.182 4 Dec 2018 16:58 32 bit (Delphi 18.5/18)",
        PrintLevel="CSV",
    )

    # Species
    species = ET.SubElement(
        mixture, "Species", Name="Species", Jmax=format_int(params.j_max)
    )

    # Linear molecule
    molecule = ET.SubElement(
        species,
        "LinearMolecule",
        Name="LinearMolecule",
        # Symmetric=str(params.symmetric),
        # AsymWt=format_int(params.asym_weight),
    )

    # Ground manifold
    ground_manifold = ET.SubElement(
        molecule,
        "LinearManifold",
        Name="Ground",
        Initial="True",
        LimitSearch="True",
    )

    ground_state = ET.SubElement(
        ground_manifold,
        "Linear",
        Name="v=0",
        S=format_int(params.ground.spin_multiplicity),
        Lambda=params.ground.lambda_symmetry.value,
    )

    ET.SubElement(
        ground_state,
        "Parameter",
        Name="B",
        Value=format_float(params.ground.rotational_constant),
    )
    # ET.SubElement(
    #     ground_state,
    #     "Parameter",
    #     Name="LambdaSS",
    #     Value=format_float(params.ground.lambda_ss),
    # )

    # Excited manifold
    excited_manifold = ET.SubElement(
        molecule,
        "LinearManifold",
        Name="Excited",
        LimitSearch="True",
    )

    excited_state = ET.SubElement(
        excited_manifold,
        "Linear",
        Name="v=1",
        S=format_int(params.excited.spin_multiplicity),
        Lambda=params.excited.lambda_symmetry.value,
        gerade="True" if params.excited.parity == Parity.gerade else "False",
    )

    ET.SubElement(
        excited_state,
        "Parameter",
        Name="Origin",
        Value=format_float(params.excited.origin),
    )
    ET.SubElement(
        excited_state,
        "Parameter",
        Name="B",
        Value=format_float(params.excited.rotational_constant),
    )
    # ET.SubElement(
    #     excited_state,
    #     "Parameter",
    #     Name="LambdaSS",
    #     Value=format_float(params.excited.lambda_ss),
    # )

    # Transition moments
    transitions = ET.SubElement(
        molecule,
        "TransitionMoments",
        Bra="Excited",
        Ket="Ground",
    )

    ET.SubElement(
        transitions,
        "SphericalTransitionMoment",
        Bra="v=1",
        Ket="v=0",
    )

    # Temperature
    ET.SubElement(
        mixture,
        "Parameter",
        Name="Temperature",
        Value=format_float(params.temperature),
    )

    # Pretty-print
    rough_string = ET.tostring(mixture, encoding="utf-8")
    parsed = minidom.parseString(rough_string)
    return parsed.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")
