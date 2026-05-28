import numpy as np

def format_float(x: float) -> str:
    return f"{x:.7f}"


def format_int(x: int) -> str:
    return str(x)

def Origin(v, Te, vib_const) -> float:
    vib_const = (list(vib_const) + [0, 0, 0, 0])[:4]
    vib_const[1] = -vib_const[1]
    x = v + 0.5
    return Te + sum(c * x**(i + 1) for i, c in enumerate(vib_const))

def Rotational_Const(v, B_e, alpha, gamma = 0.0) -> float:
    return B_e - alpha * (v + 0.5) + gamma*(v+0.5) ** 2

def Frank_Condon_Factor(R, psi1, psi2)->float:
    """
    Takes two vibrational wave functions as np array and returns the Frank Condon Factor
    Both wave functions need to be discreet on the same grid
    """
    overlap = np.trapezoid(psi1*psi2, R)
    return overlap**2

def Frank_Cordon_Matrix(R, Eigenvecs1, Eigenvecs2)-> np.ndarray:
    """
    Takes two lists of vibrational wave functions and computes Franc Cordon Factors for all combimations 
    Returns a matrix of FCF with row index from Eigenvecs1 and column index from Eigenvec2
    """
    dx = R[1] - R[0]
    Eig1_norm = Eigenvecs1 / dx **0.5
    Eig2_norm = Eigenvecs2 / dx **0.5
    FC_matrix = np.zeros((len(Eig1_norm), len(Eig2_norm)))
    for i, eig1 in enumerate(Eig1_norm):
        for j, eig2 in enumerate(Eig2_norm):
            FC_matrix[i, j] = Frank_Condon_Factor(R, eig1, eig2)

    return FC_matrix