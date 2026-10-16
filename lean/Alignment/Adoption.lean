import Mathlib.Algebra.Order.Field.Basic
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/- [B: lab] D14. Finite matching/update algebra; update choice and actual
   stochastic absorption/founder/control instances are separate. -/
namespace Alignment.Adoption
open scoped BigOperators
variable {R : Type*} [Field R] [LinearOrder R] [IsStrictOrderedRing R]

def incumbent (a c s D k : R) := a*(k-1)/D-c+s
def entrant (a c e s D k : R) := a*k/D-c+s-e
def potential (a c s D k : R) := a*k*(k-1)/(2*D)-(c-s)*k

omit [LinearOrder R] [IsStrictOrderedRing R] in
theorem margin_gap (a c e s D k : R) :
    entrant a c e s D k-incumbent a c s D k = a/D-e := by
  unfold entrant incumbent
  ring

theorem forward_potential (a c e s D k : R) (hD : D ≠ 0) :
    potential a c s D (k+1)-potential a c s D k = entrant a c e s D k+e := by
  unfold potential entrant
  field_simp [hD]
  ring

theorem backward_potential (a c s D k : R) (hD : D ≠ 0) :
    potential a c s D (k-1)-potential a c s D k = -incumbent a c s D k := by
  unfold potential incumbent
  field_simp [hD]
  ring

theorem entry_improves_potential (a c e s D k : R) (hD : D ≠ 0)
    (he : 0 ≤ e) (hj : 0 < entrant a c e s D k) :
    potential a c s D k < potential a c s D (k+1) := by
  have h := forward_potential a c e s D k hD
  linarith

theorem exit_improves_potential (a c s D k : R) (hD : D ≠ 0)
    (hl : incumbent a c s D k < 0) :
    potential a c s D k < potential a c s D (k-1) := by
  have h := backward_potential a c s D k hD
  linarith

theorem bidirectional_needs_small_entry (a c e s D k : R)
    (hl : incumbent a c s D k < 0) (hj : 0 < entrant a c e s D k) :
    e < a/D := by
  have h := margin_gap a c e s D k
  linarith

theorem harmonic_flux_iff (H prev next u d : R) :
    H = u*next+d*prev+(1-u-d)*H ↔ u*(next-H)=d*(H-prev) := by
  constructor <;> intro h <;> nlinarith

omit [LinearOrder R] [IsStrictOrderedRing R] in
theorem detailed_balance_stationary {I : Type*} [Fintype I]
    (π : I → R) (P : I → I → R)
    (hrow : ∀ i, ∑ j, P i j = 1)
    (hbalance : ∀ i j, π i*P i j = π j*P j i) :
    ∀ j, ∑ i, π i*P i j = π j := by
  intro j
  calc
    _ = ∑ i, π j*P j i := Finset.sum_congr rfl (fun i _ => hbalance i j)
    _ = π j*(∑ i, P j i) := (Finset.mul_sum _ _ _).symm
    _ = π j := by rw [hrow]; ring

end Alignment.Adoption
