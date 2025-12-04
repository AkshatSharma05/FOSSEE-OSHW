#!/usr/bin/env python3
import subprocess, time, sys, threading, os, pty

FIRMWARE = "firmware.bin"
SCRIPT = "temp.py"

# Create a pseudo-terminal pair
master, slave = pty.openpty()

# Start QEMU process
p = subprocess.Popen(
    [
        "qemu-system-xtensa",
        "-nographic",
        "-machine", "esp32",
        "-drive", f"file={FIRMWARE},format=raw,if=mtd"
    ],
    stdin=slave,
    stdout=slave,
    stderr=slave,
    text=True
)

output_buffer = ""

def reader():
    global output_buffer
    while True:
        try:
            data = os.read(master, 1024).decode(errors="ignore")
            if data:
                output_buffer += data
                print(data, end="")
            else:
                break
        except:
            break

# Start async reader
t = threading.Thread(target=reader, daemon=True)
t.start()

print("Waiting for MicroPython to finish booting...")

# Wait for MicroPython boot completion
while 'help()' not in output_buffer:
    time.sleep(0.1)

print("Boot complete. Waiting 0.5s for REPL to stabilize...")
time.sleep(0.5)

# Now REPL is stable → send Ctrl-E
os.write(master, b"\x05")
time.sleep(0.2)

# Send the script contents
with open(SCRIPT, "rb") as f:
    os.write(master, f.read())

time.sleep(0.2)

# Send Ctrl-D to execute
os.write(master, b"\x04")

# Resume interactive mode
try:
    while True:
        os.write(master, sys.stdin.read(1).encode())
except KeyboardInterrupt:
    pass
