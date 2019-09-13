--[[
Copyright 2019 the original author or authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
--]]


--[[
TODO:
[] Address The inventory list "main" @ "current_player" doesn't exist error

[] Perhaps allow other swap qubit to be deleted directly, tracking back to the original gate
[] Identify debug logging strategy
[.] Increase time for tools to appear to 30 seconds.
[.] Make minecarts stay in-world (whitelist in xschem)
[.] Make sneak code into aux code
    [.] Modify help text to reflect aux key
    [] Ask "are you sure" before deleting entire circuit, or put in right-click dialog?
[.] Give more Q blocks,
    [] perhaps earning them by solving puzzles
[] Update world with updated help signs (for wire_extender_block and q_block)
[] Stop auto-rotations after one minute, or when leaving game

[] Open/close doors when circuit correct/incorrect
[] Register escape room door without altering door mod (check forum for replies)

[] Implement TLDR instructions at top of ? signs

[] put kets on basis states blocks
[] put Dirac blocks on wall plates
[] Put more code in "if door_pos then" (that obviates need for so many nil checks)
[] create separate puzzles for garden and escape rooms
[] refactor and modularize q_command
[] address Android fast mode == special/aux key

[] Display measurement on Bloch sphere
[] Shift tiny measurement symbols on results over one pixel to left

[] Incorporate Maddy Tod qubit-HSV mapping
[] Incorporate Maddy Tod Tic-Tac-Toe game

[] Automate replacing copper with bronze blocks? (Only have to replace the block under rotate tool)
[] Add link to Minetest Tutorial, and more in-world instructions on getting around Minetest
[] Copy to OpenQASM and put pointers to running it in IQX
    - (signing up for Q Experience), training, etc. as next steps
[] Don't allow bloch sphere blocks to be placed directly?
[] Check into readonly textarea instead of a table, see
    https://github.com/minetest/minetest/blob/ded5da780002c17f2079a1d8ea09eb923a3b5e8f/doc/lua_api.txt#L2122-L2127.
[] For the named gates like Hadamard it could be nice to have their name in the tooltips for searching
[] Make use of health indicator and design gameplay with mobs, etc.
[] Find out how to give players initial inventory, and/or to stock the chests
[] Create constants for tomography measurement bases
[] Change flags to have binary set/get methods
[] Create special q_command block mode with increased circuit size capabilities (by holding special key when placing?)
[] Standardize on naming conventions for help buttons. For example, h_gate_puzzle and h_gate_desc
[] Implement suggestions in this Minetest forum thread containing QiskitBlocks feedback:
    https://forum.minetest.net/viewtopic.php?f=49&t=23121
[] Make QiskitBlocks and puzzle map world available from `Content`>`Browse online content`
    dialog in Minetest

[] Work out how more accurate way of ascertaining which wires are entangled
[] Allow Bloch sphere blocks with a quantum state to be inserted in circuits
    - This would set the state of that place in the wire to the state of the block)
[] Allow Block sphere blocks with a quantum state to be removed and carried?
[] Create a freeform circuit building area that contains a chest with blocks,
    and instructions on how to use each block
[] Create the following areas
    [] Algorithm Shore
        [] Create a pedagogical progression of quantum algorithm circuits on Algorithm Shore
    [] Bureau of Random Walks
    [] Quantum Error Correction Facility (get input from James Wootton)
    [] OpenQASM examples https://github.com/Qiskit/openqasm/tree/master/examples
[] Create area that contains examples in https://community.qiskit.org/textbook/
[] Create mob, or player, that has a Bloch sphere head
    - Perhaps collapses on certain events, to two different states (e.g. happy / grumpy)
    - Health could be signified by quantum state
[] Perhaps only play music in morning and evening
[] Remove some variables such as state_tomography_basis from q_command:init,
    making state only stored in metadata and accessible via get/set methods?
[] Create Mars and Venus blocks for cat entanglement demo
[] Set spawn point at 225, 8.5, 75
[] Investigate punch_operable for rotate and control tools
[] Implement appropriate gate images for CRZ gate
[] Improve appearance of measurement results blocks
[] Ability for measurement block to actuate (e.g. turn on a light or open a door)
    [] Investigate use of http://mesecons.net/items.html for in-world activation and sensing
    [] Ability for measured output wire to feed into input of same circuit
\[] Tighten up circuit connector blocks and wire extension appearance and behavior
    [] Modify texture configuration on circuit connector blocks (M & F) so that they appear
	correct on the back side as well
    [] Make circuit extension M block item fall where it can easily be picked up
    [] Label M & F connectors with autogenerated labels in order of being placed
    [] Protect against orphaning wire extensions
    [] Set wire_extension itemstack count to 0 when deleting wire extension related elements
    [] Don't allow extenders to be placed on extensions.
    [] Prevent digging a wire connection block if wire extension exists
[] Implement classical registers and conditionals supported by OpenQASM
[] Implement games like Tiq Taq Toe (the following, or MTod's versions)
- https://quantumfrontiers.com/2019/07/15/tiqtaqtoe/
[] Prevent ket blocks from being deleted easily
    [] Right-clicking input ket flips to opposite state
[] Make rest of tools and blocks reach farther in non-creative mode
[] Create Alice and Bob mobs that coach the player in some small way
[] Create basement under the quantum circuits in the garden that show matrices/vectors/geometric interpretation of 2D vector spaces
[] SPECIAL-right-click make X/Y/Z gates automatically rotate clockwise
[] Check for pos x and z being nil instead of ~= 0 so that things don't break on pos x==0 or z==0
[] Prevent right-clicking on wire_extension_block after wire_extension exists
[] Don't allow creating circuit if already exists
[] Create an area where a mob does a quantum random walk
[] Display wire local state
[] Clicking basis state ellipse block shows a state vector display?
[] Create game environment with rooms that are significant in quantum computing history
[] Make arrow blocks (connector, extenders, etc.) point correct direction on all sides
[] Can liquid blocks have tooltip that shows probability and other info (e.g. amp & phase)?
[] Find better way of programmatically distinguishing (than leading underscore) between
    blocks that may reside on the circuit grid and those that may not
[] Filter inventory panel (e.g. hide rotation blocks)
[] Use JWootton terrain generation mod
[] Make |0> |1> labels on measure block on left & right
[] Remove circuit_gate group code
[] Understand and standardize on when to use colon, or dot, as function separator
[] Find alternative to hardcoding node name strings everywhere
[] Remove hearts from creative mode?
[] Update music and sounds
[] Create blocks (e.g. classical optimizer) to demonstrate variational algorithms
[] Should this warning be addressed?
	2019-06-29 08:11:11: WARNING[Main]: Irrlicht: PNG warning: iCCP: CRC error
[] Upgrade to latest version of Minetest & test QiskitBlocks

[] Address James Wootton comments
    It looks great! Here are a few comments on things that could be changed.
    • In the 'Bloch sphere' hints text at the beginning, there are a few instances of 'Block' instead of 'Bloch'
    • It would be good if the cat pictures changed from happy to sad. This would be difficult for the superpositions though, I suppose. Could you get the memory and use that to make the cat image flicker randomly? That could be used for the entangled case too.
    • Why does \Phi^- in the quantum garden have no measurement blocks? (and why does it still work?)
    • The fact that you only see Z basis probs means that some context is missed: such as the difference between \Phi^+ and \Phi^-. It would be good to have a box for X basis measurement. But I guess that would complicate checking to see whether a solution is correct. (edited)
    -----------
    Regarding the measurement thing, I have an idea (maybe for long-term implementation if the SF event is soon) (edited)
    • The current measurement blocks could be changed to be Z on one side and X on the other
    • The results blocks could be changed to have a different 'water level' on one side than the other
    This means you'd easily be able to see these two perspectives, just by walking around the circuit. And it would mean that the info for both is available at the same time, so the system and player can easily see when a puzzle is solved

[] Address feedback from users J & L:
    * The design of the game is visually appealing. It made us want to explore the world!
    * I love the music! It’s very relaxing and helped me focus on the experience. On the other hand, L would
    prefer something more cheerful!
    * When the game was first loaded, the room was very dark. It was probably because it took 86s to generate the map
    and 27s to calculate the light on my old MacBook Pro. Is there a way to add a little note for players suggesting to
    wait a moment for the map generation and light calculation?
    * Is there a way to show the keys for control at the beginning of the game? For me, WASD for moving and space to
    jump is very obvious. But L (who never plays games) had no idea about which keys to press to do anything at the
    beginning.
    * We like that there are instructions and a chest of tools in each area to start with. This helped us not to feel
    lost in each area, and ensured some continuity in the gaming experience. For this reason, we think it might be even
    better if the instructions and the chest were more obvious at the beginning (for example, by adding an arrow or make
    the introductory instruction block different from the other instruction blocks)
    * The use a wagon to move from the starting point to the garden is a great idea! However, in our case, the wagon
    wasn’t at the starting point. We don’t know what the reason for this is, and although we restarted the game a few
    times, the wagon never appeared.
    * It’s a good idea to have tutorials for all the different blocks at the starting point. But I think as it is now,
    it’s a bit overwhelming. Perhaps you could divide them in a few rooms, inserting in each case only the most relevant
    information. For example, starting with the essential blocks: first room with X, H and the measurement block; second
    room with CNOT; third room with Y, Z, Rx, Ry and Rz; fourth room with the rest. It would be good to tell the players
    it’s not necessary to complete all the rooms before starting the games. They can come back any time when in doubt.
    * There are <invalid wstrings> in the instruction boxes for X, Y and Z at the starting point
    * In general, we think the instructions are too long and too technical for kids to understand (L had trouble to
    follow at times, and by the time she reached the end of an explanation, she had forgotten the beginning and the aim of the stage!). We suggest to shorten them to one paragraph and to simplify the language.
    There are also too many blocks in the chest. Maybe you could place only blocks that are useful for each area/stage.
    Players would be less confused about which ones to choose.
    * The measurement outcome for a qubit with H gate seems to have skewed probability to 1 and less often 0. Is it my
    illusion?
    * I think it’s a good idea to have an option to reset the circuit. When we started the game, we had no idea what to
    do and accidentally destroyed some pre-placed blocks.
    * Use gloomy/happy cat to represent 0/1 is a lovely idea, much more appropriate for kids than dead/alive. The
    representation of measurement probability as liquid level is very visual and intuitive.
    * In general, we find that the game is too instructive. It felt more like a tutorial than a game. It would be better
    if you could divide the circuits in the garden/cat sandbox into individual rooms, so that the player feels like
    moving forward and overcoming challenges! Each puzzle would allow the player to move to the next room. When the
    puzzle is solved, visual or sound effects to congratulate the player would make it more exciting too, as the door to
    the next puzzle opens. In this way, instead of a detailed set of instructions before the puzzle is solved, a very
    brief hint could be given as the player enters each new room and the explanation be shown only after the puzzle is
    solved to consolidate the knowledge while leaving space for exploration. Also, each puzzle could have a name, that
    indicates the concept you’ll be learning.

[] Address feedback from Elisa:
    - Please provide some basics for people that have not played minecraft before! I got really lost in the beginning.
    First I had to figure out how to walk, but that was still ok since pressing esc gives the most important keys
    (some missing though, would be good to have a list of all of them!). However, then I dropped the Hadamard gate and
    was not able to get it back into my inventory. I started walking around to look for another chest and fell into a
    cave that I did not manage to get out. Eventually I had a friend helping me, explaining the basics like how to pick
    up things by klicking for a looong time on them, chopping wood and turning it into an axe, putting blocks of wood
    below me while jumping to get out of that cave etc. I guess I’m much more unskilled in computer games than the
    average physicist, but still I think it would be good to have a short introduction into the basics.
    - I noticed that most of the puzzles I tried were not really puzzles, as it is not clear (at least to me) what you
    have to do unless you read the hints (e.g. the CNOT gate puzzle), which already tell you exactly which gate to place
    where. I think it would be much better if they would tell you to reach a specific state (which was actually the case
    for the Hadamard and X gates-puzzle, but for none of the other puzzles I have tried) and then you can either try by
    yourself or read the hints. So my suggestion would be to have a big sign on top of each puzzle that tells you which
    state you want to reach and maybe gives some limitations on which gates you are allowed to use? The hints could then
    still be there to give additional help
    - I have seen a couple of times <invalid wstring> , where some parts of the sentence were missing. I can check again, but I think that happened mostly in the Bell states hints.
    - From what I can see (some parts are missing because of the invalid wstrings), in the hints for |psi^-> the task is to build an equal superposition of |01> and |10> with opposite phases. It’s only allowed to get |10> - |01> though, while |01> - |10> is considered wrong. Maybe one should in general program it in a way that global phases do not matter?
    - The cave I mentioned earlier that I fell in actually has some quantum circuit, where it was not clear to me whether this is considered decoration or whether there is a task that I have to solve. Maybe it will become clearer if I just play a bit more though
    - That is all I got for now, I will let you know if I notice anything else once I played a bit more! Btw I am sorry for only pointing out the negative points now, my overall experience was definitely positive! I really think that this is a great idea and has lots of potential to attract people to play with quantum gates!! Also that friend who knows minecraft and helped me out loved it! For my taste it could involve more riddles, but maybe I have not played enough yet to get there

Periodic TODO:
[] Verify lines in dialog boxes are max 73 chars
[] Keep used mods updated from https://github.com/minetest-game-mods

Each release TODO if world was modified:
[] Replace copper blocks with bronze blocks under spinning tools
    [] Automate this
[] Run xschemsave & copy two files
--]]

