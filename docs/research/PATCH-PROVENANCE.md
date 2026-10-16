# Patch, build, and provenance matrix

## Patch identities

Patch hashes below are SHA-256 values of the patch contents as audited, not hashes of resulting backend binaries.

| Change | Commit/reference | Patch SHA-256 | Technical effect | Build / hardware / quality status |
|---|---|---|---|---|
| Film-holder BUSY v2 | Present on main `5c6879942e8cf9e47a752050fff7ccd970c533dd` | `62b2e840ff315ab7363b6b9c91af65132b3a63f34c3ecf6676fdb9ea7b4d4dd5` | Retries the documented film-holder BUSY response within bounded handling. | Hardware lifecycle supported by R005 report/logs; runtime binary binding remains limited. No image-quality conclusion. |
| R004 gamma padding | R004 `30b0d8a69c0263c6f2a3bba63b31a3e3e1d9c931` | `9216c1868ef40ac5cdaec515c032bc87cdb15acdd6f97172ffa3a539ed3818c5` | Sends 4096 bytes while calculating 512 values and padding the rest. | R005 technical hardware run recorded 4096/512. Tonal assessment is not quantitative. |
| R007 repeated tail | R007 `2942581853c7dd1079fde4144f9be0ea75a8027e`; experiment `f52f9aaa5d513f8484e17ab5ac0cd30c97bd2c6b` | `aae575e92f8472beeb7e3aa642323a4890a6150fde10a29b0d6cb2a184a5a7f0` | Repeats a 512-value gamma segment to fill the transfer table. | CI build success only; later local scan logs lack pinned runtime backend identity. Qualitative FAIL is historical operator observation, not measured comparison. |
| R009 gamma interpolation | R009 `025c6d908a734eaf1f9c1d7e45afbd1e9aec246e` | `ed99e92f35371d6a3342b997132692aa194bd5eeae7aff7254e15ed779427f44` | Interpolates the gamma data to the 4096-byte table. | Final hardware report records 4096/4096 and `values=16`; technical PASS only. No calibrated color claim. |

The local loose R009 patch copy has SHA-256 `e5c9ab032bb2446095695cefe5076fc12277ecc8d8277f5552d233f6aa19a115`; audit found only a comment-line difference from the GitHub patch (“Research 004” versus “Research 009”), with functional lines matching. This local copy is not a separate verified implementation and is not included in this repository documentation.

## Build and binary references

| Evidence | Reference / SHA-256 | What it establishes | What it does not establish |
|---|---|---|---|
| R007 GitHub Actions | Run `38120420971`; artifact `11695381483`; CI binary `8e4617d97988855ef2ea90b8d254f52d261c3d5a23e5bb70b377ec6a5aad26e0` | A CI build artifact was produced from its workflow/source. | No hardware execution or local backend interoperability. |
| R009 GitHub Actions | Run `38144927316`; artifact `11703769629` | Workflow/artifact reference in the R009 evidence chain. | Does not independently identify the binary loaded during the hardware run. |
| R005 archived avision backend | `2a00eec4d73afeb08a3524c99f6aa67a08a519601b819ce453210ee644f7ffed` | Archived file identity; two archived filenames share this hash. | No independent runtime loader proof. |
| R009 report backend | `732820b2bf2c1d525cc1ce91dbfc8852a77130de0e8df0e823b8dab309cc59f6` | Report/checksum identity for the R009 backend artifact. | The binary is not included in the final ZIP; does not alone prove runtime-loaded identity. |
| R005 client source | `35054579474360b7ce88b5288d6ec15a357a3ba4cadaacacae869c523b3741ae` | Source-file identity. | Does not identify a later D5/D6 Digitizer client. |

## Public release and provenance boundaries

This documentation intentionally omits RAW/TIFF/JPG originals, executable backend/client binaries, ZIP backups, complete debug logs, private local paths, and user-identifying diagnostics. Publicly useful evidence consists of source commits, patch hashes, selected artifact hashes, test criteria, and explicit provenance limits. A checksum is an identity reference, not proof that a file was loaded at runtime.
