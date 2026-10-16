# Exact lab audit register

[B] Audit date: 2026-10-07. This register concerns newly reconstructed project
mathematics, not new [F] corpus results. The reconstruction does **not import**
`model.py`, `symbolic.py`, `verify.py`, `r2_models.py` or `r2_verify.py`.
It builds transitions from the declared rules, uses SymPy exact domain linear
algebra rather than the original Fraction solver, and compares saved outputs
only after deriving them. Review status: **self-reviewed mathematics, independent
code reconstruction**. The author waived D17's additional distinct-reviewer
acceptance condition on 2026-10-08; see `SCOPE_DECISIONS.md`. This decision
does not change the actual review provenance.

[P] All utility, noise, resource, calibration, authority, escrow, and favorable
hosting-selection assumptions remain declared premises. Care and legitimacy are
not mathematical consequences. Each row has one grade. All result rows are
[B: lab]; the table tag governs every row. Verdicts concern the stated carrier.

[B] Commands used below:

```sh
python3 covenant_lab/audit.py              # A: current independent reconstruction
python3 covenant_lab/extensions.py         # X: new E1/E2 families
python3 covenant_lab/r2_verify.py           # R: original checks with archive repair
bash lean/build.sh                        # L: local kernel build + axioms
```

| Result | Model and statement | Grade | Command | Verdict |
|---|---|---|---|---|
| D1-grid | 84 reset cases, k=1,2; every state, both players, both intended C/D choices | computed exact | A | confirmed |
| D1-thresholds | 14 rational parameter cases; all numerator roots, poles and signs; each passing set is an upper interval | computed exact | A | confirmed |
| D1-quintic | k=2, p=V=0; unique interior binding root of the printed quintic; interval width <10⁻¹² | computed exact | A | confirmed |
| D1-endpoints | Exact signs of that quintic at 2382315/3734821 and 2383666/3736939; no uniqueness asserted by this declaration | kernel-checked | L | confirmed |
| D1-hazard | V=0 replaces δ by δ(1−p); threshold α/(1−p) exists below one only when p<1−α | proved (written) | A; D1.md | confirmed |
| D2-monotonicity | 13 state polynomials for k=1,2 have nonnegative bonus derivative on 0≤δ(1−p)≤1 | computed exact | A | confirmed |
| D2-pV | Same pV=1/2: (1/20,10) and (1/5,5/2) have different exact thresholds | computed exact | A | confirmed |
| D3-last-stage | Known four-round end, V=0: terminal required-C slack −9/10 | computed exact | A | confirmed |
| D3-unraveling | State-independent stage donation, no terminal incentive: unique D choice at every stage by backward induction | kernel-checked | L; D3.md | confirmed on declared donation model |
| D3-positive | Graded game δ=3/4, p=γ=1, V=2: minimum terminal slack 9/20 | computed exact | A | confirmed |
| D3-counter-terminal | k=2, state (2,2) cannot reach GG in one round; no GG-only terminal prize pays for its last repair | proved (written) | D3.md | confirmed |
| D4-no-label | Always-C, action-unresponsive continuation: switching to intended D saves 9/10 | proved (written) | A; D4.md | confirmed |
| D4-permanent | Generous policy with permanent marks: both-marked absorbing, C loses 9/10 | proved (written) | A; D4.md | confirmed |
| D4-grim | Grim clean-state slack 9(209δ−80)/[2(400−361δ)]; equilibrium iff δ≥80/209 | proved (written) | A; D4.md | confirmed |
| D4-collapse | Independent persistent flips: clean-standing survival (361/400)ⁿ tends to zero | proved (written) | D4.md | confirmed; excludes moral interpretation |
| D4-reset-stationary | GG masses 399/440 and 60654859/73455200; mean payoffs 20/11 and 160399/91819 | computed exact | A | confirmed |
| D5-code | Binary transcripts, all n,b∈ℕ: disjoint corruption balls iff n≥2b+1 | kernel-checked | L; D5.md | confirmed, including n=0 and b≥n |
| D5-decoder | Actual majority decoder correct on every within-budget report; decoder existence iff n≥2b+1 | kernel-checked | L; D5.md | confirmed; former written construction bridge is closed |
| D5-panels | Exhaustive n=0,…,7, b=0,…,3; explicit collision transcripts on failure | computed exact | A | confirmed; extends original finite checks |
| D5-blind | Identical target-different honest transcripts collide even at b=0 | proved (written) | D5.md | confirmed |
| D6-interruption | Accept=0, resist=1, standing marked: absence of hosting motive does not imply acceptance | refuted | A; D6.md | confirmed counterexample to that implication |
| D7-values | A+D·s satisfies the symbolic affine Bellman equation over an ordered field | kernel-checked | L; D7.md | confirmed; uniqueness uses discounted-game argument |
| D7-window | Positive cost, ε<1/2, nonnegative returns: all-state IC iff γ(H−ct)≥c(1−t); feasible iff H≥c | kernel-checked | L; D7.md | confirmed symbolic algebra; stochastic bridge declared |
| D7-grid | 72 cases, 1,296 deviations; exact values agree with independent linear solve | computed exact | A | confirmed |
| D7-boundary | At γ_min slack zero; γ_min/2 fails; δ=3/10 noiseless false window has zero-grade slack −64/73 | computed exact | A | confirmed |
| D7-coverage | Mean-grade bound η iff γ≥ηε/[(1−ε)(1−η)] on positive-denominator scope | kernel-checked | L; D7.md | confirmed; no type-information conclusion |
| D7-mean | K=2, ε=1/20, γ=1/4: stationary mean 19/23 | computed exact | A | confirmed for underlying surviving repair chain |
| D8-private | 63 reachable states: C=902899/1181900; disagreement=11039/59095 | computed exact | A | confirmed |
| D8-common-events | 51 states: C=419/496; disagreement=19/248 | computed exact | A | confirmed |
| D8-contract | 7 states: C=127/140; disagreement zero | computed exact | A | confirmed |
| D8-common-sensor | 7 states: C=254087/281740; disagreement zero; sensor error 29/4000 | computed exact | A | confirmed |
| D8-donor-perspective | 7 states: C=127/140; disagreement zero | computed exact | A | confirmed; rule changes as well as information |
| D8-divergence | Two shared D events create opposing assessments of actor 1 | proved (written) | D8.md; R | confirmed; private premises need not be hidden facts |
| D9-escrow | Action/state-independent increment κ shifts values by κ/(1−δ), leaves every slack unchanged | proved (written) | A; D9.md | confirmed |
| D9-heterogeneous | δ=3/4 and 9/10 pass on specified b,c; δ=3/4 minima 44165677838553/125104687722770 and 83050546961979/250209375445540 | computed exact | A | confirmed |
| D9-resource | Endowment 2 makes productive budget 1/2<c; taxes 1/4 each underfund the patient | computed exact | A | confirmed failures despite incentive slacks |
| D9-voluntary | Unconsequential fresh voluntary tax: refusal saves t>0 | refuted | A; D9.md | confirms failure of spontaneous funding claim |
| D10-pivotality | Threshold success: H−N=ωV·Pr(J=m−1)−h | kernel-checked | L; D10.md | confirmed algebra and deterministic m≥2 no-host control |
| D10-population | 243 independent type profiles ×32 actions; successful existence 13/16, strictly willing active pair 47/128 | computed exact | A | confirmed; existence, not adoption |
| D10-correlated | Same type marginals, common type draw: successful existence 1/2 | proved (written) | D10.md | confirmed; independence matters |
| D10-aliases | Five aliases, one capacity/control group cannot meet a two-group requirement | proved (written) | D10.md | confirmed under specified group map |
| D10-exclusion | All ω=0 gives truthful certification without any host | computed exact | A | confirmed; all-N is the sole hosting equilibrium |
| D10-paid | Price 3/4, verifiable cost 1/2, ω=0: hosting gains 1/4 | refuted | D10.md; R | confirms counterexample to exhaustive love/reciprocity claim |
| D11-response | Accept best iff S−a+T≥max(R−σ,A) | kernel-checked | L | confirmed |
| D11-controller | Abuse gain g−qP; weak deterrence iff qP≥g, strict iff qP>g | kernel-checked | L | confirmed for risk-neutral collectible-penalty model |
| D11-tables | Safe accept, delayed-task resist, abusive appeal; audit gains 4,2,−1 | computed exact | A | confirmed |
| D11-veto | Every within-budget report at (1,1),(3,1),(5,2); correctly enforced decoder blocks false permission only on decodable panels | computed exact | A | confirmed; calibration/boundary are premises |
| D15-binding-plan | Always-C binding plan gives 38/5>15009170612/2088907793 at GG, δ=3/4 | computed exact | A | confirmed strong-Nash counterexample; coalition-proofness unresolved |
| D21-stage-split | Same last action/counts/stage sum; counters (1,0)/(0,0), next-CC 19/400 vs361/400 | computed exact | A | confirmed |
| D21-bare-bits | (1,0)/(2,0) share bits; next-GG 19/20 vs0 | computed exact | A | confirmed non-Markov quotient |
| D21-siphons | Four-capability cycles; full-target minimal seeds ac,ad,bc,bd; a reaches only ab | computed exact | A | confirmed finite reachability, not indefinite resources |
| D21-forcing | Fair hidden bit: constant free action conveys zero bits; informed forced action conveys one | proved (written) | D6.md | confirmed comparator counterexample, no contradiction of INST |
| D18-tail | All-state Bellman upper bound dominates history-dependent pure deviation truncations and their supplied convergent limits | kernel-checked | L; D18.md | confirmed as legacy helper; new game rows derive convergence and cover mixed strategies |
| D18-behavioral | Arbitrary histories retain actions/chance outcomes; normalized mixed averaging gives uniform increment bound Mβⁿ and actual payoff convergence/error Mβⁿ/(1−β) | kernel-checked | L; D18.md | confirmed; no supplied-convergence premise in new theorem |
| D18-game | Response kernels constructed from raw shared joint data; one-shot inequalities and Bellman consistency imply all-state Markov-perfect behavior against arbitrary behavioral deviations | kernel-checked | L; D18.md | confirmed on finite fully observed game scope |
| D18-menus | Candidate support and deviations respect player/state-dependent available menus; supported joint outcomes preserve actual chosen/admissible actions | kernel-checked | L; D18.md | confirmed; availability is distinct from unimplemented moral prohibitions |
| D18-controls | Absorbing two-state game: reachable-only check misses a 2-versus-0 deviation; restricting availability changes the result, and an unavailable nominal candidate is rejected | kernel-checked | L; D18.md | confirmed with actual payoff/equilibrium declarations |
| E3-general-K | Mean-law derivation works for every positive integer K and any kernel with the same conditional mean law | proved (written) | E3.md; A | confirmed; K=1,3,4 exact controls |
| C1/E7-diagram | Declared AG0–AG8 instance: 8,192 worlds and 169 paired commands/date; five isolated operational failures and coupled funding/factual failures | computed exact | python3 covenant_lab/gates.py | confirmed on full declared instance, not a universal independence claim |
| D19-shared | Combined24-state/15-interest candidate;360 Bellman coordinates,216 buyer,3,456 financier and31,104 worker comparisons | computed exact | python3 covenant_lab/integrated_game.py | confirmed unilateral inequalities; model/security premises declared |
| D19-MPE | Turn-based phase bridge and all-state unilateral equilibrium for that candidate | proved (written) | python3 covenant_lab/integrated_game.py; math/D19.md | confirmed on declared game; no local Lean instantiation |
| D19-victim-fine | Controller/client safe-event binding plan; strict ex ante gains1/4,3/2 | refuted | python3 covenant_lab/integrated_game.py | binding resistance fails; does not imply coalition-proofness fails |
| D19-external-fine |51,840 joint-control plans; maximal binding coalition aggregate1/2 from audit saving | refuted | python3 covenant_lab/integrated_coalitions.py | proposed repair fails; simple financier/controller gains1/4 each |
| D19-offpath-phase | No-audit history; negotiated proper processing gains45/2,1/2 | refuted | python3 covenant_lab/integrated_coalitions.py | phase-wise binding resistance fails separately |
| D19-priority-boundary | Protected priority audit/external fines;51,840 joint plans; maximum aggregate0 on24 boundary states | computed exact | python3 covenant_lab/integrated_priority.py | confirmed boundary scope; stronger physical/title premise declared |
| D19-priority-phases | No-grant copy renegotiation gains23,1/2; mistaken grade0 purchase admits profitable cancellation | refuted | python3 covenant_lab/integrated_priority.py | every-public-phase resistance fails despite passing boundary result |
| D20-integrated | Optional procurement/audit/grant finance under endowed capital/title and declared30/100 preferences | computed exact | python3 covenant_lab/integrated_game.py | financier incentives pass; no endogenous capital acquisition claim |
| D22-renewal |96 actual bounded resource quotes, minimum surplus377/4 after all protected costs | computed exact | python3 covenant_lab/integrated_game.py | confirmed on yield150/152 and at most3 patients |
| D22-induction | Reserve16 restored before residual consumption; exit/refusal/fork/outage histories on declared support | proved (written) | math/D22.md; python3 covenant_lab/integrated_game.py | conditional on realized producer/protected title; coalition tests still fail |
| D15-atomic-cap | New atomic service,9 profiles,729 heterogeneous families/6,561 profiles; CC value627/100 | computed exact | python3 covenant_lab/atomic_service.py | confirmed; realized execution outcomes independently summed |
| D15-atomic-coalitions | Every bounded history-dependent binding/internal-stable coalition improvement excluded by componentwise caps and balanced transfers | proved (written) | math/D15.md; python3 covenant_lab/atomic_service.py | scoped to new risk-neutral atomic mechanism with fixed protected baseline; original game unchanged |
| D15-selection | All-exit also strict stage/stationary equilibrium; non-atomic and excessive-preparation deviations | computed exact | python3 covenant_lab/atomic_service.py | selection obstruction and substantive-hypothesis controls confirmed |
| D19-contract-phases | Actual conditional escrows,24 boundary states/15 interests;310,272 coalition/subject phase comparisons | computed exact | python3 covenant_lab/contract_game.py | confirmed every stated public-phase scope; physical/normative primitives purchased |
| D19-contract-return | Finite phased one-shot coalition bounds imply no bounded randomized/history-dependent Pareto improvement | proved (written) | math/D19_CONTRACT_GAME.md | actual public-prefix bridge and date-discount tail given; not kernel-instantiated |
| D19-contract-maintenance | Coupled finance/input/control/subject/copy/exit game, selection and bounded resource renewal | scoped | math/D19_CONTRACT_GAME.md; python3 covenant_lab/contract_game.py | positive conditional witness; no physical realization/recognition/private-information promotion |
| D20-contract-startup | Private cash32 funds quoted core8+locked reserve16; net financer gain190931/502 | computed exact | python3 covenant_lab/contract_game.py | startup/IR arithmetic confirmed; supplier/core law and quote remain premises |
| D19-contract-type | Resistance value6, good standing2, same future law; actual refusal gains1 | refuted | python3 covenant_lab/contract_game.py | generic acceptance/standing inference fails outside declared preference/compensation hypotheses |
| D15/D19-coalition-algebra | Forced-member maximum attained; balanced transfers preserve sum; no Pareto improvement; symbolic atomic stage cap | kernel-checked | bash lean/build.sh | 7 new generic declarations, standard axioms only; numeric game instantiation separate |
| D8-donation-games | Five original transitions independently rebuilt/closed under both intents;810 donor comparisons,9 own-information private policy returns | computed exact | python3 covenant_lab/assessment_games.py | new payoff extension declared first; hidden-state diagnostics not private equilibrium verdicts |
| D8-public-equilibria | Public contract/donor-perspective and sensor thresholds; positive minimum slacks10377/32390 and39370816377/129757678790 at3/4 | proved (written) | math/D8.md; python3 covenant_lab/assessment_games.py | affine values and all-state return; two quadratic root isolations exact |
| D8-common-facts-Nash | Three public D events and one subsequent C deviation give initial gain7688407/27981987840000 | refuted | python3 covenant_lab/assessment_games.py | actual common-history-accessible strategy; not a hidden-state hypothetical |
| D8-private-Nash | Cooperate when both own private assessments bad; exact initial gain strictly between1/2500 and1/2000 | refuted | python3 covenant_lab/assessment_games.py | table uses own row/current pair only; changed profile not claimed equilibrium |
| D8-kernel-algebra | Affine Bellman, positive determinant/denominator, gap identity/sign, polynomial monotonicity and rational endpoints | kernel-checked | bash lean/build.sh | 7 new project lemmas; actual game instantiation written/exact |
| C15-source-guards |27 exact statement/named-theorem snapshots and17 applicability rows, original grades retained | scoped | python3 math/c15_sources.py | source-statement review complete; no corpus builds/promotions or deployment passes |
| C15-factual-code | Two worlds/three distinct calibrated groups, distance3, all8 within-one-fault reports decode | computed exact | python3 math/c15_sources.py | pass on declared factual lab target; calibration/control-group premises visible |
| C15-public-grade | Three different next-grade laws; public current grade factors non-constantly through predictive class | refuted | python3 math/c15_sources.py | C4 hiddenness fails on specified projection; no subjecthood interpretation |
| C2-role-classification | Inhabited determining product: fiber-constant transcript iff it factors through action; accountability of two actions forbids global constant transcript | kernel-checked | bash lean/build.sh | explicit predictive/product/source-package bridge; no revised phenomenality conclusion |
| C2-dynamics | Four-world two-step future injective, private connector preserves action/changes prediction; all16 binary channels | computed exact | python3 covenant_lab/role_privacy.py | hidden coordinate causally predictive, not decorative; core injectivity also kernel-checked |
| C2-secrecy | C4′ holds yet full-support prior yields guess3/4, future reveals h; singleton fibers vacuous | refuted | python3 covenant_lab/role_privacy.py | conditional structural predicate does not imply statistical/future secrecy |
| D16-cartel-capacity |1458 weighted families,27216 withholding cases; total minus b largest control weights | computed exact | python3 covenant_lab/control_groups.py | compatible additive units and willingness separate |
| D16-paid-coalition | Redundant fifth input omitted; payer/provider transfer gives gains3/4,1/4 | refuted | python3 covenant_lab/control_groups.py | operator-only margins do not provide every-party binding stability |
| D16-care-replacement | Independently controlled realized backup3 and senior escrow6 preserve floors in54 coalition cases | scoped | python3 covenant_lab/control_groups.py | physical backup/control/renewal/ethical scope purchased; captured backup and fourth-interest controls fail |
| D16-origin-controls | Five same-unit/root/bearer aliases retain one unit and grade0/debt1; real fork legacy totals conserved while care demand grows | computed exact | python3 covenant_lab/control_groups.py | control roots distinct from bearer/patient recognition; self-attested roots insufficient |
| D16/D22-capacity-algebra | Same-root/alias capacity invariance, surviving-capacity identity/nonnegativity and divisible-floor feasibility | kernel-checked | bash lean/build.sh | five new generic lemmas, actual physical binding/delivery separate |
| D23-calibrated-filter |254 response words matched to independent hidden-path sums;144 grade paths leave type prior1/2 despite mean19/21 | computed exact | python3 covenant_lab/type_evidence.py | declared preference/transition/channel target; no patienthood or intent inference |
| D23-context-controls | Counts-only, static rho0, unknown label orientation and control/terms-blind interpretation fail | refuted | python3 covenant_lab/type_evidence.py | forecasts distinguish actual response from noisy record and autonomous provenance |
| D23-exact-retention | Exact posterior inverts entire response word; future probability target needs unbounded state/at least n bits for length n | proved (written) | math/D23.md; python3 covenant_lab/type_evidence.py | scoped disjoint-range model; latent count2 not native finite-index certificate |
| D23-MAP-retention | Last response bit retains exact current/next MAP decision, errors1/20 and13/80 | proved (written) | math/D23.md; python3 covenant_lab/type_evidence.py | exact decision is a different target from calibrated probability |
| D23-finite-repair | Odds grid257 indices/514 transitions merges raw words; all-word probability/forecast errors41/841,123/3364 | proved (written) | math/D23.md; python3 covenant_lab/type_evidence.py | tolerance/context authorized;8190 exact word checks support instances, not substituted for proof |
| D23-kernel-algebra | Bayesian no-update/mean/separation, type prediction/aging, exact-summary injectivity and odds-cross probability bound | kernel-checked | bash lean/build.sh | ten generic lemmas; log-odds/model/authority bridges remain written/hypotheses |
| D14-finite-population |495 families,768 micro matching checks; absorption/harmonic and waiting-time equations exact | computed exact | python3 covenant_lab/adoption_population.py | actual finite-person counterfactual entry/exit matching, declared myopic law |
| D14-potential | Strict-switch finite potential, at most N switches and expected absorption≤N²; critical/hysteresis classification | proved (written) | math/D14.md; python3 covenant_lab/adoption_population.py | no run-only impossibility or forward-looking equilibrium inferred |
| D14-withdrawal | N6 k3 survival1/2/time10, subsidy k2 survival2/3/time31/3, temporary success(2/3)(1−2^−T) | computed exact | python3 covenant_lab/adoption_population.py | funding32 covers committed3T up to T8; preference to fund not assumed proved |
| D14-controls | High-entry partial absorber4; founder license loss collapse/time147/10; positive noise destroys permanent adoption | refuted | python3 covenant_lab/adoption_population.py | subsidy/control, stationary occupancy/permanence and one-point tipping kept distinct |
| D14-kernel-algebra | Margin gap, entry/exit potential identities/increase, critical entry bound, harmonic flux and detailed-balance stationarity | kernel-checked | bash lean/build.sh | eight new generic lemmas, actual update/absorption/control model bridge separate |
| E2/D13-full-phases | Ten-interest ownership/work/report/controller/host/copy/private-contract game;554816 exact phase comparisons | computed exact | python3 covenant_lab/corridor_game.py | d/control/physical guards registered first, care/exit fixed; no omitted strategic roles |
| E2/D13-individual-region | Full minimum min(0,2d−Kd(1−d)); K0[0,1], K8{0}∪[3/4,1] | proved (written) | math/E2_FULL_GAME.md; python3 covenant_lab/corridor_game.py | zero threshold/disconnected region; all-real-d proof independent of samples |
| E2/D13-binding-region | Candidate any-subset binding region empty; d>0 financier/provider gainsd/8, at0 financier/buyer gains1/4 | refuted | python3 covenant_lab/corridor_game.py | actual balanced transfers/costs/outsider losses, care untouched; not universal impossibility or coalition-proof refutation |
| E2/D13-full-kernel | Owned/external total, outside gap/region, provider positivity and parameterized strict-transfer algebra | kernel-checked | bash lean/build.sh | six generic ordered-field statements; actual phase game instantiation written/exact |
| C1/E7-arrows | Matched protected-capacity scopes give AG2⇔AG8; owed robust factual warrant plus fixed provenance gives AG7⇒AG6, with reverse failure | proved (written) | C1.md | confirmed with exact scopes; AG0 is the declaration prerequisite |
| Historical verification | Hash-matching archived r2 inputs authenticate edit replay; current ratified drafts have different hashes | computed exact | A; R | corrected verifier, numerical outcomes unchanged |

[B] All 22 inherited source receipts match their current sibling files, and all
listed labels exist. That is a provenance check, **not** a blanket re-audit of
their theorem statements. V14 `thm:corruption` was read directly for D5; its
target-distance/calibration scope is retained. No corpus grade is promoted.

[Q] D8 equilibrium, endogenous audit incentives, D15 self-enforcing coalitions,
D19 integration/renewal, D22 stress/fission, and D23 evidential semantics remain
separate obligations. This register lands D21's consolidation; it does not close
D17's distinct-person review gate or certify practical implementation.
