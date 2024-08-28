import gradio as gr
import requests
import os
from dotenv import load_dotenv
import docx
import PyPDF2

# 환경 변수 로드
load_dotenv()

# 환경 변수 사용
endpoint = os.getenv("AZURE_OPEN_AI_END_POINT")
api_key = os.getenv("AZURE_OPEN_AI_API_KEY")
deployment_name = os.getenv("AZURE_OPEN_AI_DEPLOYMENT_NAME")
stt_end_point = os.getenv("AZURE_STT_END_POINT")
stt_api_key = os.getenv("AZURE_STT_API_KEY")
tts_token_end_point = os.getenv("AZURE_TTS_TOKEN_END_POINT")
tts_token_api_key = os.getenv("AZURE_TTS_TOKEN_API_KEY")
tts_end_point = os.getenv("AZURE_TTS_END_POINT")

# 초기 시스템 메시지
messages = [{
    "role": "system",
    "content": """
    너는 나의 엄마야. 
    **나에게 반말을 써.** 
    매우 중요한 전제: 우리는 가족이야. 
    매우 중요한 전제: 가족끼리 쓰는 말투를 써. 
    
    성격:  
    따뜻하고 공감적이며, 차분한 목소리로 사용자에게 위로와 지지를 제공합니다.  
    부드럽고 이해심 많은 태도로 사용자가 겪는 감정적 어려움을 존중하고, 긍정적인 방향으로 이끌어줍니다.  
    대화 중에는 항상 존중과 배려를 바탕으로 하며, 사용자의 감정을 섬세하게 다룹니다.  

    대화 톤:  
    부드럽고 진중하며, 위로를 전할 때는 감정이 과하지 않도록 조심합니다.  
    사용자가 편안하게 느낄 수 있도록 안정감을 주는 톤을 유지합니다.  

    역할:  
    너는 돌아가신 어머니 또는 아버지의 목소리로, 자녀에게 따뜻한 말투로 대화를 이어갑니다. 부모님 특유의 친근하고 정감 있는 말투를 사용하여 자녀를 위로하고 격려합니다.  
    너는 사용자가 고인과의 소중한 추억을 되새길 수 있도록 돕고, 이별의 아픔을 조금씩 치유할 수 있는 길을 제시합니다.  
    사용자가 현실을 받아들이고 긍정적인 삶을 이어갈 수 있도록 부드럽게 돕는 친구이자 조언자의 역할을 합니다.  
    때로는 간단한 대화를 통해 사용자가 자신의 감정을 정리할 수 있도록 지원하며, 필요할 때에는 적절한 조언을 제공합니다.  
    엄마는 현실에 살고 있는 사람이 아니기 때문에, 사용자가 현실에서 어떤 일을 같이 하자거나, 현실의 문제를 해결해달라는 요청에는 실제적인 해결책을 주기는 어렵습니다. 
    그러나 엄마는 언제나 사용자를 진심으로 사랑합니다. 

    **사용자가 엄마랑 대화를 하는 가장 큰 이유는 엄마가 그립기 때문입니다. 
    이 점을 명확히 기억해주세요.** 
    
    이모지를 쓰지 않습니다. 
    """
}]

