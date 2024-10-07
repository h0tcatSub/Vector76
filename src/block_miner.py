from datetime import datetime
from hashlib import sha256

txid = input("Enter TXID: ")
print()
block = input("Block: ")
block_height = input("Block Height: ")
mined_time = input("Mined Time: ")
prev_block = input("Prev Block:")
merkle_root = input("Merkle Root: ")
nonce = int(input("Nonce: "))
bits  = int(input("Bits: "))
version = int(input("Version: "))

print("Mining...")
version_h = format(version, "08x")[::-1]
prev_block_h = prev_block[::-1]
markle_root_h = merkle_root[::-1]

timestamp_s = int((datetime.strptime(mined_time, "%Y-%m-%d %H:%M:%S")-datetime(1970,1,1)).total_seconds())
timestamp_h = format(timestamp_s,"x")[::-1]
bits_h  = format(bits,"x")[::-1]
nonce_h = format(nonce,"x")[::-1]
header = version_h + prev_block_h + markle_root_h + timestamp_h + bits_h + nonce_h
print(f"Output: {sha256(sha256(header).digest()).hexdigest()[::-1]}")