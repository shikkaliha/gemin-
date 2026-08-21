# ⚡ Grok AI Chatbot (LangGraph + Streamlit)

A high-performance conversational AI assistant built into a single file (`main.py`), powered by **Groq Free-Tier LPUs**, **LangGraph ReAct Agent**, and **Streamlit**.

---

## 📌 Features

- **⚡ Modern Dark UI & CLI Modes**: Clean dark Grok-themed Streamlit chat interface with custom avatars (`⚡` / `👤`), and a terminal CLI fallback mode.
- **🎁 Active Free-Tier Groq Models**: Pre-configured support for Groq's active free-tier models:
  - `qwen/qwen3.6-27b` *(Recommended - Active Free Tier)*
  - `openai/gpt-oss-20b` *(Free Tier)*
  - `openai/gpt-oss-120b` *(Free Tier)*
- **🔧 ReAct Agent Tool Calling**:
  - `advanced_math`: Evaluates complex expressions (`sqrt`, `sin`, `cos`, `log`, `pow`, etc.).
  - `calculator`: Basic arithmetic operations.
  - `get_current_time`: Retrieves the real-time system date and time.
  - `say_hello`: Personalized greetings.
- **🌊 Real-Time Streaming & Tool Logs**: Live token-by-token streaming with expandable tool execution badges.
- **⚙️ Sidebar Controls**: Dynamic model switching, temperature slider adjustment, custom Groq API key override, and one-click chat history clearing.
- **📁 Single-File Architecture**: Clean and modular codebase in `main.py` with zero unnecessary bloat.

---

## 📁 File Structure

```text
aigen/
├── .streamlit/
│   ├── config.toml           # Streamlit theme & server configuration
│   └── secrets.toml.example  # Example secrets configuration template
├── .env                      # Environment variables (GROQ_API_KEY, GROQ_MODEL)
├── .gitignore                # Git ignore file (excludes secrets & .venv)
├── .venv/                    # Python Virtual Environment
├── main.py                   # Single-file application (Streamlit UI & CLI Agent)
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Activate Virtual Environment & Install Dependencies

Make sure your virtual environment is activated before running the app:

**Windows PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Windows Command Prompt (cmd):**
```cmd
.\.venv\Scripts\activate.bat
pip install -r requirements.txt
```

**macOS / Linux:**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

> 💡 **Troubleshooting**: If you see `streamlit : The term 'streamlit' is not recognized`, ensure you have activated your virtual environment first (`.\.venv\Scripts\Activate.ps1`).

---

### 2. Configure Environment Variables

Create or edit your `.env` file in the project root:

```ini
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=qwen/qwen3.6-27b
```

Get your free Groq API key at [console.groq.com](https://console.groq.com/keys).

---

## 🎮 Running the Application

### Option A: Launch Streamlit Web UI (Recommended)

```bash
streamlit run main.py
```
> Opens automatically in your browser at `http://localhost:8501`.

### Option B: Terminal CLI Mode

```bash
python main.py
```
> Starts an interactive chat session directly in your terminal. Type `quit` or `exit` to exit.

---

## ☁️ Deploying to Streamlit Community Cloud (Free Tier)

Deploying your app for free on Streamlit Community Cloud takes only 3 minutes:

### Step 1: Push Code to GitHub

1. Initialize git and commit your files (ensuring `.gitignore` excludes `.env` and `.venv`):
   ```bash
   git init
   git add .
   git commit -m "Configure app for Streamlit Community Cloud deployment"
   ```
2. Create a public repository on [GitHub](https://github.com/new).
3. Connect and push your code:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Sign Up / Log In to Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/).
2. Click **Continue with GitHub** to log in using your GitHub account.

### Step 3: Deploy New App

1. Click the **"Create app"** or **"New app"** button in the top right.
2. Choose **"I already have an app"**.
3. Select your repository: `YOUR_USERNAME/YOUR_REPO_NAME`.
4. Set **Branch**: `main`.
5. Set **Main file path**: `main.py`.

### Step 4: Configure Secrets (Groq API Key)

1. Before clicking Deploy, expand **Advanced settings...** (or go to **App Settings > Secrets** after deployment).
2. In the **Secrets** text box, paste your Groq API Key format:
   ```toml
   GROQ_API_KEY = "gsk_your_actual_groq_api_key_here"
   ```
3. Click **Save** and **Deploy!**

---

## 📦 Dependencies

- `langchain-core`
- `langchain-groq`
- `langgraph`
- `python-dotenv`
- `streamlit`
