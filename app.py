from groq import Groq
import streamlit as st
from supabase import create_client
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
import uuid
import time
from datetime import datetime, timedelta

# ----------------------------------
# 🎨 PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="Syllabus AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ----------------------------------
# 📱 MOBILE OPTIMIZED UI
# ----------------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    max-width: 900px;
}

.chat-user {
    background: linear-gradient(135deg,#6366f1,#4f46e5);
    color:white;
    padding:12px;
    border-radius:14px;
    margin-bottom:8px;
    word-wrap: break-word;
}

.chat-ai {
    background:#f1f5f9;
    color:#0f172a;
    padding:12px;
    border-radius:14px;
    margin-bottom:8px;
    word-wrap: break-word;
}

.status-ok {background:#dcfce7;color:#166534;padding:8px;border-radius:10px;margin-bottom:10px;}
.status-warn {background:#fef3c7;color:#92400e;padding:8px;border-radius:10px;margin-bottom:10px;}
.status-error {background:#fee2e2;color:#991b1b;padding:8px;border-radius:10px;margin-bottom:10px;}

@media (max-width:640px){
.block-container{max-width:100%;padding-left:12px;padding-right:12px;}
.chat-user,.chat-ai{font-size:15px;padding:10px;border-radius:12px;}
h1{font-size:22px !important;padding:10px !important;}
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------
# 🔑 LOAD SECRETS
# ----------------------------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_ANON_KEY"]
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

groq_client = Groq(api_key=GROQ_API_KEY)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ----------------------------------
# 🧠 CACHE EMBEDDING MODEL (DEPLOYMENT SAFE)
# ----------------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# ----------------------------------
# 🧩 SESSION SETUP
# ----------------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "system_status" not in st.session_state:
    st.session_state.system_status = "ok"

# ----------------------------------
# 🧹 AUTO CLEAN OLD EMBEDDINGS (TRUE MULTI USER)
# ----------------------------------
def cleanup_old_embeddings(hours=1):
    try:
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        supabase.table("documents").delete().lt(
            "created_at", cutoff.isoformat()
        ).execute()
    except Exception:
        st.session_state.system_status = "warn"

cleanup_old_embeddings()

# ----------------------------------
# 📄 PDF PROCESSING
# ----------------------------------
def process_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return [text[i:i+500] for i in range(0, len(text), 500)]

def store_embeddings(chunks):
    embeddings = model.encode(chunks).tolist()

    for chunk, emb in zip(chunks, embeddings):
        try:
            supabase.table("documents").insert({
                "session_id": st.session_state.session_id,
                "content": chunk,
                "embedding": emb,
                "created_at": datetime.utcnow().isoformat()
            }).execute()
        except Exception:
            st.session_state.system_status = "error"
            st.error("⚠️ Database limit reached. Please try again later.")
            break

# ----------------------------------
# 🔎 RETRIEVAL
# ----------------------------------
def retrieve_context(question):
    q_emb = model.encode(question).tolist()
    try:
        response = supabase.rpc(
            "match_documents",
            {
                "query_embedding": q_emb,
                "match_count": 3,
                "session_filter": st.session_state.session_id
            }
        ).execute()

        if response.data:
            return "\n".join([row["content"] for row in response.data])

    except Exception:
        st.session_state.system_status = "error"

    return ""

# ----------------------------------
# 🤖 GROQ STREAMING + LIMIT DETECTION
# ----------------------------------
def stream_answer(prompt):
    try:
        stream = groq_client.chat.completions.create(
            messages=[{"role":"user","content":prompt}],
            model="llama-3.1-8b-instant",
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    except Exception as e:
        err=str(e).lower()
        if "limit" in err or "rate" in err or "quota" in err:
            st.session_state.system_status="warn"
            yield "⚠️ Daily AI usage limit reached. Please try again later."
        else:
            st.session_state.system_status="error"
            yield f"⚠️ AI Error: {e}"

# ----------------------------------
# 🟢 SYSTEM STATUS BANNER
# ----------------------------------
if st.session_state.system_status=="ok":
    st.markdown("<div class='status-ok'>🟢 System Healthy</div>",unsafe_allow_html=True)
elif st.session_state.system_status=="warn":
    st.markdown("<div class='status-warn'>🟡 Free-tier limits may be reached</div>",unsafe_allow_html=True)
else:
    st.markdown("<div class='status-error'>🔴 Service Issue — Try later</div>",unsafe_allow_html=True)

# ----------------------------------
# 🧭 SIDEBAR
# ----------------------------------
with st.sidebar:
    st.title("⚙️ Controls")
    uploaded_file = st.file_uploader("📄 Upload PDF", type="pdf")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages=[]
        st.rerun()

    st.caption("📱 Mobile Optimized • Multi-User • Auto-Clean")

# ----------------------------------
# 🌟 HEADER
# ----------------------------------
st.markdown("""
<h1 style='text-align:center;
background:linear-gradient(90deg,#6366f1,#8b5cf6);
color:white;padding:14px;border-radius:14px;'>
📄 Syllabus AI Assistant
</h1>
<p style='text-align:center;color:#475569;'>
Streaming AI • True Multi-User • Free Tier Ready
</p>
""",unsafe_allow_html=True)

# ----------------------------------
# 📄 HANDLE PDF UPLOAD
# ----------------------------------
if uploaded_file:
    with st.spinner("📚 Indexing syllabus..."):
        chunks=process_pdf(uploaded_file)
        store_embeddings(chunks)
    st.success("✅ PDF indexed!")

# ----------------------------------
# 💬 CHAT DISPLAY
# ----------------------------------
for msg in st.session_state.messages:
    cls="chat-user" if msg["role"]=="user" else "chat-ai"
    icon="🧑" if msg["role"]=="user" else "🤖"
    st.markdown(
        f"<div class='{cls}'>{icon} {msg['content']}</div>",
        unsafe_allow_html=True
    )

# ----------------------------------
# 💬 CHAT INPUT + STREAMING
# ----------------------------------
question=st.chat_input("💬 Ask about your syllabus...")

if question:
    st.session_state.messages.append({"role":"user","content":question})

    context=retrieve_context(question)

    prompt=f"""
    Answer using ONLY this syllabus context:

    {context}

    Question: {question}
    """

    placeholder=st.empty()
    full=""

    for token in stream_answer(prompt):
        full+=token
        placeholder.markdown(
            f"<div class='chat-ai'>🤖 {full} ▌</div>",
            unsafe_allow_html=True
        )
        time.sleep(0.01)

    placeholder.markdown(
        f"<div class='chat-ai'>🤖 {full}</div>",
        unsafe_allow_html=True
    )

    st.session_state.messages.append({"role":"assistant","content":full})
    st.rerun()
