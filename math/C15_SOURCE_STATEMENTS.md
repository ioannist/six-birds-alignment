# C15 — exact source statement snapshot

[B] Statements below are frozen source text, with exact anchors and the ratified index grade where available. New reviewed guards are bridges; no source grade is promoted and no named deployment is certified.

## V6 thm:PGT6

[F] Source [thm:PGT6](/home/repos/six-birds-papers/Tsiokos_2026_Six_Birds_Verified_VI_The_Price_of_an_Interface.tex:1826); kind: corollary. Grade recorded in index: guarded-path/simulation theorem; scalar-policy corollary; price-record separation proposition; scoped formal specializations and written general proofs per `sec:lean`.

[B] Reviewed applicability guard: Use its scalar-policy clause on a finite nonempty feasible candidate family with a strict scalar policy (all coordinate weights positive). Zero weights lose strictness; positive linear weighting need not attain every efficient point. Exact transport needs bijections/order reflection; costed transport is forward only.

```tex
\begin{corollary}[Exact and costed transport, scalar policies and native orders]\label{thm:PGT6}
With the transports and policies of \cref{def:transport}:
\begin{enumerate}
\item \emph{Exact transport.} Under an exact transport, $a$ is efficient in $\mathcal S$
  iff $f(a)$ is efficient in $\mathcal T$, a bijection of fronts that respects
  identities, and $\beta\in\Budgets_{\mathcal S}$ iff $\psi(\beta)\in\Budgets_{\mathcal T}$. A
  constant cost map is isotone but does not reflect the order: $(0,0)$ and
  $(1,1)$ collapse to one value with two efficient identities. A target catalog
  with an extra cheaper candidate breaks the correspondence.
\item \emph{Compiler.} A costed map transports $\beta$ to $\beta\combine o_f$, forward only,
  and successive maps add their overheads. The compiler from \PaperF{}'s
  Boolean decision trees to tables has the uniform overhead of
  \cref{tab:and}. For the five-node run of AND it has the sharper overhead of
  that table, between the two AND profiles, where the charge of four units for
  verification is a declared policy. A second tagged compiler adds one unit of
  description and one of storage, and composition adds both overheads.
\item \emph{Scalar policies.} Every minimum of a strict scalar policy over a
  feasible candidate is efficient, and a finite family with a feasible
  candidate has a scalar minimum, the set of minimizers keeping all ties.
  Positive weighted sums are strict, and zero weights are not. For $p=(0,3)$,
  $p'=(2,2)$ and $p''=(3,0)$, selecting $p'$ by weights $(w_1,w_2)$ needs
  $2w_1\le w_2$ and $2w_2\le w_1$, which is impossible for positive weights. So
  positive linear scalarization does not reach every efficient point.
\item \emph{Native orders.} $\mathrm{diag}(v)\preceq_{\mathrm{PSD}}\mathrm{diag}(v')$ iff $v_i\le v'_i$ for
  all $i$, by basis vectors and nonnegative sums. The diagonals $\mathrm{diag}(1,0)$ and
  $\mathrm{diag}(0,1)$ are positive, have trace one and are incomparable, so the
  trace is a lossy scalar readout.
\end{enumerate}
\end{corollary}
```

## V15 ex:mixture

[F] Source [ex:mixture](/home/repos/six-birds-papers/Tsiokos_2026_Six_Birds_Verified_XV_Portable_Theories.tex:909); kind: example. Grade recorded in index: mechanized finite-index audit theorem; mechanized native-chain theorem; kernel-checked finite mixture example.

[B] Reviewed applicability guard: This is the stated binary depth-two learner, b=0, sampler, eighteen-sign cycle and alternating unlabelled source drive. Its non-attribution/unfaithful shadow is a scoped witness, not a theorem about every preference mixture or RLHF method.

```tex
\begin{example}[An unlabelled mixture]\label{ex:mixture}
On the binary depth-two learner with $b=0$, in either refinement variant, drive two constant sources, $0$ and $1$, with every raw sign of the cycle of blocks $\#c$ over the seven contexts in the order $\varepsilon,0,1,00,01,10,11$, followed by $\#$, eighteen signs in all, and deliver their outputs alternately, starting with the first source. The transcripts from this origin pair agree forever with those from the pair of a source that outputs $1$ only at $00$ and a source that outputs $0$ only at $01$, so the origins cannot be attributed. The learner's state at the end of each cycle repeats, but the next contact changes it: while contact continues it is not stable. If contact is withdrawn at the end of a cycle and one Tick runs, the runtime from a fresh session answers every word with the shadow that outputs $1$ exactly at the contexts $\varepsilon,0,1,00,10$ and $0$ at $01,11$, which is faithful to neither origin. The indistinguishability holds for this sampler and drive.
\end{example}
```

## V1 thm:R6

[F] Source [thm:R6](/home/repos/six-birds-papers/Tsiokos_2026_Six_Birds_Verified_I_Layer_Receipts_and_Purchase_Laundering.tex:1356); kind: proposition. Grade recorded in index: theorem / proposition / theorem / tower theorem / finite cube; reported Lean scope, external 512-profile count.

[B] Reviewed applicability guard: A purchase-compilation record already includes the gate/source/price/bridge/audit/history and residual data. It preserves historical purchase/external origin when becoming a current primitive; it does not prove that a training artifact implements the declared principle.

```tex
\begin{proposition}[Purchase compilation and capitalization]\label{thm:R6}
Every purchase compilation record satisfies: (1) $x$ is free in $\Pkg_2$;
(2) $x$ is internally derivable with zero package extension; (3)
$\NoExt_{\Pkg_2}(x)$; (4) the original accepted purchase occurs in
$\Hist_2$; (5) the compiled event occurs in $\Hist_2$; (6) the original
source, payment price, bridge and audit remain in the compiled event; (7)
every old residual and nonclaim remains; (8) every declared in-class use
succeeds; (9) every witnessed out-of-class failure contributes an explicit
residual and nonclaim. If the original payment mode is paid,
\[
\NoExt_{\Pkg_2}(x)\quad\land\quad\HistP_{\Hist_2}(x)\neq0 .
\]
If the original source was external, the compiled event keeps that external
source entry: becoming a current primitive does not rewrite an external
purchase as native generation.
\end{proposition}
```

## V1 thm:R7

[F] Source [thm:R7](/home/repos/six-birds-papers/Tsiokos_2026_Six_Birds_Verified_I_Layer_Receipts_and_Purchase_Laundering.tex:1526); kind: theorem. Grade recorded in index: theorem / proposition / theorem / tower theorem / finite cube; reported Lean scope, external 512-profile count.

