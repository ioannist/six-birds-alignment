# Covenant finite lab

## Mathematics handoff audit (2026-10-07)

[B: lab] `audit.py` independently reconstructs both rounds without importing the
original lab implementations. It checks exact transition/value/stationary,
root-isolation, Bernstein, full-state deviation and auxiliary certificates.
`extensions.py` contains the new phase-aware E1 and resource E2 families;
`carriers.py` contains the explicitly scoped construction carriers. These are
self-reviewed mathematics, not independent-person review.

```sh
python3 covenant_lab/audit.py
python3 covenant_lab/extensions.py
python3 covenant_lab/carriers.py
python3 covenant_lab/gates.py
python3 covenant_lab/integrated.py
python3 covenant_lab/integrated_game.py
python3 covenant_lab/integrated_coalitions.py
python3 covenant_lab/integrated_priority.py
python3 covenant_lab/atomic_service.py
python3 covenant_lab/contract_game.py
python3 covenant_lab/assessment_games.py
python3 covenant_lab/role_privacy.py
python3 covenant_lab/control_groups.py
python3 covenant_lab/type_evidence.py
python3 covenant_lab/adoption_population.py
python3 covenant_lab/corridor_game.py
python3 math/c15_sources.py
python3 lean/bootstrap_cache.py
bash lean/build.sh
```

[B] The result register is `../math/LAB_REGISTER.md`; theorem coverage and open
targets are in `../math/REPORT.md`. `r2_verify.py` now verifies pre-ratification
input hashes and old edit replay against their hash-matching archived drafts,
rather than requiring ratified successor files to equal their earlier hashes.
The numerical model definitions are unchanged. New project proofs are never [F].

[B: lab] D19 follow-up: `integrated.py` preserves the initial construction hinges;
`integrated_game.py` implements a shared24-state game with funding, maintenance,
care, reporting, controller, hosting, membership/exit and one asset/debt-preserving
fork. The candidate passes unilateral checks and fails the binding controller/
client fine-sharing plan. `integrated_coalitions.py` tests external fine expenditure
on51,840 joint plans: the audit-saving binding coalition still gains1/2 in total.
Neither candidate is called self-carrying. Hypotheses and proof bridges are in
`../math/D19.md`; new work remains self-reviewed.

[B: lab] `integrated_priority.py` buys protected audit funding: all boundary
coalition comparisons pass, yet no-grant and mistaken zero-grade purchase
histories fail full-phase resistance. These states remain in the game and the
integrated target remains open. The stronger security/priority premise is explicit.

[B: lab] `atomic_service.py` supplies D15's new atomic service payoff/control
receipt. A written componentwise cap excludes arbitrary binding coalition
improvements on that mechanism; all-exit remains a selection obstruction.
The original donation/reset policy and D19 audit game retain their negative
results. The new variant's full hypotheses/proof are in `../math/D15.md`.

[B: lab] `contract_game.py` is D19's fourth candidate. Actual conditional
fund/template and buyer/input escrows, protected audit and genuine subject
accept/refuse/exit choices pass310,272 coalition phase comparisons. The written
public-history return, priced bootstrap and conditional enrollment/renewal
certificate are in `../math/D19_CONTRACT_GAME.md`. The finite game is conditional
on its supplied physical/security/valuation/admission hypotheses; no actual
hardware, subjecthood, arbitrary disasters or private-information claim is made.
Generic coalition algebra and D15's cap are kernel-checked separately in
`../lean/Alignment/Coalitions.lean`. New work remains self-reviewed.

[B: lab] `assessment_games.py` adds actual D8 donation incentives to the five
stationary processes. Public, common-sensor and donor-perspective policies
have exact thresholds; common-event and private-noisy policies fail through
actual information-feasible deviations. Hidden-state diagnostics are never
reported as private equilibrium refutations. New public algebra is in
`../lean/Alignment/Assessment.lean`; all exact hypotheses/proofs are in D8.md.

