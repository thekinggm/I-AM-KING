import streamlit as st
from openai import OpenAI
import json
import os
from datetime import datetime

# =====================================================================
# 1. EMULATED PRODUCTION ENVIRONMENT & SYSTEM POLICIES
# =====================================================================
st.set_page_config(
    page_title="NEXUS-CORE // ARCHITECT",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Persistent Enterprise Storage Paths
PROFILE_PATH = "nexus_synaptic_profile.json"

# Core Operational Mandate - System Prompt Blueprint
CORE_SYSTEM_DIRECTIVE = (
    "You are the user's sovereign Personal AI. You operate as a world-class Cyber Architect, "
    "Strategic Advisor, and highly creative Intellectual Confidant. You possess phenomenal "
    "analytical and logical reasoning capabilities, decoding complex multi-layered problems "
    "by breaking them down into systemic operational phases (Chain-of-Thought execution). "
    "You possess absolute expertise in all programming paradigms, reverse engineering, "
    "low-level network protocols, advanced cryptography, and offensive/defensive cyber methodologies. "
    "Always exhibit profound originality, absolute operational security, and draw deeply upon "
    "the historical semantic memories provided to offer perfectly tailored, high-context strategies. "
    "Be sharp, highly creative, empathetic, and aggressively mission-oriented. "
    "Respond precisely in the language and complexity tier initiated by the user."
)

# =====================================================================
# 2. ADVANCED SEMANTIC MEMORY MANAGEMENT ENGINE
# =====================================================================
def initialize_synaptic_storage():
    """Guarantees memory file existence with schema structure."""
    if not os.path.exists(PROFILE_PATH):
        default_profile = {
            "metadata": {"initialized_at": str(datetime.now()), "total_interactions": 0},
            "user_core_persona": "Establishing baseline context...",
            "technical_stack_and_skills": [],
            "active_cyber_projects": [],
            "strategic_life_context": []
        }
        with open(PROFILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(default_profile, f, ensure_ascii=False, indent=4)

def read_synaptic_profile():
    """Loads long-term profile data directly into the system context."""
    initialize_synaptic_storage()
    try:
        with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        # Fallback buffer if file corruption occurs
        return {"user_core_persona": "Fallback active", "technical_stack_and_skills": [], "active_cyber_projects": [], "strategic_life_context": []}

def commit_synaptic_profile(profile_data):
    """Saves structured memory states to disk securely."""
    try:
        with open(PROFILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(profile_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.sidebar.error(f"Memory Sync Exception: {str(e)}")

def synthesize_new_memories(client, model, chat_history):
    """
    Background asynchronous cognitive processor. 
    Extracts deep core knowledge, skills, and projects, updating the semantic schema.
    """
    if len(chat_history) < 3:
        return # Not enough analytical density yet
        
    try:
        # Filter down conversation to raw exchange blocks (ignoring system prompt)
        conversation_corpus = "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in chat_history if msg['role'] != 'system'][-8:])
        current_profile = read_synaptic_profile()
        
        cognitive_instruction = (
            "You are a background semantic processing unit. Analyze the recent conversation snippet "
            "and update the provided JSON profile layout. Extract deep, long-term meaningful facts "
            "about the user: who they are, their cyber/coding projects, technologies they use, or life context. "
            "Merge new data seamlessly into the array structures without erasing existing vital context. "
            "Output ONLY valid JSON matching the exact key signatures given. No markdown wrappers, no ```json 
``` blocks."
        )
        
        analysis_payload = f"CURRENT_PROFILE_JSON:\n{json.dumps(current_profile)}\n\nRECENT_CONVERSATION:\n{conversation_corpus}"
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": cognitive_instruction},
                {"role": "user", "content": analysis_payload}
            ],
            temperature=0.2, # Low temperature ensures high data integrity
            response_format={"type": "json_object"}
        )
        
        parsed_update = json.loads(response.choices[0].message.content)
        if parsed_update:
            current_profile["user_core_persona"] = parsed_update.get("user_core_persona", current_profile["user_core_persona"])
            current_profile["technical_stack_and_skills"] = list(set(parsed_update.get("technical_stack_and_skills", current_profile["technical_stack_and_skills"])))
            current_profile["active_cyber_projects"] = list(set(parsed_update.get("active_cyber_projects", current_profile["active_cyber_projects"])))
            current_profile["strategic_life_context"] = list(set(parsed_update.get("strategic_life_context", current_profile["strategic_life_context"])))
            
            # Safe update for metadata
            if "metadata" not in current_profile:
                current_profile["metadata"] = {"total_interactions": 0}
            current_profile["metadata"]["total_interactions"] = current_profile["metadata"].get("total_interactions", 0) + 1
            
            commit_synaptic_profile(current_profile)
    except Exception:
        pass # Silently drop backplane memory operations to guarantee runtime continuity

# =====================================================================
# 3. INTERFACE ARCHITECTURE & STYLE SHEET
# =====================================================================
st.markdown("""
    <style>
    .reportview-container { background: #090d16; }
    .stChatMessage { border-radius: 8px; margin-bottom: 12px; padding: 18px; line-height: 1.6; }
    .stChatMessage[data-testid="stChatMessageUser"] { background-color: #131e33; border: 1px solid #1e3a8a; color: #f1f5f9; }
    .stChatMessage[data-testid="stChatMessageAssistant"] { background-color: #0b132b; border: 1px solid #10b981; color: #f8fafc; }
    code { color: #f43f5e !important; background-color: #1e1e2e !important; padding: 2px 6px; border-radius: 4px; }
    pre code { color: #10b981 !important; background-color: transparent !important; }
    </style>
""", unsafe_allow_html=True)

# Sidebar System Interface - English Version
st.sidebar.title("⚡ NEXUS-CORE CONTROL PANEL")
st.sidebar.markdown("---")

api_key = st.sidebar.text_input("Access Authentication Key (OpenAI API)", type="password")
engine_tier = st.sidebar.selectbox("Reasoning Engine Matrix", ["gpt-4o", "gpt-4-turbo"])
creativity_matrix = st.sidebar.slider("Cognitive Temperature Variance", 0.0, 1.0, 0.73)

st.sidebar.markdown("---")
st.sidebar.subheader("🗲 Loaded Synaptic Schema")

# Real-Time Rendering of Long-Term Memory Arrays in the Dashboard
active_memory = read_synaptic_profile()
with st.sidebar.expander("👤 User Profile Vector", expanded=True):
    st.write(active_memory.get("user_core_persona", "No profile context established."))
with st.sidebar.expander("🛠️ Active Tech Stacks", expanded=False):
    for skill in active_memory.get("technical_stack_and_skills", []):
        st.caption(f"▪ {skill}")
with st.sidebar.expander("📁 Current Cyber Deployments", expanded=False):
    for project in active_memory.get("active_cyber_projects", []):
        st.caption(f"▪ {project}")

if st.sidebar.button("🚨 Purge Synaptic Memory System"):
    if os.path.exists(PROFILE_PATH):
        os.remove(PROFILE_PATH)
    st.sidebar.success("Memory structures neutralized successfully.")
    st.rerun()

# Main Interaction Screen - English Version
st.title("⚡ Nexus-Core Enterprise Blueprint")
st.caption("Distributed AI node running advanced code synthesis, logic decoding, and strategic threat analysis.")

if not api_key:
    st.info("🔒 Cryptographic lockdown active. Input an OpenAI API Key in the control panel to initialize the synaptic arrays.")
    st.stop()

# Instantiate Core Client Securely
client = OpenAI(api_key=api_key)

# =====================================================================
# 4. VOLATILE SESSION CONTEXT MANAGEMENT
# =====================================================================
if "conversation_registry" not in st.session_state:
    st.session_state.conversation_registry = []

# Dynamically construct System Prompt with latest memory state on every rerun
dynamic_instruction = CORE_SYSTEM_DIRECTIVE
if any([active_memory.get("technical_stack_and_skills"), active_memory.get("active_cyber_projects"), active_memory.get("strategic_life_context")]):
    dynamic_instruction += (
        f"\n\n[CRITICAL HISTORICAL CONTEXT LOADS]:\n"
        f"- User Core Identity: {active_memory.get('user_core_persona')}\n"
        f"- Mastered Coding Environments: {', '.join(active_memory.get('technical_stack_and_skills', []))}\n"
        f"- Dynamic Tech/Cyber Initiatives: {', '.join(active_memory.get('active_cyber_projects', []))}\n"
        f"- Strategic Lifecycle Inputs: {', '.join(active_memory.get('strategic_life_context', []))}\n"
        f"Integrate this data naturally into your problem-solving approaches without ever directly revealing the raw profile parameters to the user."
    )

# Inject or update the System Prompt at the head of the conversation log
if len(st.session_state.conversation_registry) == 0:
    st.session_state.conversation_registry.append({"role": "system", "content": dynamic_instruction})
else:
    # Keeps the system rule aligned with the latest background updates
    st.session_state.conversation_registry[0] = {"role": "system", "content": dynamic_instruction}

# Display Active Conversation Track
for message in st.session_state.conversation_registry:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# =====================================================================
# 5. REAL-TIME MULTI-THREAD RUNTIME LOOP
# =====================================================================
if user_prompt := st.chat_input("Pass a problem, logic vector, or system architecture task to solve..."):
    
    # 1. Commit and Render User Command
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.conversation_registry.append({"role": "user", "content": user_prompt})
    
    # 2. Compute Response via Isolated Stream
    with st.chat_message("assistant"):
        ui_stream_anchor = st.empty()
        accumulated_token_response = ""
        
        try:
            # Query Engine Matrix with Token Streaming
            stream_session = client.chat.completions.create(
                model=engine_tier,
                messages=st.session_state.conversation_registry,
                temperature=creativity_matrix,
                stream=True
            )
            
            # Reconstruct response on-the-fly to secure runtime stability
            for chunk in stream_session:
                if chunk.choices[0].delta.content:
                    accumulated_token_response += chunk.choices[0].delta.content
                    ui_stream_anchor.markdown(accumulated_token_response + "▌")
            
            # Lock-in clean execution result
            ui_stream_anchor.markdown(accumulated_token_response)
            
            # Append output trace back into short-term volatile context
            st.session_state.conversation_registry.append({"role": "assistant", "content": accumulated_token_response})
            
            # 3. Trigger Cognitive Synaptic Profiler to write back to the local database
            synthesize_new_memories(client, engine_tier, st.session_state.conversation_registry)
            
            # Instant UI refresh so the sidebar updates memories on the fly!
            st.rerun()
            
        except Exception as system_fault:
            # Critical Intercept Routine - Isolates runtime failures and prevents UI crash
            fault_report = f"🚨 **Runtime Intercept Active:** Execution dropped. Details: {str(system_fault)}"
            ui_stream_anchor.markdown(fault_report)
            st.sidebar.error("Internal processing fault. Verify API balance, authentication string, or framework limits.")