from lib_3a6000 import *
import time
import argparse


def show_freq():
    RegFreqConfig0.read()
    RegFuncConfig0.read()
    RegOtherFuncConfig0.read()

    node0_main_clock = CLK_100M / RegFreqConfig0.v["L1_DIV_REFC"] * RegFreqConfig0.v["L1_DIV_LOOPC"] / RegFreqConfig0.v["L1_DIV_OUT"]
    print(f"Main Clock: {node0_main_clock / CLK_M} Mhz")

    n = RegFuncConfig0.v["Node_freq_ctrl"]
    if RegOtherFuncConfig0.v["freqscale_mode_node"] == 0:
        node0_node_clock = (n+1)/8 * node0_main_clock
    elif RegOtherFuncConfig0.v["freqscale_mode_node"] == 1:
        node0_node_clock = 1/(n+1) * node0_main_clock
    print(f"Node 0 Clock: {node0_node_clock / CLK_M} Mhz")

    if RegFuncConfig0.v["HT_clken"] == 1:
        n = RegFuncConfig0.v["HT_freq_scale_ctrl"]
        if RegOtherFuncConfig0.v["freqscale_mode_HT"] == 0:
            node0_ht_clock = (n+1)/8 * node0_node_clock
        elif RegOtherFuncConfig0.v["freqscale_mode_HT"] == 1:
            node0_ht_clock = 1/(n+1) * node0_node_clock
        print(f"Node 0 HT Clock: {node0_ht_clock / CLK_M} Mhz")
    else:
        print("Node 0 HT disabled")
    
    if RegOtherFuncConfig0.v["clken_LA132"] == 1:
        n = RegOtherFuncConfig0.v["freqscale_LA132"]
        if RegOtherFuncConfig0.v["freqscale_mode_LA132"] == 0:
            node0_la132_clock = (n+1/8) * node0_main_clock
        elif RegOtherFuncConfig0.v["freqscale_mode_LA132"] == 1:
            node0_la132_clock = 1/(n+1) * node0_main_clock
        print(f"Node 0 LA132 Clock: {node0_la132_clock / CLK_M} Mhz")
    else:
        print("Node 0 LA132 disabled")


def show_reg():
    print(RegFreqConfig0.read())
    print(RegFreqConfig1.read())
    print(RegFuncConfig0.read())
    print(RegFuncConfig1.read())
    print(RegOtherFuncConfig0.read())
    print(RegOtherFuncConfig1.read())

def avs_read_info(cmd_type, rail=0):
    RegAVSCSR.set_value(0x70000).debug().write()
    RegAVSMreg \
        .set_value(0) \
        .set_parameter("TX_EN", 1) \
        .set_parameter("cmd", AVS_MREG_CMD_READ) \
        .set_parameter("cmd_type", cmd_type) \
        .set_parameter("rail_sel", rail) \
        .debug() \
        .write()
    while RegAVSSreg.read().v["busy"] != 0:
        time.sleep(0.1)
    if RegAVSSreg.debug().v["slave_ack"] == 0:
        return RegAVSSreg.debug().v["sdata"]
    print("read fail")
    return 0

def avs_write_reg(cmd_type, value, rail=0):
    RegAVSCSR.set_value(0x70000).debug().write()
    RegAVSMreg \
        .set_value(0) \
        .set_parameter("TX_EN", 1) \
        .set_parameter("cmd", AVS_MREG_CMD_WRITE_COMMIT) \
        .set_parameter("cmd_type", cmd_type) \
        .set_parameter("cmd_data", value) \
        .set_parameter("rail_sel", rail) \
        .debug() \
        .write()
    while RegAVSSreg.read().v["busy"] != 0:
        time.sleep(0.1)
    if RegAVSSreg.debug().v["slave_ack"] == 0:
        return RegAVSSreg.debug().v["sdata"]
    print("write fail")
    return 0

def show_avs():
    total_power = 0
    for i in range(0, 2):
        voltage     = round(avs_read_info(AVS_MREG_CMD_TYPE_VOLT, i) / 1000, 3)
        current     = round(avs_read_info(AVS_MREG_CMD_TYPE_GET_CURRENT, i) / 50, 3)
        temperature = round(avs_read_info(AVS_MREG_CMD_TYPE_GET_TEMP, i) / 10, 3)
        print(f"VR rail {i} voltage: {voltage} V")
        print(f"VR rail {i} current: {current} A")
        print(f"VR rail {i} temperature: {temperature} C")
        print(f"VR rail {i} power: {round(voltage*current, 3)} W")
        total_power += voltage*current
    print(f"CPU package power: {round(total_power, 3)} W")

def show_temp():
    RegTempSample.read()
    t0_overflow = RegTempSample.v["Thsens0_overflow"]
    t1_overflow = RegTempSample.v["Thsens1_overflow"]
    t0 = RegTempSample.v["Thsens0_out"]
    t1 = RegTempSample.v["Thsens1_out"]

    t0val = ""
    if t0_overflow == 1:
        t0val = "OVERFLOW"
    else:
        t0val = t0*820/0x4000-311
    t1val = ""
    if t1_overflow == 1:
        t1val = "OVERFLOW"
    else:
        t1val = t1*820/0x4000-311

    print(f"Thermal sensor 0: {t0val} C")
    print(f"Thermal sensor 1: {t1val} C")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--freq", action="store_true")
    p.add_argument("--reg", action="store_true")
    p.add_argument("--avsinfo", action="store_true")
    p.add_argument("--temp", action="store_true")
    args = p.parse_args()

    if args.freq:
        show_freq()
    if args.reg:
        show_reg()
    if args.avsinfo:
        show_avs()
    if args.temp:
        show_temp()

if __name__ == "__main__":
    main()