# Minolta SANE experimental build

Experimental, isolated build of SANE 1.4.0's avision backend with a bounded Minolta film-holder BUSY retry and the Research-004 4096-byte gamma transfer. This does **not** install or overwrite local Homebrew SANE.

The `research-007-gamma-tail` branch adds a separate R7-1 experiment. It leaves the first calculated 512 gamma bytes and the 4096-byte transfer length unchanged, but fills bytes 512–4095 with seven further copies of the first 512-byte block. The change is restricted to USB `0638:026a`, ASIC C2. It is not a production fix and must not be merged into a stable branch without a separate audit and approval.

`tools/analyze_rgb.py` produces deterministic per-channel RGB8 RAW/TIFF histograms and summary statistics. RAW input requires the matching `*.params.txt` file:

```sh
python3 tools/analyze_rgb.py frame1.raw --params frame1.params.txt --output frame1.stats.json
python3 tools/analyze_rgb.py frame1.tiff --output frame1-tiff.stats.json
```

The workflow runs on a disposable GitHub-hosted Apple Silicon macOS runner and uploads binaries plus linker diagnostics. The output is **not yet validated** for interchangeability with Homebrew's SANE 1.4.0_2 on macOS Tahoe. Do not replace any Homebrew libraries with this artifact.

To run: GitHub → Actions → Minolta SANE ARM64 test build → Run workflow.
