# Research-007 and Research-008B

## Research-007: repeated gamma tail

The R007 source experiment repeats the existing 512-value segment to fill the 4096-byte transfer table. Its Git reference is [`2942581`](https://github.com/bjoepen/minolta-sane-patch/commit/2942581853c7dd1079fde4144f9be0ea75a8027e); the experiment commit is `f52f9aaa5d513f8484e17ab5ac0cd30c97bd2c6b`.

**PASS — build/audit only:** the GitHub Actions record is run `38120420971`, artifact `11695381483`, and reports a successful build. The CI binary SHA recorded by the audit is `8e4617d97988855ef2ea90b8d254f52d261c3d5a23e5bb70b377ec6a5aad26e0`. This is not a hardware test or evidence of compatibility with a locally installed scanner stack.

**HISTORISCH BEOBACHTET:** subsequent local R7-0 and R7-1 scan notes report technical scans with an experiment marker; R7-1 first had an open failure and later retry success. The available logs do not cryptographically bind the runtime-loaded backend to the R007 source or CI binary. The operator's qualitative judgment that R007 was a clear image-quality failure is preserved as a historical observation. No quantitative paired R7-0/R7-1 histogram or image comparison was found in the audited evidence. A baseline JSON relates to R005 and must not be represented as an R007 comparison.

## Research-008B: gamma upload disabled

The local R008B experiment disabled gamma-table upload. A scan/output is reported, but the available backend log includes a release-unit error at EOF and no backend binary hash. It is therefore **WARN**, not a clean lifecycle PASS. No independent image-quality evaluation or color-calibration result is claimed.

## Quality evidence and publication boundary

The available material supports statements about source behavior, build results, and operator observations, but not a quantitative ranking of image quality. Any future comparison should use identified existing image pairs and a separately approved offline analysis. This documentation does not include private scans, screenshots, or complete debug logs.
