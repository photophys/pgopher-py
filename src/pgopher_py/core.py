from .parse import parse_csv_output, PgopherSpectrum
from .run import run_pgopher
from .types import LinearGroundState, LinearExcitedState, SimulationParams


def simulate_spectrum(
    ground: LinearGroundState,
    excited: LinearExcitedState,
    temperature: float,
    j_max: int = 100,
    print_xml_input: bool = False,
    timeout: int = 30,
) -> PgopherSpectrum:
    """
    Run a PGOPHER simulation for a linear molecule and return the resulting spectrum.

    This function generates the PGOPHER XML input from the provided simulation parameters,
    runs the `pgo` executable, and parses the output into a `PgopherSpectrum` object.

    Designed specifically for linear molecules.

    Args:
        ground (LinearGroundState): Ground state parameters.
        excited (LinearExcitedState): Excited state parameters.
        temperature (float): Simulation temperature in Kelvin.
        j_max (int): Maximum rotational quantum number to include (defaults 100).
        print_xml_input (bool, optional): If True, print the generated PGOPHER XML input.
                                           Defaults to False.
        timeout (int, optional): Maximum time in seconds to allow the `pgo` subprocess to run.
                                 Defaults to 30.

    Returns:
        PgopherSpectrum: Spectrum containing energies and intensities extracted from
                         the simulation output.

    Raises:
        PgopherError: If the subprocess fails, times out, or returns a non-zero exit code.
    """
    res = run_pgopher(
        params=SimulationParams(
            ground=ground,
            excited=excited,
            temperature=temperature,
            j_max=j_max,
        ),
        timeout=timeout,
        print_xml_input=print_xml_input,
    )

    return parse_csv_output(res)
