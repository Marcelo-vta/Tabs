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

def play(song, timeBetweeenTabs=.2):
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
                time.sleep(.07)
                pass
            else:
                sound.play()
                time.sleep(.07)
        time.sleep(timeBetweeenTabs)


    pygame.time.delay(1100)
    pygame.mixer.quit()
        
                


    # som = gerar_tom_guitarra(82.41, 1000)
    # som2 = gerar_tom_guitarra(110.00, 1000)
    # som3 = gerar_tom_guitarra(146.83, 1000)
    # som4 = gerar_tom_guitarra(196.00, 1000)
    # som5 = gerar_tom_guitarra(246.94, 1000)
    # som6 = gerar_tom_guitarra(329.63, 1000)

    # som7 = gerar_tom_guitarra(calculate_fretted_frequency(329.63, 1), 1000)

    # som6.play()
    # time.sleep(1)
    # som7.play()
    # som2.play()
    # time.sleep(0.05)
    # som3.play()
    # time.sleep(0.05)
    # som4.play()
    # time.sleep(0.05)
    # som5.play()
    # time.sleep(0.05)
    # som6.play()

# play([[1,3,3,"X","X","X"],[3,5,5,"X","X","X"],[5,7,7,"X","X","X"],["X","X","X","X","X","X"],[3,3,3,"X","X","X"], [3,3,3,"X","X","X"], [3,3,3,"X","X","X"], [3,3,3,"X","X","X"]])
# play([[1,3,3,"X","X","X"]])

