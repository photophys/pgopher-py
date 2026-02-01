from dataclasses import dataclass


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


def parse_csv_output(stdout: bytes) -> PgopherSpectrum:
    """
    Parse the stdout output of a PGOPHER simulation to extract a spectrum.

    Args:
        stdout (bytes): Raw stdout bytes returned by the `pgo` executable.

    Returns:
        PgopherResult: Spectrum containing energies and intensities.

    Notes:
        - The first two lines of the output are skipped (PGOPHER version info, csv header).
        - Lines that cannot be parsed are silently ignored.
        - Assumes energies are in the 10th column (index 9) and intensities in the 11th column (index 10).
    """
    E = []
    I = []

    for line_idx, line in enumerate(stdout.split(b"\n")):
        if line_idx < 2:
            continue

        try:
            parts = line.decode().split(",")

            energy = float(parts[9])
            intensity = float(parts[10])

            E.append(energy)
            I.append(intensity)

        except:
            continue

    return PgopherSpectrum(energies=E, intensities=I)
