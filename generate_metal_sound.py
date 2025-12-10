"""
Generate a metal element to add to the background music
Creates a metallic synth pad/drone sound
"""
import numpy as np
import wave
import struct

def generate_metal_synth(duration=30, sample_rate=44100):
    """Generate a metallic synth sound
    
    Args:
        duration: Length in seconds
        sample_rate: Sample rate in Hz
    
    Returns:
        numpy array of audio samples
    """
    
    # Create time array
    t = np.linspace(0, duration, int(duration * sample_rate))
    
    # Base frequencies for metallic sound (minor pentatonic with octaves)
    # Tuned for a dark, industrial metal feel
    frequencies = [
        110,   # A2 - deep bass
        165,   # E3 - mid bass
        220,   # A3 - main note
        330,   # E4 - high note
        440,   # A4 - bright note
    ]
    
    # Generate harmonics with slight detuning for metallic effect
    audio = np.zeros_like(t)
    
    for i, freq in enumerate(frequencies):
        # Slightly detune each harmonic for more metallic texture
        detune = 1 + (i * 0.01)  # 1% detune per harmonic
        detune_freq = freq * detune
        
        # Use combination of sine and square waves for metallic timbre
        sine_component = np.sin(2 * np.pi * detune_freq * t) * 0.3
        
        # Add harmonics
        harmonic_freq = detune_freq * 2
        harmonic = np.sin(2 * np.pi * harmonic_freq * t) * 0.15
        
        # Combine with envelope (slower attack, long sustain)
        envelope = np.ones_like(t)
        attack_time = int(0.5 * sample_rate)
        release_time = int(2 * sample_rate)
        
        # Attack envelope
        envelope[:attack_time] = np.linspace(0, 1, attack_time)
        # Release at end
        envelope[-release_time:] = np.linspace(1, 0, release_time)
        
        audio += (sine_component + harmonic) * envelope * (1 / len(frequencies))
    
    # Add some modulation for interest
    lfo = np.sin(2 * np.pi * 0.3 * t) * 0.1 + 0.9  # 0.3 Hz LFO
    audio *= lfo
    
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
    print("🎸 Generating metal synth sound...")
    print("=" * 60)
    
    # Generate metal synth
    print("Generating metallic synth pad (30 seconds)...")
    metal_audio = generate_metal_synth(duration=30, sample_rate=44100)
    
    # Save as SFX file that can be layered with music
    output_path = "assets/audio/sfx/metal_pad.wav"
    save_wav(metal_audio, output_path, sample_rate=44100)
    print(f"✅ Saved: {output_path}")
    
    print("\n" + "=" * 60)
    print("✨ Metal element generated!")
    print("=" * 60)
    print("""
NEXT STEPS:
1. The metal synth has been saved as: assets/audio/sfx/metal_pad.wav

2. To use it as a background layer:
   - Open the audio_manager.py file
   - Modify play_music() to also play metal_pad.wav quietly in the background
   - Or use an audio editor to mix it with your existing music

3. To customize the metal sound:
   - Adjust frequencies array for different notes
   - Change duration parameter for longer/shorter loops
   - Modify the envelope attack/release times
   - Adjust the LFO rate and depth for different modulation

The generated sound is a metallic synth pad with:
- Deep bass and high notes for fullness
- Slight detuning for metallic texture
- LFO modulation for movement
- Smooth envelope for pad-like sustain
""")


if __name__ == "__main__":
    try:
        import numpy as np
    except ImportError:
        print("❌ NumPy not installed!")
        print("Run: pip install numpy")
        exit(1)
    
    main()
