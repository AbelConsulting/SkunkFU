"""
Generate placeholder background music using simple synthesis
"""
import pygame
import numpy as np
import os
from scipy.io import wavfile

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

def generate_note(frequency, duration, sample_rate=22050, volume=0.15):
    """Generate a musical note with harmonics"""
    num_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, num_samples, False)
    
    # Fundamental frequency
    wave = np.sin(frequency * 2 * np.pi * t) * volume
    
    # Add harmonics for richer sound
    wave += np.sin(frequency * 2 * 2 * np.pi * t) * (volume * 0.5)
    wave += np.sin(frequency * 3 * 2 * np.pi * t) * (volume * 0.3)
    
    # Apply ADSR envelope
    attack_samples = int(0.05 * sample_rate)
    decay_samples = int(0.1 * sample_rate)
    release_samples = int(0.1 * sample_rate)
    
    envelope = np.ones(num_samples)
    
    # Attack
    if num_samples > attack_samples:
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    
    # Decay
    if num_samples > attack_samples + decay_samples:
        envelope[attack_samples:attack_samples + decay_samples] = np.linspace(1, 0.7, decay_samples)
    
    # Release
    if num_samples > release_samples:
        envelope[-release_samples:] = np.linspace(0.7, 0, release_samples)
    
    wave = wave * envelope
    return wave

def create_beat(bpm=120, beats=4, sample_rate=22050):
    """Create a simple drum beat"""
    beat_duration = 60.0 / bpm
    total_duration = beat_duration * beats
    num_samples = int(total_duration * sample_rate)
    
    beat = np.zeros(num_samples)
    
    for i in range(beats):
        # Kick drum on each beat
        kick_start = int(i * beat_duration * sample_rate)
        kick_duration = 0.1
        kick_samples = int(kick_duration * sample_rate)
        
        if kick_start + kick_samples < num_samples:
            # Low frequency sweep for kick
            t = np.linspace(0, kick_duration, kick_samples, False)
            freq = np.linspace(150, 40, kick_samples)
            phase = 2 * np.pi * np.cumsum(freq) / sample_rate
            kick = np.sin(phase) * 0.3
            
            # Envelope
            env = np.exp(-t * 20)
            kick = kick * env
            
            beat[kick_start:kick_start + kick_samples] += kick
        
        # Hi-hat on off-beats
        if i % 2 == 1:
            hat_start = kick_start
            hat_duration = 0.05
            hat_samples = int(hat_duration * sample_rate)
            
            if hat_start + hat_samples < num_samples:
                # High frequency noise for hi-hat
                hat = np.random.uniform(-1, 1, hat_samples) * 0.08
                env = np.exp(-np.linspace(0, hat_duration, hat_samples) * 30)
                hat = hat * env
                
                beat[hat_start:hat_start + hat_samples] += hat
    
    return beat

def create_gameplay_music(duration=60, bpm=140):
    """Create energetic gameplay music"""
    sample_rate = 22050
    
    # Chord progression: Am - F - C - G (in relative minor - A minor)
    # Notes in A minor scale: A B C D E F G
    notes = {
        'A3': 220.00,
        'B3': 246.94,
        'C4': 261.63,
        'D4': 293.66,
        'E4': 329.63,
        'F4': 349.23,
        'G4': 392.00,
        'A4': 440.00,
        'C5': 523.25,
        'E5': 659.25,
        'F5': 698.46,
        'G5': 783.99
    }
    
    beat_duration = 60.0 / bpm
    measure_duration = beat_duration * 4
    
    num_measures = int(duration / measure_duration)
    total_samples = int(duration * sample_rate)
    
    music = np.zeros(total_samples)
    
    # Chord progression pattern
    progression = [
        ['A3', 'C4', 'E4'],  # Am
        ['F3', 'A3', 'C4'],  # F
        ['C3', 'E4', 'G4'],  # C
        ['G3', 'B3', 'D4']   # G
    ]
    
    # Melody pattern (simple ascending/descending)
    melody_patterns = [
        ['A4', 'C5', 'E5', 'C5'],
        ['F4', 'A4', 'C5', 'A4'],
        ['E4', 'G4', 'C5', 'G4'],
        ['D4', 'G4', 'B3', 'G4']
    ]
    
    for measure in range(num_measures):
        chord_idx = measure % 4
        measure_start = int(measure * measure_duration * sample_rate)
        
        # Add bass notes (whole notes)
        if chord_idx < len(progression):
            bass_note = notes.get(progression[chord_idx][0], 220)
            bass = generate_note(bass_note * 0.5, measure_duration, sample_rate, volume=0.2)
            
            end_idx = min(measure_start + len(bass), total_samples)
            music[measure_start:end_idx] += bass[:end_idx - measure_start]
        
        # Add melody (quarter notes)
        if chord_idx < len(melody_patterns):
            for beat in range(4):
                note_start = measure_start + int(beat * beat_duration * sample_rate)
                note_name = melody_patterns[chord_idx][beat % len(melody_patterns[chord_idx])]
                melody_freq = notes.get(note_name, 440)
                note = generate_note(melody_freq, beat_duration * 0.9, sample_rate, volume=0.15)
                
                end_idx = min(note_start + len(note), total_samples)
                if note_start < total_samples:
                    music[note_start:end_idx] += note[:end_idx - note_start]
    
    # Add drums
    num_beats = int(duration / beat_duration)
    drums = create_beat(bpm, num_beats, sample_rate)
    
    # Ensure same length
    min_length = min(len(music), len(drums))
    music = music[:min_length]
    drums = drums[:min_length]
    
    # Mix
    final = music + drums
    
    # Normalize
    max_val = np.max(np.abs(final))
    if max_val > 0:
        final = final / max_val * 0.7
    
    return final, sample_rate

def save_music_as_ogg(wave, sample_rate, filename):
    """Save wave as OGG file (via WAV then conversion)"""
    # First save as WAV
    filepath = os.path.join('assets', 'audio', 'music', filename.replace('.ogg', '.wav'))
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Convert to stereo
    stereo_wave = np.column_stack((wave, wave))
    stereo_wave = (stereo_wave * 32767).astype(np.int16)
    
    wavfile.write(filepath, sample_rate, stereo_wave)
    
    print(f"✓ Generated: {filename} (saved as WAV)")
    print(f"  Note: For OGG format, you can use ffmpeg to convert:")
    print(f"  ffmpeg -i {filepath} {filepath.replace('.wav', '.ogg')}")

def create_all_music():
    """Generate all music tracks"""
    print("🎵 Generating placeholder background music...\n")
    
    # Gameplay music - fast and energetic
    print("Creating gameplay music...")
    gameplay, sr = create_gameplay_music(duration=60, bpm=140)
    save_music_as_ogg(gameplay, sr, 'gameplay.ogg')
    
    print("\n✅ Music generated successfully!")
    print(f"📁 Saved to: assets/audio/music/")
    print("\n💡 Tip: These are placeholder tracks. For better quality:")
    print("   1. Use a DAW (FL Studio, Ableton, LMMS)")
    print("   2. Or use royalty-free music from:")
    print("      - OpenGameArt.org")
    print("      - Incompetech.com")
    print("      - Freesound.org")

if __name__ == "__main__":
    create_all_music()