LOG_DEBUG = false
MAX_C_IF_WIRES = 7

dofile(minetest.get_modpath("circuit_blocks").."/circuit_blocks.lua");
dofile(minetest.get_modpath("circuit_blocks").."/circuit_node_types.lua");

minetest.register_node("circuit_blocks:_qubit_0", {
    description = "Qubit 0 block",
    tiles = {"circuit_blocks_qubit_0.png"},
    groups = {oddly_breakable_by_hand=2},
	paramtype2 = "facedir"
})

minetest.register_node("circuit_blocks:_qubit_1", {
    description = "Qubit 1 block",
    tiles = {"circuit_blocks_qubit_1.png"},
    groups = {oddly_breakable_by_hand=2},
	paramtype2 = "facedir"
})

minetest.register_node("circuit_blocks:_alice_cat_0", {
    description = "Alice cat grumpy block",
    tiles = {"circuit_blocks_alice_cat_0.png"},
    groups = {oddly_breakable_by_hand=2},
	paramtype2 = "facedir"
})

minetest.register_node("circuit_blocks:_alice_cat_1", {
    description = "Alice cat happy block",
    tiles = {"circuit_blocks_alice_cat_1.png"},
    groups = {oddly_breakable_by_hand=2},
	paramtype2 = "facedir"
})

