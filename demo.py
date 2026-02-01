from pgopher_py import (
    simulate_spectrum,
    LinearGroundState,
    LinearExcitedState,
    Lambda,
    Parity,
)
from matplotlib import pyplot as plt
from dotenv import load_dotenv

load_dotenv()

res = simulate_spectrum(
    ground=LinearGroundState(
        spin_multiplicity=2,
        lambda_symmetry=Lambda.SIGMA_PLUS,
        rotational_constant=1.9812707,
    ),
    excited=LinearExcitedState(
        spin_multiplicity=2,
        lambda_symmetry=Lambda.PI,
        rotational_constant=1.5928686,
        origin=11807.956423,
        parity=Parity.gerade,
    ),
    temperature=200,
    # print_xml_input=True,
)

plt.stem(res.energies, res.intensities, markerfmt=" ", basefmt=" ")
plt.savefig("test.png", dpi=1200)
