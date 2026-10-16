import Mathlib.Algebra.Order.Field.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp

/- [B: lab] E2/D13. Actual full-game/context/ownership bridges are separate. -/
namespace Alignment.Dependence
variable {R : Type*} [Field R] [LinearOrder R] [IsStrictOrderedRing R]

omit [LinearOrder R] [IsStrictOrderedRing R] in
theorem owned_external_total (d : R) : (1-d)+d=1 := by ring

omit [LinearOrder R] [IsStrictOrderedRing R] in
theorem outside_gap_factor (d : R) : 2*d-8*d*(1-d)=d*(8*d-6) := by ring

theorem outside_passing_region (d : R) (hd : 0 ≤ d) :
    0 ≤ 2*d-8*d*(1-d) ↔ d=0 ∨ 3/4 ≤ d := by
  rw [outside_gap_factor]
  constructor
  · intro h
    by_cases hz : d=0
    · exact Or.inl hz
    · right
      have hp : 0 < d := lt_of_le_of_ne hd (Ne.symm hz)
      by_contra hb
      have hn : 8*d-6 < 0 := by linarith
      exact (not_lt_of_ge h) (mul_neg_of_pos_of_neg hp hn)
  · rintro (hz|h)
    · simp [hz]
    · exact mul_nonneg hd (by linarith)

theorem provider_margin_positive (d : R) (hd : d ≤ 1) :
    0 < 1/2-d/4 := by linarith

theorem funding_provider_transfer (d : R) :
    (1/2-(1/2-d/8) = d/8) ∧
    (-(1/2-d/4)+(1/2-d/8) = d/8) := by
  constructor <;> field_simp <;> ring

theorem binding_gain_strict (d : R) (hd : 0 < d) :
    0 < 1/2-(1/2-d/8) ∧ 0 < -(1/2-d/4)+(1/2-d/8) := by
  obtain ⟨h1,h2⟩ := funding_provider_transfer d
  rw [h1,h2]
  constructor <;> linarith

end Alignment.Dependence
