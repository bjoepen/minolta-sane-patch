# Research-009: final hardware PASS record

## Source and distinct runs

The source reference is commit [`025c6d9`](https://github.com/bjoepen/minolta-sane-patch/commit/025c6d908a734eaf1f9c1d7e45afbd1e9aec246e). The final hardware report is dated 11 October 2026. It refers to GitHub Actions run `38144927316`, artifact ID `11703769629`, and records backend SHA-256 `732820b2bf2c1d525cc1ce91dbfc8852a77130de0e8df0e823b8dab309cc59f6`.

The earlier 15:31 run is distinct: its log reports a 4096-byte transfer with only 512 calculated values. The available `frame1-coldstart` files are associated with this run by their shared basename, matching 15:32:13 modification times, parameter file, and client/backend logs. The RAW is 1,438,200 bytes, SHA-256 `b480f83673568c1cd2d2618d4b8a36230d7d54ab57a7871d54c95753fcc72605`; its parameter file records RGB, 564 × 850, 1692 bytes per line, 8-bit depth, 1,438,200 raw bytes, and EOF status 5. The TIFF is 1,438,358 bytes, SHA-256 `f0f4cb87b1dec0bdd09398821578a61db9be3156b8c688da3d57425229b5a8d0`; the client log records that this TIFF path was written at 15:32:13.239, followed by client exit 0 at 15:32:13.240. The backend log for that run records `table_raw_size=4096`, `table_size=512`, and `values=2`.

**Evidence qualification:** the logs and matching metadata support treating these files as outputs from the same early run. They do not establish pixel-for-pixel identity between the RAW and TIFF; no pixel comparison is claimed. This pair is not evidence for the final 17:25 hardware PASS.

The final 17:25 run reports `table_raw_size=4096`, `table_size=4096`, `values=16`, and 4096 gamma bytes per color channel. The two runs must not be merged into a single evidence record.

## Final run result

**PASS — technical scan criteria documented for the final run.** The final log/report record a completed scan, EOF, TIFF creation, `sane_close`, `sane_exit`, and process exit 0. The recorded transfer totaled 1,438,200 bytes. The report describes a 4096-entry interpolated table. These observations support the reported technical lifecycle for that run.

They do not establish calibrated color fidelity, a quantified improvement in image quality, or pixel identity between a RAW and TIFF. No such claim is made here.

## Archived evidence and manifest limits

The final outer archive is `Research-009-Hardware-PASS-2026-10-11.zip`, SHA-256 `cec18173b51ad275998afca682571deadfd46f55efc73abf6fc45f1debf367b2`, size 3,811,810 bytes. Its seven entries are the report, TIFF, backend log, client log, and three screenshots. It does not contain the RAW, parameter file, or JPG mentioned elsewhere in the outer archive/manifest material.

The outer checksum list records, among other entries:

| Artifact | SHA-256 | Presence/evidence note |
|---|---|---|
| Backend binary | `732820b2bf2c1d525cc1ce91dbfc8852a77130de0e8df0e823b8dab309cc59f6` | Checksum recorded; binary itself is not in the ZIP. |
| TIFF | `aa17b87a1bae07c65e5458748f943c56bacf5b2ae961b9a29027e1825ae93612` | Present in ZIP and checksummed. |
| JPG | `00effe85cbe3bf3e48815bf620eaf8617560eb32a8d22b52668cd6a6f1fd5e3b` | Listed in outer checksum material, absent from ZIP. |
| Backend log | `3294fb168852c3d1e44d9a1292f1b084c6754a2393061e81c416dd926b21484c` | Present and checksummed. |
| Client log | `003af7035834dee9eb929c59bcfeb1842c8566ea457fb46a381732a79025f627` | Present and checksummed. |
| Parameters | `88a0f89f9ea11be5b3fdaa5631d6a7f95c035ce42577bf270bebf1bf6dfe51dc` | Listed in outer checksum material, absent from ZIP. |
| Report | `d208c4d46c965fafc5f78e08b9a463406d13dfb9f7aa388e3d3bffe80a9c025a` | Present and checksummed. |

The report's dated manifest omits JPG and parameter entries although the outer checksum material includes them; the ZIP also omits them. `.DS_Store`, `FILES`/`LINKAGE` metadata and other outer-archive files are not all represented by the same manifest. This is a documented **WARN** and should be resolved only by a future, traceable archival revision—not by silently rewriting the protected PASS archive.

## RAW candidate boundary

A loose RAW candidate associated by filename, size, and chronology has SHA-256 `3450a26ac0a393f3ff0bbbe594c3f9966617a78ea037b0db96863055056bbb04` and size 1,438,200 bytes. It is absent from the final ZIP and its manifest. It is therefore **WARN / plausible candidate**, not a proven RAW from the final 17:25 run.
