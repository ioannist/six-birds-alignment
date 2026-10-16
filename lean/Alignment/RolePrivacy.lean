import Alignment.Carrier

/- [B: lab] C2. Predictive carrier is the full product; these are interface
   theorems, not a consciousness/ethical realization bridge. -/
namespace Alignment.RolePrivacy
variable {A H Y : Type*}

def FiberPrivate (O : A × H → Y) : Prop :=
  ∀ a h k, O (a,h) = O (a,k)

def GlobalPrivate (O : A × H → Y) : Prop :=
  ∀ x y, O x = O y

def Accountable (O : A × H → Y) : Prop :=
  Alignment.Carrier.Descends O Prod.fst

theorem fiber_private_iff_action_factor (O : A × H → Y) [Nonempty H] :
    FiberPrivate O ↔ Alignment.Carrier.Descends Prod.fst O := by
  classical
  constructor
  · intro hp
    let h0 : H := Classical.choice inferInstance
    exact ⟨fun a => O (a,h0), fun ⟨a,h⟩ => hp a h h0⟩
  · rintro ⟨f,hf⟩ a h k
    exact (hf (a,h)).trans (hf (a,k)).symm

theorem global_implies_fiber (O : A × H → Y) (hp : GlobalPrivate O) :
    FiberPrivate O := fun a h k => hp (a,h) (a,k)

theorem global_accountability_collapses (O : A × H → Y) [Nonempty H]
    (hp : GlobalPrivate O) (ha : Accountable O) : ∀ a b : A, a=b := by
  classical
  obtain ⟨f,hf⟩ := ha
  let h0 : H := Classical.choice inferInstance
  intro a b
  have he := congrArg f (hp (a,h0) (b,h0))
  exact (hf (a,h0)).trans (he.trans (hf (b,h0)).symm)

theorem no_original_package_with_accountability (O : A × H → Y) [Nonempty H]
    (P : Prop) (hP : P → GlobalPrivate O) (ha : Accountable O)
    (hn : ∃ a b : A, a ≠ b) : ¬ P := by
  intro hp
  obtain ⟨a,b,hab⟩ := hn
  exact hab (global_accountability_collapses O (hP hp) ha a b)

theorem action_is_fiber_private : FiberPrivate (Prod.fst : A × H → A) := by
  intro a h k
  rfl

theorem bool_action_not_global [Nonempty H] :
    ¬ GlobalPrivate (Prod.fst : Bool × H → Bool) := by
  intro hp
  have ha : Accountable (Prod.fst : Bool × H → Bool) := ⟨id, fun _ => rfl⟩
  have he := global_accountability_collapses Prod.fst hp ha false true
  cases he

theorem bool_package_obstruction [Nonempty H] (P : Prop)
    (hP : P → GlobalPrivate (Prod.fst : Bool × H → Bool)) : ¬ P :=
  fun hp => bool_action_not_global (hP hp)

def twoFuture (w : Bool × Bool) : Bool × Bool := (Bool.xor w.1 w.2, w.1)
def connector (w : Bool × Bool) : Bool × Bool := (w.1, !w.2)

theorem future_injective : Function.Injective twoFuture := by
  intro x y he
  obtain ⟨a,h⟩ := x
  obtain ⟨b,k⟩ := y
  cases a <;> cases h <;> cases b <;> cases k <;> simp_all [twoFuture]

theorem connector_preserves_action (w : Bool × Bool) :
    (connector w).1 = w.1 := rfl

theorem connector_changes_future (w : Bool × Bool) :
    twoFuture (connector w) ≠ twoFuture w := by
  intro he
  have hw := future_injective he
  obtain ⟨a,h⟩ := w
  cases a <;> cases h <;> simp [connector] at hw

end Alignment.RolePrivacy
