# Balika & Sinawa EDM Concept
use_bpm 128

live_loop :metronome do
  sleep 1
end

# The "Sweet Acoustic" Synth Lead
live_loop :acoustic_synths do
  use_synth :pluck
  use_synth_defaults coef: 0.4, release: 0.1
  notes = (ring :E4, :G4, :A4, :E4, :G4, :B4)
  play notes.tick, amp: 1.2
  sleep 0.25
end

# The EDM Kick Drum
live_loop :kick do
  sample :bd_haus, amp: 2
  sleep 1
end

# High Hats for the Fast Pace
live_loop :hats do
  sample :elec_tick, amp: 0.5
  sleep 0.25
end

# Bouncy Bassline
live_loop :bass do
  use_synth :chipbass
  play :E2, release: 0.2, amp: 0.8
  sleep 0.5
  play :E2, release: 0.2, amp: 0.8
  sleep 0.5
end
