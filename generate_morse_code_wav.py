# 欧文の文字列を受け取ってモールス信号のwavファイルを生成するプログラム
# 2024.8 7M4MOON
# How to use: Put this file in the same folder...
# from generate_morse_code_wav import generate_morse_code_audio
# generate_morse_code_audio("cq de 7m4mon pse k", output_filename, dot_duration=0.08, tone_freq = 700)

# モールス信号の辞書
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--',
    '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...',     # KN = '('
    ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-',
    '"': '.-..-.', '$': '...-..-', '@': '.--.-.', 
    '=': '-...-', '~': '.-.-.', '^': '...-.-',  # BT, AR, VA
}

def text_to_morse(text):
    morse_code = []
    for char in text.upper():
        if char in MORSE_CODE_DICT:
            morse_code.append(MORSE_CODE_DICT[char])
        elif char == ' ':
            morse_code.append('|')
    return ' '.join(morse_code)

# Morse code audio generation function
def generate_morse_code_audio(text, output_filename, dot_duration=0.1, tone_freq = 800):
    import numpy as np
    from scipy.io.wavfile import write
    
    SAMPLE_RATE = 8000
    FREQ = tone_freq

    morse_code = text_to_morse(text)
    print(morse_code)

    DOT_DURATION = dot_duration   # ドットの長さ（秒）
    DASH_DURATION = DOT_DURATION * 3  # ダッシュの長さ（秒）
    SYMBOL_SPACE_DURATION = DOT_DURATION
    LETTER_SPACE_DURATION = DOT_DURATION * 3
    WORD_SPACE_DURATION = DOT_DURATION * (7-3-3)  # 前後に ' ' が付くので。

    def generate_tone(duration):
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        return np.sin(2 * np.pi * FREQ * t) * 0.5

    def generate_silence(duration):
        return np.zeros(int(SAMPLE_RATE * duration))
    
    audio_sequence = []
    
    for symbol in morse_code:
        if symbol == '.':
            audio_sequence.append(generate_tone(DOT_DURATION))
            audio_sequence.append(generate_silence(SYMBOL_SPACE_DURATION))
        elif symbol == '-':
            audio_sequence.append(generate_tone(DASH_DURATION))
            audio_sequence.append(generate_silence(SYMBOL_SPACE_DURATION))
        elif symbol == ' ':
            audio_sequence.append(generate_silence(LETTER_SPACE_DURATION))
        elif symbol == '|':
            audio_sequence.append(generate_silence(WORD_SPACE_DURATION))

    audio_sequence = np.concatenate(audio_sequence)
    audio_sequence = np.int16(audio_sequence / np.max(np.abs(audio_sequence)) * 32767)

    write(output_filename, SAMPLE_RATE, audio_sequence)

    print("WAVファイルが生成されました: " + output_filename)
    return output_filename


def test_to_morse_wav_test():
    generate_morse_code_audio("TEST","test.wav", dot_duration=0.1)

# test_to_morse_wav_test()