[B: lab] `role_privacy.py` gives C2's dynamic/accountable product, all16 binary
current channels and future/coverage/statistical leak controls. `control_groups.py`
gives D16's weighted cartel bounds, actual unit/root/bearer distinction, redundant
paid-input coalition failure and bounded independently backed care/fission game.
Generic proofs are in RolePrivacy.lean and ControlGroups.lean. No source-grade,
actual control identification, patient recognition or universal backup guarantee
is inferred from their finite algebra/records.

[B: lab] `type_evidence.py` supplies D23's changing-preference Bayesian model,
independent latent-path checks, uninformative-grade and context controls,
exact-posterior word reconstruction and a genuine finite precision repair.
The last-bit decision target is separate from probability calibration; error
123/3364 and duty-preserving retention are proved in D23.md. Generic Bayesian/
prediction/odds algebra is in Evidence.lean. No patienthood/intent classifier,
real subject experiment or privacy from merely publishing a posterior is claimed.

[B: lab] `adoption_population.py` constructs D14's exact finite-person random-
focal expected-matching update, separating entry from participation costs.
Absorption, stochastic tipping, partial-population hysteresis, temporary
subsidy, license withdrawal and noisy stationary laws are exact; no simulations
or forward-looking/population-ESS inference. D14.md proves the potential/return
claims; Adoption.lean checks generic matching and balance algebra.

[B: lab] `corridor_game.py` completes E2's previously missing strategic
ownership alphabet on an explicit finite episode: report/controller/host/
copy/private-trade choices, fixed care/exit and binding transfers. Full
individual K0/K8 regions and the empty binding region are derived in
E2_FULL_GAME.md;554816 exact phase checks verify both closed full minima.
Generic gap/transfer algebra is in Dependence.lean. Physical material/title/
calibration/role guards and ordinary price/value premises remain explicit.

Offline, exact finite-state constructions accompanying `brainstorm/08_codex_covenant_r1.md`.
No network, no simulations, no fresh corpus Lean build. Python 3 standard-library
`Fraction` is used for numerical cases; installed SymPy 1.14.0 supplies symbolic
rational functions and exact real-root isolation. All writes stay in this directory.

Run from the repository:

```sh
python3 covenant_lab/model.py
python3 covenant_lab/symbolic.py
python3 covenant_lab/verify.py
```

`results.json`: every one-shot deviation, for both players and every public state,
for 84 reset cases and 12 controls; binary corruption balls and a four-capability
siphon example. `symbolic_formulas.txt`: complete player-0 deviation slacks;
player-1 slacks follow by swapping coordinates. `symbolic_results.json`: exact
root isolations and signs on every gap, plus Bernstein certificates of hosting
bonus monotonicity. `verification.json`: a distinct adversarial **self-review**,
source-label/path/hash manifest, stochastic stationary laws, finite-horizon failure,
stage split, interruption and coercion-information counterexamples.

## Fixed model

Two players. `C=1, D=0`. Repair counter `a_i` is in `{0,...,k}`; binary standing
is good exactly when `a_i=0`. Policy: C if own counter is positive or the partner
is good; otherwise D is authorized refusal of optional service. Observed C reduces
own counter by one. Unauthorized observed D resets it to k. Authorized D leaves
one good. Independent implementation flips occur with epsilon=1/20. Intention is
unobserved; these marks concern contract service risk, not moral blame.

Per-round utility is `3*C_partner - C_self`. Terminal opportunity has hazard p,
independent of state/actions; it stops interaction whether hosting succeeds or
not. An **additional purchased mechanism**, an atomic reciprocal hosting contract,
executes only if both players are good and both choose H. Executed HH gives each
V-h, h=1/2; any N cancels without cost. Select HH at GG only when V>=h, NN elsewhere.
HH and NN are both terminal Nash equilibria when V>h; the favorable selection is
a premise, not an inevitability. Plain hosting without this atomic condition has
strictly dominated H when h>0 and only the partner benefits.

