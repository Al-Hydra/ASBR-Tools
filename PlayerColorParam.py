from PyBinaryReader.binary_reader import *
from xfbin_lib.xfbin import *
import json
file = r"C:\Users\Ali\Documents\GitHub\ASBR_Tools\PlayerColorParam.bin"

def read_color_param(file):

    with open(file, "rb") as f:
        filebytes = f.read()
    
    xfbin = read_xfbin(filebytes)

    chunks = xfbin.get_chunks_by_type('NuccChunkBinary')

    binary_data = chunks[0].data

    with BinaryReader(binary_data, Endian.LITTLE, 'cp932') as br:
        br.seek(4, 0)
        version = br.read_uint32()
        print(version)
        count = br.read_uint32()
        print(count)
        br.read_uint64()

        Colors = []
        Colors_dict = {}

        for i in range(count):
            pointer = br.read_uint64()
            current_pos = br.pos()
            br.seek(pointer - 8, 1)
            character_id = br.read_str(8)
            br.seek(current_pos, 0)
            costume_slot = br.read_uint32()
            r = br.read_uint32()
            g = br.read_uint32()
            b = br.read_uint32()

            Colors.append(Color(character_id, costume_slot, r, g, b))

            '''Colors_dict[i] = {
                "Character ID": character_id,
                "Costume Slot": costume_slot,
                "R": r,
                "G": g,
                "B": b
            }'''
    
    return Colors

def dump_color_param(Colors: dict):
    with open("PlayerColorParam.json", "w") as f:
        json.dump(Colors, f, indent=4)

def write_color_param(Colors: list, path):
    
    with BinaryReader(bytearray(), Endian.LITTLE, 'cp932') as br:
        version = br.write_uint32(1000)
        count = len(Colors)
        br.write_uint32(count)
        br.write_uint64(8) # pointer to first color

        color_buf = BinaryReader(bytearray(), Endian.LITTLE, 'cp932')
        string_buf = BinaryReader(bytearray(), Endian.LITTLE, 'cp932')

        for i in range(count):
            #get the color by the index
            color: Color = Colors[i]

            #let's calculate the pointer to the string
            pointer = (24 * count) - (16 * i)
            color_buf.write_uint64(pointer)
            color_buf.write_uint32(color.costume_slot)
            color_buf.write_uint32(color.r)
            color_buf.write_uint32(color.g)
            color_buf.write_uint32(color.b)

            #write the string to the string buffer
            string_buf.write_str_fixed(color.character_id, 8)

        
        br.extend(color_buf.buffer())
        br.seek(color_buf.size(), 1)
        br.extend(string_buf.buffer())

        
        xfbin = Xfbin()
        #xfbin.add_chunk(NuccChunkNull())

        binary_chunk: NuccChunkBinary = NuccChunkBinary("PlayerColorParam.bin", "PlayerColorParam")
        binary_chunk.binary_data = bytes(br.buffer())
        binary_chunk.has_data = True
        binary_chunk.has_props = True
        xfbin.add_chunk_page(binary_chunk)
        
        write_xfbin_to_path(xfbin, path)

class Color:
    def __init__(self, character_id, costume_slot, r, g, b):
        self.character_id = character_id
        self.costume_slot = costume_slot
        self.r = r
        self.g = g
        self.b = b

if __name__ == "__main__":
    '''Colors = read_color_param(file)
    dump_color_param(Colors)'''
    with open("PlayerColorParam.json", "r") as f:
        Colors = json.load(f)
    write_color_param(Colors)
