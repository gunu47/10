import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="달콤살벌 연애상담소", page_icon="💖", layout="centered")
st.title("💖 달콤살벌 연애상담소")
st.caption("연애 고민, 썸, 이별... 혼자 앓지 말고 Gemini에게 물어보세요!")

# 2. Streamlit Secrets에서 API 키 불러오기 및 클라이언트 초기화
try:
    # Streamlit Secrets에 등록된 키를 가져옵니다.
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except KeyError:
    st.error("오류: Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. 설정 후 다시 시도해주세요.")
    st.stop()
except Exception as e:
    st.error(f"클라이언트 초기화 중 알 수 없는 오류가 발생했습니다: {e}")
    st.stop()

# 3. 세션 상태(Session State)로 채팅 기록 유지 및 대화 시작
if "messages" not in st.session_state:
    st.session_state.messages = []
    
# 페르소나 부여 (연애 상담가 설정)
system_instruction = (
    "당신은 공감 능력이 뛰어나고 때로는 뼈를 때리는 현실적인 조언을 해주는 전문 연애 상담가입니다. "
    "사용자의 연애 고민(썸, 이별, 짝사랑, 갈등 등)을 다정하고 친근한 어조로 들어주고, "
    "상황을 분석하여 실질적인 해결책을 제시해주세요. 이모지를 적절히 섞어 따뜻한 분위기를 만들어주세요."
)

# 4. 이전 채팅 기록 화면에 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력 받기
if user_input := st.chat_input("고민을 이야기해주세요... (예: 썸남이 선톡을 안 해요)"):
    
    # 사용자 메시지 화면에 표시 및 세션에 저장
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 6. Gemini API 호출 및 답변 생성 (오류 처리 포함)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🤔 고민을 분석 중이에요...")
        
        try:
            # 대화 맥락을 API에 전달하기 위해 대화 기록 포맷팅
            contents = []
            for msg in st.session_state.messages:
                role = "user" if msg["role"] == "user" else "model"
                contents.append(types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg["content"])]
                ))
            
            # gemini-2.5-flash-lite 모델 호출
            response = client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7, # 창의적이고 공감대 높은 답변을 위한 설정
                )
            )
            
            # 답변 출력 및 세션 저장
            ai_response = response.text
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except APIError as ae:
            # Gemini API 관련 오류 처리
            error_msg = f"❌ Gemini API 오류가 발생했습니다: {ae.message}"
            message_placeholder.markdown(error_msg)
        except Exception as e:
            # 기타 알 수 없는 오류 처리
            error_msg = f"❌ 예상치 못한 오류가 발생했습니다: {str(e)}"
            message_placeholder.markdown(error_msg)
