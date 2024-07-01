import amulet
from amulet.utils.world_utils import block_coords_to_chunk_coords

level = amulet.load_level("C://Users//PC//AppData//Roaming//.minecraft//saves//test2")

x, y, z = -15, -60, -4

universal_block = level.get_block(x, y, z, "minecraft:overworld")

print("==============================")
print(universal_block)
print("==============================")