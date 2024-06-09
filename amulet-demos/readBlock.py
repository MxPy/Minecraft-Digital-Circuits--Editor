import amulet
from amulet.utils.world_utils import block_coords_to_chunk_coords

# load the level
level = amulet.load_level("test")

# lets get the block at -12, -60, -3 which in the world I am testing in is a redstone torch.
x, y, z = -15, -60, -4

# Like with the previous level.get_version_block method there
# is a helper method to get the universal Block object.
# This method also adds a bit of overhead so is not
# great at scale but lets show how it works anyway.
universal_block = level.get_block(x, y, z, "minecraft:overworld")
# Block(universal_minecraft:piston_head[facing="up",short="false"])
print("==============================")
print(universal_block)
print("==============================")

# Lets look into what level.get_block actually does.
# first lets find which chunk the block is in.

cx, cz = block_coords_to_chunk_coords(x, z)
# 0, 1

# read in the chunk
chunk = level.get_chunk(cx, cz, "minecraft:overworld")

# note that level.get_block and level.get_chunk may raise ChunkLoadError or ChunkDoesNotExist
# wrap them in a try except block to handle the error.

# get the offset within the chunk.
offset_x, offset_z = x - 16 * cx, z - 16 * cz
# 9, 8

# chunk.blocks is a custom class designed to behave like an infinite height array.
# It stores a dictionary mapping sub-chunk location to a numpy array
# of size 16x16x16 which can be directly accessed and modified.
# It also implements __getitem__ and __setitem__ methods so that it can emulate numpy slicing behaviour.

# Get the runtime id of the block at a given location within the chunk.
block_id = chunk.blocks[offset_x, y, offset_z]
print("==============================")
print(block_id)
print("==============================")
# 79

# The block's runtime id for this level will remain constant while the level is open.
# Each new level will start with an empty block palette and it will be populated as each new block is found.

# Look up the runtime id in the block palette to find the universal block state.
universal_block = chunk.block_palette[block_id]
# Block(universal_minecraft:piston_head[facing="up",short="false"])
print("==============================")
print(universal_block)
print("==============================")

# We now have the universal block state. From the blockstate we can see that it is a piston head facing up that is fully extended.

# There may also be a block entity for this block
universal_block_entity = chunk.block_entities.get((9, 98, 24), None)
# None (there is not a block entity but that is okay)
print("==============================")
print(universal_block_entity)
print("==============================")

# If we want to modify this block state we must first convert it to a version of our choice
# We have the block state in Bedrock 1.16.210 format and there is no block entity in this format.
# The final boolean should always be False when converting from the universal format.

java_block, java_block_entity, java_extra = level.translation_manager.get_version(
    "java", (1, 20, 6)
).block.from_universal(universal_block, universal_block_entity)

print("==============================")
print(java_block, java_block_entity, java_extra)
print("==============================")
# Block(minecraft:piston_head[facing="up",short="false",type="normal"]), None, False
# We have the block state in Java 1.16.2 format and there is no block entity in this format.

# close the world
level.close()