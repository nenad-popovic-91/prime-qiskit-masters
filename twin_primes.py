from qiskit import QuantumCircuit, execute, IBMQ
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
import circuit_provider

t = 6
n = 9
a = 5

# kreiranje kola eksperimenta
circuit = QuantumCircuit(t + n, t)
# stanje jednake superpozicije
circuit.h(range(t + n - a))
# Groverov operator
grover_operator = circuit_provider.grover_operator(n, circuit_provider.twin_prime_oracle, a)
# kreiranje stanja (|0> - |1>)/sqrt(2)
# na pomocnoj poziciji
circuit.x(t+n-1)
circuit.h(t+n-1)
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
# vraćanje stanja (|0> - |1>)/sqrt(2)
# na pomocnoj poziciji natrag u |0>
circuit.h(t+n-1)
circuit.x(t+n-1)

# merenje
circuit.measure(range(t), range(t))

# prikaz kreiranog kola
circuit.draw(output='mpl', style={"name": "bw", "dpi": 300})

# izvrsavanje eksperimenta na (`cloud`) kvantnom simulatoru
provider = IBMQ.load_account()
backend = provider.get_backend('ibmq_qasm_simulator')
counts = execute(circuit, backend, shots=1000).result().get_counts()
plot_histogram(counts, color="gray")

plt.show()
