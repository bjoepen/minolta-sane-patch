# Minolta SANE research index

This index separates source-level and CI evidence from observations made during local hardware tests. A successful build is not a hardware test, and a technically successful scan does not establish image quality or color accuracy.

## Chronology

| Research | Scope and outcome | Evidence status |
|---|---|---|
| R003 | Early investigation of the Minolta DiMAGE Scan Dual II / Avision path. Surviving material is incomplete; no independent PASS claim is made here. | WARN — historical sources are incomplete. |
| R004 / Research-005 | Film-holder BUSY retry and a 4096-byte gamma-table transfer with 512 calculated values and padded tail. Four-frame hardware run documented at 600 dpi, RGB8, 564 × 850. | PASS for the documented scan lifecycle; image-quality assessment is not a measured result. See [Research-005](RESEARCH-005-HARDWARE-PASS.md). |
| R006 | No separate primary-source record was identified in the audited repository/archive set that would support an independent result. | WARN — do not infer a result from numbering or later files. |
| R007 | Gamma-tail repetition experiment. The GitHub branch and Actions evidence establish source/build history, not hardware behavior. Later local scans are described separately and their loaded backend binary is not hash-bound to the Git branch. | WARN; qualitative rejection is a historical operator observation. See [Research-007 and R008B](RESEARCH-007-GAMMA-TAIL.md). |
| R008 | No distinct R008 primary-source record was identified in the audited set; R008B is documented separately below. | WARN — no result assigned. |
| R008B | Local scan experiment with gamma upload disabled. A successful image transfer is reported, but an EOF-time backend release error is present in the available log. | WARN — not a clean backend lifecycle PASS; no image-quality conclusion. |
| R009 | Gamma interpolation to 4096 calculated values; final hardware run documented on 11 October 2026, distinct from an earlier 15:31 run that calculated only 512 values. | PASS for the documented final run's technical scan criteria; see [Research-009](RESEARCH-009-HARDWARE-PASS.md). |

The GitHub research references are immutable commit links: [R004](https://github.com/bjoepen/minolta-sane-patch/commit/30b0d8a69c0263c6f2a3bba63b31a3e3e1d9c931), [R007](https://github.com/bjoepen/minolta-sane-patch/commit/2942581853c7dd1079fde4144f9be0ea75a8027e), and [R009](https://github.com/bjoepen/minolta-sane-patch/commit/025c6d908a734eaf1f9c1d7e45afbd1e9aec246e). The repository main examined for this consolidation is `5c6879942e8cf9e47a752050fff7ccd970c533dd`.

## Historical draft pull requests (checked 2026-10-16)

Both pull requests remain open drafts and are **not merged**. Experimental research branches are not automatically part of `main`.

| PR | Title and status | Base | Head | Relationship |
|---|---|---|---|---|
| [#1](https://github.com/bjoepen/minolta-sane-patch/pull/1) | “Research 004: isolated Minolta gamma 4096-byte transfer experiment” — open, draft, `merged=false`, `merged_at=null`. | `main` at `5c6879942e8cf9e47a752050fff7ccd970c533dd` | `research-004-gamma-4096` at `30b0d8a69c0263c6f2a3bba63b31a3e3e1d9c931` | Proposes R004's padded 4096-byte transfer experiment; does not establish gamma semantic correctness. |
| [#2](https://github.com/bjoepen/minolta-sane-patch/pull/2) | “Research 007: gamma-tail A/B experiment” — open, draft, `merged=false`, `merged_at=null`. | `research-004-gamma-4096` at `30b0d8a69c0263c6f2a3bba63b31a3e3e1d9c931` | `research-007-gamma-tail` at `2942581853c7dd1079fde4144f9be0ea75a8027e` | A stacked experiment over the R004 branch, not directly over `main`. The later R009 branch is a separate line and is not descended from the R007 head. |

GitHub's PR API also populated `merge_commit_sha` for these open drafts; that field is not evidence of a completed merge here because both records explicitly report `merged=false`, `merged_at=null`, and `state=open`.

## Patch provenance

See [patch and build provenance](PATCH-PROVENANCE.md) for patch hashes, CI references, backend hashes, and the distinction between documented binary identity and independently established runtime identity.

## Evidence limits

- Local Research-005 directories later accumulated R009-named files. Directory membership alone does not make those files R005 evidence.
- The standalone R009 RAW candidate has no manifest entry tying it to the final PASS archive. It is not presented as the final run's verified RAW.
- No research report here claims a calibrated color result or independently verified RAW/TIFF pixel identity.
- Large image artifacts, binaries, private logs, and ZIP backups are intentionally not included in this public documentation proposal.