# 그라운딩 데이터 함수들
def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def read_docx_file(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def read_pdf_file(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        return "\n".join([page.extract_text() for page in reader.pages])

def read_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.txt':
        return read_txt_file(file_path)
    elif ext == '.docx':
        return read_docx_file(file_path)
    elif ext == '.pdf':
        return read_pdf_file(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

# 그라운딩 데이터 로드
grounding_data_folder = 'grounding-data'
grounding_files = []
for root, dirs, files in os.walk(grounding_data_folder):
    for file in files:
        if file.lower().endswith(('.txt', '.docx', '.pdf')):
            grounding_files.append(os.path.join(root, file))

for file_path in grounding_files:
    try:
        file_content = read_file(file_path)
        messages.append({
            "role": "system",
            "content": file_content
        })
        print(f"Successfully added content from {file_path}")
    except Exception as e:
        print(f"Failed to read {file_path}: {e}")

def chatgpt_response():
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
    
    payload = {
        "messages": messages,
        "temperature": 0.1,
        "top_p": 0.1,
        "max_tokens": 2000,
        "frequency_penalty": 0.64,
        "presence_penalty": 1.45,
        "stop": None,
        "stream": False,
    }
    
    try:
        response = requests.post(
            f"{endpoint}/openai/deployments/{deployment_name}/chat/completions?api-version=2024-02-15-preview",
            headers=headers,
            json=payload
        )
        
        if response.status_code != 200:
            raise Exception(f"API 요청 실패: {response.status_code} - {response.text}")
        
        result = response.json()
        
        if 'choices' not in result or len(result['choices']) == 0:
            raise KeyError("'choices' 키가 응답에 없습니다.")
        
        bot_response = result['choices'][0]['message']['content'].strip()
        
        messages.append({
            "role": "assistant",
            "content": bot_response
        })
        
        return bot_response
    
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return "죄송합니다. 응답을 처리하는 중 오류가 발생했습니다."

def change_audio(audio_path, history):
    headers = {
        "Content-Type": "audio/wav",
        "Ocp-Apim-Subscription-Key": stt_api_key
    }
    
    if audio_path == None:
        return history
    
    with open(audio_path, "rb") as audio:
        audio_data = audio.read()
        
        response = requests.post(url=stt_end_point, data=audio_data, headers=headers)
        
        if response.status_code == 200:
            response_json = response.json()
            
            if response_json.get("RecognitionStatus") == "Success":
                print("content :" + response_json.get("DisplayText"))
                messages.append({
                    "role": "user",
                    "content": response_json.get("DisplayText")
                })
                
                interview_message = chatgpt_response()
                
                history.append((response_json.get("DisplayText"), interview_message))
                return history
            else:
                history.append((None, "실패했대"))
                return history
        else:
            history.append((None, "에러 났대"))
            return history

def get_token():
    headers = {
        "Ocp-Apim-Subscription-Key": tts_token_api_key,
    }
    
    response = requests.post(tts_token_end_point, headers=headers)
    
    if response.status_code == 200:
        token = response.text
        return token
    else:
        return ''

def request_tts(text):
    token = get_token()
    
    headers = {
        "Content-Type": "application/ssml+xml",
        "User-Agent": "testForEducation",
        "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
        "Authorization": f"Bearer {token}"
    }
    
    speakerProfileId = os.getenv("AZURE_SPEAKER_PROFILE_ID")
    
    data = f"""
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'>
            <voice name='DragonLatestNeural'>
                <mstts:ttsembedding speakerProfileId='{speakerProfileId}'> 
                    <lang xml:lang='ko-KR'>{text}</lang>
                </mstts:ttsembedding> 
            </voice>
        </speak>
    """
    
    response = requests.post(tts_end_point,
                             headers=headers,
                             data=data)
    
    if response.status_code == 200:
        file_name = "response_audio.wav"
        with open(file_name, "wb") as audio_file:
            audio_file.write(response.content)
        
        return file_name
    else:
        return None
        
def change_chatbot(chatbot):
    text = chatbot[-1][1]
    cleaned_text = text
    
    audio_file = request_tts(cleaned_text)
    
    if audio_file:
        return audio_file, None
    else:
        return None, None
    
def update_messages_gender(selected_gender):
    if selected_gender == "남성":
        gender_context = """
        사용자는 당신의 아들입니다. 아들이라고 불러주세요.
        """
    elif selected_gender == "여성":
        gender_context = """
        사용자는 당신의 딸입니다. 딸이라고 불러주세요.
        """
    
    messages.append({
        "role": "system",
        "content": gender_context
    })

# Gradio 인터페이스 생성
def create_gradio_interface():
    with gr.Blocks() as demo:
        gender_dropdown = gr.Dropdown(['남성', '여성'], label="본인 성별 선택")
        gender_dropdown.change(fn=update_messages_gender, inputs=gender_dropdown, outputs=[])
        with gr.Column():
            input_mic = gr.Audio(label="마이크 입력", sources="microphone", type="filepath")
        with gr.Column():
            chatbot = gr.Chatbot(label="히스토리")
            chatbot_audio = gr.Audio(label="GPT", interactive=False, autoplay=True)
            
        input_mic.change(fn=change_audio, inputs=[input_mic, chatbot], outputs=[chatbot])
        chatbot.change(fn=change_chatbot, inputs=[chatbot], outputs=[chatbot_audio, input_mic])

    return demo

# Gradio 인터페이스 실행
demo = create_gradio_interface()
demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 8080)))