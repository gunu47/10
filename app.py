# app.py

import streamlit as st

st.set_page_config(
    page_title="고민 상담 앱",
    page_icon="💬",
    layout="centered"
)

st.title("💬 고민 상담 앱")
st.write("편하게 고민을 입력해보세요.")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
user_input = st.chat_input("고민을 입력하세요")

# 간단한 상담 응답 함수
def 상담응답(text):
    text = text.lower()

    if "힘들" in text or "지쳐" in text:
        return "많이 힘들었겠어요. 너무 혼자 버티려고 하지 않아도 괜찮아요."

    elif "불안" in text or "걱정" in text:
        return "걱정이 많을 때는 해야 할 일을 아주 작은 단위로 나누면 도움이 될 수 있어요."

    elif "외로" in text:
        return "외로움을 느끼는 건 자연스러운 감정이에요. 가까운 사람과 짧게라도 대화를 나눠보세요."

    elif "공부" in text:
        return "완벽하게 하려고 하기보다 오늘 할 수 있는 만큼 해보는 게 중요해요."

    elif "연애" in text:
        return "상대방의 마음보다 지금 내 감정을 먼저 잘 살펴보는 것도 중요해요."

    else:
        return "당신의 이야기를 들려줘서 고마워요. 충분히 의미 있는 고민이에요."

# 입력 처리
if user_input:

    # 사용자 메시지 저장
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답 생성
    response = 상담응답(user_input)

    # AI 메시지 저장
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    # AI 메시지 출력
    with st.chat_message("assistant"):
        st.markdown(response)
