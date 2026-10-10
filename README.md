# Minolta SANE experimental build

Experimental, isolated build of SANE 1.4.0's avision backend with a bounded Minolta film-holder BUSY retry. This does **not** install or overwrite local Homebrew SANE.

The workflow runs on a disposable GitHub-hosted Apple Silicon macOS runner and uploads binaries plus linker diagnostics. The output is **not yet validated** for interchangeability with Homebrew's SANE 1.4.0_2 on macOS Tahoe. Do not replace any Homebrew libraries with this artifact.

To run: GitHub → Actions → Minolta SANE ARM64 test build → Run workflow.
