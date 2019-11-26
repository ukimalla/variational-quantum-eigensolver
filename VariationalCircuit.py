from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


class VariationalCircuit:
    def __init__(self, num_qubits, bool_custom):
        self._bool_custom = bool_custom
        self._num_qubits = num_qubits

    def isCustom(self):
        return self._bool_custom


    def generateCircuit(self, params):

        # This first problem has 4 vertices, and thus requires four qubits (without exploiting symmetry).
        qr = QuantumRegister(self._num_qubits, name="q")
        cr = ClassicalRegister(self._num_qubits, name="c")
        qc = QuantumCircuit(qr, cr)

        # Generate the first layer of U3 gates:
        for i in range(self._num_qubits):
            index = i * 3
            qc.u3(params[index], params[index + 1], params[index + 2], qr[i])

        # Generate the first layer of CX gates:
        for i in range(self._num_qubits - 1):
            qc.cx(i, i + 1)

        # Generate the second layer of U3 gates:
        for i in range(self._num_qubits):
            index = (i * 3) + (self._num_qubits * 3)
            qc.u3(params[index], params[index + 1], params[index + 2], qr[i])

        # Generate the second layer of CX gates:
        for i in range(self._num_qubits - 1):
            qc.cx(i, i + 1)



        if self._bool_custom:
            # Generate the third layer of U3 gates:
            for i in range(self._num_qubits):
                index = (i * 3) + (2 * self._num_qubits * 3)
                qc.u3(params[index], params[index + 1], params[index + 2], qr[i])

            # Generate the third layer of CX gates:
            for i in range(self._num_qubits - 1):
                qc.cx(i, i + 1)


        # Measurement gates
        for i in range(self._num_qubits):
            qc.measure(qr[i], cr[i])


        return qc




