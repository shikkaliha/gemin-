"""
Single-file ReAct AI Chatbot with Streamlit UI & CLI modes.
Powered by LangGraph, LangChain, and Groq (Free Tier Models).
Usage:
  Streamlit UI: streamlit run main.py
  Terminal CLI: python main.py
"""

import os
import sys
import math
import datetime
import warnings
from dotenv import load_dotenv

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

load_dotenv()

# Imports for LangChain / LangGraph / ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

# ==========================================
# 1. TOOL DEFINITIONS
# ==========================================

@tool
def calculator(a: float, b: float) -> str:
    """Useful for performing basic arithmetic addition with two numbers."""
    return f"The sum of {a} and {b} is {a + b}"

@tool
def advanced_math(expression: str) -> str:
    """Useful for calculating mathematical expressions like '2**10', 'sqrt(144)', 'cos(0)', '(15 * 8) / 4'.
    Input should be a valid mathematical expression string.
    """
    allowed_names = {
        "sin": math.sin, "cos": math.cos, "tan": math.tan,
        "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
        "exp": math.exp, "pi": math.pi, "e": math.e,
        "abs": abs, "round": round, "pow": pow
    }
    try:
        clean_expr = expression.strip().replace("^", "**")
        result = eval(clean_expr, {"__builtins__": None}, allowed_names)
        return f"Result: {clean_expr} = {result}"
    except Exception as err:
        return f"Error evaluating expression '{expression}': {str(err)}"

@tool
def say_hello(name: str) -> str:
    """Useful for greeting a user by their name."""
    return f"Hello {name}! I hope you are having a wonderful day."

@tool
def get_current_time() -> str:
    """Useful for getting the current local date and time."""
    now = datetime.datetime.now()
    return f"Current Date & Time: {now.strftime('%Y-%m-%d %H:%M:%S')}"

# List of tools provided to the agent
TOOLS = [calculator, advanced_math, say_hello, get_current_time]

# Active Free-Tier Groq Models
FREE_TIER_MODELS = {
    "qwen/qwen3.6-27b": "Qwen 3.6 27B (Recommended - Active Free Tier)",
    "openai/gpt-oss-20b": "GPT OSS 20B (Free Tier)",
    "openai/gpt-oss-120b": "GPT OSS 120B (Free Tier)"
}




# ==========================================
# 2. AGENT FACTORY
# ==========================================

def get_agent_executor(model_name: str, temperature: float = 0.2, api_key: str = None):
    """Initializes and returns a LangGraph ReAct agent with Groq LLM."""
    effective_key = api_key
    if not effective_key:
        try:
            import streamlit as st
            if "GROQ_API_KEY" in st.secrets:
                effective_key = st.secrets["GROQ_API_KEY"]
        except Exception:
            pass
    if not effective_key:
        effective_key = os.getenv("GROQ_API_KEY")

    if not effective_key:
        raise ValueError("GROQ_API_KEY is not set. Please set it in Streamlit Cloud Secrets, your .env file, or the sidebar override.")

    model = ChatGroq(
        model=model_name,
        temperature=temperature,
        groq_api_key=effective_key
    )

    system_prompt = (
        "You are Grok, an intelligent, helpful, and concise AI assistant. "
        "You have access to tools for math calculation, greetings, and real-time date/time checks. "
        "Use your tools whenever necessary to provide accurate answers."
    )

    try:
        agent = create_react_agent(model=model, tools=TOOLS, prompt=system_prompt)
    except TypeError:
        agent = create_react_agent(model=model, tools=TOOLS, state_modifier=system_prompt)

    return agent


# ==========================================
# 3. STREAMLIT SIMPLE GROK UI
# ==========================================

