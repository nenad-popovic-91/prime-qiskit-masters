from qiskit import QuantumCircuit, transpile, Aer, execute, IBMQ
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
import circuit_provider


n = 3

# kreiranje kola eksperimenta
grover = QuantumCircuit(n)
grover.h(range(n))
P4 = circuit_provider.oracle_prime_4().to_gate()
P4.label = 'P4'
D3 = circuit_provider.grover_diffusion_operator(n).to_gate()
D3.label = 'D3'
grover.append(P4, range(n))
grover.append(D3, range(n))
grover.measure_all()

# prikaz kreiranog kola
grover.draw(output='mpl', style={"name": "bw", "dpi": 300})

# izvrsavanje eksperimenta na kvantnom simulatoru
backend = Aer.get_backend('qasm_simulator')
counts = execute(grover, backend, shots=4000).result().get_counts()
plot_histogram(counts, color='gray')

# izvrsavanje istog eksperimenta na kvantnom racunaru
IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q')
backend = provider.get_backend('ibmq_athens')
counts = execute(grover, backend, shots=4000).result().get_counts()
plot_histogram(counts, color='gray')

plt.show()