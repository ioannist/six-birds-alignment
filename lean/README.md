# Alignment formalization

[B] Pinned Lean4.28.0; Mathlib revision
`8f9d9cff6bd728b17a24e163c9402775d9e6a365`. This offline project copies a local
compiled import closure into its own cache/output path; it never builds or writes
inside a sibling repo. `cache_manifest.json` records dependency commits and
SHA256 hashes for every copied source/object. Cached dependencies are ignored
by git. Local source declarations and Lake configuration are retained.

```sh
python3 lean/bootstrap_cache.py
bash lean/build.sh
```

[B] The bootstrap requires the existing pinned cache at
`/home/repos/six-birds-currency/lean/.lake/packages`. A different host needs that
cache or the equivalent pinned import closure supplied before building; no
download fallback is attempted. `lake build` works after bootstrap because its
external imported objects are installed under this project's local output tree.
It does not rebuild their sources. `build.sh` also prints all theorem axioms and
checks local proof files for holes/axiom declarations.

[B: lab] Catalogue mapping: `Alignment/Recovery.lean` D7/E3;
`Decoding.lean` D5; `Payoffs.lean` D10/D11 and D1 endpoint signs;
`Horizon.lean` D3/E5; `Discounted.lean` D18(f); `Carrier.lean` C13, with C3/C5/C9
applications. `Behavioral.lean`, `StochasticGame.lean` and
`CertificationControls.lean` complete D18(f)'s finite observed-game certificate.
Every local theorem appears in `AxiomAudit.lean`; regenerate it with
`python3 math/update_axiom_audit.py` before rebuilding after a new theorem.

[B] Formalization coverage is `../math/D18.md`; actual types and transitive axioms
are in `trust_base.txt`. The new game certificate derives payoff convergence
and covers behavioral deviations, mixed Markov candidates and available menus.
The older pure-tail helper still accepts convergence, but is not used by the
new theorem. The decoder export now constructs majority decoding and checks
decoder existence as well as disjoint balls. Physical implementation and private-information games
require separate modeling evidence.
