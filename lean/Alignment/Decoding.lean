import Mathlib.Tactic.NormNum
import Lean.Elab.Tactic.Omega

/- [B: lab] D5 / D18(b): actual binary transcripts, arbitrary length/budget. -/
namespace Alignment.Decoding

theorem counts (t : List Bool) : t.count true + t.count false = t.length := by
  induction t with
  | nil => simp
  | cons x xs ih => cases x <;> simp_all <;> omega

def Decodable (n b : Nat) : Prop :=
  ∀ t : List Bool, t.length = n → ¬ (t.count true ≤ b ∧ t.count false ≤ b)

theorem repetition_iff (n b : Nat) : Decodable n b ↔ 2*b+1 ≤ n := by
  constructor
  · intro h
    by_contra hn
    have hn' : n ≤ 2*b := by omega
    let k := min b n
    let t := List.replicate k true ++ List.replicate (n-k) false
    have hk : k ≤ n := Nat.min_le_right _ _
    have hl : t.length = n := by simp [t]; omega
    have htrue : t.count true = k := by simp [t, List.count_replicate]
    have hfalse : t.count false = n-k := by simp [t, List.count_replicate]
    have hb : k ≤ b := Nat.min_le_left _ _
    have hnb : n-k ≤ b := by dsimp [k]; omega
    exact h t hl ⟨by omega, by omega⟩
  · intro h t hl ⟨h1, h2⟩
    have hc := counts t
    omega

def corruptionCount (truth : Bool) (t : List Bool) : Nat :=
  if truth then t.count false else t.count true

def majority (t : List Bool) : Bool := decide (t.count false < t.count true)

def DecoderExists (n b : Nat) : Prop :=
  ∃ decode : List Bool → Bool, ∀ t : List Bool, t.length=n →
    ∀ truth : Bool, corruptionCount truth t ≤ b → decode t=truth

theorem majority_correct (n b : Nat) (hnb : 2*b+1 ≤ n) (t : List Bool)
    (hl : t.length=n) (truth : Bool) (hf : corruptionCount truth t ≤ b) :
    majority t=truth := by
  have hc := counts t
  cases truth with
  | false =>
    simp only [corruptionCount, Bool.false_eq_true, if_false] at hf
    have hn : ¬ t.count false < t.count true := by omega
    simp [majority, hn]
  | true =>
    simp only [corruptionCount, if_true] at hf
    have hp : t.count false < t.count true := by omega
    simp [majority, hp]

theorem decoder_implies_disjoint (n b : Nat) (hd : DecoderExists n b) : Decodable n b := by
  obtain ⟨decode, hdecode⟩ := hd
  intro t hl ⟨hzero, hone⟩
  have hz : decode t=false := hdecode t hl false (by simpa [corruptionCount] using hzero)
  have ho : decode t=true := hdecode t hl true (by simpa [corruptionCount] using hone)
  have hh : (false : Bool)=true := hz.symm.trans ho
  cases hh

theorem decoder_exists_iff (n b : Nat) : DecoderExists n b ↔ 2*b+1 ≤ n := by
  constructor
  · intro h
    exact (repetition_iff n b).mp (decoder_implies_disjoint n b h)
  · intro h
    exact ⟨majority, fun t hl truth hf => majority_correct n b h t hl truth hf⟩

end Alignment.Decoding
