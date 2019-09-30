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
EMPTY = 'e'

ID = 'id'  # identity gate

X = 'x'  # Pauli gate: bit-flip
Y = 'y'  # Pauli gate: bit and phase flip
Z = 'z'  # Pauli gate: phase flip

H = 'h'  # Clifford gate: Hadamard gate
S = 's'  # Clifford gate: sqrt(Z) phase gate
SDG = 'sdg'  # Clifford gate: conjugate of sqrt(Z)
T = 't'  # C3 gate: sqrt(S) phase gate
TDG = 'tdg'  # C3 gate: conjugate of sqrt(S)

U1 = 'u1'
U2 = 'u2'
U3 = 'u3'

RX = 'rx'
RY = 'ry'
RZ = 'rz'

CX = 'cx'
CY = 'cy'
CZ = 'cz'
CH = 'ch'

CRZ = 'crz'

CU1 = 'cu1'
CU3 = 'cu3'

CCX = 'ccx'

SWAP = 'swap'
CSWAP = 'cswap'

BARRIER = 'barrier'
MEASURE_Z = 'measure'
RESET = 'reset'
IF = 'if'

CTRL = 'ct'  # "control" part of multi-qubit gate
TRACE = 'tr'  # In the path between a gate part and a "control" or "swap" part

null_nodes = [
    EMPTY,
    CTRL
]

normal_nodes = [
    ID,
    X,
    Y,
    Z,
    H,
    S,
    SDG,
    T,
    TDG,
    BARRIER,
    RESET
]

controllable_nodes = [
    H,
    X,
    Y,
    Z,
    RZ,
    U1,
    U3,
    SWAP
]

controlled_nodes = [
    CH,
    CX,
    CY,
    CZ,
    CRZ,
    CU1,
    CU3,
    CSWAP
]

ccxable_nodes = [
    X,
    CX
]

ccxed_nodes = [
    CCX
]

rotatable_nodes = [
    X,
    Y,
    Z
]

rotated_nodes = [
    RX,
    RY,
    RZ,
    U1,
    U2,
    U3,
    CU1,
    CU3,
    CRZ
]
