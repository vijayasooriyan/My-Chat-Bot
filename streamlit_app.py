import streamlit as st
import os
from dotenv import load_dotenv
from embedder import embed_User_query
from vectorstore import search_in_pinecone
from llm import query_llm_with_context
from datetime import datetime
import uuid

load_dotenv()

PINECONE_KEY = os.getenv("PINECONE_API_KEY")
GROQ_KEY     = os.getenv("GROQ_API_KEY")

st.set_page_config(
    page_title="VK · Portfolio AI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
if "messages"        not in st.session_state: st.session_state.messages        = []
if "query_count"     not in st.session_state: st.session_state.query_count     = 0
if "conversation_id" not in st.session_state: st.session_state.conversation_id = str(uuid.uuid4())[:8].upper()
if "sb_tab"          not in st.session_state: st.session_state.sb_tab          = "info"  # "info" | "stats" | "help"

# ─── DESIGN SYSTEM ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --ink:        #0d0d0f;
    --ink-2:      #1a1a1f;
    --ink-3:      #2a2a33;
    --muted:      #5a5a6e;
    --muted-2:    #8a8aa0;
    --line:       #e8e8f0;
    --line-2:     #f0f0f6;
    --paper:      #faf9f8;
    --white:      #ffffff;
    --gold:       #c9a84c;
    --gold-dim:   #a8883a;
    --gold-pale:  #f7f0e0;
    --radius:     4px;
    --font-display: 'DM Serif Display', Georgia, serif;
    --font-body:    'DM Sans', system-ui, sans-serif;
    --font-mono:    'DM Mono', 'Courier New', monospace;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: var(--paper) !important;
    font-family: var(--font-body) !important;
    color: var(--ink) !important;
    -webkit-font-smoothing: antialiased;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--ink-3); border-radius: 8px; }

/* ══════════════════════════════════════════
   SIDEBAR SHELL
══════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: var(--ink) !important;
    border-right: none !important;
    min-width: 272px !important;
    max-width: 272px !important;
}
[data-testid="stSidebar"] > div        { background: var(--ink) !important; padding: 0 !important; }
[data-testid="stSidebar"] > div > div  { padding: 0 !important; }
[data-testid="stSidebar"] .block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stSidebar"] section[data-testid="stSidebarContent"] { padding: 0 !important; }

/* ── Identity block ── */
.sb-identity {
    padding: 1.6rem 1.5rem 1.2rem;
    border-bottom: 1px solid var(--ink-3);
}
.sb-mono {
    width: 42px; height: 42px;
    background: var(--gold); border-radius: 3px;
    display: flex; align-items: center; justify-content: center;
    font-family: var(--font-display); font-size: 1.1rem;
    color: var(--ink); margin-bottom: 0.9rem;
}
.sb-name {
    font-family: var(--font-display); font-size: 1.1rem;
    color: #fff; line-height: 1.2; margin-bottom: 0.2rem;
}
.sb-role {
    font-family: var(--font-mono); font-size: 0.6rem;
    color: var(--muted-2); letter-spacing: 0.14em;
    text-transform: uppercase; margin-bottom: 0.7rem;
}
.sb-online {
    display: inline-flex; align-items: center; gap: 5px;
    font-family: var(--font-mono); font-size: 0.6rem;
    color: #4ade80; letter-spacing: 0.1em; text-transform: uppercase;
}
.sb-dot {
    width: 5px; height: 5px; border-radius: 50%; background: #4ade80;
    animation: blink 2s ease-in-out infinite; flex-shrink: 0;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* ── Tab row ── */
.sb-tabs {
    display: flex;
    border-bottom: 1px solid var(--ink-3);
    padding: 0 0.25rem;
    gap: 0;
}
/* Override Streamlit columns inside sidebar tab row */
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
    gap: 0 !important;
    padding: 0 !important;
    border-bottom: 1px solid var(--ink-3);
}
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] .stButton > button {
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    background: transparent !important;
    color: var(--muted) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.65rem 0 !important;
    font-weight: 400 !important;
    width: 100% !important;
    margin-bottom: -1px !important;
    transition: color 0.15s, border-color 0.15s !important;
    box-shadow: none !important;
    transform: none !important;
}
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] .stButton > button:hover {
    color: rgba(255,255,255,0.8) !important;
    border-bottom-color: var(--muted) !important;
    background: transparent !important;
    transform: none !important; box-shadow: none !important;
}

