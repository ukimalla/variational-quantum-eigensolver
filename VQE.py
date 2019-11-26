from qiskit.aqua.components.optimizers import COBYLA, ADAM, AQGD
from qiskit import Aer, execute
import numpy as np
from matplotlib import pyplot
import math

from VariationalCircuit import VariationalCircuit
from KnapsackOperator import KnapsackOperator
from IndependentSetOperator import IndependentSetOperator



class VQE:
    def __init__(self, num_qubits, cost_function, variational_circuit: VariationalCircuit):

        self._num_qubits = num_qubits
        self._cost_function = cost_function
        self._variational_circuit = variational_circuit

        self._num_shots = 10000

        self.min_cost = 9e9
        self._max_itr = int(2000 * (num_qubits / 4))
        self._tol = float('1e-' + str(num_qubits))

        print(self._max_itr, "tol", self._tol)

        self._num_itr = 0


        self._backend = Aer.get_backend("qasm_simulator")
        self._optimizer = COBYLA(rhobeg=1.5,maxiter=self._max_itr, tol=self._tol)

        self._SCALE_FACTOR = 1 # Factor by which the expectation value is scaled by


    # This method is similar to the objective_function method in the piazza example.
    def objective_function(self, params):

        qc = self._variational_circuit.generateCircuit(params)
        result = execute(qc, self._backend, shots=self._num_shots).result().get_counts()
        cost = self._cost_function(result)

        if cost < self.min_cost:
            self.min_cost = cost

        self._num_itr += 1

        if self._num_itr == self._max_itr:
            print("max itr reached")

        return cost


    def execute(self):

        # Bool to check whether the variational circuit is a custom one
        isCustom = self._variational_circuit.isCustom()

        num_params = self._num_qubits
        num_params *= 9 if isCustom else 6 # Scaling the number of parameters according the the circuit

        print("Processing...")
        # Using the optimizer to optimize the parameters for the quantum circuit.
        self._optimizer.optimize(num_vars=num_params,
                                 objective_function=self.objective_function,
                                 initial_point=np.zeros(num_params))

        print("Processing Complete")

        # Returning the min cost.
        return -self.min_cost / self._SCALE_FACTOR



'''
    # 2.2 Performance Analysis

    The custom variational circuit repeats a pattern, consisting of a single layer of parameterized U3 gates followed 
    by a linear chain of CX gates, thrice. Note that if the circuit operates on n qubits, there should be 3 ·(n−1) CX 
    gates, 3n U3 gates, and a total of 3 · 3 · n = 9n parameters. The circuit looks like the diagram bellow for 4 qubits. 
    This is a derivative of the circuit that was given to us. 
    
    However, note that tha parameters to the U3 gates aren't all zeros or even initialized to zeros. They only represent 
    the fact that they are parameters. The parameters are tuned by the optimizers just as in the given circuit and 
    are initialized to random values. 
    
        ┌───────────┐     ┌───────────┐                          ┌───────────┐                               ┌─┐
q_0: |0>┤ U3(0,0,0) ├──■──┤ U3(0,0,0) ├───────────────────■──────┤ U3(0,0,0) ├───────────────────■───────────┤M├──────────────
        ├───────────┤┌─┴─┐└───────────┘┌───────────┐    ┌─┴─┐    └───────────┘┌───────────┐    ┌─┴─┐         └╥┘     ┌─┐      
q_1: |0>┤ U3(0,0,0) ├┤ X ├──────■──────┤ U3(0,0,0) ├────┤ X ├──────────■──────┤ U3(0,0,0) ├────┤ X ├──────■───╫──────┤M├──────
        ├───────────┤└───┘    ┌─┴─┐    └───────────┘┌───┴───┴───┐    ┌─┴─┐    └───────────┘┌───┴───┴───┐┌─┴─┐ ║      └╥┘┌─┐   
q_2: |0>┤ U3(0,0,0) ├─────────┤ X ├──────────■──────┤ U3(0,0,0) ├────┤ X ├──────────■──────┤ U3(0,0,0) ├┤ X ├─╫───■───╫─┤M├───
        ├───────────┤         └───┘        ┌─┴─┐    ├───────────┤    └───┘        ┌─┴─┐    ├───────────┤└───┘ ║ ┌─┴─┐ ║ └╥┘┌─┐
q_3: |0>┤ U3(0,0,0) ├──────────────────────┤ X ├────┤ U3(0,0,0) ├─────────────────┤ X ├────┤ U3(0,0,0) ├──────╫─┤ X ├─╫──╫─┤M├
        └───────────┘                      └───┘    └───────────┘                 └───┘    └───────────┘      ║ └───┘ ║  ║ └╥┘
 c_0: 0 ══════════════════════════════════════════════════════════════════════════════════════════════════════╩═══════╬══╬══╬═
                                                                                                                      ║  ║  ║ 
 c_1: 0 ══════════════════════════════════════════════════════════════════════════════════════════════════════════════╩══╬══╬═
                                                                                                                         ║  ║ 
 c_2: 0 ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╩══╬═
                                                                                                                            ║ 
 c_3: 0 ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╩═
                                                                            
    
              
    In terms of finding the optimal solution, it performed almost as well as the circuit that was given to us in most 
    cases. There were some cases where it performed worse, however, if we conducted more test with different optimizers
    it may perform better since it has more parameters. For a particular IndependentSet problem that required 8 qubits, 
    the custom circuit consistently performed better. Although, as before, this could be caused by randomness from 
    different parts of the algorithm. Since each optimization took a significant amount of time for the custom circuit, 
    I wasn't able to conduct enough tests to get statistically significant results. 
    
    In terms of time required for parameter optimization, the custom model consistently took longer. This can be 
    attributed to the increase in the number of parameters. 


'''


