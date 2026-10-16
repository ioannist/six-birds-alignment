import Mathlib.Algebra.Order.Field.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Tactic.Linarith

/- [B: lab] D15/D19. Algebraic coalition certificate used by exact audits.
   Physical execution and instantiated game/phase inequalities are separate. -/
namespace Alignment.Coalitions
open scoped BigOperators
variable {I R : Type*} [Fintype I] [Field R] [LinearOrder R] [IsStrictOrderedRing R]

def coalitionSum (d : I → R) (members : I → Bool) : R :=
  ∑ i, if members i = true then d i else 0

def forcedUpper (d : I → R) (required : I → Bool) : R :=
  ∑ i, if required i = true then d i else max (d i) 0

theorem coalition_sum_le_forced_upper (d : I → R) (required members : I → Bool)
    (h : ∀ i, required i = true → members i = true) :
    coalitionSum d members ≤ forcedUpper d required := by
  apply Finset.sum_le_sum
  intro i _
  by_cases hr : required i = true
  · have hm := h i hr
    simp [hr, hm]
  · by_cases hm : members i = true
    · simp only [hr, hm, ↓reduceIte]
      exact le_max_left _ _
    · simp only [hr, hm]
      exact le_max_right _ _

theorem no_positive_coalition_sum (d : I → R) (required members : I → Bool)
    (h : ∀ i, required i = true → members i = true)
    (hu : forcedUpper d required ≤ 0) : coalitionSum d members ≤ 0 :=
  (coalition_sum_le_forced_upper d required members h).trans hu

def maximizingMembers (d : I → R) (required : I → Bool) (i : I) : Bool :=
  if required i = true ∨ 0 < d i then true else false

omit [Fintype I] [IsStrictOrderedRing R] in
theorem maximizing_contains_required (d : I → R) (required : I → Bool) :
    ∀ i, required i = true → maximizingMembers d required i = true := by
  intro i hi
  simp [maximizingMembers, hi]

omit [IsStrictOrderedRing R] in
theorem forced_upper_attained (d : I → R) (required : I → Bool) :
    coalitionSum d (maximizingMembers d required) = forcedUpper d required := by
  apply Finset.sum_congr rfl
  intro i _
  by_cases hr : required i = true
  · simp [maximizingMembers, hr]
  · by_cases hd : 0 < d i
    · simp [maximizingMembers, hr, hd, max_eq_left (le_of_lt hd)]
    · have hnonpos : d i ≤ 0 := le_of_not_gt hd
      simp [maximizingMembers, hr, hd, max_eq_right hnonpos]

omit [LinearOrder R] [IsStrictOrderedRing R] in
theorem balanced_transfers_preserve_sum (d t : I → R) (members : I → Bool)
    (ht : coalitionSum t members = 0) :
    coalitionSum (fun i => d i+t i) members = coalitionSum d members := by
  have pointwise : ∀ i, (if members i = true then d i+t i else 0) =
      (if members i = true then d i else 0)+(if members i = true then t i else 0) := by
    intro i
    by_cases h : members i = true <;> simp [h]
  simp only [coalitionSum, pointwise, Finset.sum_add_distrib]
  change coalitionSum d members+coalitionSum t members = coalitionSum d members
  rw [ht, add_zero]

theorem no_pareto_improvement (d : I → R) (members : I → Bool)
    (hbound : coalitionSum d members ≤ 0)
    (hnonnegative : ∀ i, members i = true → 0 ≤ d i) :
    ¬ ∃ j, members j = true ∧ 0 < d j := by
  rintro ⟨j, hj, hdj⟩
  have hsum : 0 < coalitionSum d members := by
    apply Finset.sum_pos'
    · intro i _
      by_cases hm : members i = true
      · simpa [hm] using hnonnegative i hm
      · simp [hm]
    · exact ⟨j, Finset.mem_univ j, by simpa [hj] using hdj⟩
  exact (not_lt_of_ge hbound) hsum

theorem atomic_stage_cap (p q x y B a : R)
    (hp : 0 ≤ p) (hpq : p ≤ q) (hxy : x ≤ y) (hB : 0 ≤ B)
    (hcoefficient : 0 ≤ B*y-a) : p*(B*x-a) ≤ q*(B*y-a) := by
  have h1 : B*x-a ≤ B*y-a := sub_le_sub_right (mul_le_mul_of_nonneg_left hxy hB) a
  exact (mul_le_mul_of_nonneg_left h1 hp).trans
    (mul_le_mul_of_nonneg_right hpq hcoefficient)

end Alignment.Coalitions