minetest.register_node("circuit_blocks:_bob_cat_0", {
    description = "Bob cat grumpy block",
    tiles = {"circuit_blocks_bob_cat_0.png"},
    groups = {oddly_breakable_by_hand=2},
	paramtype2 = "facedir"
})

minetest.register_node("circuit_blocks:_bob_cat_1", {
    description = "Bob cat happy block",
    tiles = {"circuit_blocks_bob_cat_1.png"},
    groups = {oddly_breakable_by_hand=2},
	paramtype2 = "facedir"
})

minetest.register_tool("circuit_blocks:control_tool", {
	description = "Control tool",
	inventory_image = "circuit_blocks_control_tool.png",
	wield_image = "circuit_blocks_control_tool.png",
	wield_scale = { x = 1, y = 1, z = 1 },
	range = 16,
	tool_capabilities = {},
})

minetest.register_tool("circuit_blocks:rotate_tool", {
	description = "Rotate tool",
	inventory_image = "circuit_blocks_rotate_tool.png",
	wield_image = "circuit_blocks_rotate_tool.png",
	wield_scale = { x = 1, y = 1, z = 1 },
	range = 16,
	tool_capabilities = {},
})

minetest.register_tool("circuit_blocks:swap_tool", {
	description = "Swap tool",
	inventory_image = "circuit_blocks_swap_tool.png",
	wield_image = "circuit_blocks_swap_tool.png",
	wield_scale = { x = 1, y = 1, z = 1 },
	range = 16,
	tool_capabilities = {},
})