/* Active tab highlight injected via inline style on the button label –
   we simulate it by styling the *selected* button differently using a
   data attribute set in Python via a wrapper div */
.tab-active button {
    color: var(--gold) !important;
    border-bottom-color: var(--gold) !important;
}

/* ── Panel area ── */
.sb-panel {
    padding: 1.2rem 1.5rem;
    overflow-y: auto;
    flex: 1;
}
.sb-panel::-webkit-scrollbar { width: 3px; }

.sb-lbl {
    font-family: var(--font-mono); font-size: 0.58rem;
    letter-spacing: 0.15em; text-transform: uppercase;
    color: var(--muted); margin-bottom: 0.65rem; margin-top: 1.1rem;
}
.sb-lbl:first-child { margin-top: 0; }

/* Stack items */
.sb-stack {
    display: flex; align-items: center; gap: 9px;
    padding: 0.42rem 0.4rem; border-radius: var(--radius);
    margin-bottom: 2px; transition: background 0.15s;
}
.sb-stack:hover { background: var(--ink-3); }
.sb-s-icon {
    width: 22px; height: 22px; background: var(--ink-3);
    border-radius: 3px; display: flex; align-items: center;
    justify-content: center; font-size: 0.7rem; flex-shrink: 0;
}
.sb-s-name { font-family: var(--font-body); font-size: 0.78rem; color: rgba(255,255,255,0.68); }
.sb-s-badge {
    margin-left: auto;
    font-family: var(--font-mono); font-size: 0.53rem;
    color: var(--gold-dim); letter-spacing: 0.06em; text-transform: uppercase;
    background: rgba(201,168,76,0.1); padding: 1px 5px; border-radius: 2px;
}

/* Tip box */
.sb-tip {
    background: rgba(201,168,76,0.06); border: 1px solid rgba(201,168,76,0.18);
    border-radius: var(--radius); padding: 0.7rem 0.85rem; margin-top: 0.75rem;
}
.sb-tip p {
    font-family: var(--font-body); font-size: 0.76rem;
    color: rgba(255,255,255,0.5); line-height: 1.55; margin: 0;
}

/* Stats grid */
.sb-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 7px; }
.sb-s-cell {
    background: var(--ink-2); border: 1px solid var(--ink-3);
    border-radius: var(--radius); padding: 0.85rem 0.6rem; text-align: center;
}
.sb-s-n { font-family: var(--font-display); font-size: 1.85rem; color: var(--gold); line-height: 1; margin-bottom: 0.25rem; }
.sb-s-l { font-family: var(--font-mono); font-size: 0.55rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--muted); }

.sb-id-box {
    background: var(--ink-2); border: 1px solid var(--ink-3);
    border-radius: var(--radius); padding: 0.65rem 0.9rem;
    display: flex; align-items: center; justify-content: space-between; margin-top: 0.85rem;
}
.sb-id-lbl { font-family: var(--font-mono); font-size: 0.58rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--muted); }
.sb-id-val { font-family: var(--font-mono); font-size: 0.7rem; color: rgba(255,255,255,0.45); }

