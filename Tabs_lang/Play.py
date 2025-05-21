import pygame
import numpy as np
import time

def calculate_fretted_frequency(base_frequency, fret_number):
    # semitone_ratio = 2**(1/12)
    return base_frequency * (2**(fret_number / 12))


def gerar_tom_guitarra(freq, duracao_ms, volume=0.5, sample_rate=44100):
    duracao = duracao_ms / 1000
    t = np.linspace(0, duracao, int(sample_rate * duracao), endpoint=False)

    attack = 0.01  # seconds
    decay = duracao - attack
    envelope = np.concatenate([
        np.linspace(0, 1, int(sample_rate * attack)),          # Attack
        np.exp(-4 * np.linspace(0, decay, int(sample_rate * decay)))  # Decay
    ])

    wave = (
        np.sin(2 * np.pi * freq * t) +                
        0.5 * np.sin(2 * np.pi * freq * 2 * t) +      
        0.3 * np.sin(2 * np.pi * freq * 3 * t)        
    )

    wave *= envelope * volume
    wave = np.int16(wave / np.max(np.abs(wave)) * 32767)

    wave_stereo = np.column_stack((wave, wave))
    return pygame.sndarray.make_sound(wave_stereo)

def play(song, timeBetweeenTabs=0.01):
    std_tune = [82.41, 110.00, 146.83, 196.00, 246.94, 329.63]
    pygame.mixer.init(frequency=44100, size=-16, channels=2)

    for tab in song:

        sounds = []
        for i, note in enumerate(tab):
            if note.isnumeric():
                note_frequency = calculate_fretted_frequency(std_tune[i], int(note))
                sounds.append(gerar_tom_guitarra(note_frequency, 1000))
            else:        
                sounds.append("X")
        
        for sound in sounds:
            if sound == "X":
                time.sleep(.05)
                pass
            else:
                sound.play()
                time.sleep(0.07)
        time.sleep(timeBetweeenTabs)


    pygame.time.delay(1100)
    pygame.mixer.quit()
