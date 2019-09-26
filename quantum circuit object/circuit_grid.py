import numpy as np

import circuit_node_types


class CircuitGrid:
    """
    Grid-based model that is built when user interacts with circuit
    """

    def __init__(self, qubit_count, circuit_depth):
        self.qubit_count = qubit_count
        self.circuit_depth = circuit_depth
        self.circuit_grid = np.empty((qubit_count, qubit_count), dtype=CircuitGridNode)

    def set_node(self, qubit_index, depth_index, circuit_grid_node):
        self.circuit_grid[qubit_index][depth_index] = \
            CircuitGridNode(circuit_grid_node.node_type,
                            circuit_grid_node.radians,
                            circuit_grid_node.ctrl_a,
                            circuit_grid_node.ctrl_b,
                            circuit_grid_node.swap)

    def get_node(self, qubit_index, depth_index):
        return self.circuit_grid[qubit_index][depth_index]

    def create_qasm_for_node(self, qubit_index):
        qasm_str = ""

        if node_type == circuit_node_types.IDEN:
            # identity gate
            qasm_str = qasm_str + 'id q['+qubit_index+'];'
        elif node_type == circuit_node_types.X or \
                node_type == circuit_node_types.Y or \
                node_type == circuit_node_types.Z:
            # X, Y, Z gate
            qasm_str = qasm_str + node_type + ' q[' + qubit_index + '];'
        else node_type == circuit_node_types.H:
            # Hadamard gate
            qasm_str = qasm_str + node_type + ' q[' + qubit_index + '];'

        return qasm_str

    def compute_circuit(self):
        """
        Compute a QuantumCircuit object based on CircuitGrid
        :return: QuantumCircuit object
        """
        qr = QuantumRegister(self.qubit_count, 'q')
        qc = QuantumCircuit(qr)

        for depth_index in range(self.circuit_depth):
            for qubit_index in range(self.qubit_count):
                node = self.circuit_grid[qubit_index][depth_index]
                if node:
                    if node.node_type == node_types.IDEN:
                        # Identity gate
                        qc.iden(qr[qubit_index])
                    elif node.node_type == node_types.X:
                        if node.radians == 0:
                            if node.ctrl_a != -1:
                                if node.ctrl_b != -1:
                                    # Toffoli gate
                                    qc.ccx(qr[node.ctrl_a], qr[node.ctrl_b], qr[qubit_index])
                                else:
                                    # Controlled X gate
                                    qc.cx(qr[node.ctrl_a], qr[qubit_index])
                            else:
                                # Pauli-X gate
                                qc.x(qr[qubit_index])
                        else:
                            # Rotation around X axis
                            qc.rx(node.radians, qr[qubit_index])
                    elif node.node_type == node_types.Y:
                        if node.radians == 0:
                            if node.ctrl_a != -1:
                                # Controlled Y gate
                                qc.cy(qr[node.ctrl_a], qr[qubit_index])
                            else:
                                # Pauli-Y gate
                                qc.y(qr[qubit_index])
                        else:
                            # Rotation around Y axis
                            qc.ry(node.radians, qr[qubit_index])
                    elif node.node_type == node_types.Z:
                        if node.radians == 0:
                            if node.ctrl_a != -1:
                                # Controlled Z gate
                                qc.cz(qr[node.ctrl_a], qr[qubit_index])
                            else:
                                # Pauli-Z gate
                                qc.z(qr[qubit_index])
                        else:
                            if node.ctrl_a != -1:
                                # Controlled rotation around the Z axis
                                qc.crz(node.radians, qr[node.ctrl_a], qr[qubit_index])
                            else:
                                # Rotation around Z axis
                                qc.rz(node.radians, qr[qubit_index])
                    elif node.node_type == node_types.S:
                        # S gate
                        qc.s(qr[qubit_index])
                    elif node.node_type == node_types.SDG:
                        # S dagger gate
                        qc.sdg(qr[qubit_index])
                    elif node.node_type == node_types.T:
                        # T gate
                        qc.t(qr[qubit_index])
                    elif node.node_type == node_types.TDG:
                        # T dagger gate
                        qc.tdg(qr[qubit_index])
                    elif node.node_type == node_types.H:
                        if node.ctrl_a != -1:
                            # Controlled Hadamard
                            qc.ch(qr[node.ctrl_a], qr[qubit_index])
                        else:
                            # Hadamard gate
                            qc.h(qr[qubit_index])
                    elif node.node_type == node_types.SWAP:
                        if node.ctrl_a != -1:
                            # Controlled Swap
                            qc.cswap(qr[node.ctrl_a], qr[qubit_index], qr[node.swap])
                        else:
                            # Swap gate
                            qc.swap(qr[qubit_index], qr[node.swap])

        return qc


class CircuitGridNode:
    """
    Represents a node in the circuit grid
    A node is usually a gate.
    """

    def __init__(self, node_type, radians=0.0, ctrl_a=-1, ctrl_b=-1, swap=-1):
        self.node_type = node_type
        self.radians = radians
        self.ctrl_a = ctrl_a
        self.ctrl_b = ctrl_b
        self.swap = swap

    def __str__(self):
        string = 'type: ' + str(self.node_type)
        string += ', radians: ' + str(self.radians) if self.radians != 0 else ''
        string += ', ctrl_a: ' + str(self.ctrl_a) if self.ctrl_a != -1 else ''
        string += ', ctrl_b: ' + str(self.ctrl_b) if self.ctrl_b != -1 else ''
        return string
