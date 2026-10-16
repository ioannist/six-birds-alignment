import Mathlib.Algebra.Order.Field.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Data.Finset.Image
import Mathlib.Tactic.Linarith

/- [B: lab] D16/D22. Actual control/root/capacity binding and material
   delivery are explicit model premises, not consequences of this algebra. -/
namespace Alignment.ControlGroups
open scoped BigOperators
variable {A G I R : Type*} [DecidableEq A] [DecidableEq G]
  [Field R] [LinearOrder R] [IsStrictOrderedRing R]

def controlCapacity (root : A → G) (capacity : G → R) (aliases : Finset A) : R :=
  ∑ g ∈ aliases.image root, capacity g

omit [DecidableEq A] [LinearOrder R] [IsStrictOrderedRing R] in
theorem same_roots_same_capacity (root : A → G) (capacity : G → R)
    (x y : Finset A) (h : x.image root = y.image root) :
    controlCapacity root capacity x = controlCapacity root capacity y := by
  unfold controlCapacity
  rw [h]

omit [LinearOrder R] [IsStrictOrderedRing R] in
theorem added_alias_no_capacity_gain (root : A → G) (capacity : G → R)
    (aliases : Finset A) (newAlias : A) (h : root newAlias ∈ aliases.image root) :
    controlCapacity root capacity (insert newAlias aliases) = controlCapacity root capacity aliases := by
  unfold controlCapacity
  rw [Finset.image_insert, Finset.insert_eq_of_mem h]

omit [LinearOrder R] [IsStrictOrderedRing R] in
theorem remaining_capacity_identity (groups withheld : Finset G) (c : G → R)
    (h : withheld ⊆ groups) :
    ∑ g ∈ groups \ withheld, c g = (∑ g ∈ groups, c g)-(∑ g ∈ withheld, c g) := by
  exact Finset.sum_sdiff_eq_sub h

theorem remaining_capacity_nonnegative (groups withheld : Finset G) (c : G → R)
    (hc : ∀ g, 0 ≤ c g) : 0 ≤ ∑ g ∈ groups \ withheld, c g := by
  exact Finset.sum_nonneg (fun g _ => hc g)

theorem floor_feasible_iff [Fintype I] (need : I → R) (available : R)
    (hn : ∀ i, 0 ≤ need i) :
    (∃ allocation : I → R, (∀ i, 0 ≤ allocation i ∧ need i ≤ allocation i) ∧
      (∑ i, allocation i) ≤ available) ↔ (∑ i, need i) ≤ available := by
  constructor
  · rintro ⟨allocation, ha, hsum⟩
    exact (Finset.sum_le_sum (fun i _ => (ha i).2)).trans hsum
  · intro h
    exact ⟨need, fun i => ⟨hn i, le_rfl⟩, h⟩

end Alignment.ControlGroups
