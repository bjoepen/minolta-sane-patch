import json
import struct
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import analyze_rgb


PIXELS = bytes((0, 10, 255, 100, 20, 200, 200, 30, 100, 255, 40, 0))


def write_tiff(path):
    entries = 10
    extras = 8 + 2 + entries * 12 + 4
    bits_offset = extras
    pixels_offset = extras + 6
    with path.open("wb") as stream:
        stream.write(b"II")
        stream.write(struct.pack("<HIH", 42, 8, entries))
        def entry(tag, kind, count, value):
            stream.write(struct.pack("<HHII", tag, kind, count, value))
        entry(256, 4, 1, 2)
        entry(257, 4, 1, 2)
        entry(258, 3, 3, bits_offset)
        entry(259, 3, 1, 1)
        entry(262, 3, 1, 2)
        entry(273, 4, 1, pixels_offset)
        entry(277, 3, 1, 3)
        entry(278, 4, 1, 2)
        entry(279, 4, 1, len(PIXELS))
        entry(284, 3, 1, 1)
        stream.write(struct.pack("<IHHH", 0, 8, 8, 8))
        stream.write(PIXELS)


class AnalyzeRgbTest(unittest.TestCase):
    def test_raw_statistics_and_padding(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = root / "sample.raw"
            params = root / "sample.params.txt"
            raw.write_bytes(PIXELS[:6] + b"xx" + PIXELS[6:] + b"yy")
            params.write_text("format=RGB\npixels_per_line=2\nlines=2\ndepth=8\nbytes_per_line=8\n")
            result = analyze_rgb.analyze(raw, params)
            self.assertEqual(result["pixel_count"], 4)
            self.assertEqual(result["channels"]["red"]["histogram"][0], 1)
            self.assertEqual(result["channels"]["red"]["histogram"][255], 1)
            self.assertEqual(result["channels"]["green"]["mean"], 25)

    def test_tiff_matches_raw_pixels(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.tiff"
            write_tiff(path)
            result = analyze_rgb.analyze(path)
            self.assertEqual(result["width"], 2)
            self.assertEqual(result["height"], 2)
            self.assertEqual(result["channels"]["blue"]["minimum"], 0)
            self.assertEqual(result["channels"]["blue"]["maximum"], 255)
            json.dumps(result)


if __name__ == "__main__":
    unittest.main()
