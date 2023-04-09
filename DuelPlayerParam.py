from PyBinaryReader.binary_reader import *
from xfbin_lib.xfbin import *


def read_dpp_Xfbin(xfbin_path):

    with open(xfbin_path, "rb") as f:
        filebytes = f.read()
    
    xfbin = read_xfbin(filebytes)

    return xfbin.get_chunks_by_type('NuccChunkBinary')

def read_prm_bas(dpp_chunk):
    
    binary_data: NuccChunkBinary = dpp_chunk.binary_data
    with BinaryReader(binary_data, Endian.LITTLE, 'cp932') as br:        
        version = br.read_uint32()

        prm_bas = PRM_bas()
        prm_bas.CharacterCode = br.read_str(8)
        prm_bas.PRM_bas_Code = br.read_str(8)

        for i in range(16):
            prm_bas.ModelCodes[i] = br.read_str(8)
            
        prm_bas.StandCode = br.read_str(8)

        #Character Collision
        prm_bas.CollisionThreshold = br.read_uint32()
        prm_bas.CameraHeight = br.read_uint32()
        prm_bas.CollisionRadius = br.read_uint32()

        #Hurt Spheres
        prm_bas.HurtSphereName1 = br.read_str(32)
        prm_bas.HorizontalSize1 = br.read_uint32()
        prm_bas.VerticalSize1 = br.read_uint32()

        prm_bas.HurtSphereName2 = br.read_str(32)
        prm_bas.HorizontalSize2 = br.read_uint32()
        prm_bas.VerticalSize2 = br.read_uint32()

        prm_bas.HurtSphereName3 = br.read_str(32)
        prm_bas.HorizontalSize3 = br.read_uint32()
        prm_bas.VerticalSize3 = br.read_uint32()

        prm_bas.HurtSphereName4 = br.read_str(32)
        prm_bas.HorizontalSize4 = br.read_uint32()
        prm_bas.VerticalSize4 = br.read_uint32()

        prm_bas.HealthPoints = br.read_uint32()
        prm_bas.GuardPoints = br.read_uint32()

        prm_bas.unk1 = br.read_uint32()
        prm_bas.unk2 = br.read_uint32()
        prm_bas.unk3 = br.read_uint32()
        
        prm_bas.FireDamage = br.read_float()
        prm_bas.LightningDamage = br.read_float()
        prm_bas.HamonDamage = br.read_float()
        prm_bas.UnkDamage1 = br.read_float()
        prm_bas.UnkDamage2 = br.read_float()
        prm_bas.UnkDamage3 = br.read_float()
        prm_bas.UnkDamage4 = br.read_float()
        prm_bas.UnkDamage5 = br.read_float()
        prm_bas.UnkDamage6 = br.read_float()
        prm_bas.UnkDamage7 = br.read_float()
        
        CharaPhysics = prm_bas.CharacterPhysics

        CharaPhysics.ForwardWalkSpeed = br.read_uint32()
        CharaPhysics.BackwardWalkSpeed = br.read_uint32()

        CharaPhysics.ForwardRunSpeed = br.read_uint32()
        CharaPhysics.BackwardRunSpeed = br.read_uint32()

        CharaPhysics.GravityStrength = br.read_uint32()

        CharaPhysics.JumpUpStrength = br.read_uint32()
        CharaPhysics.JumpForwardStrength = br.read_uint32()

        CharaPhysics.DashJumpHeight = br.read_float()
        CharaPhysics.DashJumpDistance = br.read_float()

        StandPhysics = prm_bas.StandPhysics

        StandPhysics.ForwardWalkSpeed = br.read_uint32()
        StandPhysics.BackwardWalkSpeed = br.read_uint32()

        StandPhysics.ForwardRunSpeed = br.read_uint32()
        StandPhysics.BackwardRunSpeed = br.read_uint32()

        StandPhysics.GravityStrength = br.read_uint32()

        StandPhysics.JumpUpStrength = br.read_uint32()
        StandPhysics.JumpForwardStrength = br.read_uint32()

        StandPhysics.DashJumpHeight = br.read_float()
        StandPhysics.DashJumpDistance = br.read_float()

        OtherPhysics = prm_bas.OtherPhysics

        OtherPhysics.ForwardWalkSpeed = br.read_uint32()
        OtherPhysics.BackwardWalkSpeed = br.read_uint32()

        OtherPhysics.ForwardRunSpeed = br.read_uint32()
        OtherPhysics.BackwardRunSpeed = br.read_uint32()

        OtherPhysics.GravityStrength = br.read_uint32()

        OtherPhysics.JumpUpStrength = br.read_uint32()
        OtherPhysics.JumpForwardStrength = br.read_uint32()

        OtherPhysics.DashJumpHeight = br.read_float()
        OtherPhysics.DashJumpDistance = br.read_float()

        br.seek(4, 1)

        prm_bas.DLC_Code = br.read_uint32()

        prm_bas.IconCode = br.read_uint32()

        prm_bas.CorpsePartString = br.read_str(32)

        prm_bas.Style = br.read_int32()

        prm_bas.unk12 = br.read_uint32()

        prm_bas.RosterPosition = br.read_uint32()

        prm_bas.unk13 = br.read_uint32()

        prm_bas.unk14 = br.read_uint32()

        prm_bas.padding = br.read_bytes(0x1C)

        return prm_bas

