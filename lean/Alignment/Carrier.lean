import Mathlib.Tactic.NormNum

/- [B: lab] C13 (also C3/C5/C9): target descent through a declared lens. -/
namespace Alignment.Carrier
variable {S Q T Z : Type*}

def Descends (q : S → Q) (target : S → T) : Prop :=
  ∃ f : Q → T, ∀ s, target s = f (q s)

theorem descent_iff_fibers (q : S → Q) (target : S → T)
    (hq : Function.Surjective q) :
    Descends q target ↔ ∀ x y, q x = q y → target x = target y := by
  classical
  constructor
  · rintro ⟨f, hf⟩ x y he
    rw [hf x, hf y, he]
  · intro h
    refine ⟨fun z => target (Classical.choose (hq z)), ?_⟩
    intro s
    exact h s (Classical.choose (hq (q s)))
      (Classical.choose_spec (hq (q s))).symm

theorem repaired_target (q : S → Q) (target : S → T) :
    Descends (fun s => (q s, target s)) target := by
  exact ⟨Prod.snd, fun s => rfl⟩

theorem repair_preserves_current (q : S → Q) (target : S → T) :
    Descends (fun s => (q s, target s)) q := by
  exact ⟨Prod.fst, fun s => rfl⟩

theorem repair_is_coarsest (q : S → Q) (target : S → T) (r : S → Z)
    (hq : Descends r q) (ht : Descends r target) :
    Descends r (fun s => (q s, target s)) := by
  obtain ⟨f, hf⟩ := hq
  obtain ⟨g, hg⟩ := ht
  exact ⟨fun z => (f z, g z), fun s => by
    change (q s, target s) = (f (r s), g (r s))
    rw [hf s, hg s]⟩

theorem duty_split : ¬ Descends (fun s : Bool × Bool => s.2) (fun s => s.1) := by
  rintro ⟨f, hf⟩
  have h0 := hf (false, false)
  have h1 := hf (true, false)
  simp only at h0 h1
  have : (false : Bool) = true := h0.trans h1.symm
  cases this

end Alignment.Carrier
