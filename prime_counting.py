from qiskit import QuantumCircuit, Aer, execute
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
import circuit_provider

t = 6
n = 6

# kreiranje kola eksperimenta
circuit = QuantumCircuit(t + n, t)
# stanje jednake superpozicije
circuit.h(range(t + n))
# Groverov operator
grover_operator = circuit_provider.grover_operator(n, circuit_provider.oracle_prime_55)
# dodavanje operatora G^{2^k} u kolo,
# gde svaki sledeći stepen operatora kreiramo
# korišćenjem prethodnog
G = [grover_operator]
CG0 = G[0].to_gate().control(1)
circuit.append(CG0, [0] + list(range(t, t + n)))
for i in range(1, t):
    G.append(QuantumCircuit(n))
    G[i] = G[i] + G[i-1] + G[i-1]
    gG = G[i].to_gate()
    gG.name = '$G^{' + str(2**i) + '}$'
    CG = gG.control(1)
    circuit.append(CG, [i] + list(range(t, t+n)))
# dodavanje inverzne QFT u kolo
circuit.append(circuit_provider.inverse_qft(t).to_gate(), range(t))
circuit.measure(range(t), range(t))

# prikaz kreiranog kola
circuit.draw(output='mpl', style={"name": "bw", "dpi": 300})
# izvrsavanje eksperimenta na (lokalnom) kvantnom simulatoru
backend = Aer.get_backend('qasm_simulator')
counts = execute(circuit, backend, shots=2000).result().get_counts()
plot_histogram(counts, color='gray')

plt.show()