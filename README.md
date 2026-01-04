# 🌱 AURA AI

AURA AI  is an AI-powered chatbot for crop diagnostics that combines  
**retrieval-augmented generation (RAG)**, **rule-based agronomy logic**, and **live farm sensor data**.

The system provides farmers with clear, actionable insights about crop health and growth issues.

## Features

1. **Level 1 (Knowledge-based)**
     - Answers general farming questions using a vector database (Chroma + embeddings) & LLM.

2. **Level 2 (Data-driven Diagnosis)**

    - Uses live farm sensor data.
    - Applies deterministic diagnostic rules.
    - Explains issues and corrective actions using an LLM.

3. **Hybrid AI Design**

    - LLM used only for explanation and symptom classification.
    - Core diagnosis handled by rule engine to avoid hallucinations.

4. **Interactive Chatbot UI**
    - Built with Streamlit.
    - Farm sensor connection toggle.
    - Persistent chat history.


## Tech Stack

- **Python**
- **Streamlit** (UI)
- **LangChain**
- **Chroma DB** (Vector Store)
- **HuggingFace Sentence Transformers**
- **Groq LLM API**
- **Rule-based Expert System**

## Launching AURA AI

1. Clone this repository 
    ```bash
    git clone https://github.com/Sanmeet007/aura-chatbot-sanmeet.git
    ```

2. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

3. Set environment variables

   ```bash
   GROQ_API_KEY=your_api_key
   ```
    > You can get api key from `https://console.groq.com/keys` after registering

4. Navigate to the `aura-chatbot` directory
   ```
   cd aura-chatbot
   ```
5. Strt the app

   ```bash
   streamlit run app.py
   ```

## Notes

- Diagnostic accuracy is ensured using **explicit agronomy rules**.
- The LLM never invents sensor values or diagnoses.
- Designed for clarity, explainability, and reliability.