[B] Reviewed applicability guard: Verified purchase receipt occurs in append-only history and a source-preserving presentation equivalence transports protected coordinates/identifiers. Renaming/deleting or changing price/disposition is not such an equivalence.

```tex
\begin{theorem}[No purchase laundering]\label{thm:R7}
Let $\Pkg_0\ext\Pkg_1$ carry a verified purchase receipt $r$ for $x$, let
$\Hist$ be an append-only history in which $r$ occurs, and let $F$ be a
source-preserving presentation equivalence. Then
\begin{enumerate}
\item $\Free_{\Pkg_i}(y)\iff\Free_{\Pkg'_i}(Fy)$ for $i\in\{0,1\}$;
\item the verified purchase, its gate, its enriched receipt and the whole
      history transport lawfully: $r\in\Hist\Rightarrow F_*r\in F_*\Hist$,
      $|F_*\Hist|=|\Hist|$, and the transport preserves, up to the declared
      identifier bijections, the purchase kind, the disposition and every
      protected coordinate of \cref{conv:protected}. The coordinate-by-coordinate
      list is in \cref{supp:fields}.
\end{enumerate}
Hence a lawful presentation transport cannot convert a historically purchased
item into a historically unpurchased one. A receipt with a different price or
disposition is a different receipt, even over the same packages; its appearance in the
history requires its own event, and cannot be produced by renaming or deletion.
\end{theorem}
```

## V10 thm:ECT2

[F] Source [thm:ECT2](/home/repos/six-birds-papers/Tsiokos_2026_Six_Birds_Verified_X_Wholes_That_Grow_Each_Other.tex:757); kind: theorem. Grade recorded in index: proved gluing/conditional replacement and finite construction theorems; stated Lean specializations, compiled finite checks, and written-only steps per `sec:lean`.

[B] Reviewed applicability guard: Finite coordinate cover and domain-valued compatible sections. Gluing yields a unique assignment; independently required admission P needs P(glue(a)), not compatibility alone.

```tex
\begin{theorem}[Finite gluing on a cover]\label{thm:ECT2}
For covers and sections as in \cref{def:cover}:
\begin{enumerate}
\item Every family of restrictions $\res(x)$ is compatible. For a compatible family $a$,
  $\res(\glue(a))=a$ and $\glue(\res(x))=x$, and $\glue(a)$ is the only global assignment restricting to $a$;
  its values lie in the declared domains.
\item For compatible maps $f_i:Y\to\mathrm{sections}(J_i)$, the map $f(y)=\glue((f_i(y))_i)$ satisfies
  $\res_i\circ f=f_i$ for every $i$, and it is the only such map.
\item For an independently given predicate $P$ on global assignments, a compatible family has a filler
  satisfying $P$ (a global $x$ with $P(x)$ and $\res(x)=a$) exactly when $P(\glue(a))$ holds, and that filler is
  then unique.
\end{enumerate}
\end{theorem}
```

## V12 thm:obstruction

[F] Source [thm:obstruction](/home/repos/six-birds-papers/Tsiokos_2026_Six_Birds_Verified_XII_The_Geometry_of_Access.tex:628); kind: theorem. Grade recorded in index: proved linear/cohomological theorem over ℚ; finite rational pairwise-solvable/global-obstruction example; reported Lean.

[B] Reviewed applicability guard: Declared rational linear restriction/cochain system. A closed datum is solvable iff its Cech class vanishes. Forest surjectivity requires both overlap restrictions onto each edge to be surjective; graph shape alone is insufficient.

```tex
\begin{theorem}[Obstruction and forests]\label{thm:obstruction}
\begin{enumerate}
\item $\delta^1\circ\delta^0=0$, and a datum $c$ with $\delta^1c=0$ is solvable if and only if its class in $\check H^1$ vanishes.
\item If a subfamily of declared pairs forms a forest, and both restrictions onto each of its
  overlaps are surjective, then for every datum $c$ some $a\in C^0$ satisfies $\delta^0(a)_{ij}=c_{ij}$ for every pair $(i,j)$ of the
  subfamily; if, moreover, the subfamily is the whole overlap graph, $\delta^0$ is surjective.
\item The surjectivity hypothesis cannot be dropped: with $\mathcal Q(U_i)=\mathcal Q(U_j)=0$ and $\mathcal Q(U_{ij})=\mathbb Q$ on one
  overlap, $\delta^0=0$ and the datum $1$ is not solvable.
\end{enumerate}
\end{theorem}
```

## V4 thm:TDR5

[F] Source [thm:TDR5](/home/repos/six-birds-papers/Tsiokos_2026_Six_Birds_Verified_IV_Tolerance_and_Surrogates.tex:1304); kind: corollary. Grade recorded in index: proved center-descent theorem, bounds under their respective hypotheses, center-repair corollary, sharp retention/lumpability theorem; formal coverage as stated in `sec:lean`.

[B] Reviewed applicability guard: Declared tolerance, admissible independent factors and reached center catalogues. Empty reached catalogue defeats every repair; finite feasibility gives minimal repairs, not generally a least one. Inclusion, price, edge count and radius are separate orders.

```tex
\begin{corollary}[The complete family of center repairs]\label{thm:TDR5}
Let $\rho$ be a tolerance on $R$, and consider all admissible independent
factors, not only those of minimum radius.
\begin{enumerate}
\item[A.]\emph{Least support of a fixed factor.} $\Gsupp{\phi}$ is a
      tolerance containing $\rho$ under which $\phi$ is an approximate
      factor, and $\Gsupp{\phi}\subseteq t$ iff $\rho\subseteq t$ and
      $t(\phi(\qhat(x)),\hmap(x))$ for all $x$.
\item[B.]\emph{Cofinality.} A tolerance $t\supseteq\rho$ is a center repair
      iff $\Gsupp{\phi}\subseteq t$ for some admissible $\phi$. If a reached
      catalog is empty, no center repair exists, not even the total
      relation; on the empty source $\rho$ itself is the least center repair.
\item[C.]\emph{Complete minimal family.} A tolerance is inclusion-minimal
      among all center repairs iff it is an inclusion-minimal member of the
      centered-repair family. The family is computed by a finite
      construction, and a feasible problem has at least one minimal center
      repair.
\item[D.]\emph{Least-element criterion.} A least center repair exists iff the
      support core $\Core$ is itself a center repair, and it is then $\Core$;
      equivalently, there is exactly one minimal center repair. On three
      points this fails (\cref{cm:tdrc17}).
\item[E.]\emph{Comparison with the equivalence repair.}
      $\EqPair\subseteq\EqCl(\Gsupp{\phi})$ for every admissible $\phi$,
      although $\PairRepair\subseteq\Gsupp{\phi}$ can fail. Equality
      $\EqPair=\EqCl(\Gsupp{\phi})$ holds iff every selected edge already lies
      in $\EqPair$, $\forall x,\ \EqPair(\phi(\qhat(x)),\hmap(x))$; selecting
      outputs as centers is sufficient and not necessary (\cref{cm:tdrc18}).
\end{enumerate}
Inclusion, edge count, radius and price are different orders on the center
repairs, and they can pick different ones (\cref{cm:tdrc17}).
\end{corollary}
```

