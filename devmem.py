import subprocess

def read32(addr):
    return int("0x"+subprocess.check_output(["./devmem", hex(addr), "w"]).decode(), 16)

def write32(addr, val):
    return subprocess.check_output(["./devmem", hex(addr), "w", hex(val)])

def read64(addr):
    return int("0x"+subprocess.check_output(["./devmem", hex(addr), "q"]).decode(), 16)

def write64(addr, val):
    return subprocess.check_output(["./devmem", hex(addr), "q", hex(val)])

read_map = {
    32: read32,
    64: read64
}

write_map = {
    32: write32,
    64: write64
}

def read(size, addr):
    return read_map[size](addr)

def write(size, addr, val):
    return write_map[size](addr, val)