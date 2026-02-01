import subprocess
import tempfile
from pathlib import Path
import os

from .input import write_linear_spectrum_xml
from .types import SimulationParams


class PgopherError(RuntimeError):
    """Base exception for PGOPHER-related failures."""


def run_pgopher(params: SimulationParams, print_xml_input: bool, timeout: int) -> bytes:
    """
    Generate a PGOPHER XML input file in a temporary directory,
    run the `pgo` executable on it, and return its stdout output.

    Args:
        params (SimulationParams): Simulation parameters used to generate the XML input.
        print_xml_input (bool): If True, print the generated XML content to stdout.
        timeout (int): Maximum time in seconds to allow the `pgo` subprocess to run.

    Returns:
        bytes: The stdout output produced by the `pgo` executable.

    Raises:
        PgopherError: If the subprocess fails, times out, or `pgo` returns a non-zero exit code.
    """

    # Get PGOPHER_PATH from .env
    pgopher_path = os.getenv("PGOPHER_PATH")
    if not pgopher_path:
        raise EnvironmentError("PGOPHER_PATH is not set")
    pgopher_path = Path(pgopher_path)

    print(f"Using '{pgopher_path}'")

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            xml_file = tmp_path.joinpath("input.pgo")

            # Create the XML file
            write_linear_spectrum_xml(
                file=xml_file,
                params=params,
                print_input=print_xml_input,
            )

            # Run the executable *in* the temp directory
            result = subprocess.run(
                [pgopher_path, xml_file],
                cwd=tmp_path,
                capture_output=True,
                timeout=timeout,
                check=False,  # check return code later
            )

            if result.returncode != 0:
                raise PgopherError(
                    f"PGOPHER failed with return code {result.returncode}.\n"
                    f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
                )

            return result.stdout

    except subprocess.TimeoutExpired as e:
        raise PgopherError(f"PGOPHER timed out after {timeout} seconds") from e

    except Exception as e:
        raise PgopherError("An error occurred while running PGOPHER") from e