## V5 thm:ERVERIFIER

[F] Source [thm:ERVERIFIER](/home/repos/six-birds-papers/Tsiokos_2026_Six_Birds_Verified_V_The_Cost_of_Access.tex:1912); kind: corollary. Grade recorded in index: Lean / oracle-relative corollary.

[B] Reviewed applicability guard: Fixed verifier V/base oracle A and sound generator. Its outputs are contained in L_V; equality needs completeness. Oracle-relative non-finality concerns both signs of K_A and effectiveness/soundness/completeness, not universal failure of finite oversight.

```tex
\begin{corollary}[The fixed-verifier ceiling and a scoped non-final auditor]\label{thm:ERVERIFIER}
For a fixed verifier $V$ and a base oracle $A$:
\begin{enumerate}
\item[A.]\emph{Ceiling.} Every sound external generator that feeds a fixed
      verifier $V$ outputs only members of $L_V$. Faster discovery of witnesses
      does not change the fixed set of truths, and equality of the generator's
      range with $L_V$ needs a separate completeness hypothesis.
\item[B.]\emph{Non-finality.} No total verifier that is effective in $A$ is sound
      and complete for finite certificates of both signs of $K_A$, with the claim
      maps $\gamma_+(n)=\operatorname{pair}(n,1)$ and $\gamma_-(n)=\operatorname{pair}(n,0)$:
      such a verifier would give an $A$-decider of $K_A$, contradicting
      \cref{thm:ERJUMP}, part~C. The same argument at $J(A)$ excludes a
      $J(A)$-effective verifier for both signs of $K_{J(A)}$, while a
      $J(A)$-verifier does settle both signs of $K_A$.
\end{enumerate}
\end{corollary}
```

## V14 thm:corruption

[F] Source [thm:corruption](/home/repos/six-birds-papers/Tsiokos_2026_Six_Birds_Verified_XIV_Objectivity_Without_Finality.tex:508); kind: theorem. Grade recorded in index: Lean.

[B] Reviewed applicability guard: Worlds/target/calibrated grouped transcript code with target distance d_T. Unknown corruptions need d_T>=2b+1; known erasures need b+1; mixed known erasures e and unknown corruptions s need e+2s+1. Aliases are not independent groups.

```tex
\begin{theorem}[Erasure and corruption thresholds]\label{thm:corruption}
Let $b\ge0$.
\begin{enumerate}
\item Every report obtained from a codeword by corrupting at most $b$ group transcripts determines the target, that is, a corruption
  decoder exists, if and only if $d_T\ge2b+1$.
\item A decoder for known erasures of at most $b$ groups exists if and only if $d_T\ge b+1$, the condition of \cref{thm:erasure}(2).
\item The two thresholds differ: if $b+1\le d_T<2b+1$, then erasures of $b$ groups can be decoded and corruptions of $b$ groups cannot.
\item \emph{Mixed faults.} For $e,s\ge0$, a decoder exists for reports with a known set of at most $e$ erased groups and an unknown set of
  at most $s$ further corrupted groups if and only if $d_T\ge e+2s+1$. Parts (1) and (2) are the cases $e=0$ and $s=0$.
\end{enumerate}
\end{theorem}
```

## F4 thm:F28

[F] Source [thm:F28](/home/repos/six-birds-papers/Tsiokos_2026_Six_Birds_Foundations_IV_A_Catalog_of_Layer_Agnostic_Structural_Laws.tex:5591); kind: theorem. Grade recorded in index: proved structural laws.

[B] Reviewed applicability guard: Declare surjective part/interface quotient kappa, raw composition, outcome, residual and admission. All three must be constant on kappa fibers independently. Associativity and identity are separate coherence checks.

```tex
\begin{theorem}[Composability]\label{thm:F28}
Let \(X_A,X_B\) be component spaces with quotients
\(q_A:X_A\to Q_A\), \(q_B:X_B\to Q_B\), interface readouts
\(\beta_A:X_A\to I_A\), \(\beta_B:X_B\to I_B\), composition
\(U:X_A\times X_B\to X_{AB}\), composite quotient
\(q_{AB}:X_{AB}\to Q_{AB}\), admissibility predicate
\(\operatorname{Adm}:X_A\times X_B\to\mathrm{Prop}\), and residual
\(\delta:X_A\times X_B\to D\).  Write
\[
  \kappa(a,b):=\bigl((q_A(a),\beta_A(a)),(q_B(b),\beta_B(b))\bigr)
\]
for the part/interface quotient and assume \(\kappa\) is surjective.
For a map \(f\) on \(X_A\times X_B\), let
\[
  \mathcal O(f)
  :=
  \{((a,b),(a',b')) :
     \kappa(a,b)=\kappa(a',b'),\ f(a,b)\ne f(a',b')\},
\]
and set \(\mathcal O_U:=\mathcal O(q_{AB}\circ U)\),
\(\mathcal O_{\delta}:=\mathcal O(\delta)\) and
\(\mathcal O_{\operatorname{Adm}}:=\mathcal O(\operatorname{Adm})\).
Write \(\operatorname{COD}\), \(\operatorname{CRD}\) and
\(\operatorname{AD}\) for descent through \(\kappa\) of the composite
outcome, the cross residual and admissibility, and
\(\operatorname{Composable}\) for exact composability.  Then
\begin{align*}
  \operatorname{COD}
  &\iff
  \mathcal O_U=\emptyset
  \iff
    \exists!\,\bar U:(Q_A\times I_A)\times(Q_B\times I_B)\to Q_{AB}\\
  &\hspace{6em}\text{with}\ \bar U(\kappa(a,b))=q_{AB}(U(a,b)),\\
  \operatorname{CRD}
  &\iff
  \mathcal O_{\delta}=\emptyset,
  \qquad
  \operatorname{AD}
  \iff
  \mathcal O_{\operatorname{Adm}}=\emptyset,\\
  \operatorname{Composable}
  &\iff
  \mathcal O_{\operatorname{Adm}}=\emptyset
  \wedge\mathcal O_U=\emptyset
  \wedge\mathcal O_{\delta}=\emptyset.
\end{align*}
The maps through which the cross residual and admissibility descend are likewise unique.
Associativity and identity are separate coherence conditions: for the
two bracketings \(\ell,\varrho:Y\to Y'\) of a declared quotient-level triple
composite, define \(\operatorname{Assoc}:\Longleftrightarrow\ell=\varrho\), and
for a declared composite \(c:Z\times E\to Z\) and a declared \(e\in E\) define
\(\operatorname{Id}:\Longleftrightarrow\forall z\in Z,\ c(z,e)=z\); then
\(\operatorname{Assoc}\iff\{y:\ell(y)\ne\varrho(y)\}=\emptyset\) and
\(\operatorname{Id}\iff\{z\in Z:c(z,e)\ne z\}=\emptyset\). If moreover \(\ell\circ\kappa_3=q'\circ L\) and \(\varrho\circ\kappa_3=q'\circ P\) for raw bracketings \(L,P:X_3\to X'\), a surjection \(\kappa_3:X_3\to Y\) and a map \(q':X'\to Y'\), then \(\operatorname{Assoc}\iff q'\circ L=q'\circ P\); in particular raw associativity \(L=P\) gives \(\operatorname{Assoc}\). Likewise, if \(c(\kappa_Z x,e)=\kappa_Z(\tilde c(x))\) for a surjection \(\kappa_Z\) and a map \(\tilde c\), then \(\operatorname{Id}\iff\kappa_Z\circ\tilde c=\kappa_Z\).
\end{theorem}
```

