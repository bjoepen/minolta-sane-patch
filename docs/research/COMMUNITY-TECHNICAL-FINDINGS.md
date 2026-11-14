# Minolta DiMAGE Scan Dual II — technical findings for SANE maintainers

**Status:** research summary, not an upstream patch submission. Updated 2026-11-14.

## Device and scope

- Scanner: Minolta DiMAGE Scan Dual II, USB VID:PID `0638:026a`.
- Backend: SANE `avision`, based on upstream SANE 1.4.0.
- Host for documented local tests: Apple Silicon macOS.
- Objective: document film-holder BUSY handling and the Minolta-specific gamma-table transfer, without implying broader device or color-calibration validation.

## Two independent changes

### 1. Film-holder BUSY handling

The isolated `minolta-film-holder-busy-v2.patch` on `main` adds bounded retry handling for the film-holder BUSY response (20 retries, 100 ms delay in the research implementation). See [patch provenance](PATCH-PROVENANCE.md) and [R005 hardware record](RESEARCH-005-HARDWARE-PASS.md).

### 2. Gamma-table interpolation (Research-009)

Research-009 changes the Minolta-specific gamma table from a 4096-byte transfer containing fewer calculated values to a full 4096-value interpolated table. The final hardware log records `table_raw_size=4096`, `table_size=4096`, `values=16`, with 4096 gamma bytes per channel.

The source reference is [commit `025c6d9`](https://github.com/bjoepen/minolta-sane-patch/commit/025c6d908a734eaf1f9c1d7e45afbd1e9aec246e) on the research branch, **not** a patch merged into `main`. See the [R009 hardware record](RESEARCH-009-HARDWARE-PASS.md) and [provenance matrix](PATCH-PROVENANCE.md).

## Reproducibility and observed results

- [GitHub Actions R009 run 38144927316](https://github.com/bjoepen/minolta-sane-patch/actions/runs/38144927316) is the cited build/artifact reference.
- The final 11 October 2026 hardware report documents a completed 600 dpi RGB8 scan, 564 × 850 pixels, 1,438,200 bytes transferred, EOF, TIFF creation, `sane_close`, `sane_exit`, and exit code 0.
- The reported R009 backend SHA-256 is `732820b2bf2c1d525cc1ce91dbfc8852a77130de0e8df0e823b8dab309cc59f6`. The archived evidence does not independently prove which backend binary the runtime loader selected.
- A technically completed scan is **not** evidence of calibrated color accuracy, gamma semantic correctness, or general compatibility with other modes/devices.

## Research-008C: qualitative tone comparison

An operator-created four-panel comparison distinguishes:
1. NoGamma, inverted only.
2. NoGamma, common/global stretch.
3. NoGamma, independent RGB stretch.
4. Gamma enabled, inverted only.

These are **different processing pipelines**, not a controlled gamma-on/gamma-off A/B test. The comparison illustrates how dramatically tone and color appearance depend on gamma upload and subsequent processing; it does **not** establish that gamma-enabled output is better, more accurate, or directly comparable to the stretched variants.

The original image has **not** been added to this public repository update; image publication and provenance should be reviewed separately.

## Additional static reverse-engineering observation (unverified against upstream implementation)

Static inspection of the original Windows `DS_Dual2U.dll` suggests a 256-to-4096 sample interpolation routine, with 16 output steps per source interval and a repeated final sample. Integer rounding/truncation and any inversion flags may differ from a floating-point SANE implementation. This is a **research lead**, not proof of equivalent device output or a fully verified upstream fix. The DLL itself is not redistributed.

## Upstream discussion and next steps

Potential upstream context: [SANE merge request !1066](https://gitlab.com/sane-project/backends/-/merge_requests/1066) and [work item #894](https://gitlab.com/sane-project/backends/-/work_items/894). Their contents and relationship to this research **have not yet been verified**, due to GitLab rate limiting. Do not post this report as a response claiming those discussions cover these findings until their contents are reviewed.

Suggested maintainer review: inspect the bounded BUSY retry independently; inspect Minolta-specific gamma table length and interpolation separately; decide on a minimal upstream patch only after review. No scanner installation or local Homebrew library change is required to read or review this document.
