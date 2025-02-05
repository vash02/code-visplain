[DEMO_VIDEO]https://github.com/vash02/code-visplain/blob/main/static/code_visplain_demo.mov
# 📌 Code-Visplain

🚀 **Code-Visplain** is an AI-powered tool that **analyzes, summarizes, and visualizes** codebases. It helps developers understand the **execution flow, component interactions, and key parameters** in a structured and intuitive manner particularly for AI model codebases.

## 🌟 Features
- 🔷 **Component Graphs**: Shows **class-level relationships** within the repository.
- 📊 **Block Diagrams**: High-level **execution flow visualization**.
- 🤖 **AI-Powered Summaries**: Uses **LLaMA 3.2** to generate **detailed explanations**.
- 🔄 **Execution Order Detection**: Uses **topological sorting** for function dependencies.
- 🏗 **Supports GitHub Repositories**.

---

## 📸 Screenshots

### 🔷 **Sample Generated Block Diagram**
![block_diagram.png](static%2Fblock_diagram.png)

### 📄 **Sample Component Summaries**
![Screenshot 2025-02-04 at 11.40.52 PM.png](..%2F..%2F..%2F..%2Fvar%2Ffolders%2Fq3%2Fmq53py8958ndz_blwtj161xm0000gn%2FT%2FTemporaryItems%2FNSIRD_screencaptureui_u6Qd1C%2FScreenshot%202025-02-04%20at%2011.40.52%E2%80%AFPM.png)


---

## 🛠 Tech Stack
- 🔹 **Frontend**: React.js (Flask API Calls)
- 🔹 **Backend**: Flask (Python)
- 🔹 **AI Model**: LLaMA 3.2 (Component Extraction & Summaries)
- 🔹 **Graph Processing**: NetworkX, Graphviz

---

## 📂 Project Structure
```plaintext
code-visplain/
│── frontend/          # React.js frontend
│── components/        # Core backend modules
│── app.py             # Main Flask app
│── config.py          # Configuration settings
│── requirements.txt   #Required package names
│── README.md          # Project documentation
```
## 🚀 Local Setup Instructions for Code-Visplain

## 📌 Prerequisites

Before setting up the project, ensure you have the following installed:

- **Python** (>= 3.8)
- **pip** (Python package manager)
- **Node.js** (for frontend, >= 14.x)
- **Git** (to clone the repository)
- **virtualenv** (recommended for dependency management)

---

## ⚙️ Backend Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/code-visplain.git
cd code-visplain
```
### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```
### 3️⃣ Install Dependencies
```bash 
pip install -r requirements.txt
```
### 4️⃣ Set Up Configuration
Add you git personal access token in the config.py file
```bash
GITHUB_TOKEN=<your_github_personal_access_token>
LLM_MODEL_NAME="llama3.2"   # Modify if using a different model
```
## 🎨 Frontend Setup (React.js)
### 1️⃣ Navigate to the Frontend Directory
```bash
cd frontend
```
### 2️⃣ Install Dependencies
```bash
npm install
```
### 3️⃣ Start the React Frontend
```bash
npm start
```
This will start the frontend on http://localhost:3000/.

## 🚀 Running the Backend (Flask)
### 1️⃣ Navigate Back to the Root Directory
```bash
cd ..
```
### 2️⃣ Run the Flask Backend
```bash
python app.py
```
This will start the backend on http://127.0.0.1:5000/.

## 🎯 Features
- Extracts execution order of components
- Generates structured repository summaries
- Visualizes class-based execution flow as a block diagram
- Uses LLMs (Llama 3.2) for insights
- Supports GitHub repository analysis

## 🛠️ Planned Enhancements
- 🔹 Multi-language support (currently Python-only)
- 🔹 More detailed function-level analysis
- 🔹 Improving determination of execution order 
- 🔹 Improved dependency tracking across files
- 🔹 Interactive UI for block diagram elements
- 🔹 Using metadata files other than code files to enhance results