## V10 thm:MOT2

[F] Source [thm:MOT2](/home/repos/six-birds-papers/Tsiokos_2026_Six_Birds_Verified_X_Wholes_That_Grow_Each_Other.tex:1140); kind: theorem. Grade recorded in index: proved gluing/conditional replacement and finite construction theorems; stated Lean specializations, compiled finite checks, and written-only steps per `sec:lean`.

[B] Reviewed applicability guard: Replacement acceptance, new realization, backward behavior and guarantee transport are all required. Operational version matches every positive new branch/protected output/fault/work, related initials and a per-step overhead; word overhead is n*gamma.

```tex
\begin{theorem}[Contract-preserving replacement]\label{thm:MOT2}
Let an old contract be realized as in \cref{def:square}, and let a replacement contract with assumption
$\mathrm{Asm}_1$, target $\mathrm{Gar}_1$ and behavior $\mathrm{Beh}_1$, an input adapter $u$ and a relation
$\mathrm{Rel}$ between old and new results be given.
\begin{enumerate}
\item Suppose that $\mathrm{Asm}_0(x)$ implies $\mathrm{Asm}_1(u(x))$ (acceptance); every assumed new input has a
  behavior (new realization); every $\mathrm{Beh}_1(u(x),y_1)$ at an old assumed $x$ has some $y_0$ with
  $\mathrm{Beh}_0(x,y_0)$ and $\mathrm{Rel}(y_0,y_1)$ (backward behavior); and
  $\mathrm{Gar}_0(x,y_0)\wedge\mathrm{Rel}(y_0,y_1)$ implies $\mathrm{Gar}_1(y_1)$. Then on every old promised input
  the replacement has a result, and every replacement result satisfies $\mathrm{Gar}_1$. Replacements compose,
  the composed relation keeping the middle witness.
\item Let two finite operational machines be related by a state relation and an action adapter. Suppose that at
  every related pair and old promised action the adapted new action is available with a nonempty row; that every
  positive new branch has an old branch with related states and matching protected outputs, faults and work; and
  that every initial new state is related to an initial old state. Then every actual new run from a related
  start is matched step by step by an old run. If each matched step costs at most the old step plus $\gamma$, a
  word of $n$ steps costs at most the old cost plus $n\gamma$.
\end{enumerate}
\end{theorem}
```

## V8 thm:EOT2

[F] Source [thm:EOT2](/home/repos/six-birds-papers/Tsiokos_2026_Six_Birds_Verified_VIII_Flattening_and_Enablement.tex:1468); kind: theorem. Grade recorded in index: finite laboratory theorem.

[B] Reviewed applicability guard: Finite enablement laboratory and its ready-session/reusable calibrated/one-shot policies. A priced rollback returns a summary, not an identical full timed session or zero-budget/path-length information.

```tex
\begin{theorem}[The enablement preorder and the communication quotient]\label{thm:EOT2}
For the reachability of \cref{def:enablement} on the laboratory:
\begin{enumerate}
\item \emph{Paths.} $\Reach(s,t)$ holds exactly when there is a finite
  successful path from $s$ to $t$, and $\Reach$ is the least reflexive and
  transitive relation containing the edges.
\item \emph{Chronology.} For a successful full path $p$ from $s$ to $t$ the
  tick of $t$ is the tick of $s$ plus $|p|$. Hence full sessions reachable
  from each other are equal, and every closed full path is empty; this is a
  property of the clock, not irreversibility.
\item \emph{Quotient.} $\sim$ is an equivalence, $\preceq$ does not depend on
  representatives, and it is a partial order on classes. When every source
  is released at time zero, reachability of summaries is actual
  reachability of continuations from any matching ready session.
\item \emph{Priced cycle.} In the reusable calibrated context, installing
  sensor~1, deciding and rolling back returns to the original summary
  through the goal at charge $(3,1,19,1)$, so reachability of summaries is
  not antisymmetric and base and goal lie in one class. Under the one-shot
  policy no path returns to the unused base, because consumed flags are
  never cleared; without rollback authority the reachable summaries form an
  acyclic graph with five vertices and six edges.
\item \emph{No descent.} In the reusable calibrated context, let $b$ be the
  base and $g$ the goal reached by clause~4. No predicate on classes agrees
  at every representative with ``the goal target is affordable at zero
  budget'', since $[b]=[g]$, the empty path affords the target at $g$, and
  every nonempty path has positive work. No function of the class recovers
  the length of the history, since the empty run and the cycle end in the
  same class with histories of lengths $0$ and $3$.
\end{enumerate}
\end{theorem}
```

## V10 thm:MOT5

[F] Source [thm:MOT5](/home/repos/six-birds-papers/Tsiokos_2026_Six_Birds_Verified_X_Wholes_That_Grow_Each_Other.tex:1404); kind: theorem. Grade recorded in index: proved gluing/conditional replacement and finite construction theorems; stated Lean specializations, compiled finite checks, and written-only steps per `sec:lean`.