circuit_blocks:register_circuit_block(CircuitNodeTypes.EMPTY, false, false, 0, false)

circuit_blocks:register_circuit_block(CircuitNodeTypes.X, false, false, 16, true)
circuit_blocks:register_circuit_block(CircuitNodeTypes.X, true, true, 16, true)
circuit_blocks:register_circuit_block(CircuitNodeTypes.X, true, false, 16, true)
circuit_blocks:register_circuit_block(CircuitNodeTypes.X, false, true, 16, true)

circuit_blocks:register_circuit_block(CircuitNodeTypes.H, false, false, 0, true)
circuit_blocks:register_circuit_block(CircuitNodeTypes.H, true, false, 0, true)
circuit_blocks:register_circuit_block(CircuitNodeTypes.H, false, true, 0, true)

circuit_blocks:register_circuit_block(CircuitNodeTypes.Y, false, false, 16, true)
circuit_blocks:register_circuit_block(CircuitNodeTypes.Y, true, false, 16, true)
circuit_blocks:register_circuit_block(CircuitNodeTypes.Y, false, true, 16, true)

circuit_blocks:register_circuit_block(CircuitNodeTypes.Z, false, false, 16, true)
circuit_blocks:register_circuit_block(CircuitNodeTypes.Z, true, false, 16, true)
circuit_blocks:register_circuit_block(CircuitNodeTypes.Z, false, true, 16, true)