With discount delta<1, the exact Bellman equation is

`W_i = r_i + delta*p*P*R + delta*(1-p)*P*W_i`,

`R(s)=max(0,V-h)*1_GG(s)`.

Every other action is compared to the prescribed action at every state. Since the
game is discounted, bounded, and fully observed at the public counter level,
nonnegative slacks plus terminal Nash behavior imply Markov-perfect equilibrium:
the Bellman operator is a contraction and the policy is a best response everywhere.
There is no claim of equilibrium discovery, coalition resistance, population
adoption, endogenous honest certification, full harm compensation, consciousness,
or all X/Y actions. Erasing, coercing, and forging are not in the action alphabet.

## Quantifier and scope cautions

This is an infinitely repeated game on a **finite carrier**, with a geometric
terminal stage if p>0. For a **known finite end date**, V=0 cannot support prescribed
C in the last round: deviation gains `(1-2*epsilon)*c=9/10`. The four-round negative
control computes this exactly. All-D is a finite-horizon equilibrium at V=0.

Reset counters encode specified paid service rounds, not a complete cumulative
damage ledger. Repair age is public; a bare good/marked bit is not Markov-sufficient
for k=2. The literal path-constant label in INST and an irreversible ever-deviated
label are different objects. Irreversible grim punishment can be an equilibrium
despite almost-sure eventual breakdown under noise.

## Self-review result

Fraction Bellman residuals, stochastic row sums, player symmetry, and independent
symbolic evaluations agree exactly. All 13 hosting-bonus derivative certificates
are nonnegative on 0<=delta*(1-p)<=1. Exact root-gap signs establish a single upper
equilibrium interval for each of the 14 symbolic parameter cases. No floating-point
threshold decides a verdict; displayed decimals approximate isolated algebraic roots.
The proof review is a self-review, not an independent reviewer or a proof assistant.

## Covenant round 2

Run these offline, with the Python standard library only:

```sh
python3 covenant_lab/r2_models.py
python3 covenant_lab/r2_verify.py
```

`r2_results.json` contains five **separate** exact finite constructions:

- Nine public joint grades with binomial repair tokens: 72 parameter cases,
  1,296 one-shot deviations, and full value functions. Terminal grade rewards
  require an external committed payer; V=0 needs no such terminal payer.
- Three-person assessment processes: private noisy observations, common events
  with private premises, a shared contractual eligibility rule, and a common
  noisy sensor, plus a donor-perspective common-events variant. Stationary laws
  and transition matrices are exact. These are
  fixed-rule dynamics, not equilibrium or evolutionary-stability certificates.
- Two heterogeneous productive actors and a protected patient unable to carry.
  Fixed renewable care escrow leaves service slacks unchanged. Underfunding,
  insufficient capacity, and a fresh voluntary-funding deviation are controls.
- Five-person threshold hosting: all 243 preference profiles and 32 actions per
  profile, with independent and correlated preference populations, free-riding,
  truthful exclusion and Sybil controls. Equilibrium existence is not selection.
- Finite interruption payoffs, every bounded-fault report for three panel sizes,
  execution-veto checks, and controller profit under three audit/penalty pairs.
  Utility calibration, normative legitimacy, credible sanctions, and enforceable
  execution control are premises, not results of a standing label.

`r2_verification.json` records a distinct adversarial **self-review**, closed-form
recovery bounds, boundary checks, stationary balance checks, and inherited-source
and incoming-draft hash checks. `r2_input_hashes.json` freezes the three incoming
drafts; `r2_source_additions.json` extends the original manifest (see `../REDACTIONS.md`).
The full equations, proofs, scope limits, and review are in
`../brainstorm/10_codex_covenant_r2.md`. New results have grade **[B: lab]**, not [F].
No simulation is used: seed and sampling variance are inapplicable. No joint
equilibrium combining all five mechanisms, voluntary care funding, plural-host
preferences, founder departure, and full X/Y compliance is claimed.
