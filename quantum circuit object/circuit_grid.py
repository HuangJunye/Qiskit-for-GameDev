import numpy as np
import math

import circuit_node_types as node_types


class CircuitGridModel:
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
                self.set_node(qubit_index, depth_index, CircuitGridNode(node_types.EMPTY))

        self.threshold = 0.0001

    def __str__(self):
        gate_array_string = ''
        for qubit_index in range(self.qubit_count):
            gate_array_string += '\n'
            for depth_index in range(self.circuit_depth):
                gate_array_string += str(self.get_node_type(qubit_index, depth_index)) + ', '
        return f'CircuitGridModel: {gate_array_string}'

    def set_node(self, qubit_index, depth_index, circuit_grid_node):
        self.circuit_grid[qubit_index][depth_index] = \
            CircuitGridNode(circuit_grid_node.node_type,
                            circuit_grid_node.radians,
                            circuit_grid_node.ctrl_a,
                            circuit_grid_node.ctrl_b,
                            circuit_grid_node.swap)

    def get_node(self, qubit_index, depth_index):
        return self.circuit_grid[qubit_index][depth_index]

    def get_node_type(self, qubit_index, depth_index):
        requested_node = self.circuit_grid[qubit_index][depth_index]
        if requested_node and requested_node.node_type != node_types.EMPTY:
            # Node is occupied so return its gate
            return requested_node.node_type
        else:
            # Check for control nodes from gates in other nodes in this column
            nodes_in_column = self.circuit_grid[:, depth_index]
            for idx in range(self.qubit_count):
                if idx != qubit_index:
                    other_node = nodes_in_column[idx]
                    if other_node:
                        if other_node.ctrl_a == qubit_index or other_node.ctrl_b == qubit_index:
                            return node_types.CTRL
                        elif other_node.swap == qubit_index:
                            return node_types.SWAP

        return node_types.EMPTY

    def get_gate_qubit_for_control_node(self, control_qubit_index, depth_index):
        """Get qubit index for gate that belongs to a control node on the given qubit"""
        gate_qubit_index = -1
        nodes_in_column = self.circuit_grid[:, depth_index]
        for qubit_index in range(self.qubit_count):
            if qubit_index != control_qubit_index:
                other_node = nodes_in_column[qubit_index]
                if other_node:
                    if other_node.ctrl_a == control_qubit_index or \
                            other_node.ctrl_b == control_qubit_index:
                        gate_qubit_index = qubit_index
                        print(f'Found gate: {self.get_node_type(gate_qubit_index, depth_index)} '
                              f'on wire: {gate_qubit_index}')
        return gate_qubit_index

    def qasm_for_normal_node(self, node_type, qubit_index):
        return f'{node_type} q[{qubit_index}];'


    def qasm_for_controllable_node(self, circuit_grid_node, qubit_index):
        node_type = circuit_grid_node.node_type
        ctrl_a = circuit_grid_node.ctrl_a

        if ctrl_a == -1:
            # normal gate
            qasm_str = f'{node_type} q[{qubit_index}];'
        else:
            # controlled gate
            qasm_str = f'c{node_type} q[{ctrl_a}], q[{qubit_index}];'
        return qasm_str

    def qasm_for_rotatable_node(self, circuit_grid_node, qubit_index):
        node_type = circuit_grid_node.node_type
        radians = circuit_grid_node.radians

        qasm_str = f'r{node_type}({radians}) q[{qubit_index}];'
        return qasm_str

    def create_qasm_for_node(self, circuit_grid_node, qubit_index):
        qasm_str = ""
        node_type = circuit_grid_node.node_type
        radians = circuit_grid_node.radians
        ctrl_a = circuit_grid_node.ctrl_a
        ctrl_b = circuit_grid_node.ctrl_b
        swap = circuit_grid_node.swap

        if node_type in node_types.normal_nodes:
            # identity gate
            qasm_str += self.qasm_for_normal_node(node_type, qubit_index)
        elif node_type == node_types.X or \
                node_type == node_types.Y or \
                node_type == node_types.Z:
            # X, Y, Z gate
            if abs(radians - math.pi) <= self.threshold:
                qasm_str += self.qasm_for_controllable_node(circuit_grid_node, qubit_index)
            else:
                qasm_str += self.qasm_for_rotatable_node(circuit_grid_node, qubit_index)
        elif node_type == node_types.H:
            # Hadamard gate
            qasm_str += self.qasm_for_normal_node(node_type, qubit_index)
        return qasm_str

    def create_qasm_for_circuit(self):
        qasm_str = 'OPENQASM 2.0;include "qelib1.inc";'  # include header
        qasm_str += f'qreg q[{self.qubit_count}];'  # define quantum registers
        qasm_str += 'id q;'  # add a column of identity gates to protect simulators from an empty circuit

        for depth_index in range(self.circuit_depth):
            for qubit_index in range(self.qubit_count):
                qasm_str += self.create_qasm_for_node(self.circuit_grid[qubit_index][depth_index], qubit_index)
        return qasm_str

    def reset_circuit(self):
        self.circuit_grid = np.empty((self.qubit_count, self.circuit_depth), dtype=CircuitGridNode)


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
        string = f'type: {self.node_type}'
        string += f', radians: {self.radians}' if self.radians != 0 else ''
        string += f', ctrl_a: {self.ctrl_a}' if self.ctrl_a != -1 else ''
        string += f', ctrl_b: {self.ctrl_b}' if self.ctrl_b != -1 else ''
        return string