/* Q cards */
.sb-q {
    background: var(--ink-2); border: 1px solid var(--ink-3);
    border-left: 2px solid var(--gold); border-radius: var(--radius);
    padding: 0.5rem 0.7rem; margin-bottom: 0.45rem;
    font-family: var(--font-body); font-size: 0.78rem;
    color: rgba(255,255,255,0.6); line-height: 1.45; transition: all 0.15s;
}
.sb-q:hover { background: var(--ink-3); color: rgba(255,255,255,0.85); border-left-color: #ddb84e; }

/* ── Clear button ── */
[data-testid="stSidebar"] .stButton.clear-btn > button,
[data-testid="stSidebar"] > div .stButton > button:not([data-testid]) {
    background: transparent !important;
    border: 1px solid var(--ink-3) !important;
    border-radius: var(--radius) !important;
    color: var(--muted-2) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.55rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
    transform: none !important;
}
[data-testid="stSidebar"] > div .stButton > button:not([data-testid]):hover {
    background: var(--ink-3) !important;
    color: rgba(255,255,255,0.7) !important;
    border-color: var(--muted) !important;
    transform: none !important; box-shadow: none !important;
}

/* ══════════════════════════════════════════
   MAIN AREA
══════════════════════════════════════════ */
.block-container {
    max-width: 820px !important;
    padding: 2.5rem 2rem 2rem !important;
    margin: 0 auto !important;
}

.page-header { margin-bottom: 2rem; padding-bottom: 1.75rem; border-bottom: 1px solid var(--line); }
.hdr-eyebrow { font-family: var(--font-mono); font-size: 0.63rem; letter-spacing: 0.22em; text-transform: uppercase; color: var(--gold); margin-bottom: 0.45rem; }
.hdr-title   { font-family: var(--font-display); font-size: 2.2rem; color: var(--ink); line-height: 1.15; letter-spacing: -0.02em; margin-bottom: 0.4rem; }
.hdr-title em { font-style: italic; color: var(--muted); }
.hdr-sub     { font-family: var(--font-body); font-size: 0.88rem; color: var(--muted); font-weight: 300; line-height: 1.6; }

.empty-state { text-align: center; padding: 4rem 2rem; }
.empty-icon  { font-size: 1.8rem; margin-bottom: 0.7rem; opacity: 0.28; }
.empty-text  { font-family: var(--font-display); font-style: italic; font-size: 1.1rem; color: var(--muted); margin-bottom: 0.35rem; }
.empty-hint  { font-family: var(--font-mono); font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted-2); }

