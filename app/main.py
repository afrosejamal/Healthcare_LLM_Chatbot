import streamlit as st
import base64
import os
from llm import get_chat_response
from prompts import SYSTEM_PROMPT
from safety import (
    check_emergency, check_self_harm, check_diagnosis_request,
    EMERGENCY_RESPONSE, SELF_HARM_RESPONSE, DIAGNOSIS_GUARD_NOTE
)
from rag import retrieve

st.set_page_config(page_title="HealthMate", page_icon="🩺", layout="centered")

# ---------- BACKGROUND IMAGE (base64 embed) ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BG_PATH = os.path.join(BASE_DIR, "assets", "wave_bg.png")

def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_base64 = get_base64(BG_PATH)

# ---------- GLOBAL STYLING ----------
st.markdown(f"""
<style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-position: center 45%;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    /* Kill every dark wrapper around the bottom chat input */
    div[data-testid="stBottom"],
    div[data-testid="stBottomBlockContainer"],
    div[data-testid="stChatInputContainer"],
    footer {{
        background-color: rgba(247, 249, 251, 0.95) !important;
        backdrop-filter: blur(8px);
    }}

    header[data-testid="stHeader"] {{
        background-color: rgba(247, 249, 251, 0.0) !important;
    }}

    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.88);
        backdrop-filter: blur(8px);
        border-radius: 20px;
        padding: 2rem 2.5rem;
        margin-top: 1rem;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
    }}

    section[data-testid="stSidebar"] {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-right: 1px solid #e3e8ee;
    }}
    section[data-testid="stSidebar"] * {{
        color: #14213d !important;
    }}

    .header-container {{
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 4px 0 22px 0;
    }}
    .header-logo {{ font-size: 44px; line-height: 1; }}
    .header-title {{
        font-size: 30px; font-weight: 800; color: #14213d !important;
        margin: 0; letter-spacing: -0.5px;
    }}
    .header-subtitle {{ font-size: 14.5px; color: #5f6b7a !important; margin: 0; }}

    div[data-testid="stChatMessage"] {{
        background-color: rgba(255, 255, 255, 0.92);
        border-radius: 16px;
        padding: 6px 10px;
        border: 1px solid #e8ecf1;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }}
    div[data-testid="stChatMessage"] p {{ color: #1a1a1a !important; }}

    .stButton>button {{
        border-radius: 10px;
        border: 1px solid #d8e0ea;
        background-color: #ffffff;
        color: #14213d !important;
        font-weight: 500;
    }}
    .stButton>button:hover {{
        border-color: #0e9488;
        color: #0e9488 !important;
    }}

    /* The actual typing box */
    div[data-testid="stChatInput"] {{
        background-color: #ffffff !important;
        border-radius: 14px !important;
        border: 1px solid #d8e0ea !important;
    }}
    div[data-testid="stChatInput"] textarea {{
        background-color: #ffffff !important;
        color: #14213d !important;
        caret-color: #14213d !important;
    }}
    div[data-testid="stChatInput"] textarea::placeholder {{
        color: #8a97a8 !important;
    }}
    div[data-testid="stChatInput"] button {{
        background-color: #0e9488 !important;
        border-radius: 8px !important;
    }}

    .stAlert p {{ color: #6b5a1a !important; }}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("### 🩺 HealthMate")
    st.caption("AI Healthcare Information Assistant")
    st.markdown("---")
    st.markdown(
        "**What I can help with:**\n"
        "- 🩹 Common symptoms\n"
        "- 🦠 General diseases\n"
        "- 🏃 Healthy lifestyle tips\n"
        "- 🥗 Nutrition & diet\n"
        "- 🛡️ Preventive healthcare\n"
        "- 🚑 First-aid guidance"
    )
    st.markdown("---")
    st.warning(
        "⚠️ General health information only — not a substitute for "
        "professional medical advice, diagnosis, or treatment. "
        "In an emergency, call your local emergency number."
    )
    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.rerun()

# ---------- HEADER ----------
st.markdown("""
<div class="header-container">
    <div class="header-logo">🩺</div>
    <div>
        <p class="header-title">HealthMate</p>
        <p class="header-subtitle">Your general healthcare information assistant</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# ---------- QUICK START ----------
example_clicked = None
if len(st.session_state.messages) == 1:
    st.markdown("**💡 Try asking:**")
    cols = st.columns(2)
    example_map = {
        "🩹 Symptoms of dehydration?": "What are symptoms of dehydration?",
        "🥗 Give me a healthy diet plan": "Give me a healthy diet plan",
        "🚑 First aid for a minor burn": "First aid for a minor burn",
        "🧘 Tips to reduce stress": "Tips to reduce stress",
    }
    for i, (label, query) in enumerate(example_map.items()):
        if cols[i % 2].button(label, use_container_width=True):
            example_clicked = query

# ---------- RENDER CHAT HISTORY ----------
for msg in st.session_state.messages[1:]:
    avatar = "🧑" if msg["role"] == "user" else "🩺"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ---------- INPUT HANDLING ----------
user_input = st.chat_input("Ask a health-related question...")
if example_clicked:
    user_input = example_clicked

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🩺"):
        if check_self_harm(user_input):
            reply = SELF_HARM_RESPONSE
            st.markdown(reply)
        elif check_emergency(user_input):
            reply = EMERGENCY_RESPONSE
            st.markdown(reply)
        else:
            with st.spinner("Thinking..."):
                retrieved = retrieve(user_input, top_k=2)

                context_block = ""
                sources = []
                if retrieved:
                    context_block = "\n\nRelevant reference information:\n"
                    for r in retrieved:
                        context_block += f"- [{r['topic']}]: {r['content']}\n"
                        sources.append(r["topic"])

                temp_messages = st.session_state.messages.copy()
                augmented_content = user_input + context_block
                if check_diagnosis_request(user_input):
                    augmented_content += DIAGNOSIS_GUARD_NOTE
                temp_messages[-1] = {"role": "user", "content": augmented_content}

                reply = get_chat_response(temp_messages)
                st.markdown(reply)

                if sources:
                    st.caption(f"📚 Sources referenced: {', '.join(sources)}")

    st.session_state.messages.append({"role": "assistant", "content": reply})