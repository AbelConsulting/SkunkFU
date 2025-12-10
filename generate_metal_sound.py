"""
Generate a ninja-themed metal guitar riff to add to the background music
Creates slow, atmospheric power chords with Eastern-inspired melodies and distortion
"""
import numpy as np
import wave

def generate_metal_guitar(duration=30, sample_rate=44100):
    """Generate a ninja-themed metal guitar riff with atmospheric power chords
    
    Args:
        duration: Length in seconds
        sample_rate: Sample rate in Hz
    
    Returns:
        numpy array of audio samples
    """
    
    # Create time array
    t = np.linspace(0, duration, int(duration * sample_rate))
    
    # Ninja metal riff - slower BPM (95 instead of 120) with Eastern-inspired melody
    # Each tuple: (base_freq, duration_in_beats)
    # BPM = 95, so each beat = 0.631 seconds
    
    audio = np.zeros_like(t)
    
    # Define the ninja-themed metal guitar riff (slower, more atmospheric)
    # Using pentatonic/modal scales for Eastern feel with metal power chords
    riff_pattern = [
        (98, 1.0),    # B1 - quarter note (low, menacing)
        (147, 1.0),   # D3 (pentatonic - Eastern feel)
        (196, 0.5),   # G3 - power chord root
        (147, 0.5),   # D3 (minor sound)
        (98, 1.5),    # B1 - longer hold
        (165, 0.5),   # E3 (Eastern modal)
        (110, 0.5),   # A2 - power chord
        (165, 1.0),   # E3
        (98, 2.0),    # B1 - sustained (rest/hold)
    ]
    
    # Build the riff multiple times to fill the duration
    beat_duration = 0.631  # 95 BPM = 0.631 seconds per beat
    current_time = 0
    
    while current_time < duration:
        for base_freq, num_beats in riff_pattern:
            if current_time >= duration:
                break
            
            note_duration = num_beats * beat_duration
            start_sample = int(current_time * sample_rate)
            end_sample = int((current_time + note_duration) * sample_rate)
            
            if end_sample > len(t):
                end_sample = len(t)
            
            note_t = t[start_sample:end_sample]
            
            # Generate the note with distortion
            # Power chord: fundamental + harmonics (Eastern-influenced)
            fundamental = np.sin(2 * np.pi * base_freq * note_t) * 0.35
            
            # Add harmonics for fullness (reduced for more atmospheric feel)
            harmonic_2 = np.sin(2 * np.pi * base_freq * 2 * note_t) * 0.15
            harmonic_3 = np.sin(2 * np.pi * base_freq * 3 * note_t) * 0.08
            
            # Add subtle 7th for Eastern modal feel
            harmonic_7 = np.sin(2 * np.pi * base_freq * 1.875 * note_t) * 0.05
            
            # Combine
            note_signal = fundamental + harmonic_2 + harmonic_3 + harmonic_7
            
            # Apply distortion (lighter for ninja atmosphere)
            # Soft clipping for aggressive tone but more controlled
            distortion = np.tanh(note_signal * 2.5)  # Reduced distortion for elegance
            
            # Add envelope (slower attack for ninja atmosphere)
            envelope_samples = len(note_t)
            attack_samples = min(int(0.05 * sample_rate), envelope_samples // 3)  # Cap attack to 1/3 of note
            decay_start = attack_samples
            decay_samples = max(1, envelope_samples - decay_start)
            
            envelope = np.ones(envelope_samples)
            # Attack
            if attack_samples > 0 and envelope_samples > 0:
                envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
            # Decay (slower, more sustained)
            if decay_samples > 0:
                envelope[decay_start:] = np.linspace(1, 0.2, decay_samples)
            
            # Apply envelope
            note_with_envelope = distortion * envelope
            
            # Add to audio
            audio[start_sample:end_sample] = note_with_envelope * 0.7
            
            current_time += note_duration
    
    # Normalize to prevent clipping
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.8  # Leave some headroom
    
    return audio.astype(np.float32)


def save_wav(audio, filename, sample_rate=44100):
    """Save audio array as WAV file
    
    Args:
        audio: numpy array of audio samples (-1.0 to 1.0)
        filename: Output filename
        sample_rate: Sample rate in Hz
    """
    
    # Convert float samples to int16
    audio_int = np.int16(audio * 32767)
    
    with wave.open(filename, 'w') as wav_file:
        # Set parameters: 1 channel (mono), 2 bytes per sample, sample rate
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        # Write audio data
        wav_file.writeframes(audio_int.tobytes())


def main():
    print("🥷 Generating ninja-themed metal guitar riff...")
    print("=" * 60)
    
    # Generate metal guitar
    print("Generating ninja metal guitar riff (30 seconds)...")
    guitar_audio = generate_metal_guitar(duration=30, sample_rate=44100)
    
    # Save as SFX file that can be layered with music
    output_path = "assets/audio/sfx/metal_pad.wav"
    save_wav(guitar_audio, output_path, sample_rate=44100)
    print(f"✅ Saved: {output_path}")
    
    print("\n" + "=" * 60)
    print("✨ Ninja metal guitar generated!")
    print("=" * 60)
    print("""
FEATURES:
- Slower BPM (95 instead of 120) for atmospheric tension
- Eastern-inspired pentatonic/modal scales
- Power chords with reduced distortion for elegance
- Slower attack (50ms) for stealth vibe
- Harmonic 7th for mysterious tone
- Rich, sustained notes for ninja atmosphere

The ninja guitar now layers with your background music!
You'll hear it when you start gameplay.

To customize:
- Adjust 'riff_pattern' for different chord progressions
- Change distortion amount (multiply factor before tanh)
- Modify BPM by changing beat_duration (0.631 for 95 BPM)
- Add more Eastern scales for atmosphere
""")


if __name__ == "__main__":
    try:
        import numpy as np
    except ImportError:
        print("❌ NumPy not installed!")
        print("Run: pip install numpy")
        exit(1)
    
    main()