circuit_blocks:register_circuit_block(CircuitNodeTypes.SWAP, false, false, 0, true, "", "")
circuit_blocks:register_circuit_block(CircuitNodeTypes.SWAP, true, false, 0, true, "", "")
circuit_blocks:register_circuit_block(CircuitNodeTypes.SWAP, false, true, 0, true, "", "")
circuit_blocks:register_circuit_block(CircuitNodeTypes.SWAP, false, false, 0, true, "", "_mate")
circuit_blocks:register_circuit_block(CircuitNodeTypes.SWAP, true, false, 0, true, "", "_mate")
circuit_blocks:register_circuit_block(CircuitNodeTypes.SWAP, false, true, 0, true, "", "_mate")

circuit_blocks:register_circuit_block(CircuitNodeTypes.S, false, false, 0, true)
circuit_blocks:register_circuit_block(CircuitNodeTypes.SDG, false, false, 0, true)
circuit_blocks:register_circuit_block(CircuitNodeTypes.T, false, false, 0, true)
circuit_blocks:register_circuit_block(CircuitNodeTypes.TDG, false, false, 0, true)

circuit_blocks:register_circuit_block(CircuitNodeTypes.CTRL, true, true, 0, false, "", "")
circuit_blocks:register_circuit_block(CircuitNodeTypes.CTRL, true, false, 0, false, "", "")
circuit_blocks:register_circuit_block(CircuitNodeTypes.CTRL, false, true, 0, false, "", "")
circuit_blocks:register_circuit_block(CircuitNodeTypes.CTRL, true, true, 0, false, "", "_b")
circuit_blocks:register_circuit_block(CircuitNodeTypes.CTRL, true, false, 0, false, "", "_b")
circuit_blocks:register_circuit_block(CircuitNodeTypes.CTRL, false, true, 0, false, "", "_b")