/* Messages */
.msg-row { display: flex; gap: 0.65rem; margin-bottom: 1.4rem; animation: mi 0.2s ease-out both; }
@keyframes mi { from{opacity:0;transform:translateY(5px)} to{opacity:1;transform:translateY(0)} }
.msg-row.user { flex-direction: row-reverse; }
.msg-av {
    width: 26px; height: 26px; border-radius: 2px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-family: var(--font-mono); font-size: 0.6rem; margin-top: 2px;
}
.msg-av.u { background: var(--ink); color: var(--white); }
.msg-av.b { background: var(--gold-pale); color: var(--gold); border: 1px solid #e8d8a0; }
.msg-body { max-width: 80%; }
.msg-bubble { border-radius: var(--radius); padding: 0.68rem 0.92rem; font-family: var(--font-body); font-size: 0.87rem; line-height: 1.65; }
.msg-bubble.u { background: var(--ink); color: var(--white); border-bottom-right-radius: 1px; }
.msg-bubble.b { background: var(--white); color: var(--ink); border: 1px solid var(--line); border-bottom-left-radius: 1px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
.msg-time { font-family: var(--font-mono); font-size: 0.57rem; letter-spacing: 0.06em; color: var(--muted-2); margin-top: 0.22rem; text-align: right; }
.msg-row.user .msg-time { text-align: left; }

[data-testid="stChatInput"] { background: var(--white) !important; border: 1.5px solid var(--line) !important; border-radius: var(--radius) !important; box-shadow: 0 1px 8px rgba(0,0,0,0.04) !important; transition: border-color 0.2s !important; }
[data-testid="stChatInput"]:focus-within { border-color: var(--gold) !important; box-shadow: 0 2px 16px rgba(201,168,76,0.1) !important; }
[data-testid="stChatInput"] textarea { font-family: var(--font-body) !important; font-size: 0.87rem !important; color: var(--ink) !important; caret-color: var(--gold) !important; }
[data-testid="stChatInput"] textarea::placeholder { color: var(--muted-2) !important; font-style: italic !important; }
[data-testid="stChatInput"] button { background: var(--gold) !important; border-radius: 2px !important; color: var(--ink) !important; }
[data-testid="stChatInput"] button:hover { background: #ddb84e !important; }

[data-testid="stSpinner"] p { font-family: var(--font-mono) !important; font-size: 0.7rem !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; color: var(--muted) !important; }

.stats-row { display: flex; gap: 1px; background: var(--line); border: 1px solid var(--line); border-radius: var(--radius); overflow: hidden; margin-top: 1.75rem; }
.stats-cell { flex: 1; background: var(--white); padding: 0.65rem 1rem; text-align: center; }
.stats-num  { font-family: var(--font-display); font-size: 1.25rem; color: var(--ink); line-height: 1; }
.stats-lbl  { font-family: var(--font-mono); font-size: 0.56rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--muted-2); margin-top: 0.18rem; }

.page-footer { margin-top: 1.75rem; padding-top: 1.1rem; border-top: 1px solid var(--line); display: flex; align-items: center; justify-content: space-between; }
.footer-l { font-family: var(--font-mono); font-size: 0.62rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted-2); }
.footer-r { font-family: var(--font-mono); font-size: 0.6rem; color: var(--muted-2); background: var(--line-2); padding: 0.17rem 0.42rem; border-radius: 2px; }

hr { border-color: var(--line) !important; margin: 1.25rem 0 !important; }

@media (max-width: 768px) {
    .block-container { padding: 1.25rem 1rem !important; }
    .hdr-title { font-size: 1.65rem !important; }
}
</style>
""", unsafe_allow_html=True)


# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    q_count = st.session_state.query_count
    r_count = sum(1 for m in st.session_state.messages if m["role"] == "assistant")
    tab     = st.session_state.sb_tab

    # ── Identity (always visible) ────────────────────────────────────────────
    st.markdown("""
    <div class="sb-identity">
      <div class="sb-mono">VK</div>
      <div class="sb-name">Vijayasooriyan<br>Kamarajah</div>
      <div class="sb-role">AI / Data Specialist</div>
      <div class="sb-online"><span class="sb-dot"></span>System online</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Tab buttons ──────────────────────────────────────────────────────────
    # Wrap each in a div so we can apply .tab-active when selected
    c1, c2, c3 = st.columns(3)
    with c1:
        active_cls = "tab-active" if tab == "info" else ""
        st.markdown(f"<div class='{active_cls}'>", unsafe_allow_html=True)
        if st.button("ⓘ Info",  key="t_info",  use_container_width=True):
            st.session_state.sb_tab = "info";  st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        active_cls = "tab-active" if tab == "stats" else ""
        st.markdown(f"<div class='{active_cls}'>", unsafe_allow_html=True)
        if st.button("◎ Stats", key="t_stats", use_container_width=True):
            st.session_state.sb_tab = "stats"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        active_cls = "tab-active" if tab == "help" else ""
        st.markdown(f"<div class='{active_cls}'>", unsafe_allow_html=True)
        if st.button("? Help",  key="t_help",  use_container_width=True):
            st.session_state.sb_tab = "help";  st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Panel: Info ──────────────────────────────────────────────────────────
    if tab == "info":
        st.markdown("""
        <div class="sb-panel">
          <div class="sb-lbl">Tech Stack</div>
          <div class="sb-stack"><div class="sb-s-icon">🗄</div><div class="sb-s-name">Pinecone</div><span class="sb-s-badge">Vector DB</span></div>
          <div class="sb-stack"><div class="sb-s-icon">🔢</div><div class="sb-s-name">Sentence Transformers</div><span class="sb-s-badge">Embed</span></div>
          <div class="sb-stack"><div class="sb-s-icon">⚡</div><div class="sb-s-name">Groq · Llama 3.3</div><span class="sb-s-badge">LLM</span></div>
          <div class="sb-stack"><div class="sb-s-icon">🐍</div><div class="sb-s-name">Python · Streamlit</div><span class="sb-s-badge">App</span></div>
          <div class="sb-lbl">How it works</div>
          <div class="sb-tip">
            <p>Your question is embedded into a vector, matched against CV chunks in Pinecone, and the top-5 results are fed to Llama 3.3 for a grounded answer.</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Panel: Stats ─────────────────────────────────────────────────────────
    elif tab == "stats":
        total_msgs = len(st.session_state.messages)
        st.markdown(f"""
        <div class="sb-panel">
          <div class="sb-lbl">This Session</div>
          <div class="sb-grid">
            <div class="sb-s-cell"><div class="sb-s-n">{q_count}</div><div class="sb-s-l">Questions</div></div>
            <div class="sb-s-cell"><div class="sb-s-n">{r_count}</div><div class="sb-s-l">Answers</div></div>
            <div class="sb-s-cell"><div class="sb-s-n">{total_msgs}</div><div class="sb-s-l">Messages</div></div>
            <div class="sb-s-cell"><div class="sb-s-n">5</div><div class="sb-s-l">Chunks/query</div></div>
          </div>
          <div class="sb-id-box">
            <span class="sb-id-lbl">Session ID</span>
            <span class="sb-id-val">{st.session_state.conversation_id}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Panel: Help ──────────────────────────────────────────────────────────
    else:
        st.markdown("""
        <div class="sb-panel">
          <div class="sb-lbl">Try asking…</div>
          <div class="sb-q">What are your core technical skills?</div>
          <div class="sb-q">Describe your most complex project.</div>
          <div class="sb-q">What certifications do you hold?</div>
          <div class="sb-q">Python or SQL — which do you prefer?</div>
          <div class="sb-q">Any experience with cloud platforms?</div>
          <div class="sb-q">Walk me through your ML pipeline work.</div>
          <div class="sb-lbl">Tips</div>
          <div class="sb-tip">
            <p>Be specific — <em>"Python projects using pandas"</em> returns sharper results than <em>"Python"</em> alone. The search is semantic, so natural phrasing works best.</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Clear button (always visible at bottom) ──────────────────────────────
    st.markdown("<div style='padding: 0.75rem 1.5rem; border-top: 1px solid var(--ink-3);'>",
                unsafe_allow_html=True)
    if st.button("↺  Clear conversation", use_container_width=True, key="clear_btn"):
        st.session_state.messages    = []
        st.session_state.query_count = 0
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# ─── MAIN ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
  <div class="hdr-eyebrow">◈ Portfolio Intelligence</div>
  <div class="hdr-title">Ask anything about<br><em>my CV</em></div>
  <div class="hdr-sub">
    Semantic search over the full CV corpus, answered by Groq Llama 3.3.
  </div>
</div>
""", unsafe_allow_html=True)

# ── Messages ───────────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
      <div class="empty-icon">◇</div>
      <div class="empty-text">No conversation yet</div>
      <div class="empty-hint">Type a question below to begin</div>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        role, content = msg["role"], msg["content"]
        try:    time_str = datetime.fromisoformat(msg.get("timestamp","")).strftime("%H:%M")
        except: time_str = ""

        if role == "user":
            st.markdown(f"""
            <div class="msg-row user">
              <div class="msg-av u">you</div>
              <div class="msg-body">
                <div class="msg-bubble u">{content}</div>
                <div class="msg-time">{time_str}</div>
              </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-row">
              <div class="msg-av b">◈</div>
              <div class="msg-body">
                <div class="msg-bubble b">{content}</div>
                <div class="msg-time">{time_str}</div>
              </div>
            </div>""", unsafe_allow_html=True)

# ── Input ──────────────────────────────────────────────────────────────────────
prompt = st.chat_input("Ask about skills, projects, experience, certifications…")

if prompt and prompt.strip():
    ts_now = datetime.now().isoformat()
    st.session_state.messages.append({"role": "user", "content": prompt.strip(), "timestamp": ts_now})
    st.session_state.query_count += 1

    with st.spinner("Searching CV corpus…"):
        try:
            query_vector   = embed_User_query(prompt)
            matched_chunks = search_in_pinecone(query_vector, top_k=5)
            if not matched_chunks or not matched_chunks.strip():
                response = ("I couldn't find relevant information in the CV for that question. "
                            "Try asking about skills, experience, projects, or certifications.")
            else:
                response = query_llm_with_context(prompt, matched_chunks)
        except Exception as exc:
            response = f"⚠ An error occurred: {str(exc)[:200]}"

    st.session_state.messages.append({"role": "assistant", "content": response, "timestamp": datetime.now().isoformat()})
    st.rerun()

# ── Stats bar (only after first message) ──────────────────────────────────────
if st.session_state.messages:
    total   = len(st.session_state.messages)
    asked   = sum(1 for m in st.session_state.messages if m["role"] == "user")
    replied = sum(1 for m in st.session_state.messages if m["role"] == "assistant")
    st.markdown(f"""
    <div class="stats-row">
      <div class="stats-cell"><div class="stats-num">{total}</div><div class="stats-lbl">Messages</div></div>
      <div class="stats-cell"><div class="stats-num">{asked}</div><div class="stats-lbl">Questions</div></div>
      <div class="stats-cell"><div class="stats-num">{replied}</div><div class="stats-lbl">Responses</div></div>
    </div>""", unsafe_allow_html=True)

st.markdown(f"""
<div class="page-footer">
  <span class="footer-l">Streamlit · Pinecone · Groq</span>
  <span class="footer-r">session&nbsp;{st.session_state.conversation_id}</span>
</div>""", unsafe_allow_html=True)