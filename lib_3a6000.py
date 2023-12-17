from struct import pack, unpack
from collections import namedtuple
from devmem import *

REG_DEBUG_ENABLE = False

class Reg():
    def __init__(self, name, addr, size, parameters):
        self.name = name
        self.addr = addr
        self.size = size
        self.parameters = parameters
        self.pmax = 0
        vsum = 0
        for n, v in parameters.items():
            self.pmax = max(len(n), self.pmax)
            vsum += v
        assert vsum == size

    def remap(self):
        self.val_map = {}
        reg_bits = bin(self.value)[2:].rjust(self.size, '0')
        assert(len(reg_bits) == self.size)

        for name, length in self.parameters.items():
            self.val_map[name] = int("0b"+reg_bits[-length:], 2)
            reg_bits = reg_bits[:-length]
        return self
    
    def set_parameter(self, name, value):
        bcount = 0
        for k, v in self.parameters.items():
            bcount += v
            if k == name:
                # |-----higher-----|----new----|----lower----|
                # |                |<--------bcount--------->|
                # |                |<----v---->|             |
                valbin = bin(value)[2:].rjust(v, '0')
                higher = bin(self.value)[2:][:-bcount].rjust(self.size-bcount, '0')
                lower = bin(self.value)[2:][-bcount+v:].rjust(bcount-v, '0')
                # print("original: ", bin(self.value)[2:])
                # print("new parameter binary: ", valbin)
                # print("higher: ", higher)
                # print("lower: ", lower)
                self.value = int("0b"+higher+valbin+lower, 2)
        self.remap()
        return self
    
    def set_value(self, value):
        self.value = value
        self.remap()
        return self

    def read(self):
        self.value = read(self.size, self.addr)
        self.remap()
        return self

    def write(self):
        write(self.size, self.addr, self.value)
        return self
    
    def __str__(self) -> str:
        header = f"{self.name} [0x{hex(self.addr)[2:].rjust(8, '0')}] = 0x{hex(self.value)[2:].rjust(8, '0')}\n"
        vals = ""
        vhexmax = 0
        for v in self.val_map.values():
            vhexmax = max(vhexmax, len(hex(v)))
        bit = 0
        for k, v in self.val_map.items():
            name = f"[{bit+self.parameters[k]}:{bit}]".rjust(8, ' ')
            vals += f"{name} {k.ljust(self.pmax+1, ' ')}: {hex(v).ljust(vhexmax, ' ')} / {v}\n"
            bit += self.parameters[k]
        return header+vals
    
    def debug(self):
        if REG_DEBUG_ENABLE:
            print(self)
        return self

    @property
    def v(self):
        return self.val_map



CLK_M = 1000*1000
CLK_100M = 100*CLK_M

FreqConfigParameter = {
    "SEL_PLL_NODE": 1,
    "RSVD1": 1,
    "SOFT_SET_PLL": 1,
    "BYPASS_L1": 1,
    "BYPASS_L2": 1,
    "RSVD2": 3,
    "VDDA_LDO_EN": 1,
    "VDDD_LDO_EN": 1,
    "L2_DSMCLK_SEL": 1,
    "L2_bypass_reg": 1,
    "L2_RSTN": 1,
    "L2_CKOUT_EN": 1,
    "L2_CP_SEL": 1,
    "L2_FRAC_EN": 1,
    "LOCKED_L1": 1,
    "LOCKED_L2": 1,
    "RSVD3": 1,
    "PD_L1": 1,
    "PD_L2": 1,
    "L2_VCO_START": 1,
    "L2_SEL": 1,
    "RSVD4": 3,
    "L1_DIV_REFC": 6,
    "L1_DIV_LOOPC": 9,
    "RSVD5": 1,
    "L1_DIV_OUT": 6,
    "L2_DIV_REF": 4,
    "RSVD6": 3,
    "L2_DIV_LOOP": 9
}

FuncConfigParameter = {
    "RSVD1": 1,
    "RSVD2": 1,
    "RSVD3": 2,
    "MC0_disable_confspace": 1,
    "MC0_defult_confspace": 1,
    "RSVD4": 1,
    "MC0_resetn": 1,
    "MC0_clken": 1,
    "MC1_disable_confspace": 1,
    "MC1_defult_confspace": 1,
    "RSVD5": 1,
    "MC1_resetn": 1,
    "MC1_clken": 1,
    "RSVD6": 10,
    "HT_freq_scale_ctrl": 3,
    "HT_clken": 1,
    "RSVD7": 3,
    "RSVD8": 1,
    "RSVD9": 8,
    "Node_freq_ctrl": 3,
    "RSVD10": 1,
    "RSVD11": 12,
    "Cpu_version": 8,
}