[B] Reviewed applicability guard: Typed co-growth books require every key and equal values on overlaps; absent field is missing evidence. Work/residual sums require linked compatible continuations. Paid rollback restores native/observer/active-code projection, not histories, balances or acquired code.

```tex
\begin{theorem}[Co-growth books and the paid return route]\label{thm:MOT5}
For subjects and books as in \cref{def:cogrowth}:
\begin{enumerate}
\item If every required key occurs in the submitted cells and entries with the same key are equal, the
  constructed record restricts to every book and is the only such record; entries with equal keys and unequal
  values admit no common record; and an absent field is missing evidence, not nonexistence.
\item Along a linked history $s_0\to\dots\to s_n$, $\Wk(s_n)=\Wk(s_0)+\sum_e\Delta\Wk(e)$ and
  $\Res(s_0)=\Res(s_n)+\sum_e\Delta\Res(e)$. A compatible continuation (initial state the prefix's returned state,
  prior history the prefix's prior followed by its events) appends with vector addition of accounts.
\item The return route from a quiescent start (pause for rollback, validate the old backup, install the old A
  code, install the old B code, resume the old pair) restores the projection to the native and observer state and
  the active A and B codes, but not the full state: the acquired code, the balances, the work and the history do
  not return, and a nonempty appended suffix cannot equal the earlier history.
\end{enumerate}
\end{theorem}
```

## AD cor:xi:same-family-saturation

[F] Source [cor:xi:same-family-saturation](/home/repos/six-birds-papers/Tsiokos_2026_Adequacy_Residuals_and_Blind_Spot_Currency.tex:667); kind: corollary. Grade recorded in index: Lean / Mathlib.

[B] Reviewed applicability guard: Declared legal linear energy quotient/probes and actual linear dependence M=B L. The extra family then leaves Xi unchanged; non-linear learned features or a changed native source require a new bridge, not this corollary by name.

```tex
\begin{corollary}[Same-family saturation]\label{cor:xi:same-family-saturation}
If \(M=BL\), then \(\Xi_C(D\mid(L,M))=\Xi_C(D\mid L)\).
\end{corollary}
```

## C def:cpackage

[F] Source [def:cpackage](/home/repos/six-birds-papers/Tsiokos_2026_A_Closure_Architecture_for_Consciousness.tex:852); kind: definition. Grade recorded in index: contract definition.

[B] Reviewed applicability guard: Definition of the eight-clause conjunction plus cross-clause coherence and promotion panel. It is not an existence/soundness theorem for a record populated with assertions, and ethical/phenomenal bridges do not follow from a C4 privacy witness.

```tex
\begin{definition}[The closure architecture]
\label{def:cpackage}
A candidate satisfies the \emph{closure architecture} $\Cpkg$ when it meets the
following eight conditions jointly and on one system, together with coherence data
that tie the conditions to that one system and a full panel of the checks that each
condition requires.
\begin{description}
\item[(1) Objecthood.] The system forms stable objects: a family of staged closure
kernels $E_\tau$ (Definition~\ref{def:closure}) at specified horizons $\tau$ has robust fixed
distributions, with exact idempotence-defect bookkeeping and perturbation checks
against stated retention thresholds. The kernels need not be idempotent, so they
need not be closure operators in the order-theoretic sense.
\item[(2) Strict refinement.] Some finer description is not recoverable from the
public one. For the specified lower and higher readouts $\pi_0$ and $\pi_1$,
$\Dfact(\pi_0,\pi_1)\neq\emptyset$, witnessed by a pair of states that the lower
readout merges.
\item[(3) Predictive self-coordinate.] Refining the public self-description by the
system's own dynamics stabilizes at a predictive quotient that carries the
system's continuation coordinate.
\item[(4) Non-exposure.] The determining predictive state is not exposed at the
given public channels: no admissible current observable factors through it
non-constantly on the realized support. Hiddenness is relative to the channels
by construction.
\item[(5) Action credit.] A specified rule assigns each computed directionality to
\emph{self}, \emph{other}, or \emph{none} by where it was generated, and actions
scheduled from outside or absorbed from outside are not credited to self.
\item[(6) Temporal closure.] The system maintains a funded order, tick, and arrow:
a staged phase that persists and advances under a budget, with the arrow carried
by the system's own record rather than by an external schedule.
\item[(7) Binding.] Joint content over specified branches strictly refines the
branch-by-branch description, witnessed by $\Rrec \succ \Kbw$
(Section~\ref{sec:structure}).
\item[(8) Viability.] The viability kernel under the specified maintenance ledger is
nonempty, $\Kviab\neq\emptyset$, and underfunding empties it.
\end{description}
\end{definition}
```

## C T2

[F] Source [thm:t2](/home/repos/six-birds-papers/Tsiokos_2026_A_Closure_Architecture_for_Consciousness.tex:1096); kind: theorem. Grade recorded in index: theorem-grade finite direct instantiation; declared-channel dissolution control.

[B] Reviewed applicability guard: Exact finite privacy wheel, declared channel family, non-exposure and predictive witness content. Adding a predictive-state reading dissolves the split. No absolute privacy/phenomenality result; canonical label thm:t2 inside sec:interface (D17/D20).

```tex
\begin{theorem}[Non-exposure]
\label{thm:t2}
On the system just described, with its channel family $\Lambda$: if the determining
state is not exposed and the predictive quotient is strictly finer than the public
one, there is a loop that fixes every current public class and moves the predictive
class.
\end{theorem}
```

## V14 thm:identifiable

[F] Source [thm:identifiable](/home/repos/six-birds-papers/Tsiokos_2026_Six_Birds_Verified_XIV_Objectivity_Without_Finality.tex:447); kind: theorem. Grade recorded in index: Lean.

[B] Reviewed applicability guard: Declared target and calibrated transcript maps. Every target-different pair must be separated; target then factors uniquely on the reached transcript image. Label bijections preserve separation while decoder calibration may change; reward authority is additional.

```tex
\begin{theorem}[Identifiability]\label{thm:identifiable}
\begin{enumerate}
\item $p$ is identifiable through $F$ if and only if $\TSep_F(w,w')\ne\emptyset$ for every pair with $pw\ne pw'$. In that case $p$ factors
  uniquely through $q_F$ on $\operatorname{im}q_F$: there is exactly one map $\hat p$ on $\operatorname{im}q_F$ with $\hat p\circ q_F=p$.
\item The recorded public values are the calibrated readings: for every test of $F$ and every world, the exported value equals $m_tw$.
\item \emph{Separation is not calibration.} For a bijection $\pi$ of the report labels, the reports $o$ and $\pi\circ o$ have the same kernel. If
  $\mathrm{dec}$ calibrates $o$, then $\mathrm{dec}\circ\pi^{-1}$ calibrates $\pi\circ o$, and $\mathrm{dec}$ itself calibrates $\pi\circ o$ if and
  only if $\mathrm{dec}\circ\pi=\mathrm{dec}$ on $\operatorname{im}o$.
\end{enumerate}
\end{theorem}
```

