# Balika & Sinawa EDM Concept (Improved)
use_bpm 128

# Master Metronome for Sync
live_loop :metronome do
  sleep 1
end

# The Sweet Acoustic Synth Lead with Reverb
live_loop :acoustic_synths do
  sync :metronome
  with_fx :reverb, room: 0.7, mix: 0.3 do
    use_synth :pluck
    use_synth_defaults coef: 0.4, release: 0.1
    notes = (ring :E4, :G4, :A4, :E4, :G4, :B4)
    play notes.tick, amp: 1.2
  end
  sleep 0.25
end

# The EDM Kick Drum
live_loop :kick do
  sync :metronome
  sample :bd_haus, amp: 2
  sleep 1
end

# NEW FEATURE: Snare on beats 2 and 4
live_loop :snare do
  sync :metronome
  sleep 1 # wait for beat 1 (kick)
  sample :snare_electro, amp: 1.5, cutoff: 110
  sleep 1 # wait for beat 3
  sleep 2 # finish the 4-beat bar
end

# High Hats for the Fast Pace
live_loop :hats do
  sync :metronome
  sample :elec_tick, amp: 0.5
  sleep 0.25
end

# Bouncy Bassline
live_loop :bass do
  sync :metronome
  use_synth :chipbass
  play :E2, release: 0.2, amp: 0.8
  sleep 0.5
  play :E2, release: 0.2, amp: 0.8
  sleep 0.5
end
