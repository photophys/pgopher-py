from dataclasses import dataclass
from io import StringIO
import csv
import re
from .datatypes import PgopherError, StateInformation, TransitionInformation


@dataclass
class PgopherSpectrum:
    """
    Spectrum simulated with PGOPHER.

    Attributes:
        energies (list[float]): Spectral energies (in cm⁻¹).
        intensities (list[float]): Corresponding intensities.
    """

    energies: list[float]
    intensities: list[float]
    transitions: list[TransitionInformation]





def parse_csv_output(stdout: bytes) -> PgopherSpectrum:
    """
    Parse the stdout output of a PGOPHER simulation to extract a spectrum.

    Args:
        stdout (bytes): Raw stdout bytes returned by the `pgo` executable.

    Returns:
        PgopherResult: Spectrum containing energies, intensities and labeling information.

    Notes:
        - The first two lines of the output are skipped (PGOPHER version info, csv header).
        - Lines that cannot be parsed are silently ignored.
        - Assumes energies are in the 10th column (index 9) and intensities in the 11th column (index 10).
    """
   
    lines = iter(stdout.decode().splitlines())
    next(lines)  # skip metadata
    reader = csv.DictReader(lines)
    E = []
    I = []
    transitions = []
    for row in reader: 
        if row.get("Label") is None:
            continue
        try:
            E.append(float(row["Position"]))
            I.append(float(row["Intensity"]))
            excited_text, ground_text = row["Label"].split(" - ")
            vg, Fg = parse_label(ground_text)
            ve, Fe = parse_label(excited_text)
            ground = StateInformation(vg,float(row['J"']) ,row['Sym"'],Fg)
            excited = StateInformation(ve, float(row["J'"]), row["Sym'"], Fe)
            transitions.append(TransitionInformation(float(row["Position"]), float(row["Intensity"]), row["Branch"], ground, excited))
        except: 
            print(row)
            raise ValueError("Could not parse line ")
    return PgopherSpectrum(E, I, transitions)

def parse_label(label: str):
     
    v_match = re.search(r"v=(\d+)", label)
    f_match = re.search(r"F\d", label)

    assert v_match is not None
    assert f_match is not None

    return(
        int(v_match.group(1)),
        f_match.group(0)
    )