OtherFuncConfigParameter = {
    "disable_jtag": 1,
    "disable_jtag_Core": 1,
    "disable_LA132": 1,
    "disable_jtag_LA132": 1,
    "Disable_antifuse0": 1,
    "Disable_antifuse1": 1,
    "Disable_ID": 1,
    "RSVD1": 1,
    "resetn_LA132": 1,
    "sleeping_LA132": 1,
    "soft_int_LA132": 1,
    "RSVD2": 1,
    "core_int_en_LA132": 4,
    "freqscale_LA132": 3,
    "clken_LA132": 1,
    "RSVD3": 1,
    "stable_resetn": 1,
    "freqscale_percore": 1,
    "clken_percore": 1,
    "confbus_timeout": 4,
    "HT_softresetn": 2,
    "RSVD4": 2,
    "freqscale_mode_core": 4,
    "freqscale_mode_node": 1,
    "freqscale_mode_LA132": 1,
    "freqscale_mode_HT": 2,
    "freqscale_mode_stable": 1,
    "RSVD5": 3,
    "freqscale_stable": 3,
    "clken_stable": 1,
    "EXT_INT_en": 1,
    "INT_encode": 1,
    "DS_en": 1,
    "Int_Remap_en": 1,
    "RSVD6": 2,
    "RSVD7": 1,
    "RSVD8": 1,
    "thsensor_sel": 2,
    "RSVD9": 2,
    "Auto_scale": 3,
    "Auto_scale_doing": 1
}

TempSampleParameter = {
    "RSVD1": 16,
    "RSVD2": 4,
    "dotest": 1,
    "RSVD3": 1,
    "RSVD4": 2,
    "Thsens0_overflow": 1,
    "Thsens1_overflow": 1,
    "RSVD5": 6,
    "Thsens0_out": 16,
    "Thsens1_out": 16
}

RegFreqConfig0 = Reg("FreqConfig0", 0x1fe001b0, 64, FreqConfigParameter)
RegFreqConfig1 = Reg("FreqConfig1", 0x1fe101b0, 64, FreqConfigParameter)

RegFuncConfig0 = Reg("FuncConfig0", 0x1fe00180, 64, FuncConfigParameter)
RegFuncConfig1 = Reg("FuncConfig1", 0x1fe10180, 64, FuncConfigParameter)

RegOtherFuncConfig0 = Reg("OtherFuncConfig0", 0x1fe00420, 64, OtherFuncConfigParameter)
RegOtherFuncConfig1 = Reg("OtherFuncConfig1", 0x1fe10420, 64, OtherFuncConfigParameter)

RegTempSample = Reg("TempSampleReg", 0x1fe00198, 64, TempSampleParameter)

RegAVSCSR = Reg("AVSCSR", 0x1fe00160, 32, {
    "RSVD1": 16,
    "Dmux": 1,
    "clk_div": 3,
    "rx_delay": 4,
    "rx_ctrl": 1,
    "mask_a": 1,
    "mask_c": 1,
    "mask_s": 1,
    "mask_i": 1,
    "mask_ack": 2,
    "resyn": 1
})

AVS_MREG_CMD_WRITE_COMMIT = 0
AVS_MREG_CMD_WRITE        = 1
AVS_MREG_CMD_RSVD1        = 2
AVS_MREG_CMD_READ         = 3

AVS_MREG_CMD_TYPE_VOLT              = 0
AVS_MREG_CMD_TYPE_SLEW_RATE         = 1
AVS_MREG_CMD_TYPE_GET_CURRENT       = 2
AVS_MREG_CMD_TYPE_GET_TEMP          = 3
AVS_MREG_CMD_TYPE_SET_DEFAULT_VOLT  = 4
AVS_MREG_CMD_TYPE_POWER             = 5
AVS_MREG_CMD_TYPE_SET_CLEAR_STATUS  = 0xe
AVS_MREG_CMD_TYPE_GET_READ_VERSION  = 0xf

RegAVSMreg = Reg("AVSMreg", 0x1fe00164, 32, {
    "RSVD1": 4,
    "cmd_data": 16,
    "rail_sel": 4,
    "cmd_type": 4,
    "group": 1,
    "cmd": 2,
    "TX_EN": 1,
})

RegAVSSreg = Reg("AVSSreg", 0x1fe00168, 32, {
    "sdata": 16,
    "RSVD1": 9,
    "alert_a": 1,
    "alert_c": 1,
    "alert_s": 1,
    "alert_i": 1,
    "slave_ack": 2,
    "busy": 1,
})