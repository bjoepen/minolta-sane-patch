# Research-005: R004 hardware PASS record

## Scope and source basis

This page records the original Research-005 hardware result associated with the R004 source state, not later R009-named files subsequently stored alongside it. The Git source reference is R004 commit [`30b0d8a`](https://github.com/bjoepen/minolta-sane-patch/commit/30b0d8a69c0263c6f2a3bba63b31a3e3e1d9c931). The local recovery report is the primary narrative source; the archived client/backend logs and checksums are supporting evidence.

## Technical result

**PASS — technical scan workflow as documented.** The report and per-frame logs describe four sequential frames, each handled by a separate client process, with the film-holder BUSY retry, gamma upload, completed transfer, EOF, TIFF output, SANE close/exit, and process exit 0. The documented profile was 600 dpi, RGB8, 564 × 850 pixels, 1692 bytes per line, and 1,438,200 RAW bytes per frame. The reported gamma upload was 4096 bytes per channel with 512 calculated values and a padded remainder. Separate processes and an approximately 30-second inter-frame pause are reported.

This establishes neither calibrated color fidelity nor a comparative image-quality result. “Technical PASS” is limited to the recorded lifecycle and outputs.

## Provenance

| Item | SHA-256 / reference | Evidence qualification |
|---|---|---|
| R004 commit | `30b0d8a69c0263c6f2a3bba63b31a3e3e1d9c931` | Git source reference. |
| Backend binary (`libsane-avision.1.so`; same hash reported for `libsane-avision-pre-R007.so`) | `2a00eec4d73afeb08a3524c99f6aa67a08a519601b819ce453210ee644f7ffed` | Archived binary identity; see limitation below regarding runtime loading. |
| Client binary | `cfb3ba28d854a40806119d17df37acfda23859dd03da8b0f066515e39ba20f5a` | Archived file identity. |
| Client source | `35054579474360b7ce88b5288d6ec15a357a3ba4cadaacacae869c523b3741ae` | Source identity recorded in the archive. |
| Batch shell script | `f72e4e6947ef646aa6c99789c685db792f3a1f258da1b94eb69230671e67464b` | Archived file identity. |

The backend SHA ties the archived binary to a particular file, but the available record does not independently prove that this exact file was the image loaded by the scanner process at runtime. Treat runtime backend identity as **WARN**, not as cryptographically established.

## Archive boundary

The original Research-005 evidence set includes the four-frame logs, parameters, RAW/TIFF artifacts, client and backend binaries, source/script, and checksum manifests. A later recovery ZIP additionally contains the recovery report, patch materials, and a Git snapshot at R004. These are distinct archive products; their file lists and manifests should not be conflated. The archive hashes recorded by the audit are:

- Initial Research-005 PASS ZIP: `bae90344cd3cf0153e566cc639de23411dc6703e72d5b158c56fa85f0c2e22b2`.
- Recovery ZIP: `6c0535a4cf221bec5c6eb91a36b468fb4d7b7c8c910f6b00a6e8f2ca4cbf4ce6`.

The original checksum manifest covers selected core binaries/source/script rather than every scan output. Do not infer a scan artifact's manifest status from the existence of a separate archive-level hash.

The current loose `frame2.tiff` at the historical Research-005 location has SHA-256 `d53f736815f1e202957ca48e5d7eb4d0cbfeaeaab0c0d512f5fb0c6c8275e40f`. This corrects the incomplete value transcribed in an earlier audit. The prior read-only stream comparison reported that both initial and recovery ZIP members matched this file; this consolidation did not extract or modify either archive.

## Later files in the Research-005 directory

Files named `r009-test-01.*` and the corresponding 4096/4096 log belong to a later R009-era experiment by naming, timestamps, and contents. Their placement in the Research-005 directory does not reclassify them as R005 evidence. The loose RAW is a plausible R009 candidate, but it is not listed in the final R009 archive manifest and is not established as the final-run RAW.
