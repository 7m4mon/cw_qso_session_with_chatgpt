
# 生成AIを相手にしてCWの交信練習をしてみよう！
# 2024.8 7M4MON
# Description:
# Clientに初期プロンプトで交信の条件などを設定したら、入力待ち状態になります。
# ターミナルでCQをこちらから出すと、生成AIが適当なコールサインで応答してきます。
# 応答された文字列からモールス信号の wav ファイルを作成して再生しますので、音響受信を行います。文字列はターミナル上に表示されますので、ミスコピーしても大丈夫です。
# AIが応答したコールサインに対して通常のQSOを進めていきます。つまり、RSTレポート、名前、QTHの交換などです。
# 交信を進めて送るものがなくなったらファイナルを送ります。
# 最後は「CL」という文字列でセッションを終了します。


import os
from openai import OpenAI
from generate_morse_code_wav import generate_morse_code_audio
from pydub import AudioSegment
from pydub.playback import play

# 環境変数からAPIキーを読み込む
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is None:
    raise ValueError("OpenAI APIキーが設定されていません。環境変数 'OPENAI_API_KEY' を設定してください。")

client = OpenAI(api_key = os.environ['OPENAI_API_KEY'])

def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are participating in an amateur radio Morse code QSO session."},
                  {"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content

# 初期プロンプト
initial_prompt = """
Let's start an amateur radio typical CW QSO session!
I will send the CQ call, reply with your callsign (only "my callsign + 'DE' + your callsign").
After I callback your callsign, let's exchange a signal report, name, QTH, etc...
Use of common CW abbreviations in session.
The following notations are used for codes sent without pauses: 'BT' for '=', 'AR' for '+', 'KN' for '(', 'SK' for '~'.
Receiver's callsign is placed before 'DE', and after "DE" is the callsign of the sender. 
"""

# ユーザーの入力
chat_log = initial_prompt

while True:
    user_message = input("I: ")
    chat_log += f"\nI: {user_message}"
    
    if user_message.strip().upper() == "CL":
        print("END QSO SESSIONs")
        break
    
    response = chat_with_gpt(chat_log)
    print(f"ChatGPT: {response}")
    chat_log += f"\nChatGPT: {response}"

    # Morseコードのオーディオファイルを生成
    output_filename = "morse_code.wav"
    generate_morse_code_audio(response, output_filename, dot_duration=0.07, tone_freq = 700)

    # 生成したWAVファイルを再生 FFmpeg が必要
    audio = AudioSegment.from_wav(output_filename)
    play(audio)