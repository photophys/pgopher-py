def format_float(x: float) -> str:
    return str(x)


def format_int(x: int) -> str:
    return str(x)

def Origin(v, Te, vib_const):
    vib_const = (list(vib_const) + [0, 0, 0, 0])[:4]
    vib_const[1] = -vib_const[1]
    x = v + 0.5
    return Te + sum(c * x**(i + 1) for i, c in enumerate(vib_const))

def Rotational_Const(v, B_e, alpha, gamma = 0.0):
    return B_e - alpha * (v + 0.5) + gamma*(v+0.5) ** 2