def run_streamlit_ui():
    import streamlit as st

    st.set_page_config(
        page_title="Grok AI Chatbot",
        page_icon="⚡",
        layout="centered"
    )

    # Simple Dark Grok Theme Styling
    st.markdown("""
        <style>
        .stApp {
            background-color: #0b0c10;
            color: #c5c6c7;
        }
        .header-title {
            font-size: 1.8rem;
            font-weight: 800;
            color: #66fcf1;
            margin-bottom: 0px;
        }
        .header-subtitle {
            color: #8892b0;
            font-size: 0.85rem;
            margin-bottom: 20px;
        }
        div[data-testid="stChatMessage"] {
            background-color: #1f2833 !important;
            border-radius: 12px !important;
            border: 1px solid #45a29e22 !important;
        }
        section[data-testid="stSidebar"] {
            background-color: #12141d;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
        <div>
            <h1 class="header-title">⚡ GROK AI</h1>
            <p class="header-subtitle">Groq Accelerated • Free-Tier Models • ReAct Agent</p>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar Options
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        # Free tier model dropdown
        selected_model = st.selectbox(
            "Groq Free Model",
            options=list(FREE_TIER_MODELS.keys()),
            format_func=lambda x: FREE_TIER_MODELS[x],
            index=0
        )

        temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.05)
        
        api_key_input = st.text_input("Groq API Key Override", type="password", placeholder="gsk_...")
        
        st.markdown("---")
        if st.button("🧹 Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # Session State Memory
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Chat History
    for msg in st.session_state.messages:
        role = msg["role"]
        avatar = "⚡" if role == "assistant" else "👤"
        with st.chat_message(role, avatar=avatar):
            if "tools" in msg and msg["tools"]:
                for t in msg["tools"]:
                    with st.expander(f"🔧 Tool: `{t['name']}`", expanded=False):
                        st.code(t['output'], language="text")
            st.markdown(msg["content"])

    # User Chat Input
    user_prompt = st.chat_input("Ask Grok anything or request calculations...")
    if user_prompt:
        # Save & display human message
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_prompt)

        # Generate Assistant response
        with st.chat_message("assistant", avatar="⚡"):
            response_box = st.empty()
            status_box = st.empty()
            status_box.markdown("⚡ *Thinking...*")
            
            collected_text = ""
            tool_logs = []

            try:
                # Initialize Agent
                agent = get_agent_executor(
                    model_name=selected_model,
                    temperature=temperature,
                    api_key=api_key_input.strip() if api_key_input else None
                )

                # Format chat history for agent
                history = []
                for m in st.session_state.messages[:-1]:
                    if m["role"] == "user":
                        history.append(HumanMessage(content=m["content"]))
                    elif m["role"] == "assistant":
                        history.append(AIMessage(content=m["content"]))
                history.append(HumanMessage(content=user_prompt))

                # Stream response & tools
                for chunk in agent.stream({"messages": history}):
                    if "tools" in chunk and "messages" in chunk["tools"]:
                        for t_msg in chunk["tools"]["messages"]:
                            t_name = getattr(t_msg, "name", "tool")
                            t_out = str(t_msg.content)
                            tool_logs.append({"name": t_name, "output": t_out})
                            status_box.markdown(f"🔧 *Executed tool `{t_name}`*")

                    if "agent" in chunk and "messages" in chunk["agent"]:
                        for a_msg in chunk["agent"]["messages"]:
                            if a_msg.content:
                                collected_text += a_msg.content
                                response_box.markdown(collected_text + " ▌")

                status_box.empty()
                response_box.markdown(collected_text)

                # Save assistant message to state
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": collected_text,
                    "tools": tool_logs
                })
                st.rerun()

            except Exception as err:
                status_box.empty()
                err_text = f"⚠️ Error: {str(err)}"
                response_box.markdown(err_text)
                st.session_state.messages.append({"role": "assistant", "content": err_text})


# ==========================================
# 4. CLI TERMINAL MODE
# ==========================================

def run_cli_mode():
    groq_key = os.getenv("GROQ_API_KEY")
    model_name = os.getenv("GROQ_MODEL", "qwen/qwen3.6-27b")



    print("=" * 60)
    print("⚡ GROK AI Assistant (CLI Mode)")
    print(f"Model: {model_name} (Free Tier)")
    print("=" * 60)

    if not groq_key:
        print("⚠️ Warning: GROQ_API_KEY is not set in environment.")

    try:
        agent = get_agent_executor(model_name=model_name)
    except Exception as e:
        print(f"Error initializing agent: {e}")
        return

    print("Type 'quit' to exit.")
    print("-" * 60)

    while True:
        try:
            user_input = input("\nYou > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["quit", "exit"]:
                print("\nGoodbye!")
                break

            print("\nGrok > ", end="", flush=True)
            for chunk in agent.stream({"messages": [HumanMessage(content=user_input)]}):
                if "agent" in chunk and "messages" in chunk["agent"]:
                    for msg in chunk["agent"]["messages"]:
                        print(msg.content, end="", flush=True)
                elif "tools" in chunk and "messages" in chunk["tools"]:
                    for msg in chunk["tools"]["messages"]:
                        print(f"\n[🔧 Tool Output: {msg.content}]\n", flush=True)
            print()
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as err:
            print(f"\n[Error: {err}]")


# ==========================================
# 5. ENTRYPOINT ROUTER
# ==========================================

if __name__ == "__main__":
    # Check if running via Streamlit
    try:
        import streamlit as st
        # If run via `streamlit run main.py`, st.runtime.exists() is True
        if st.runtime.exists():
            run_streamlit_ui()
        else:
            run_cli_mode()
    except Exception:
        run_cli_mode()
