import numpy as np
from sympy import pi

from qiskit import QuantumCircuit

from . import circuit_node_types
import logging

THRESHOLD = 0.0001


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
                self.set_node(qubit_index, depth_index, CircuitGridNode(circuit_node_types.EMPTY))

    def __str__(self):
        gate_array_string = ''
        for qubit_index in range(self.qubit_count):
            gate_array_string += '\n'
            for depth_index in range(self.circuit_depth):
                gate_array_string += f'{self.get_node_type(qubit_index, depth_index)}, '
        return f'CircuitGridModel: {gate_array_string}'

    def set_node(self, qubit_index, depth_index, circuit_grid_node):
        circuit_grid_node.qubit_index = qubit_index # overwrite node qubit_index
        ctrl_a = circuit_grid_node.ctrl_a
        ctrl_b = circuit_grid_node.ctrl_b
        self.circuit_grid[qubit_index][depth_index] = circuit_grid_node

        if ctrl_a is not None:
            self.circuit_grid[ctrl_a][depth_index] = CircuitGridNode(circuit_node_types.CTRL, ctrl_a)

        if ctrl_b is not None:
            self.circuit_grid[ctrl_b][depth_index] = CircuitGridNode(circuit_node_types.CTRL, ctrl_b)

    def get_node(self, qubit_index, depth_index):
        return self.circuit_grid[qubit_index][depth_index]

    def get_node_type(self, qubit_index, depth_index):
        requested_node = self.circuit_grid[qubit_index][depth_index]
        if requested_node and requested_node.node_type != circuit_node_types.EMPTY:
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
                            return circuit_node_types.CTRL
                        elif other_node.swap == qubit_index:
                            return circuit_node_types.SWAP

        return circuit_node_types.EMPTY

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
                        logging.info(f'Found gate: {self.get_node_type(gate_qubit_index, depth_index)} '
                              f'on qubit: {gate_qubit_index}')
        return gate_qubit_index

    def create_qasm_for_circuit(self):
        qasm_str = 'OPENQASM 2.0;include "qelib1.inc";'  # include header
        qasm_str += f'qreg q[{self.qubit_count}];'  # define quantum registers
        qasm_str += f'creg c[{self.qubit_count}];'  # define classical registers
        # add a column of identity gates to protect simulators from an empty circuit
        qasm_str += 'id q;'

        for depth_index in range(self.circuit_depth):
            for qubit_index in range(self.qubit_count):
                qasm_str += self.circuit_grid[qubit_index][depth_index].qasm()
        return qasm_str

    def compute_circuit(self):
        qasm_str = self.create_qasm_for_circuit()
        print(qasm_str)
        circuit = QuantumCircuit.from_qasm_str(qasm_str)
        return circuit

    def reset_circuit(self):
        self.circuit_grid = np.empty((self.qubit_count, self.circuit_depth), dtype=CircuitGridNode)


class CircuitGridNode:
    """
    Represents a node in the circuit grid
    A node is usually a gate.
    """

    def __init__(self, node_type, qubit_index=None, theta=pi, phi=None, lam=None,
                                        ctrl_a=None, ctrl_b=None, swap=None):
        self.node_type = node_type
        self.qubit_index = qubit_index
        self.theta = theta
        self.phi = phi
        self.lam = lam
        self.ctrl_a = ctrl_a
        self.ctrl_b = ctrl_b
        self.swap = swap
        self.update_node_type()

    def __str__(self):
        string = f'type: {self.node_type}'
        string += f', qubit index: {self.qubit_index}' if self.qubit_index is not None else ''
        string += f', theta: {self.theta}' if self.theta is not None else ''
        string += f', phi: {self.phi}' if self.phi is not None else ''
        string += f', lam: {self.lam}' if self.lam is not None else ''
        string += f', ctrl_a: {self.ctrl_a}' if self.ctrl_a is not None else ''
        string += f', ctrl_b: {self.ctrl_b}' if self.ctrl_b is not None else ''
        string += f', swap: {self.swap}' if self.swap is not None else ''
        return string

    def update_node_type(self):
        self.rotate_node(self.theta)
        self.add_control_node(self.ctrl_a)
        self.add_control_control_node(self.ctrl_a, self.ctrl_b)
        return

    def rotate_node(self, theta):
        theta = (self.theta + theta) % (2 * pi)

        if (self.node_type in circuit_node_types.rotatable_nodes) \
                                or (self.node_type in circuit_node_types.rotated_nodes):
            self.theta = theta

            if theta != pi:
                if self.node_type in circuit_node_types.rotatable_nodes:
                    print('add r')
                    self.node_type = f'r{self.node_type}'
            else:
                if self.node_type in circuit_node_types.rotated_nodes:
                    print('remove r')
                    self.node_type = self.node_type.replace('r', '')  # remove r

    def add_control_node(self, ctrl_a):
        if (self.node_type in circuit_node_types.controllable_nodes) \
                                or (self.node_type in circuit_node_types.controlled_nodes):
            self.ctrl_a = ctrl_a
            if ctrl_a is not None:
                if self.node_type not in circuit_node_types.controlled_nodes:
                    self.node_type = f'c{self.node_type}'
        #else:
            #self.ctrl_a = None
            #logging.warning(f'"{self.node_type}" gate cannot be controlled!')

    def add_control_control_node(self, ctrl_a, ctrl_b):
        if (self.node_type in circuit_node_types.ccxable_nodes) \
                                or (self.node_type in circuit_node_types.ccxed_nodes):
            self.ctrl_a = ctrl_a
            self.ctrl_b = ctrl_b
            if (ctrl_a is not None) and (ctrl_b is not None):
                if self.node_type != circuit_node_types.CCX:
                    self.node_type = circuit_node_types.CCX
        #else:
            #self.ctrl_b = None
            #logging.warning(f'"{self.node_type}" gate cannot be converted to CCX gate!')

    def qasm(self):
        """generate qasm for the node"""
        # no qasm for null nodes: empty and control nodes
        if self.node_type in circuit_node_types.null_nodes:
            return ''

        # for measurement
        if self.node_type == circuit_node_types.MEASURE_Z:
            return f'{self.node_type} q[{self.qubit_index}] -> c[{self.qubit_index}];'

        # rotation angle parameters
        rotation = ''
        if self.theta != pi:
            rotation += f'{self.theta}'
            if self.phi is not None:
                rotation += f',{self.phi}'
                if self.lam is not None:
                    rotation += f',{self.lam}'
        else:
            rotation = None

        # qubit indices
        qubits = ''
        if self.ctrl_a is not None:
            qubits += f'q[{self.ctrl_a}],'
            if self.ctrl_b is not None:
                qubits += f'q[{self.ctrl_b}],'
        if self.swap is not None:
            qubits += f'q[{self.swap}],'

        qubits += f'q[{self.qubit_index}]'

        if rotation:
            qasm_str = f'{self.node_type}({rotation}) {qubits};'
        else:
            qasm_str = f'{self.node_type} {qubits};'

        return qasm_str
