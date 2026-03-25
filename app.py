import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

st.set_page_config(
    page_title="NeuraChat · AI Assistant",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');
:root {
    --bg-primary:#0a0a0f;--bg-secondary:#0f0f1a;--bg-card:#13131f;--bg-input:#1a1a2e;
    --accent-1:#7c3aed;--accent-2:#06b6d4;--accent-3:#f59e0b;
    --text-primary:#e2e8f0;--text-muted:#64748b;--border:#1e1e35;
    --border-glow:rgba(124,58,237,0.4);--user-bg:rgba(124,58,237,0.12);
    --ai-bg:rgba(6,182,212,0.07);--radius:14px;--radius-sm:8px;
}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif!important;background-color:var(--bg-primary)!important;color:var(--text-primary)!important;}
#MainMenu,footer,header{visibility:hidden;}.stDeployButton{display:none;}
.main .block-container{padding:0 2rem 2rem 2rem!important;max-width:960px!important;}
.neurachat-header{display:flex;align-items:center;gap:16px;padding:28px 0 20px 0;border-bottom:1px solid var(--border);margin-bottom:28px;}
.header-icon{width:48px;height:48px;background:linear-gradient(135deg,var(--accent-1),var(--accent-2));border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:22px;box-shadow:0 0 24px rgba(124,58,237,0.4);}
.header-title{font-family:'Space Mono',monospace!important;font-size:26px;font-weight:700;background:linear-gradient(90deg,var(--accent-2),var(--accent-1));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.header-subtitle{font-size:13px;color:var(--text-muted);margin-top:2px;}
.status-dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:#22c55e;box-shadow:0 0 8px #22c55e;animation:pulse 2s infinite;margin-right:6px;}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.4}}
section[data-testid="stSidebar"]{background-color:var(--bg-secondary)!important;border-right:1px solid var(--border)!important;}
section[data-testid="stSidebar"] .block-container{padding:2rem 1.5rem!important;}
.sidebar-logo{font-family:'Space Mono',monospace!important;font-size:18px;font-weight:700;color:var(--accent-2);margin-bottom:28px;}
.sidebar-section{font-size:11px;text-transform:uppercase;letter-spacing:1.5px;color:var(--text-muted);margin:20px 0 10px 0;font-weight:600;}
.stat-row{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--border);font-size:13px;}
.stat-val{font-family:'Space Mono',monospace!important;color:var(--accent-3);font-size:12px;font-weight:700;}
.msg-row{display:flex;gap:14px;align-items:flex-start;margin-bottom:16px;animation:fadeIn 0.3s ease;}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.msg-row.user{flex-direction:row-reverse;}
.avatar{width:36px;height:36px;border-radius:10px;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:16px;}
.avatar.ai{background:linear-gradient(135deg,rgba(6,182,212,0.2),rgba(124,58,237,0.2));border:1px solid rgba(6,182,212,0.3);}
.avatar.user{background:linear-gradient(135deg,rgba(124,58,237,0.3),rgba(245,158,11,0.2));border:1px solid rgba(124,58,237,0.4);}
.msg-bubble{max-width:78%;padding:14px 18px;border-radius:var(--radius);font-size:15px;line-height:1.65;}
.msg-bubble.ai{background:var(--ai-bg);border:1px solid rgba(6,182,212,0.15);border-top-left-radius:4px;}
.msg-bubble.user{background:var(--user-bg);border:1px solid rgba(124,58,237,0.2);border-top-right-radius:4px;}
.msg-meta{font-size:11px;color:var(--text-muted);margin-top:5px;font-family:'Space Mono',monospace!important;}
.stTextInput>div>div>input{background-color:var(--bg-input)!important;border:1px solid var(--border)!important;border-radius:var(--radius)!important;color:var(--text-primary)!important;font-size:15px!important;padding:14px 18px!important;}
.stTextInput>div>div>input:focus{border-color:var(--accent-1)!important;box-shadow:0 0 0 3px var(--border-glow)!important;}
.stTextArea textarea{background-color:var(--bg-input)!important;border:1px solid var(--border)!important;border-radius:var(--radius-sm)!important;color:var(--text-primary)!important;}
.stButton>button{background:linear-gradient(135deg,var(--accent-1),#5b21b6)!important;color:white!important;border:none!important;border-radius:var(--radius-sm)!important;font-weight:600!important;font-size:14px!important;padding:10px 24px!important;box-shadow:0 4px 15px rgba(124,58,237,0.3)!important;transition:all 0.2s ease!important;}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 6px 20px rgba(124,58,237,0.5)!important;}
.stSelectbox>div>div{background-color:var(--bg-input)!important;border:1px solid var(--border)!important;border-radius:var(--radius-sm)!important;color:var(--text-primary)!important;}
.empty-state{text-align:center;padding:60px 20px;color:var(--text-muted);}
.empty-icon{font-size:48px;margin-bottom:16px;opacity:0.5;}
.empty-title{font-family:'Space Mono',monospace!important;font-size:18px;color:var(--text-primary);margin-bottom:8px;}
::-webkit-scrollbar{width:6px;}::-webkit-scrollbar-track{background:var(--bg-primary);}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px;}
::-webkit-scrollbar-thumb:hover{background:var(--accent-1);}
</style>
""", unsafe_allow_html=True)

# ── Session State ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_count" not in st.session_state:
    st.session_state.chat_count = 0
if "pending_input" not in st.session_state:
    st.session_state.pending_input = ""

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">⬡ NeuraChat</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">🔑 Authentication</div>', unsafe_allow_html=True)
    groq_api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...", label_visibility="collapsed")
    if groq_api_key:
        st.success("✓ API key loaded", icon="🔐")

    st.markdown('<div class="sidebar-section">🤖 Model</div>', unsafe_allow_html=True)
    model_options = {
        "llama-3.3-70b-versatile": "⚡ LLaMA 3.3 · 70B",
        "llama-3.1-8b-instant":    "🚀 LLaMA 3.1 · 8B (Fast)",
        "mixtral-8x7b-32768":      "🌀 Mixtral · 8×7B",
        "gemma2-9b-it":            "💎 Gemma 2 · 9B",
    }
    selected_model = st.selectbox("Model", options=list(model_options.keys()),
                                  format_func=lambda x: model_options[x], label_visibility="collapsed")

    st.markdown('<div class="sidebar-section">⚙️ Parameters</div>', unsafe_allow_html=True)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.05)
    max_tokens  = st.slider("Max Tokens",  256, 4096, 1024, 128)

    st.markdown('<div class="sidebar-section">🧠 System Prompt</div>', unsafe_allow_html=True)
    system_prompt = st.text_area("System Prompt",
        value="You are NeuraChat, a helpful AI assistant. Be precise, thoughtful, and slightly witty.",
        height=100, label_visibility="collapsed")

    st.markdown('<div class="sidebar-section">📊 Session Stats</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="stat-row"><span>Messages</span><span class="stat-val">{len(st.session_state.messages)}</span></div>'
                f'<div class="stat-row"><span>Exchanges</span><span class="stat-val">{st.session_state.chat_count}</span></div>',
                unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑 Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_count = 0
        st.session_state.pending_input = ""
        st.rerun()

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="neurachat-header">
  <div class="header-icon">⬡</div>
  <div>
    <div class="header-title">NeuraChat</div>
    <div class="header-subtitle"><span class="status-dot"></span>Powered by Groq · LangChain · Streamlit</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── LLM Call ───────────────────────────────────────────────────────────────────
def get_response(user_msg: str, api_key: str) -> str:
    llm = ChatGroq(groq_api_key=api_key, model_name=selected_model,
                   temperature=temperature, max_tokens=max_tokens)
    lc_msgs = [SystemMessage(content=system_prompt)]
    for m in st.session_state.messages:
        lc_msgs.append(HumanMessage(content=m["content"]) if m["role"] == "user"
                       else AIMessage(content=m["content"]))
    lc_msgs.append(HumanMessage(content=user_msg))
    return llm.invoke(lc_msgs).content

# ── Process pending input FIRST (before rendering) ─────────────────────────────
if st.session_state.pending_input:
    user_msg = st.session_state.pending_input
    st.session_state.pending_input = ""          # clear BEFORE API call
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.spinner("NeuraChat is thinking…"):
        try:
            reply = get_response(user_msg, groq_api_key)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.session_state.chat_count += 1
        except Exception as e:
            st.session_state.messages.pop()       # remove orphaned user msg
            err = str(e)
            if "401" in err or "api_key" in err.lower() or "auth" in err.lower():
                st.error("❌ Invalid API Key — check your Groq key in the sidebar.")
            elif "rate" in err.lower():
                st.error("⏳ Rate limit reached. Wait a moment and retry.")
            elif "connect" in err.lower() or "timeout" in err.lower():
                st.error("🔌 Connection error. Check your internet connection.")
            else:
                st.error(f"❌ {err}")

# ── Render Messages ────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">⬡</div>
        <div class="empty-title">Start a conversation</div>
        <div style="font-size:14px;line-height:1.7">
            Enter your Groq API key in the sidebar, choose a model,<br>
            then type a message below and click <strong>Send</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        safe = (msg["content"].replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"))
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-row user">
              <div class="avatar user">👤</div>
              <div><div class="msg-bubble user">{safe}</div>
                   <div class="msg-meta" style="text-align:right">You</div></div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-row">
              <div class="avatar ai">⬡</div>
              <div><div class="msg-bubble ai">{safe}</div>
                   <div class="msg-meta">NeuraChat · {model_options.get(selected_model,'')}</div></div>
            </div>""", unsafe_allow_html=True)

# ── Input Row ─────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns([9, 1])
with col1:
    user_input = st.text_input("Message", placeholder="Type your message and click Send…",
                               label_visibility="collapsed", key="chat_input")
with col2:
    send_clicked = st.button("Send", use_container_width=True)

if send_clicked:
    if not user_input.strip():
        st.warning("Please type a message first.")
    elif not groq_api_key:
        st.error("⚠️ Enter your Groq API Key in the sidebar first.")
    else:
        st.session_state.pending_input = user_input.strip()
        st.rerun()
