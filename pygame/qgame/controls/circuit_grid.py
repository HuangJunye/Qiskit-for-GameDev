#!/usr/bin/env python
#
# Copyright 2019 the original author or authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import numpy as np
from sympy import pi

import pygame

from ..model import circuit_node_types as node_types
from ..model.circuit_grid_model import CircuitGridNode
from ..utils.colors import *
from ..utils.navigation import *
from ..utils.resources import load_image
from ..utils.parameters import *


class CircuitGrid(pygame.sprite.RenderPlain):
    """Enables interaction with circuit"""

    def __init__(self, xpos, ypos, circuit_grid_model):
        self.xpos = xpos
        self.ypos = ypos
        self.circuit_grid_model = circuit_grid_model
        self.selected_qubit = 0
        self.selected_depth = 0
        self.circuit_grid_background = CircuitGridBackground(circuit_grid_model)
        self.circuit_grid_cursor = CircuitGridCursor()
        self.gate_tiles = np.empty((circuit_grid_model.qubit_count, circuit_grid_model.circuit_depth),
                                   dtype=CircuitGridGate)

        for row_idx in range(self.circuit_grid_model.qubit_count):
            for col_idx in range(self.circuit_grid_model.circuit_depth):
                self.gate_tiles[row_idx][col_idx] = \
                    CircuitGridGate(circuit_grid_model, row_idx, col_idx)

        pygame.sprite.RenderPlain.__init__(self, self.circuit_grid_background,
                                           self.gate_tiles,
                                           self.circuit_grid_cursor)
        self.update()

    def update(self, *args):

        sprite_list = self.sprites()
        for sprite in sprite_list:
            sprite.update()

        self.circuit_grid_background.rect.left = self.xpos
        self.circuit_grid_background.rect.top = self.ypos

        for row_idx in range(self.circuit_grid_model.qubit_count):
            for col_idx in range(self.circuit_grid_model.circuit_depth):
                self.gate_tiles[row_idx][col_idx].rect.centerx = \
                    self.xpos + GRID_WIDTH * (col_idx + 1.5)
                self.gate_tiles[row_idx][col_idx].rect.centery = \
                    self.ypos + GRID_HEIGHT * (row_idx + 1.0)

        self.highlight_selected_node(self.selected_qubit, self.selected_depth)

    def highlight_selected_node(self, qubit_index, depth_index):
        self.selected_qubit = qubit_index
        self.selected_depth = depth_index
        self.circuit_grid_cursor.rect.left = self.xpos + GRID_WIDTH * (self.selected_depth + 1) + round(
            0.375 * WIDTH_UNIT)
        self.circuit_grid_cursor.rect.top = self.ypos + GRID_HEIGHT * (self.selected_qubit + 0.5) + round(
            0.375 * WIDTH_UNIT)

    def reset_cursor(self):
        self.highlight_selected_node(0, 0)

    def display_exceptional_condition(self):
        # TODO: Make cursor appearance indicate condition such as unable to place a gate
        return

    def move_to_adjacent_node(self, direction):
        if direction == MOVE_LEFT and self.selected_depth > 0:
            self.selected_depth -= 1
        elif direction == MOVE_RIGHT and self.selected_depth < self.circuit_grid_model.circuit_depth - 1:
            self.selected_depth += 1
        elif direction == MOVE_UP and self.selected_qubit > 0:
            self.selected_qubit -= 1
        elif direction == MOVE_DOWN and self.selected_qubit < self.circuit_grid_model.qubit_count - 1:
            self.selected_qubit += 1

        self.highlight_selected_node(self.selected_qubit, self.selected_depth)

    def get_selected_node_gate_part(self):
        return self.circuit_grid_model.get_node_type(self.selected_qubit, self.selected_depth)

    def handle_input_x(self):
        # Add X gate regardless of whether there is an existing gate
        # circuit_grid_node = CircuitGridNode(node_types.X)
        # self.circuit_grid_model.set_node(self.selected_qubit, self.selected_depth, circuit_grid_node)

        # Allow deleting using the same key only
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part == node_types.EMPTY:
            circuit_grid_node = CircuitGridNode(node_types.X)
            self.circuit_grid_model.set_node(self.selected_qubit, self.selected_depth, circuit_grid_node)
        elif selected_node_gate_part == node_types.X:
            self.handle_input_delete()
        self.update()

    def handle_input_y(self):
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part == node_types.EMPTY:
            circuit_grid_node = CircuitGridNode(node_types.Y)
            self.circuit_grid_model.set_node(self.selected_qubit, self.selected_depth, circuit_grid_node)
        elif selected_node_gate_part == node_types.Y:
            self.handle_input_delete()
        self.update()

    def handle_input_z(self):
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part == node_types.EMPTY:
            circuit_grid_node = CircuitGridNode(node_types.Z)
            self.circuit_grid_model.set_node(self.selected_qubit, self.selected_depth, circuit_grid_node)
        elif selected_node_gate_part == node_types.Z:
            self.handle_input_delete()
        self.update()

    def handle_input_h(self):
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part == node_types.EMPTY:
            circuit_grid_node = CircuitGridNode(node_types.H)
            self.circuit_grid_model.set_node(self.selected_qubit, self.selected_depth, circuit_grid_node)
        elif selected_node_gate_part == node_types.H:
            self.handle_input_delete()
        self.update()

    def handle_input_delete(self):
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part == node_types.X or \
                selected_node_gate_part == node_types.Y or \
                selected_node_gate_part == node_types.Z or \
                selected_node_gate_part == node_types.H:
            self.delete_controls_for_gate(self.selected_qubit, self.selected_depth)

        if selected_node_gate_part == node_types.CTRL:
            gate_qubit_index = \
                self.circuit_grid_model.get_gate_qubit_for_control_node(self.selected_qubit,
                                                                            self.selected_depth)
            if gate_qubit_index >= 0:
                self.delete_controls_for_gate(gate_qubit_index,
                                              self.selected_depth)
        elif selected_node_gate_part != node_types.SWAP and \
                selected_node_gate_part != node_types.CTRL and \
                selected_node_gate_part != node_types.TRACE:
            circuit_grid_node = CircuitGridNode(node_types.EMPTY)
            self.circuit_grid_model.set_node(self.selected_qubit, self.selected_depth, circuit_grid_node)

        self.update()

    def handle_input_ctrl(self):
        # TODO: Handle Toffoli gates. For now, control qubit is assumed to be in ctrl_a variable
        #       with ctrl_b variable reserved for Toffoli gates
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part == node_types.X or \
                selected_node_gate_part == node_types.Y or \
                selected_node_gate_part == node_types.Z or \
                selected_node_gate_part == node_types.H:
            circuit_grid_node = self.circuit_grid_model.get_node(self.selected_qubit, self.selected_depth)
            if circuit_grid_node.ctrl_a is not None:
                # Gate already has a control qubit so remove it
                orig_ctrl_a = circuit_grid_node.ctrl_a
                circuit_grid_node.ctrl_a = None
                self.circuit_grid_model.set_node(self.selected_qubit, self.selected_depth, circuit_grid_node)

                # Remove TRACE nodes
                for qubit_index in range(min(self.selected_qubit, orig_ctrl_a) + 1,
                                      max(self.selected_qubit, orig_ctrl_a)):
                    if self.circuit_grid_model.get_node_type(qubit_index,
                                                                  self.selected_depth) == node_types.TRACE:
                        self.circuit_grid_model.set_node(qubit_index, self.selected_depth,
                                                         CircuitGridNode(node_types.EMPTY))
                self.update()
            else:
                # Attempt to place a control qubit beginning with the wire above
                if self.selected_qubit is not None:
                    if self.place_ctrl_qubit(self.selected_qubit, self.selected_qubit - 1) == -1:
                        if self.selected_qubit < self.circuit_grid_model.qubit_count:
                            if self.place_ctrl_qubit(self.selected_qubit, self.selected_qubit + 1) == -1:
                                print("Can't place control qubit")
                                self.display_exceptional_condition()

    def handle_input_move_ctrl(self, direction):
        # TODO: Handle Toffoli gates. For now, control qubit is assumed to be in ctrl_a variable
        #       with ctrl_b variable reserved for Toffoli gates
        # TODO: Simplify the logic in this method, including considering not actually ever
        #       placing a TRACE, but rather always dynamically calculating if a TRACE s/b displayed
        selected_node_gate_part = self.get_selected_node_gate_part()
        if selected_node_gate_part == node_types.X or \
                selected_node_gate_part == node_types.Y or \
                selected_node_gate_part == node_types.Z or \
                selected_node_gate_part == node_types.H:
            circuit_grid_node = self.circuit_grid_model.get_node(self.selected_qubit, self.selected_depth)
            if 0 <= circuit_grid_node.ctrl_a < self.circuit_grid_model.qubit_count:
                # Gate already has a control qubit so try to move it
                if direction == MOVE_UP:
                    candidate_qubit_index = circuit_grid_node.ctrl_a - 1
                    if candidate_qubit_index == self.selected_qubit:
                        candidate_qubit_index -= 1
                else:
                    candidate_qubit_index = circuit_grid_node.ctrl_a + 1
                    if candidate_qubit_index == self.selected_qubit:
                        candidate_qubit_index += 1
                if 0 <= candidate_qubit_index < self.circuit_grid_model.qubit_count:
                    if self.place_ctrl_qubit(self.selected_qubit, candidate_qubit_index) == candidate_qubit_index:
                        print("control qubit successfully placed on wire ", candidate_qubit_index)
                        if direction == MOVE_UP and candidate_qubit_index < self.selected_qubit:
                            if self.circuit_grid_model.get_node_type(candidate_qubit_index + 1,
                                                                          self.selected_depth) == node_types.EMPTY:
                                self.circuit_grid_model.set_node(candidate_qubit_index + 1, self.selected_depth,
                                                                 CircuitGridNode(node_types.TRACE))
                        elif direction == MOVE_DOWN and candidate_qubit_index > self.selected_qubit:
                            if self.circuit_grid_model.get_node_type(candidate_qubit_index - 1,
                                                                          self.selected_depth) == node_types.EMPTY:
                                self.circuit_grid_model.set_node(candidate_qubit_index - 1, self.selected_depth,
                                                                 CircuitGridNode(node_types.TRACE))
                        self.update()
                    else:
                        print("control qubit could not be placed on wire ", candidate_qubit_index)

    def handle_input_rotate(self, theta):
        circuit_grid_node = self.circuit_grid_model.get_node(self.selected_qubit, self.selected_depth)
        circuit_grid_node.rotate_node(theta)

        self.update()

    def place_ctrl_qubit(self, gate_qubit_index, candidate_ctrl_qubit_index):
        """Attempt to place a control qubit on a wire.
        If successful, return the wire number. If not, return -1
        """
        if candidate_ctrl_qubit_index < 0 or candidate_ctrl_qubit_index >= self.circuit_grid_model.qubit_count:
            return -1
        candidate_wire_gate_part = \
            self.circuit_grid_model.get_node_type(candidate_ctrl_qubit_index,
                                                       self.selected_depth)
        if candidate_wire_gate_part == node_types.EMPTY or \
                candidate_wire_gate_part == node_types.TRACE:
            circuit_grid_node = self.circuit_grid_model.get_node(gate_qubit_index, self.selected_depth)
            circuit_grid_node.ctrl_a = candidate_ctrl_qubit_index
            self.circuit_grid_model.set_node(gate_qubit_index, self.selected_depth, circuit_grid_node)
            self.circuit_grid_model.set_node(candidate_ctrl_qubit_index, self.selected_depth,
                                             CircuitGridNode(node_types.EMPTY))
            self.update()
            return candidate_ctrl_qubit_index
        else:
            print("Can't place control qubit on wire: ", candidate_ctrl_qubit_index)
            return -1

    def delete_controls_for_gate(self, gate_qubit_index, depth_index):
        control_a_qubit_index = self.circuit_grid_model.get_node(gate_qubit_index, depth_index).ctrl_a
        control_b_qubit_index = self.circuit_grid_model.get_node(gate_qubit_index, depth_index).ctrl_b

        # Choose the control wire (if any exist) furthest away from the gate wire
        control_a_wire_distance = 0
        control_b_wire_distance = 0
        if control_a_qubit_index is not None:
            control_a_wire_distance = abs(control_a_qubit_index - gate_qubit_index)
        if control_b_qubit_index is not None:
            control_b_wire_distance = abs(control_b_qubit_index - gate_qubit_index)

        control_qubit_index = None
        if control_a_wire_distance > control_b_wire_distance:
            control_qubit_index = control_a_qubit_index
        elif control_a_wire_distance < control_b_wire_distance:
            control_qubit_index = control_b_qubit_index

        if control_qubit_index is not None:
            # TODO: If this is a controlled gate, remove the connecting TRACE parts between the gate and the control
            # ALSO: Refactor with similar code in this method
            for wire_idx in range(min(gate_qubit_index, control_qubit_index),
                                  max(gate_qubit_index, control_qubit_index) + 1):
                print("Replacing wire ", wire_idx, " in column ", depth_index)
                circuit_grid_node = CircuitGridNode(node_types.EMPTY)
                self.circuit_grid_model.set_node(wire_idx, depth_index, circuit_grid_node)


