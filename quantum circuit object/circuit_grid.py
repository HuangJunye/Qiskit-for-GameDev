import numpy as np

import circuit_node_types


class CircuitGrid:
    """
    Grid-based model that is built when user interacts with circuit
    """

    def __init__(self, qubit_count, circuit_depth):
        self.qubit_count = qubit_count
        self.circuit_depth = circuit_depth
        self.circuit_grid = np.empty((qubit_count, circuit_depth), dtype=CircuitGridNode)
        # initialize empty circuit_grid
        for depth_index in range(self.circuit_depth):
            for qubit_index in range(self.qubit_count):
                self.set_node(qubit_index, depth_index, CircuitGridNode(circuit_node_types.EMPTY))


    def set_node(self, qubit_index, depth_index, circuit_grid_node):
        self.circuit_grid[qubit_index][depth_index] = \
            CircuitGridNode(circuit_grid_node.node_type,
                            circuit_grid_node.radians,
                            circuit_grid_node.ctrl_a,
                            circuit_grid_node.ctrl_b,
                            circuit_grid_node.swap)

    def get_node(self, qubit_index, depth_index):
        return self.circuit_grid[qubit_index][depth_index]

    def create_qasm_for_node(self, circuit_grid_node, qubit_index):
        qasm_str = ""
        node_type = circuit_grid_node.node_type
        if node_type == circuit_node_types.IDEN:
            # identity gate
            qasm_str = qasm_str + 'id q[' + str(qubit_index) + '];'
        elif node_type == circuit_node_types.X or \
                node_type == circuit_node_types.Y or \
                node_type == circuit_node_types.Z:
            # X, Y, Z gate
            qasm_str = qasm_str + node_type + ' q[' + str(qubit_index) + '];'
        elif node_type == circuit_node_types.H:
            # Hadamard gate
            qasm_str = qasm_str + node_type + ' q[' + str(qubit_index) + '];'

        return qasm_str

    def create_qasm_for_circuit(self):
        # include header
        qasm_str = 'OPENQASM 2.0;include "qelib1.inc";'

        # define quantum registers
        qasm_str = qasm_str + 'qreg q[' + str(self.qubit_count) + '];'

        # add a column of identity gates to protect simulators from an empty circuit
        qasm_str = qasm_str+'id q;'

        for depth_index in range(self.circuit_depth):
            for qubit_index in range(self.qubit_count):
                qasm_str = qasm_str + self.create_qasm_for_node(self.circuit_grid[qubit_index][depth_index], qubit_index)
        return qasm_str


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
