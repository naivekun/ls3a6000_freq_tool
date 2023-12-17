# Loongson 3A6000 freq tool

monitor/configure Loongson 3A6000 frequency/power/temperature

## Usage

```
usage: freq_tool.py [-h] [--freq] [--reg] [--avsinfo] [--temp]

optional arguments:
  -h, --help  show this help message and exit
  --freq
  --reg
  --avsinfo
  --temp
```

Example output

```
root@naivekun-3a6000:/home/naivekun/ls3a6000_freq_tool# python3 freq_tool.py --freq --avs --temp
Main Clock: 2800.0 Mhz
Node 0 Clock: 2800.0 Mhz
Node 0 HT Clock: 1050.0 Mhz
Node 0 LA132 Clock: 350.0 Mhz
VR rail 0 voltage: 1.282 V
VR rail 0 current: 29.0 A
VR rail 0 temperature: 42.0 C
VR rail 0 power: 37.178 W
VR rail 1 voltage: 1.148 V
VR rail 1 current: 3.5 A
VR rail 1 temperature: 34.0 C
VR rail 1 power: 4.018 W
CPU package power: 41.196 W
Thermal sensor 0: 31.784423828125 C
Thermal sensor 1: 32.985595703125 C
```