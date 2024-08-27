# 음성 상호작용 프로젝트

이 프로젝트는 Azure의 AI 서비스를 활용하여 사용자와 AI 사이의 음성 대화를 구현한 대화형 애플리케이션입니다. 특히, 사용자의 음성을 텍스트로 변환하고, AI의 응답을 생성한 후, 이를 다시 음성으로 변환하여 출력하는 기능을 포함합니다.

## 주요 기능

1. 음성-텍스트 변환 (STT)
2. AI 대화 생성 (Azure OpenAI)
3. 텍스트-음성 변환 (TTS)
4. 개인화된 AI 음성 생성

## 설치 방법

1. 필요한 패키지 설치:
   ```
   pip install gradio python-dotenv requests pydub
   ```

2. `.env` 파일을 생성하고 다음 환경 변수를 설정:
   - AZURE_OPEN_AI_END_POINT
   - AZURE_OPEN_AI_API_KEY
   - AZURE_OPEN_AI_DEPLOYMENT_NAME
   - AZURE_STT_END_POINT
   - AZURE_STT_API_KEY
   - AZURE_TTS_TOKEN_END_POINT
   - AZURE_TTS_TOKEN_API_KEY
   - AZURE_TTS_END_POINT
   - AZURE_SPEAKER_PROFILE_ID
   - AZURE_PERSONAL_VOICE_END_POINT
   - AZURE_PERSONAL_VOICE_RESOURCE_KEY

## 사용 방법

1. Jupyter Notebook을 실행하고 `main.ipynb` 파일을 열어 각 셀을 순서대로 실행합니다.

2. Gradio 인터페이스가 실행되면, 사용자의 성별을 선택하고 마이크를 통해 음성 입력을 제공합니다.

3. AI의 응답이 텍스트로 표시되고, 음성으로 재생됩니다.

## 개인화된 AI 음성 생성

1. `voices/m4a` 폴더에 `.m4a` 형식의 음성 파일을 준비합니다.

2. 변환 스크립트를 실행하여 `.m4a` 파일을 `.mp3` 형식으로 변환합니다.

3. Azure Personal Voice 서비스를 이용해 개인화된 AI 음성을 생성합니다:
   - 프로젝트 생성
   - 콘센트 생성 (동의 음성 필요)
   - 개인화된 음성 모델 생성

## 주의사항

- 이 프로젝트는 Azure AI 서비스를 사용하므로, 관련 API 키와 엔드포인트가 필요합니다.
- 개인화된 음성 생성 시, 최소 256Kb 크기의 MP3 파일이 필요하며, 최대 20개까지 사용할 수 있습니다.
- 프라이버시 및 데이터 보호에 주의를 기울여야 합니다.

## 라이선스

이 프로젝트는 CC0 1.0 Universal (CC0 1.0) 라이선스 하에 배포됩니다. 자세한 내용은 프로젝트 루트 디렉토리의 [LICENSE](./LICENSE) 파일을 참조하세요.

## 기여

이 프로젝트에 기여하고 싶으시다면, 풀 리퀘스트를 보내주시기 바랍니다. 모든 기여는 환영합니다!

## 문의

질문이나 문제가 있으시면 이슈를 열어 문의해 주세요.