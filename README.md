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

## Launching / Running AURA AI

1. **Clone this repository**

   ```bash
   git clone https://github.com/Sanmeet007/aura-chatbot-sanmeet.git
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**

   You can choose **either** of the following methods:

   **Option A: Using `.env.local` (recommended)**

   * Create a `.env.local` file inside the `aura-ai directory` (project root → aura-chatbot)
   * Add your Groq API key:

     ```env
     GROQ_API_KEY="your_api_key"
     ```

   **Option B: Using command line**

   ```bash
   export GROQ_API_KEY=your_api_key
   ```

   > You can get the API key from [https://console.groq.com/keys](https://console.groq.com/keys) after registering.

4. **Navigate to the project directory -> aura-chatbot**

   ```bash
   cd aura-chatbot-sanmeet/aura-chatbot
   ```

5. **Start the application**

   ```bash
   streamlit run app.py
   ```
## Working

1. The user asks a question through the Streamlit chatbot interface.
2. If no farm is connected, AURA AI uses **Level 1**:

   * Retrieves relevant information from the agricultural knowledge base using **Chroma vector search**.
   * Generates a general explanation using the LLM.
3. If a farm is connected, AURA AI uses **Level 2**:

   * The LLM first classifies the user's question into a **base symptom**.
   * Live farm sensor data is fetched and evaluated using **rule-based diagnostic logic**.
   * The rule engine identifies the most likely causes and corrective actions.
   * The LLM then explains the diagnosis using sensor values, rules, and knowledge base context.
4. The final response is displayed in the chat with clear diagnosis, evidence, and recommended actions.

This hybrid approach ensures **accurate, explainable, and non-hallucinated responses**.


## Test Cases

### **Test Case 1: Level 1 – RAG System**

**Question:**
`Why is my lettuce growing slowly?`

**Expected:**

* Searches the vector database.
* Retrieves relevant agricultural knowledge entries.
* Uses the LLM to generate a natural language response.
* Response mentions possible causes such as:

  * Temperature
  * Nutrient availability
  * Light conditions

### **Test Case 2: Level 2 – Rule-Based Diagnosis**

**Farm:** `farm_102` (Low EC)
**Question:**
`Why is my lettuce yellowing?`

**Expected:**

* Identifies EC value (`0.8 mS/cm`) as below optimal range.
* Diagnoses nutrient deficiency.
* Suggests increasing nutrient concentration to correct EC levels.


### **Test Case 3: Level Switching**

1. Ask a question without connecting farm sensors.
2. Observe a **Level 1** (knowledge-based) response.
3. Connect farm sensors.
4. Ask the same question again.

**Expected:**

* First response uses general knowledge (Level 1).
* Second response uses live sensor data and rules (Level 2).

## Notes

- Diagnostic accuracy is ensured using **explicit agronomy rules**.
- The LLM never invents sensor values or diagnoses.
- Designed for clarity, explainability, and reliability.