class PRM_bas: #inherits from BrStruct later
    def __init__(self):
        self.CharacterCode = ""
        self.PRM_bas_Code = ""

        self.ModelCodes = [""] * 16
        self.StandCode = ""

        #Character Collision
        self.CollisionThreshold = 0
        self.CameraHeight = 0
        self.CollisionRadius = 0

        #Hurt Spheres
        self.HurtSphereName1 = ""
        self.HorizontalSize1 = 0
        self.VerticalSize1 = 0

        self.HurtSphereName2 = ""
        self.HorizontalSize2 = 0
        self.VerticalSize2 = 0

        self.HurtSphereName3 = ""
        self.HorizontalSize3 = 0
        self.VerticalSize3 = 0

        self.HurtSphereName4 = ""
        self.HorizontalSize4 = 0
        self.VerticalSize4 = 0

        #Character Attributes
        self.HealthPoints = 0
        self.GuardPoints = 0
        
        self.unk1 = 0
        self.unk2 = 0
        self.unk3 = 0

        #Elemental Damage Modifiers
        self.FireDamage = 0
        self.LightningDamage = 0
        self.HamonDamage = 0

        self.UnkDamage1 = 0
        self.UnkDamage2 = 0
        self.UnkDamage3 = 0
        self.UnkDamage4 = 0
        self.UnkDamage5 = 0
        self.UnkDamage6 = 0
        self.UnkDamage7 = 0

        #Physics
        self.CharacterPhysics = Physics()
        self.StandPhysics = Physics()
        self.OtherPhysics = Physics()

        self.DLC_Code = 0

        self.IconCode = 0

        self.CorpsePartString = ""

        self.Style = 0

        self.unk12 = 0

        self.RosterPosition = 0

        self.unk13 = 0
        self.unk14 = 0

        self.padding = 0

class Physics:
    def __init__(self):

        self.ForwardWalkSpeed = 0
        self.BackwardWalkSpeed = 0

        self.ForwardRunSpeed = 0
        self.BackwardRunSpeed = 0

        self.GravityStrength = 0

        self.JumpHeight = 0
        self.JumpDistance = 0

        self.DashJumpHeight = 0
        self.DashJumpDistance = 0
    
'''    def __br_read__(self, br: 'BinaryReader', *args):
        
        self.ForwardWalkSpeed = br.read_uint32()
        self.BackwardWalkSpeed = br.read_uint32()

        self.ForwardRunSpeed = br.read_uint32()
        self.BackwardRunSpeed = br.read_uint32()

        self.GravityStrength = br.read_uint32()

        self.JumpHeight = br.read_uint32()
        self.JumpDistance = br.read_uint32()

        self.DashJumpHeight = br.read_uint32()
        self.DashJumpDistance = br.read_uint32()'''