#!/usr/bin/env python3
"""Deterministic RGB8 RAW/baseline-TIFF statistics without third-party modules."""

import argparse
import hashlib
import json
import struct
from pathlib import Path


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_params(path):
    values = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()
    required = ("format", "pixels_per_line", "lines", "depth", "bytes_per_line")
    missing = [key for key in required if key not in values]
    if missing:
        raise ValueError("missing parameter(s): " + ", ".join(missing))
    if values["format"] != "RGB" or int(values["depth"]) != 8:
        raise ValueError("only interleaved RGB with depth=8 is supported")
    return {
        "width": int(values["pixels_per_line"]),
        "height": int(values["lines"]),
        "depth": 8,
        "samples_per_pixel": 3,
        "bytes_per_line": int(values["bytes_per_line"]),
    }


def read_raw(path, params_path):
    meta = read_params(params_path)
    packed_row = meta["width"] * 3
    if meta["bytes_per_line"] < packed_row:
        raise ValueError("bytes_per_line is smaller than packed RGB row")
    data = path.read_bytes()
    expected = meta["bytes_per_line"] * meta["height"]
    if len(data) != expected:
        raise ValueError(f"RAW size {len(data)} does not match parameters {expected}")
    if meta["bytes_per_line"] != packed_row:
        data = b"".join(
            data[row * meta["bytes_per_line"]:row * meta["bytes_per_line"] + packed_row]
            for row in range(meta["height"])
        )
    return data, meta


def read_tiff(path):
    blob = path.read_bytes()
    if len(blob) < 8 or blob[:2] not in (b"II", b"MM"):
        raise ValueError("not a TIFF file")
    endian = "<" if blob[:2] == b"II" else ">"
    u16 = lambda offset: struct.unpack_from(endian + "H", blob, offset)[0]
    u32 = lambda offset: struct.unpack_from(endian + "I", blob, offset)[0]
    if u16(2) != 42:
        raise ValueError("unsupported TIFF magic")
    ifd_offset = u32(4)
    count = u16(ifd_offset)
    type_sizes = {1: 1, 3: 2, 4: 4}
    tags = {}
    for index in range(count):
        offset = ifd_offset + 2 + index * 12
        tag, value_type = struct.unpack_from(endian + "HH", blob, offset)
        value_count = u32(offset + 4)
        if value_type not in type_sizes:
            continue
        byte_count = type_sizes[value_type] * value_count
        value_offset = offset + 8 if byte_count <= 4 else u32(offset + 8)
        code = {1: "B", 3: "H", 4: "I"}[value_type]
        tags[tag] = list(struct.unpack_from(endian + code * value_count, blob, value_offset))

    def one(tag, default=None):
        if tag not in tags:
            if default is not None:
                return default
            raise ValueError(f"required TIFF tag {tag} missing")
        return tags[tag][0]

    width, height = one(256), one(257)
    bits = tags.get(258, [])
    if one(259, 1) != 1 or one(262) != 2 or one(277, 1) != 3 or one(284, 1) != 1:
        raise ValueError("only uncompressed contiguous RGB TIFF is supported")
    if bits != [8, 8, 8]:
        raise ValueError("only RGB8 TIFF is supported")
    offsets, counts = tags.get(273), tags.get(279)
    if not offsets or not counts or len(offsets) != len(counts):
        raise ValueError("invalid TIFF strip metadata")
    data = b"".join(blob[offset:offset + size] for offset, size in zip(offsets, counts))
    expected = width * height * 3
    if len(data) != expected:
        raise ValueError(f"TIFF raster size {len(data)} does not match dimensions {expected}")
    return data, {
        "width": width,
        "height": height,
        "depth": 8,
        "samples_per_pixel": 3,
        "bytes_per_line": width * 3,
    }


def percentile_from_histogram(histogram, count, percent):
    if count == 1:
        return next(index for index, amount in enumerate(histogram) if amount)
    position = (count - 1) * percent / 100.0
    low_rank = int(position)
    high_rank = min(low_rank + 1, count - 1)

    def value_at(rank):
        seen = 0
        for value, amount in enumerate(histogram):
            seen += amount
            if seen > rank:
                return value
        raise AssertionError("rank outside histogram")

    low, high = value_at(low_rank), value_at(high_rank)
    return low + (high - low) * (position - low_rank)


def channel_stats(data, channel):
    histogram = [0] * 256
    total = 0
    count = len(data) // 3
    for value in data[channel::3]:
        histogram[value] += 1
        total += value
    minimum = next(i for i, amount in enumerate(histogram) if amount)
    maximum = next(i for i in range(255, -1, -1) if histogram[i])
    return {
        "minimum": minimum,
        "maximum": maximum,
        "mean": total / count,
        "median": percentile_from_histogram(histogram, count, 50),
        "percentiles": {
            "0.1": percentile_from_histogram(histogram, count, 0.1),
            "1": percentile_from_histogram(histogram, count, 1),
            "99": percentile_from_histogram(histogram, count, 99),
            "99.9": percentile_from_histogram(histogram, count, 99.9),
        },
        "value_0": {"count": histogram[0], "fraction": histogram[0] / count},
        "value_255": {"count": histogram[255], "fraction": histogram[255] / count},
        "histogram": histogram,
    }


def analyze(input_path, params_path=None):
    suffix = input_path.suffix.lower()
    if suffix in (".tif", ".tiff"):
        data, meta = read_tiff(input_path)
        input_format = "TIFF"
    elif suffix == ".raw":
        if params_path is None:
            raise ValueError("--params is required for RAW input")
        data, meta = read_raw(input_path, params_path)
        input_format = "RAW"
    else:
        raise ValueError("input must end in .raw, .tif or .tiff")
    if not data:
        raise ValueError("empty raster")
    return {
        "schema": "beblog-rgb-statistics-v1",
        "input": input_path.name,
        "input_format": input_format,
        "file_size_bytes": input_path.stat().st_size,
        "sha256": sha256(input_path),
        **meta,
        "pixel_count": meta["width"] * meta["height"],
        "percentile_method": "linear interpolation between zero-based ranks",
        "channels": {
            name: channel_stats(data, index)
            for index, name in enumerate(("red", "green", "blue"))
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--params", type=Path, help="key=value SANE parameter file for RAW")
    parser.add_argument("--output", type=Path, help="JSON output; stdout if omitted")
    args = parser.parse_args()
    result = analyze(args.input, args.params)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