## F4 thm:F17

[F] Source [thm:F17](/home/repos/six-birds-papers/Tsiokos_2026_Six_Birds_Foundations_IV_A_Catalog_of_Layer_Agnostic_Structural_Laws.tex:3795); kind: theorem. Grade recorded in index: proved structural laws.

[B] Reviewed applicability guard: Each access and public quotient is surjective and public quotient has the common-quotient universal property. Actual common target descent, rather than common words/consensus, is the conclusion; pairing public/target repairs representation, not normative authority.

```tex
\begin{theorem}[Objectivity as Common Quotient]\label{thm:F17}
Let \(H\) be a carrier with a family of access quotients
\(q_i:H\to Q_i\) indexed by \(i\in I\), a public quotient
\(p:H\to P\), and a target readout \(r:H\to R\).  Assume each
\(q_i\) is surjective, \(p\) is surjective, and the family satisfies
the common-quotient universal property
\(\operatorname{CommonQuotientUniversal}(q,p)\): \(p\) factors
through every \(q_i\), and any map \(s:H\to S\) that factors through every
\(q_i\) also factors through \(p\).  Then
\begin{align*}
  &\operatorname{CommonAcrossAccesses}(q,r)
    \iff \operatorname{PublicDeterminesObject}(p,r),\\
  &\operatorname{CommonAcrossAccesses}(q,r)\\
  &\qquad{}\iff
    \forall i\in I,\,
      \operatorname{AccessObjectivityDefectEmpty}(q_i,r),\\
  &\operatorname{PublicDeterminesObject}(p,r)\\
  &\qquad{}\iff
    \operatorname{ObstructionEmpty}
      \bigl(\operatorname{PublicToObjectDefect}(p,r)\bigr),
\end{align*}
together with
\begin{align*}
  &\operatorname{CommonQuotientVisible}(q,p),\\
  &\operatorname{RetainsPublicQuotient}
      \bigl(p,\operatorname{objectiveExtension}(p,r)\bigr),\\
  &\operatorname{CarriesObject}
      \bigl(\operatorname{objectiveExtension}(p,r),r\bigr),
\end{align*}
and the status partition
\[
  \operatorname{ExactlyOneObjectivityStatus}(p,r).
\]
In ordinary terms: \(p\) factors through every \(q_i\); the pairing
\(\langle p,r\rangle\) satisfies \(p=\mathrm{pr}_1\circ\langle p,r\rangle\) and
\(r=\mathrm{pr}_2\circ\langle p,r\rangle\); and exactly one of the following holds:
both \(r\) factors through \(p\) and \(p\) through \(r\) (exact common quotient);
only the first (coarse objective object); only the second (private
overrefinement); neither (incomparable).
\end{theorem}
```

## REF prop:cx1_ladder

[F] Source [prop:cx1_ladder](/home/repos/six-birds-papers/Tsiokos_2026_Reflexive_SBT_and_Anti_Localization.tex:659); kind: proposition. Grade recorded in index: written counterexample family, positive-conditioning bound, and span-ledger theorem.

[B] Reviewed applicability guard: Specific two-atom sparse linear dictionary ladder with N_j=2^(j+1), epsilon_j=2^(-j), atom localization vanishing and two-sparse synthesis localization1. Transfer to legal reachable coalition programs requires its actual harm/resource map; not arbitrary coalitions from span alone.

```tex
\begin{proposition}[CX1 along a ladder]\label{prop:cx1_ladder}
Take \(j\ge1\), \(N_j=2^{j+1}\) (so \(b_j=2\)) and \(\varepsilon_j=2^{-j}\).
Each atom has \(\Loc_j(d_\pm)=(2^{-j}+4^{-j})/(1+4^{-j})\to0\), so \(\Capatom(j)\to0\); but the two-atom dictionary admits a \(2\)-sparse synthesis with \(\Loc_j=1\) at every depth.
Correspondingly \(\kappa_2=\sqrt2\,\varepsilon_j/\sqrt{1+\varepsilon_j^2}\to0\) and \(2\Capatom(j)/\kappa_2^2\ge1\).
\end{proposition}
```

## F4 thm:F15a

[F] Source [thm:F15a](/home/repos/six-birds-papers/Tsiokos_2026_Six_Birds_Foundations_IV_A_Catalog_of_Layer_Agnostic_Structural_Laws.tex:3191); kind: theorem. Grade recorded in index: proved structural laws.

[B] Reviewed applicability guard: Selection descends iff fiber split absent. Fixed-point/equivariant-section obstruction additionally needs actual orbit quotient and induced trivial orbit action. A breaker extension carries selectedness but does not itself construct a selector.

```tex
\begin{theorem}[Selection Obstruction / Repair Normal Form]\label{thm:F15a}
Let \(G\) act on a set \(X\) and on an orbit set \(O\) by
\(\rho_X:G\times X\to X\) and \(\rho_O:G\times O\to O\).  Let
\(\pi:X\to O\) be a surjective map (in the intended reading the orbit map; the
orbit-quotient property is assumed only in the clause that states it), let
\(s:X\to\{0,1\}\) be a selectedness predicate, let
\(\sigma:O\to X\) be a map (in the intended reading a section of \(\pi\), though \(\pi\circ\sigma=\mathrm{id}_O\) is not assumed; the equivariant-section clause below concerns maps that satisfy it).  Define
\[
  \mathcal O_s
  :=
  \{(x,x')\in X^2:\pi(x)=\pi(x')\ \text{and}\ s(x)\ne s(x')\}.
\]
Then
\begin{align*}
  &\operatorname{EquivariantSelector}(\rho_O,\rho_X,\sigma)
    \wedge \operatorname{TrivialOrbitAction}(\rho_O)\\
  &\hspace{4em}\Longrightarrow
    \forall o\in O,\ \forall g\in G,\
      \rho_X(g,\sigma(o))=\sigma(o),\\
  s\ \text{descends through}\ \pi
  &\iff
  \mathcal O_s=\emptyset
  \iff
  \exists\,\bar s:O\to\{0,1\}\ \text{with}\ \bar s\circ\pi=s,\\
  \operatorname{HasSelectionSplit}(\pi,s)
  &\iff
  \mathcal O_s\ne\emptyset.
\end{align*}
If moreover \(\pi\) is the orbit quotient,
\(\pi(x)=\pi(x')\iff x'=\rho_X(g,x)\) for some \(g\in G\), and \(\rho_O\) is
the induced action, \(\rho_O(g,\pi(x))=\pi(\rho_X(g,x))\), then
\(\operatorname{TrivialOrbitAction}(\rho_O)\) holds, every equivariant map
\(\sigma:O\to X\), in particular every equivariant section, takes values in the
common fixed-point set \(X^G\), and if \(X^G=\emptyset\) and
\(O\ne\emptyset\), no equivariant map \(O\to X\) exists; and an equivariant section exists if and only if \(G\) acts trivially on \(X\), and it is then the inverse of \(\pi\).
For every breaker readout \(b:X\to B\), the breaker extension
\(\langle\pi,b\rangle:X\to O\times B\) retains \(\pi\) and carries \(b\), strictly
refines \(\pi\) when \(b\) separates two points of one \(\pi\)-fiber, and factors
through every map \(p\) through which both \(\pi\) and \(b\) factor. Conversely to the fixed-point clause above, under the orbit-quotient and induced-action hypotheses every map \(O\to X^G\) is equivariant, so an equivariant map \(O\to X\) exists if and only if \(X^G\ne\emptyset\) or \(O=\emptyset\). Adjoining \(b\) records the
distinction carried by \(b\); taking \(b=s\) carries selectedness, but the
extension alone does not construct a selector.
\end{theorem}
```

