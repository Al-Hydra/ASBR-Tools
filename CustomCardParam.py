from PyBinaryReader.binary_reader import *
from xfbin_lib.xfbin import *
import json
file = r"C:\Users\Ali\Documents\GitHub\ASBR_Tools\PlayerColorParam.bin"

def read_card_param(file):

    with open(file, "rb") as f:
        filebytes = f.read()
    
    xfbin = read_xfbin(filebytes)

    chunks = xfbin.get_chunks_by_type('NuccChunkBinary')

    binary_data = chunks[0].data

    with BinaryReader(binary_data, Endian.LITTLE, 'cp932') as br:
        br.seek(4, 0)
        version = br.read_uint32()
        count = br.read_uint32()
        br.read_uint64()

        Cards = []
        #Cards_dict = {}

        for i in range(count):
            
            card = Medal()

            card_pointer = br.read_uint64()
            pos = br.pos()
            br.seek(card_pointer - 8, 1)
            card.CardID = br.read_str()
            br.seek(pos, 0)
            
            card.Part = br.read_uint32()
            card.InteractionType = br.read_uint32()
            card.MedalType = br.read_uint64()

            letter_pointer = br.read_uint64()
            pos = br.pos()
            br.seek(letter_pointer - 8, 1)
            card.Letter = br.read_str()
            br.seek(pos, 0)

            #unk1 = br.read_int32(4)
            card.Unk1 = br.read_int32()
            card.Unk2 = br.read_int32()
            card.Unk3 = br.read_int32()
            card.Unk4 = br.read_int32()

            sfx1_pointer = br.read_uint64()
            pos = br.pos()
            br.seek(sfx1_pointer - 8, 1)
            card.SFX1 = br.read_str()
            br.seek(pos, 0)

            sfx2_pointer = br.read_uint64()
            pos = br.pos()
            br.seek(sfx2_pointer - 8, 1)
            card.SFX2 = br.read_str()
            br.seek(pos, 0)

            sfx3_pointer = br.read_uint64()
            pos = br.pos()
            br.seek(sfx3_pointer - 8, 1)
            card.SFX3 = br.read_str()
            br.seek(pos, 0)

            sfx4_pointer = br.read_uint64()
            pos = br.pos()
            br.seek(sfx4_pointer - 8, 1)
            card.SFX4 = br.read_str()
            br.seek(pos, 0)

            #unk2 = br.read_uint32(2)
            card.Unk5 = br.read_uint32()
            card.Unk6 = br.read_uint32()

            characode_pointer = br.read_uint64()
            pos = br.pos()
            br.seek(characode_pointer - 8, 1)
            card.CharacterCode = br.read_str()
            br.seek(pos, 0)

            card.DLCID = br.read_uint32()

            card.Patch = br.read_uint32()

            card.UnlockCondition = br.read_uint32()
            
            card.Unk8 = br.read_uint32()

            cost = br.read_uint64()

            medal_pointer = br.read_uint64()
            pos = br.pos()
            br.seek(medal_pointer - 8, 1)
            card.Medal = br.read_str()
            br.seek(pos, 0)

            detail_pointer = br.read_uint64()
            pos = br.pos()
            br.seek(detail_pointer - 8, 1)
            card.Detail = br.read_str()
            br.seek(pos, 0)

            card.Index = br.read_uint64()
            
            Cards.append(card)

    return Cards


def dump_card_param(cards: list, path: str):
    with open("CustomCardParam.json", "w") as f:
        json.dump(cards, f, indent=4)