circuit_blocks:register_circuit_block(CircuitNodeTypes.TRACE, false, false, 0, false)
circuit_blocks:register_circuit_block(CircuitNodeTypes.BARRIER, false, false, 0, false)

circuit_blocks:register_circuit_block(CircuitNodeTypes.MEASURE_Z, false, false, 0, false,"", "z")
circuit_blocks:register_circuit_block(CircuitNodeTypes.MEASURE_Z, false, false, 0, false,"","0")
circuit_blocks:register_circuit_block(CircuitNodeTypes.MEASURE_Z, false, false, 0, false, "","1")
circuit_blocks:register_circuit_block(CircuitNodeTypes.MEASURE_Z, false, false, 0, false, "","alice_cat")
circuit_blocks:register_circuit_block(CircuitNodeTypes.MEASURE_Z, false, false, 0, false, "","bob_cat")
circuit_blocks:register_circuit_block(CircuitNodeTypes.MEASURE_Z, false, false, 0, false, "","alice_cat_0")
circuit_blocks:register_circuit_block(CircuitNodeTypes.MEASURE_Z, false, false, 0, false, "","alice_cat_1")
circuit_blocks:register_circuit_block(CircuitNodeTypes.MEASURE_Z, false, false, 0, false, "","bob_cat_0")
circuit_blocks:register_circuit_block(CircuitNodeTypes.MEASURE_Z, false, false, 0, false, "","bob_cat_1")

circuit_blocks:register_circuit_block(CircuitNodeTypes.CONNECTOR_M, false, false, 0, false, "q_command:wire_extension_block")

circuit_blocks:register_circuit_block(CircuitNodeTypes.QUBIT_BASIS, false, false, 0, true,"","qubit_0")
circuit_blocks:register_circuit_block(CircuitNodeTypes.QUBIT_BASIS, false, false, 0, true,"","qubit_1")

local ROTATION_RESOLUTION = 32
for idx = 0, ROTATION_RESOLUTION do
    circuit_blocks:register_circuit_block(CircuitNodeTypes.X, false, false, idx, true)
    circuit_blocks:register_circuit_block(CircuitNodeTypes.Y, false, false, idx, true)
    circuit_blocks:register_circuit_block(CircuitNodeTypes.Z, false, false, idx, true)
end

for y_rot = 0, 8 do
    for z_rot = 0, 15 do
        circuit_blocks:register_circuit_block(CircuitNodeTypes.BLOCH_SPHERE, false, false, 0, false, "", "", y_rot, z_rot)
        circuit_blocks:register_circuit_block(CircuitNodeTypes.COLOR_QUBIT, false, false, 0, false, "", "", y_rot, z_rot)
    end
end

-- Create blank and entangled Block spheres
circuit_blocks:register_circuit_block(CircuitNodeTypes.BLOCH_SPHERE, false, false, 0, false, "", "blank", nil, nil)
circuit_blocks:register_circuit_block(CircuitNodeTypes.BLOCH_SPHERE, false, false, 0, false, "", "entangled", nil, nil)

-- Create blank and entangled color qubits spheres
circuit_blocks:register_circuit_block(CircuitNodeTypes.COLOR_QUBIT, false, false, 0, false, "", "blank", nil, nil)
circuit_blocks:register_circuit_block(CircuitNodeTypes.COLOR_QUBIT, false, false, 0, false, "", "entangled", nil, nil)

-- Create classical if blocks
for wire_idx = 0, MAX_C_IF_WIRES - 1 do
    for eq_val = 0, 1 do
        circuit_blocks:register_circuit_block(CircuitNodeTypes.C_IF, false, false,
                0, false, "", "c" .. tostring(wire_idx) .. "_eq" .. tostring(eq_val))
    end
end