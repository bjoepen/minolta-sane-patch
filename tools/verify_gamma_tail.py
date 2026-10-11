#!/usr/bin/env python3
"""Model and verify the sole R7-1 gamma-tail transformation."""

import hashlib


reference_block = bytes((index * 73 + 19) % 256 for index in range(512))
reference = reference_block + bytes([reference_block[-1]]) * (4096 - 512)
experiment = reference_block * 8

assert len(reference) == 4096
assert len(experiment) == 4096
assert experiment[:512] == reference[:512]
assert experiment[512:] != reference[512:]
assert all(experiment[offset:offset + 512] == reference_block for offset in range(0, 4096, 512))

print("payload_length=4096")
print("unchanged_prefix=512")
print("repeated_blocks=8")
print("reference_prefix_sha256=" + hashlib.sha256(reference[:512]).hexdigest())
print("experiment_prefix_sha256=" + hashlib.sha256(experiment[:512]).hexdigest())