class CircuitGridBackground(pygame.sprite.Sprite):
    """Background for circuit grid"""

    def __init__(self, circuit_grid_model):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([GRID_WIDTH * (18 + 2),
                                     GRID_HEIGHT * (3 + 1)])
        self.image.convert()
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, BLACK, self.rect, LINE_WIDTH)

        for qubit_index in range(circuit_grid_model.qubit_count):
            pygame.draw.line(self.image, BLACK,
                             (GRID_WIDTH * 0.5, (qubit_index + 1) * GRID_HEIGHT),
                             (self.rect.width - (GRID_WIDTH * 0.5), (qubit_index + 1) * GRID_HEIGHT),
                             LINE_WIDTH)


class CircuitGridGate(pygame.sprite.Sprite):
    """Images for nodes"""

    def __init__(self, circuit_grid_model, qubit_index, depth_index):
        pygame.sprite.Sprite.__init__(self)
        self.circuit_grid_model = circuit_grid_model
        self.qubit_index = qubit_index
        self.depth_index = depth_index

        self.update()

    def update(self):
        node_type = self.circuit_grid_model.get_node_type(self.qubit_index, self.depth_index)

        if node_type == node_types.H:
            self.image, self.rect = load_image('gate_images/h_gate.png', -1)
        elif (node_type == node_types.X) or (node_type == node_types.RX):
            node = self.circuit_grid_model.get_node(self.qubit_index, self.depth_index)
            if node.ctrl_a is not None or node.ctrl_b is not None:
                # This is a control-X gate or Toffoli gatex
                # TODO: Handle Toffoli gates more completely
                if self.qubit_index > max(node.ctrl_a, node.ctrl_b):
                    self.image, self.rect = load_image('gate_images/not_gate_below_ctrl.png', -1)
                else:
                    self.image, self.rect = load_image('gate_images/not_gate_above_ctrl.png', -1)
            elif node.theta != pi:
                self.image, self.rect = load_image('gate_images/rx_gate.png', -1)
                self.rect = self.image.get_rect()
                pygame.draw.arc(self.image, MAGENTA, self.rect, 0, node.theta % (2 * pi), 6)
                pygame.draw.arc(self.image, MAGENTA, self.rect, node.theta % (2 * pi), 2 * pi, 1)
            else:
                self.image, self.rect = load_image('gate_images/x_gate.png', -1)
        elif node_type == node_types.Y:
            node = self.circuit_grid_model.get_node(self.qubit_index, self.depth_index)
            if node.theta != pi:
                self.image, self.rect = load_image('gate_images/ry_gate.png', -1)
                self.rect = self.image.get_rect()
                pygame.draw.arc(self.image, MAGENTA, self.rect, 0, node.theta % (2 * pi), 6)
                pygame.draw.arc(self.image, MAGENTA, self.rect, node.theta % (2 * pi), 2 * pi, 1)
            else:
                self.image, self.rect = load_image('gate_images/y_gate.png', -1)
        elif node_type == node_types.Z:
            node = self.circuit_grid_model.get_node(self.qubit_index, self.depth_index)
            if node.theta != pi:
                self.image, self.rect = load_image('gate_images/rz_gate.png', -1)
                self.rect = self.image.get_rect()
                pygame.draw.arc(self.image, MAGENTA, self.rect, 0, node.theta % (2 * pi), 6)
                pygame.draw.arc(self.image, MAGENTA, self.rect, node.theta % (2 * pi), 2 * pi, 1)
            else:
                self.image, self.rect = load_image('gate_images/z_gate.png', -1)
        elif node_type == node_types.S:
            self.image, self.rect = load_image('gate_images/s_gate.png', -1)
        elif node_type == node_types.SDG:
            self.image, self.rect = load_image('gate_images/sdg_gate.png', -1)
        elif node_type == node_types.T:
            self.image, self.rect = load_image('gate_images/t_gate.png', -1)
        elif node_type == node_types.TDG:
            self.image, self.rect = load_image('gate_images/tdg_gate.png', -1)
        elif node_type == node_types.ID:
            # a completely transparent PNG is used to place at the end of the circuit to prevent crash
            # the game crashes if the circuit is empty
            self.image, self.rect = load_image('gate_images/transparent.png', -1)
        elif node_type == node_types.CTRL:
            # TODO: Handle Toffoli gates correctly
            if self.qubit_index > \
                    self.circuit_grid_model.get_gate_qubit_for_control_node(self.qubit_index, self.depth_index):
                self.image, self.rect = load_image('gate_images/ctrl_gate_bottom_wire.png', -1)
            else:
                self.image, self.rect = load_image('gate_images/ctrl_gate_top_wire.png', -1)
        elif node_type == node_types.TRACE:
            self.image, self.rect = load_image('gate_images/trace_gate.png', -1)
        elif node_type == node_types.SWAP:
            self.image, self.rect = load_image('gate_images/swap_gate.png', -1)
        else:
            self.image = pygame.Surface([GATE_TILE_WIDTH, GATE_TILE_HEIGHT])
            self.image.set_alpha(0)
            self.rect = self.image.get_rect()

        self.image.convert()


class CircuitGridCursor(pygame.sprite.Sprite):
    """Cursor to highlight current grid node"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('cursor_images/circuit-grid-cursor.png', -1)
        self.image.convert_alpha()
