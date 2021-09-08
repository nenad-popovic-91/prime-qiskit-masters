from qiskit import QuantumCircuit
from math import pi


# funkcija koja kreira Groverov operator difuzije dimenzije 'n'
def grover_diffusion_operator(n):
    gd = QuantumCircuit(n)
    # dodajemo n operatora H
    gd.h(range(n))
    # dodajemo n operatora X
    gd.x(range(n))
    # dodajemo visestruko kontrolisani operator Z
    gd.mcp(pi, list(range(1, n)), 0)
    gd.x(range(n))
    gd.h(range(n))
    return gd


# funkcija koja kreira Groverov operator dimenzije 'n',
# za dati orakl i broj pomoćnih kubita dat kao broj 'ancilla'
def grover_operator(n, oracle_provider, ancilla=0):
    # kreiramo difuzni operator
    D = grover_diffusion_operator(n - ancilla)
    # kreiramo orakl
    Orc = oracle_provider()
    go = QuantumCircuit(n)
    # dodajemo orakl u kolo Groverovog operatora
    go = go + Orc
    # dodajemo difuzni operator u kolo Groverog operatora
    go.append(D.to_gate(), range(n - ancilla))
    go.name = 'G'

    return go


# funkcija koja kreira kolo inverzne
# Furijeove transformacije dimenzije 'n'
def inverse_qft(n):
    iqft = QuantumCircuit(n)

    # dodajemo SWAP operatore
    for i in range(n // 2 - 1, -1, -1):
        iqft.swap(i, n - 1 - i)

    for i in range(n):
        # dodajemo kola R_k
        for j in range(0, i):
            iqft.cp(-pi / 2 ** (i - j), j, i)
        # dodajemo operator H
        iqft.h(i)

    iqft.name = 'QFT+'
    return iqft


# funkcija koja kreira simulirani orakl
# za proste brojeve manje od 55
def oracle_prime_55():
    orc = QuantumCircuit(6)

    orc.x(1)
    orc.mcp(pi, [1, 2], 0)
    orc.x(1)

    orc.x(4)
    orc.mcp(pi, [3, 4, 5], 0)
    orc.x(4)

    orc.x(5)
    orc.mcp(pi, [1, 5], 0)

    orc.x([3, 1])
    orc.mcp(pi, [5, 4, 3, 1], 0)
    orc.x([1])

    orc.x([4, 2, 0])
    orc.mcp(pi, [5, 4, 3, 2, 1], 0)
    orc.x([5, 4, 3, 2, 0])

    orc.x(1)
    orc.mcp(pi, [5, 4, 3, 2, 1], 0)
    orc.x(1)

    orc.x([5, 4])
    orc.mcp(pi, [5, 4, 3, 2, 1], 0)
    orc.x([4])

    orc.x([2])
    orc.mcp(pi, [5, 4, 3, 2, 1], 0)
    orc.x([5, 2])

    orc.name = 'P55'
    return orc


# funkcija koja kreira simulirani orakl
# za proste brojeve manje od 4
def oracle_prime_4():
    orc = QuantumCircuit(3)

    orc.x(2)
    orc.cp(pi, 2, 1)
    orc.x(2)

    orc.name = 'P4'
    return orc


# funkcija koja kreira simulirani orakl
# sa pomoćnim kubitom,
# za proste brojeve manje od 16
def oracle_prime_16():
    orc = QuantumCircuit(5)

    orc.x([0, 2, 3])
    orc.mcx([0, 1, 2, 3], 4)
    orc.x(0)

    orc.mcx([0, 1, 2, 3], 4)
    orc.x(2)

    orc.x(1)
    orc.mcx([0, 1, 2, 3], 4)
    orc.x(1)

    orc.mcx([0, 1, 2, 3], 4)
    orc.x(3)

    orc.x(2)
    orc.mcx([0, 1, 2, 3], 4)
    orc.x(2)

    orc.x(1)
    orc.mcx([0, 1, 2, 3], 4)
    orc.x(1)

    return orc


# funkcija koja kreira orakl
# sa pomoćnim kubitom,
# za proste brojeve blizance manje od 16
def twin_prime_oracle():
    circuit = QuantumCircuit(9)
    P16 = oracle_prime_16().to_gate()
    P16.name = "$P_{16}$"
    DEC = decrementer(4).to_gate()
    DEC.name = "DEC"
    P16_dg = P16.inverse()
    P16_dg.name = "$P_{16}^\dagger$"
    DEC_dg = DEC.inverse()
    DEC_dg.name = "$DEC^\dagger$"
    # dodajemo prvi orakl P_16,
    # koji vrši proveru za |x>
    circuit.append(P16, range(5))
    circuit.cx(4, 6)
    # dodajemo dva dekrementera
    circuit.append(DEC, range(4))
    circuit.append(DEC, range(4))
    # dodajemo drugi orakl P_16,
    # koji vrši proveru za |x-2>
    circuit.append(P16, list(range(4)) + [5])
    circuit.cx(5, 7)
    # cuvamo rezultat na poziciji 8
    circuit.ccx(6, 7, 8)
    # invertujemo prethodne operacije
    circuit.cx(5, 7)
    circuit.append(P16_dg, list(range(4)) + [5])
    circuit.append(DEC_dg, range(4))
    circuit.append(DEC_dg, range(4))
    circuit.cx(4, 6)
    circuit.append(P16_dg, range(5))

    circuit.name = "TwP"
    return circuit


# funkcija koja kreira kolo dekrementera
# dimenzije 'n'
def decrementer(n):
    dec = QuantumCircuit(n)

    dec.x(0)
    for i in range(1, n):
        dec.mcx(list(range(i)), i)

    return dec
