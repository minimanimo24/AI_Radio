import time, os, sys
import speech_recognition as sr
import speech_recognition
import urllib.request
import content
from playsound import playsound
from openai import OpenAI
from gpiozero import Button
from signal import pause
#네이버 api key
client_id = "[Clovar API]"
client_secret = "[Clovar API]"
#open api key
open_api_key = "[Chat-GPT API]"
# 터미널 오류 출력 설절 부분
denvnull = os.open(os.devnull, os.O_WRONLY)
old_stderr = os.dup(2)
sys.stderr.flush()
os.dup2(denvnull, 2)
os.close(denvnull)
#임베디드 부분 코드
button = Button(2)

result = ""
aiVoice = ""
switch = True
error_switch = False

def GPT_A(text) -> str:
    """
    인공지능 A버전
    """
    client = OpenAI(
        api_key=open_api_key,
    )
    query = text

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": content.text_A},
            {"role": "user",
             "content": query}
        ]
    )
    return completion.choices[0].message.content

def GPT_B(text) -> str:
    """
    인공지능 B버전
    """
    client = OpenAI(
        api_key=open_api_key,
    )
    query = text

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": content.text_B},
            {"role": "user",
             "content": query}
        ]
    )
    return completion.choices[0].message.content

def answer_AI(input_text):
    """
    AI 대답 스피커 출력
    """
    global result
    global switch
    global aiVoice

    if switch == True:
        result = GPT_B(input_text)
        switch = False
        aiVoice = "ndain"
    else:
        result = GPT_A(input_text)
        switch = True
        aiVoice = "nmeow"
    speak(result)
    # print(result)

def speak(text):
    """
    네이버 클로바 API 연동하여 TTS 생성 함수
    """
    global aiVoice
    print('[인공지능] : ' + text)
    file_name = "voice.mp3"
    encText = urllib.parse.quote(text)
    data = "speaker=" + aiVoice + "&volume=0&speed=0&pitch=0&format=mp3&text=" + encText;
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
    request.add_header("X-NCP-APIGW-API-KEY", client_secret)
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()

    if (rescode == 200):
        response_body = response.read()
        with open('voice.mp3', 'wb') as f:
            f.write(response_body)
    else:
        print("Error Code:" + rescode)
    os.system("mpg123 " + file_name)

    if os.path.exists(file_name):
        os.remove(file_name)
    # os.system("mpg123 " + file_name)  # 리눅스 환경에서 파일 실행
def set_result():
    global result
    result = "새로운 주제로 대화"

def listen_STT():
    """
    마이크로 음성인식
    """
    global result
    global error_switch
    print('음성인식 중...')
    with m as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 1
        audio = r.listen(source, None, 20)
    try:
        result = r.recognize_google(audio, language="ko-KR")
        print("[사용자] : " + result)
    except speech_recognition.UnknownValueError:
        print("음성 인식 실패")
        set_result()
        error_switch = True
        pass
    except speech_recognition.RequestError:
        print("HTTP Request Error 발생")

r = sr.Recognizer()
m = sr.Microphone()
# playsound("main_test.mp3")
print('음성인식 중...')
while True:
    if button.is_pressed():
        listen_STT()
        if error_switch == True:
            for i in range(2):
                for k in range(7):
                    answer_AI(result)
                error_switch = False
                set_result()
                os.system("mpg123 " + "YesYes.mp3")
        else:
            for i in range(2):
                for k in range(7):
                    answer_AI(result)
                set_result()
                os.system("mpg123 " + "YesYes.mp3")

# button.when_pressed = listen_STT()  # 버튼이 눌렸을 때 실행될 콜백함수 지정
# button.when_released = say_goodbye  # 버튼이 눌렸다가 놓아졌을 때 실행될 콜백함수 지정

pause()