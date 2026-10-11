# Research-005 RGB baseline

Generated with `tools/analyze_rgb.py` from the preserved Research-005 files. Each RAW result was checked against the corresponding TIFF result; channel histograms and dimensions are identical.

All images are RGB8, 564 × 850 (479,400 pixels). Percentiles use linear interpolation between zero-based ranks.

| Frame | Channel | Mean | Min | Max | Value 0 | Value 255 |
|---:|---|---:|---:|---:|---:|---:|
| 1 | R | 243.223 | 0 | 255 | 11,478 | 397,030 |
| 1 | G | 195.691 | 0 | 255 | 1,292 | 18,567 |
| 1 | B | 142.380 | 0 | 194 | 11,636 | 0 |
| 2 | R | 246.652 | 0 | 255 | 5,923 | 426,143 |
| 2 | G | 218.633 | 0 | 255 | 1,432 | 122,016 |
| 2 | B | 145.400 | 0 | 198 | 6,897 | 0 |
| 3 | R | 249.864 | 0 | 255 | 1,075 | 444,438 |
| 3 | G | 209.782 | 0 | 255 | 137 | 22,542 |
| 3 | B | 138.544 | 0 | 195 | 2,920 | 0 |
| 4 | R | 247.100 | 0 | 255 | 895 | 397,949 |
| 4 | G | 201.175 | 0 | 255 | 133 | 47,182 |
| 4 | B | 131.656 | 0 | 198 | 3,506 | 0 |

The complete 256-bin histograms, SHA-256 values, percentiles, medians and exact fractions are in the adjacent JSON files. These measurements describe unconverted negative scans; they do not diagnose the gamma tail by themselves.