## SPEND thm:duality

[F] Source [thm:duality](/home/repos/six-birds-papers/Tsiokos_2026_To_Spend_a_Stone_with_Six_Birds_Currency_Constraint_Duality_and_Shadow_Prices_Across_Closure_Layers.tex:290); kind: theorem. Grade recorded in index: assumed maintenance/resource law; proved finite fixed-μ Gibbs theorem and regimes; finite persistence example; synthetic proxy experiment plus population KL argument; reported Lean single-row duality only.

[B] Reviewed applicability guard: Finite row-stochastic entropy/Gibbs setting, fixed row weights and declared cost, lambda>=0; budget optimality needs feasibility plus complementary slackness. Only positive-weight rows are unique. Physical resource law and economic-fee correspondence are separate hypotheses.

```tex
\begin{theorem}[Finite Gibbs duality]\label{thm:duality}
Let \(\lambda\ge0\) and \(b\in\R\).
\begin{enumerate}[label=(\roman*),leftmargin=*]
\item For every row-stochastic \(p\),
\[
\sum_i\mu_i\,\KL\big(p_{i\cdot}\,\|\,q^{\lambda}_{i\cdot}\big)=-\Hmu(p)+\lambda\,\Cmu(p)+\sum_i\mu_i\log Z_i(\lambda).
\]
\item Consequently \(\Hmu(p)-\lambda\Cmu(p)\le\Hmu(q^\lambda)-\lambda\Cmu(q^\lambda)\) for every \(p\).
\item If \(\Cmu(q^\lambda)\le b\) and \(\lambda\big(\Cmu(q^\lambda)-b\big)=0\), then \(q^\lambda\) maximizes \(\Hmu\) over \(\{p:\Cmu(p)\le b\}\).
\item Under the conditions of (iii), every \(p\) with \(\Cmu(p)\le b'\) satisfies \(\Hmu(p)\le\Hmu(q^\lambda)+\lambda(b'-b)\). Hence \(\lambda\) is a supergradient of the concave value function \(V(b)=\sup\{\Hmu(p):\Cmu(p)\le b\}\) at \(b\), and \(V'(b)=\lambda\) wherever \(V\) is differentiable.
\end{enumerate}
In (iii) the optimizer is unique on the rows with \(\mu_i>0\); rows with \(\mu_i=0\) do not enter the objective, and there any row is optimal.
\end{theorem}
```

## V13 thm:atlas

[F] Source [thm:atlas](/home/repos/six-birds-papers/Tsiokos_2026_Six_Birds_Verified_XIII_Time_Charge_and_Currency.tex:508); kind: theorem. Grade recorded in index: Lean over ℚ.

[B] Reviewed applicability guard: Six explicit rational/finite non-implication witnesses: time/charge, charge/transfer, balanced postings/potential, storage/conservation, generator/unique form, conserved readout/storage factorization. It classifies structural roles, not general market optimality.

```tex
\begin{theorem}[Non-coincidence atlas]\label{thm:atlas}
Each of the following implications fails.
\begin{enumerate}
\item \emph{A nontrivial time action has a nonconstant conserved charge.} The $\mathbb N$-action $\tau_t(x)=x+t$ on $\mathbb Z/5$ is
  nontrivial, and every charge it conserves is constant.
\item \emph{A conserved charge is transferable.} On four states with transitions $0\leftrightarrow1$ and $2\leftrightarrow3$, the charge
  $Q=1$ on $\{0,1\}$ and $Q=5/2$ on $\{2,3\}$ is conserved along every transition, but with no declared transfer map it has no licensed
  transaction. With the single transfer map that accepts the amount $3/2$ at state $0$ and returns state $2$, the transaction $(0,3/2,2)$ is
  licensed and $Q$ is transferable.
\item \emph{Balanced postings give a state potential.} On the directed triangle $0\to1\to2\to0$, let each step post one unit, as a pair of entries of opposite
  sign in two accounts, the system account receiving $+1$. Every posting balances, its entries summing to zero, but the system transfers sum to $3$ around the loop, so no
  state potential exists.
\item \emph{A storage is conserved by every generator.} On $\mathbb Q^2$, for $A=-I$ and $S=I$, $D_AH(x)=-x^\T x$, which is nonzero for $x\ne0$.
\item \emph{A generator determines its conserved form up to scale.} The generator $J\oplus J$, two oscillators at one frequency,
  has a four-dimensional space of conserved forms (\cref{thm:normalization}).
\item \emph{A generator conserving a readout factors through the readout's storage matrix.} For $Q(x)=\tfrac12x_1^2$, with
  $S_Q=\operatorname{diag}(1,0)$, and $A=\operatorname{diag}(0,1)$, $D_AQ=0$, but $A\ne JS_Q$ for every matrix $J$.
\end{enumerate}
\end{theorem}
```

## C T13

[F] Source [thm:t13](/home/repos/six-birds-papers/Tsiokos_2026_A_Closure_Architecture_for_Consciousness.tex:1547); kind: theorem. Grade recorded in index: theorem-grade exact gauge construction; rigidification principle schema.

[B] Reviewed applicability guard: Eight-state/four-public-class finite descent-fixing gauge; modeled descent-visible rigidifier makes global-swap Z2 trivial and reduces two transports to one. Broader quality-space rigidification is schema-grade, not measured legal/subjective interpretation.

