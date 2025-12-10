"""
Generate a metal guitar riff to add to the background music
Creates distorted power chord stabs with aggressive tone
"""
import numpy as np
import wave

def generate_metal_guitar(duration=30, sample_rate=44100):
    """Generate a metal guitar riff with power chords
    
    Args:
        duration: Length in seconds
        sample_rate: Sample rate in Hz
    
    Returns:
        numpy array of audio samples
    """
    
    # Create time array
    t = np.linspace(0, duration, int(duration * sample_rate))
    
    # Metal guitar riff pattern - power chords with rhythm
    # Each tuple: (base_freq, duration_in_beats)
    # BPM = 120, so each beat = 0.5 seconds
    
    audio = np.zeros_like(t)
    
    # Define the metal guitar riff (repeating pattern)
    riff_pattern = [
        (110, 0.5),   # E2 - quarter note
        (110, 0.5),   # E2
        (165, 0.5),   # E3 (octave up)
        (220, 0.5),   # A3 (power chord)
        (165, 0.25),  # E3 - eighth note
        (110, 0.25),  # E2
        (220, 0.5),   # A3
        (165, 0.5),   # E3
        (110, 1.0),   # E2 - half note (rest)
    ]
    
    # Build the riff multiple times to fill the duration
    beat_duration = 0.5  # 120 BPM = 0.5 seconds per beat
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
            # Power chord: fundamental + harmonics
            fundamental = np.sin(2 * np.pi * base_freq * note_t) * 0.4
            
            # Add harmonics for fullness
            harmonic_2 = np.sin(2 * np.pi * base_freq * 2 * note_t) * 0.2
            harmonic_3 = np.sin(2 * np.pi * base_freq * 3 * note_t) * 0.1
            
            # Combine
            note_signal = fundamental + harmonic_2 + harmonic_3
            
            # Apply distortion (guitar amp overdrive)
            # Soft clipping for aggressive tone
            distortion = np.tanh(note_signal * 3.5)  # Increase for more distortion
            
            # Add envelope (percussive attack, gradual decay)
            envelope_samples = len(note_t)
            attack_samples = int(0.01 * sample_rate)  # 10ms sharp attack
            decay_samples = max(1, envelope_samples - attack_samples)
            
            envelope = np.ones(envelope_samples)
            # Attack
            if attack_samples > 0:
                envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
            # Decay
            envelope[attack_samples:] = np.linspace(1, 0.3, decay_samples)
            
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
    print("🎸 Generating metal guitar riff...")
    print("=" * 60)
    
    # Generate metal guitar
    print("Generating metal guitar riff (30 seconds)...")
    guitar_audio = generate_metal_guitar(duration=30, sample_rate=44100)
    
    # Save as SFX file that can be layered with music
    output_path = "assets/audio/sfx/metal_pad.wav"
    save_wav(guitar_audio, output_path, sample_rate=44100)
    print(f"✅ Saved: {output_path}")
    
    print("\n" + "=" * 60)
    print("✨ Metal guitar generated!")
    print("=" * 60)
    print("""
FEATURES:
- Aggressive power chord riff
- Heavy distortion with soft clipping
- Sharp attack for percussive guitar tone
- Repeating pattern synced to 120 BPM
- Rich harmonics for thickness

The metal guitar now layers with your background music!
You'll hear it when you start gameplay.

To customize:
- Adjust 'riff_pattern' for different chord progressions
- Change distortion amount (multiply factor before tanh)
- Modify BPM by changing beat_duration (0.5 for 120 BPM)
- Add more frequencies for different power chords
""")


if __name__ == "__main__":
    try:
        import numpy as np
    except ImportError:
        print("❌ NumPy not installed!")
        print("Run: pip install numpy")
        exit(1)
    
    main()
