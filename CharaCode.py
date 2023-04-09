from PyBinaryReader.binary_reader import *
from xfbin_lib.xfbin import *

class Character:
    def __init__(self) -> None:
        self.code = None
        self.index = None

def read_chara_code(file):
    with open(file, "rb") as f:
        filebytes = f.read()
    
    xfbin = read_xfbin(filebytes)

    chunks = xfbin.get_chunks_by_type('NuccChunkBinary')

    binary_data = chunks[0].binary_data

    characodes = []

    with BinaryReader(binary_data, Endian.LITTLE, 'cp932') as br:
        count = br.read_uint32()
        for i in range(count):
            chara = Character()
            chara.index = br.read_uint32()
            chara.code = br.read_str(8)
            characodes.append(chara)

    return characodes

def write_chara_code(path, characodes):
    
    with BinaryReader(bytearray(), Endian.LITTLE, 'cp932') as br:
        br.write_uint32(len(characodes))
        for chara in characodes:
            br.write_uint32(chara.index)
            br.write_str_fixed(chara.code, 8)
        binary_data = bytes(br.buffer())

    xfbin = Xfbin()
    
    binary_chunk = NuccChunkBinary('D:/JARP/trunk/param/player/Converter/bin/characode.bin', 'characode')
    binary_chunk.binary_data = binary_data
    binary_chunk.has_props = True
    binary_chunk.has_data = True

    xfbin.add_chunk_page(binary_chunk)

    try:
        write_xfbin_to_path(xfbin, path)
        return True
    except:
        return False
