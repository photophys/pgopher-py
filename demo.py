from pgopher_py import (
    simulate_spectrum,
    LinearGroundState,
    LinearExcitedState,
    Lambda,
    Parity,
)
from matplotlib import pyplot as plt
import numpy as np
from dotenv import load_dotenv

load_dotenv()

res = simulate_spectrum(
    ground=LinearGroundState(
        spin_multiplicity=1,
        lambda_symmetry=Lambda.SIGMA_MINUS,
        rotational_constant=1.2,
        vibrational_constants=(1600, 17, 2)
    ),
    excited=LinearExcitedState(
        spin_multiplicity=1,
        lambda_symmetry=Lambda.SIGMA_MINUS,
        rotational_constant=0.7,
        origin=11807.956423,
        parity=Parity.ungerade,
        vibrational_constants=(900, 60, 3), 
    ),
    temperature=300,
    franck_condon_matrix=np.ones((5, 5))
    # print_xml_input=True,
)
# print(res.transitions[:10])

plt.stem(res.energies, res.intensities, markerfmt=" ", basefmt=" ")
plt.savefig("test.png", dpi=1200)
