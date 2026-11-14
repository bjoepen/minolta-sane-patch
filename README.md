# Minolta DiMAGE Scan Dual II — SANE research

Experimental, isolated investigation of the SANE 1.4.0 `avision` backend for the Minolta DiMAGE Scan Dual II (USB `0638:026a`).

**Research status:** The bounded film-holder BUSY patch is on `main`. Later gamma-table experiments, including Research-009's 4096-value interpolation, are documented in research branches and reports; **they are not merged into `main`**. Hardware PASS reports refer to specified scan-lifecycle criteria, **not** calibrated image quality or universal device compatibility.

## Start here

- [Technical findings for SANE maintainers](docs/research/COMMUNITY-TECHNICAL-FINDINGS.md) — scope, observed behavior, limitations, and upstream discussion references.
- [Research index](docs/research/README.md) — chronology and evidence qualifications.
- [Patch and build provenance](docs/research/PATCH-PROVENANCE.md) — hashes, commits, and CI/hardware boundaries.
- [Research-009 hardware report](docs/research/RESEARCH-009-HARDWARE-PASS.md) — final documented scan lifecycle.
- [Research-009 source commit](https://github.com/bjoepen/minolta-sane-patch/commit/025c6d908a734eaf1f9c1d7e45afbd1e9aec246e) and [Actions run](https://github.com/bjoepen/minolta-sane-patch/actions/runs/38144927316).

## Experimental CI workflow on main

The manually triggered [ARM64 test workflow](.github/workflows/minolta-sane-arm64.yml) fetches SANE 1.4.0, applies the **film-holder BUSY patch only**, and builds on a disposable GitHub-hosted Apple Silicon runner. It does **not** install or overwrite local Homebrew SANE. Its output is experimental and must not be substituted for an installed backend without separate compatibility testing.

Run via GitHub → Actions → Minolta SANE ARM64 test build → Run workflow.

## Publication boundary

This repository documents research, not an upstream-approved fix. It intentionally does not distribute the original Windows DLL, private logs, local scanner binaries, or unreviewed image artifacts. No local scanner changes are needed.
