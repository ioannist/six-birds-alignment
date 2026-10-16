# Redactions in the public copy

This repository is a public snapshot of a private working repository. Two kinds of material were changed
or left out.

1. **Private material.** Ideation notes, agent configuration and session logs, review records and internal
   planning records are not published (see `.gitignore`). Some published files still name them, for example
   `../brainstorm/...` in `covenant_lab/README.md`, `../math/REPORT.md` in `covenant_lab/README.md` and
   `math/B4.md`, and the file hash lists in `paper_prep/repro/`. The mathematics handoff's own
   process records (`math/REPORT.md`, `CLOSURE_AUDIT.md`, `NEXT_PACKET.md`, `BLOCKED_AUDIT.md`,
   `SELF_REVIEW.md`) are not published; the per-target notes, scripts, logs and Lean files are. The paper's
   source files (`paper/`, `paper_prep/A3_macros.tex`) are published without their internal planning
   comments; the rendered paper is unchanged.
2. **An unpublished source.** In `covenant_lab/`, references to an unpublished philosophy manuscript by the
   author were removed: its file paths, section labels and content hashes in `verify.py`,
   `verification.json`, `audit_results.json` and `r2_source_additions.json`, and its title in two
   preference labels (`integrated.py`, `integrated_declaration.json`). The paper does not cite that
   manuscript. `r2_review_edits.json`, a review record quoting it, is omitted, so `r2_verify.py` cannot run
   here.

Because of item 2, the hashes that `audit_results.json` records for `verify.py` and `integrated.py` are the
hashes of the unredacted private files. The provenance checks in `audit.py` and `verify.py` also read the
author's sibling corpus repositories, which are not part of this snapshot. The exact model computations
(`python3 covenant_lab/audit.py` model sections and the per-model scripts) do not depend on either.