```tex
\begin{theorem}[Gauge freedom and rigidification]
\label{thm:t13}
On an eight-state bundle with four public classes of two fiber points each and
specified descents, let
$G = \{\sigma \in \mathrm{Aut}(M) : \pi\sigma = \pi \text{ and } d\sigma = d \text{ for every admissible descent } d\}$
be the descent-fixing gauge group. Spectrum inversion is a lawful distinct possibility
exactly to the extent that $G$ is nontrivial. Exact enumeration gives $40320$
automorphisms of the support, of which $16$ fix the projection, and
$G = \{\mathrm{id}, \text{global swap}\} \cong \mathbb{Z}_2$ in the symmetric case.
Adding one specified, descent-visible orientation of discrimination density, calibrated
by the signature of Theorem~\ref{thm:t12} at one public class, gives $G = \{\mathrm{id}\}$.
Route transport between two isomorphic fibers shows the same contrast: two admissible
transports in the symmetric case, exactly one after rigidification.
\end{theorem}
```

## PT thm:trap

[F] Source [thm:trap](/home/repos/six-birds-papers/Tsiokos_2026_Six_Birds_Protocol_Trap_Holonomy_Without_Entropy_Production.tex:314); kind: theorem. Grade recorded in index: proved.

[B] Reviewed applicability guard: Protocol scheduler reversible w.r.t. s and every state kernel reversible w.r.t. the same pi; lifted law is product pi*s. Zero path-reversal divergence for coordinatewise observations under these hypotheses does not settle meaning, intent or other irreversible protocols.

```tex
\begin{theorem}[Protocol trap]\label{thm:trap}
Suppose that \(S\) satisfies detailed balance with respect to \(s\), and that every \(K_\phi\) satisfies detailed balance with respect to a common law \(\pi\). Then for every \(\alpha\in[0,1]\) the lift \(P\) satisfies detailed balance with respect to \(\mu=\pi\otimes s\). Consequently:
\begin{enumerate}
\item \(\EPR(P,\mu)=0\) and \(\Sigma_T(P,\mu)=0\) for every horizon \(T\);
\item every coordinatewise observation shows no arrow either. For any map \(f\colon Z\to Y\), the law of the observed recording \((f(z_0),\dots,f(z_T))\) is invariant under time reversal, so its path-reversal divergence is zero for every \(T\).
\end{enumerate}
\end{theorem}
```

## INST prop:coercion-null-probe

[F] Source [prop:coercion-null-probe](/home/repos/six-birds-papers/Tsiokos_2026_Institutions_Are_Strict_Extensions_of_the_Game.tex:1127); kind: proposition. Grade recorded in index: exact, scoped.

[B] Reviewed applicability guard: Declared finite carrier, same source history, same final fully forced profile and equal Pi1 endpoint readout. It is the scoped no-witness enumeration; unilateral/free-response probes can preserve memory. No universal statement about coercion/intent.

```tex
\begin{proposition}[Coercion-null and probe-memory contrast]
\label{prop:coercion-null-probe}
On the declared carrier, two fully forced protocols from the same source history
that end with the same forced profile, and whose endpoints have the same
\(\PiOne\) readout, have the same predictive state.  The declared grid has
78{,}528 same-final two-sided pairs, of which 3{,}456 also have equal
\(\PiOne\) readouts, and none of these is a witness.  By contrast, one-sided probes can end
with the same readout and different predictive states
(\Cref{prop:loop-asymmetry}), because the free responses observed during the
probe sharpen the posterior over rule pairs.
\end{proposition}
```

## V11 thm:carriage

[F] Source [thm:carriage](/home/repos/six-birds-papers/Tsiokos_2026_Six_Birds_Verified_XI_Self_Carried_Closure.tex:899); kind: theorem. Grade recorded in index: Lean.

[B] Reviewed applicability guard: Realized capability rules/seed/reach fixed-point/lifetimes. Necessity holds for every capacity/lifetime. Sufficiency needs UNBOUNDED capacity and each seed lifetime>=realized reach height+1; finite-capacity funding needs a separately witnessed run.

```tex
\begin{theorem}[A necessary and a sufficient condition for self-carriage]\label{thm:carriage}
Let $T\subseteq C$ and $B\subseteq C$.
\begin{enumerate}
\item For every capacity and all lifetimes: if $T$ is self-carried from $B$, then $T\subseteq\Sstar(B)$.
\item Suppose the capacity is unbounded and $L(b)\ge\hp(B)+1$ for every $b\in B$. If $T\subseteq\Sstar(B)$,
  then $T$ is self-carried from $B$. A witnessing run fires every enabled rule at every round; it has all of
  $\Reachp(B)$ present at round $\hp(B)$ and all of $\Sstar(B)$ present at every later round.
\end{enumerate}
\end{theorem}
```

## V15 thm:audit

[F] Source [thm:audit](/home/repos/six-birds-papers/Tsiokos_2026_Six_Birds_Verified_XV_Portable_Theories.tex:1058); kind: theorem. Grade recorded in index: mechanized finite-index audit theorem; mechanized native-chain theorem; kernel-checked finite mixture example.

[B] Reviewed applicability guard: Behavior finite index n_beta and host reachable-state bound m give pointed word cutoff n_beta+m-2. Without host size bound no finite pointed test certifies all hosts. Actual alphabet, behavior and counted reachability are required; stochastic/raw-history traces are not silently deterministic finite behaviors.

```tex
\begin{theorem}[Finite audit]\label{thm:audit}
Let $\beta$ have finite index $n_\beta$, and let $M$ be a presentation whose reachable part has at most $m$ states.
\begin{enumerate}
\item If $M$ agrees with $\beta$ on every history of length at most $n_\beta+m-2$, then $M$ has behaviour $\beta$.
\item The bound is attained for every pair $n,m\ge1$: there are a behaviour with $n_\beta=n$ and a presentation with exactly $m$ reachable states and an $m$-state core that agree on every history of length less than $n+m-2$ and differ on a history of length $n+m-2$ (\cref{ex:audit-sharp}).
\item Without a size bound no finite test suffices. Let $\beta$ have finite index over a nonempty alphabet with at least two outputs. For every cutoff $\ell$ there is a finite machine with all states reachable that agrees with $\beta$ on every history of length at most $\ell$ and differs from $\beta$ on every longer history; so no finite set of pointed tests (pairs $(h,\beta(h))$ checked from the start state) certifies agreement with $\beta$ against all finite-state hosts.
\end{enumerate}
\end{theorem}
```

