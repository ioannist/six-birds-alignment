import Mathlib.Algebra.Order.Field.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Lean.Elab.Tactic.Omega

/- [B: lab] D10, D11 / D18(c,d). Legitimacy/finance are hypotheses. -/
namespace Alignment.Payoffs
variable {R : Type*} [Field R] [LinearOrder R] [IsStrictOrderedRing R]

omit [IsStrictOrderedRing R] in
theorem interruption_iff (S a T r σ A : R) :
    (S-a+T ≥ r-σ ∧ S-a+T ≥ A) ↔ S-a+T ≥ max (r-σ) A := by
  exact (max_le_iff).symm

theorem deterrence_iff (g q P : R) : g-q*P ≤ 0 ↔ g ≤ q*P := by
  constructor <;> intro h <;> linarith

theorem strict_deterrence_iff (g q P : R) : g-q*P < 0 ↔ g < q*P := by
  constructor <;> intro h <;> linarith

-- pBelow = Pr(J < m-1), pPiv = Pr(J = m-1), pAbove = Pr(J >= m).
omit [LinearOrder R] [IsStrictOrderedRing R] in
theorem hosting_pivotal_gain (ω V h pPiv pAbove : R) :
    (ω*V*(pPiv+pAbove)-h) - (ω*V*pAbove) = ω*V*pPiv-h := by ring

theorem hosting_best_response (ω V h pPiv pAbove : R) :
    ω*V*pAbove ≤ ω*V*(pPiv+pAbove)-h ↔ h ≤ ω*V*pPiv := by
  constructor <;> intro h' <;> nlinarith

def hostUtility (ω V h : R) (m others : Nat) (host : Bool) : R :=
  ω*V*(if m ≤ others+(if host then 1 else 0) then 1 else 0) -
  h*(if host then 1 else 0)

theorem all_N_strict (ω V h : R) (m : Nat) (hm : 2 ≤ m) (hh : 0 < h) :
    hostUtility ω V h m 0 true < hostUtility ω V h m 0 false := by
  have h0 : ¬ m ≤ 0 := by omega
  have h1 : ¬ m ≤ 1 := by omega
  simp [hostUtility, h0, h1, hh]

-- D1: sign isolation at the exact endpoints; this does not prove uniqueness.
def thresholdPolynomial (d : R) : R :=
  23588101*d^5-512020740*d^4+915214800*d^3-
  30787520000*d^2-672000000*d+12800000000

theorem threshold_endpoint_signs :
    0 < thresholdPolynomial (2382315/3734821 : ℚ) ∧
    thresholdPolynomial (2383666/3736939 : ℚ) < 0 := by
  norm_num [thresholdPolynomial]

end Alignment.Payoffs