def write_card_param(cards: list, path: str):
    
    with BinaryReader(bytearray(), Endian.LITTLE, 'cp932') as br:
        size = 0
        br.write_uint32(0)
        version = br.write_uint32(1000)
        count = len(cards)
        br.write_uint32(count)
        br.write_uint64(8) # pointer to first card

        card_buf = BinaryReader(bytearray(), Endian.LITTLE, 'cp932')
        string_buf = BinaryReader(bytearray(), Endian.LITTLE, 'cp932')

        size = 144 * count
        for i in range(count):
            card: Medal = cards[i]
            card_pointer = card_buf.write_uint64(size + string_buf.size() - card_buf.pos())
            string_buf.write_str(card.CardID)
            string_buf.align(8)

            card_buf.write_uint32(int(card.Part))
            card_buf.write_uint32(card.InteractionType)
            card_buf.write_uint64(card.MedalType)

            if card.Letter == "":
                card_buf.write_uint64(0)
            else:
                letter_pointer = card_buf.write_uint64(size + string_buf.size() - card_buf.pos())
                string_buf.write_str(card.Letter)
                string_buf.align(8)

            card_buf.write_int32(card.Unk1)
            card_buf.write_int32(card.Unk2)
            card_buf.write_int32(card.Unk3)
            card_buf.write_int32(card.Unk4)

            if card.SFX1 == "":
                card_buf.write_uint64(0)
            else:
                sfx1_pointer = card_buf.write_uint64(size + string_buf.size() - card_buf.pos())
                string_buf.write_str(card.SFX1)
                string_buf.align(8)

            if card.SFX2 == "":
                card_buf.write_uint64(0)
            else:
                sfx2_pointer = card_buf.write_uint64(size + string_buf.size() - card_buf.pos())
                string_buf.write_str(card.SFX2)
                string_buf.align(8)

            if card.SFX3 == "":
                card_buf.write_uint64(0)
            else:
                sfx3_pointer = card_buf.write_uint64(size + string_buf.size() - card_buf.pos())
                string_buf.write_str(card.SFX3)
                string_buf.align(8)

            if card.SFX4 == "":
                card_buf.write_uint64(0)
            else:
                sfx4_pointer = card_buf.write_uint64(size + string_buf.size() - card_buf.pos())
                string_buf.write_str(card.SFX4)
                string_buf.align(8)

            card_buf.write_uint32(card.Unk5)
            card_buf.write_uint32(card.Unk6)
            
            characode_pointer = card_buf.write_uint64(size + string_buf.size() - card_buf.pos())
            string_buf.write_str(card.CharacterCode)
            string_buf.align(8)

            card_buf.write_uint32(card.DLCID)
            card_buf.write_uint32(card.Patch)
            card_buf.write_uint32(card.UnlockCondition)
            card_buf.write_uint32(card.Unk8)
            card_buf.write_uint64(card.Cost)

            if card.Medal == "":
                card_buf.write_uint64(0)
            else:
                medal_pointer = card_buf.write_uint64(size + string_buf.size() - card_buf.pos())
                string_buf.write_str(card.Medal)
                string_buf.align(8)

            if card.Detail == "":
                card_buf.write_uint64(0)
            else:
                detail_pointer = card_buf.write_uint64(size + string_buf.size() - card_buf.pos())
                string_buf.write_str(card.Detail)
                string_buf.align(8)

            card_buf.write_uint64(card.Index)

        br.extend(card_buf.buffer())
        br.seek(card_buf.size(), 1)

        br.extend(string_buf.buffer())
        br.seek(0,0)

        br.set_endian(Endian.BIG)
        br.write_uint32(br.size() - 4)
    
        binary_chunk = NuccChunkBinary('CustomCardParam.bin', 'CustomCardParam')
        binary_chunk.data = br.buffer()
        binary_chunk.has_data = True
        binary_chunk.has_props = False

        xfbin: Xfbin = Xfbin()
        xfbin.add_chunk_page(binary_chunk)

        write_xfbin_to_path(xfbin, path)


class Medal:
    def __init__(self):
        self.CardID = ""
        self.Part = 0
        self.InteractionType = 0
        self.MedalType = 0
        self.Letter = ""
        self.Unk1 = 0
        self.Unk2 = 0
        self.Unk3 = 0
        self.Unk4 = 0
        self.SFX1 = ""
        self.SFX2 = ""
        self.SFX3 = ""
        self.SFX4 = ""
        self.Unk5 = 0
        self.Unk6 = 0
        self.CharacterCode = ""
        self.DLCID = 0
        self.Patch = 0
        self.UnlockCondition = 0
        self.Unk8 = 0
        self.Cost = 0
        self.Medal = ""
        self.Detail = ""
        self.Index = 0
        

if __name__ == "__main__":
    
    cards = read_card_param(file="CustomCardParam.bin")
    dump_card_param(cards)
    write_card_param(cards)

    