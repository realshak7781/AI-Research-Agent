
# 🧠 Autonomous AI Research Agent 

An asynchronous, self-correcting AI research system built with **LangGraph**, **Google Gemini**, and **Tavily**. 

**The concept is simple but the execution is agentic:** Ask a complex question, and the agent will autonomously plan a research strategy, scrape the web, critique its own findings, and iteratively gather more data until it has enough context to write a comprehensive, technical Markdown report.



## 🎯 Why I Built This (Project Goals)
I built this project to move beyond simple, linear LLM wrappers (like basic RAG pipelines) and engineer a true **Cyclic Agentic Workflow**. The goal was to build a system capable of "First Principles" thinking: breaking down problems, evaluating data quality, and self-correcting without human hand-holding.

## 🏗️ System Architecture & Data Flow

The system operates as a **State Machine**, where a shared `ResearchState` object is mutated by highly specialized node functions:

1. **Planner Node (The Brain):** Decomposes a broad user query into a strict Pydantic schema of 3-5 high-intent search tasks.
2. **Researcher Node (The Eyes):** Acts as a tool-calling agent, hitting the live internet via the Tavily API and appending raw data to the state memory.
3. **Critic Node (The Judge):** Evaluates the gathered research against strict criteria (e.g., technical depth, specific timelines). It outputs a structured boolean decision on whether the data is sufficient.
4. **The Router (Conditional Edges):** If the Critic fails the data, the Router loops the graph back to the Researcher. If it passes, it routes to the Writer.
5. **Writer Node (The Scribe):** Synthesizes the accumulated (and potentially massive) context window into a deduplicated, heavily formatted Markdown report.

## 💡 Key Technical Learnings for AI Engineering

* **Stateful Graph Orchestration:** Mastered LangGraph's `StateGraph` to manage asynchronous node transitions and cyclic loops, proving that LLMs are best utilized as reasoning engines within a broader software architecture.
* **Structured Data Contracts:** Utilized `Pydantic` and `.with_structured_output()` to force the LLM to return strict JSON, ensuring deterministic data flow between nodes.
* **State Accumulation:** Implemented `operator.add` in the State Schema to safely append history (handling up to 40k+ characters of dynamic context) without overwriting previous research passes.
* **Defensive AI Programming:** Engineered safeguards against "infinite LLM loops" by implementing backward array iteration for safe context extraction and strict recursion limits.
* **Modern Python Tooling:** Managed the entire project environment using `uv`, ensuring 10x faster dependency resolution and fully reproducible builds.

## 🛠️ Tech Stack
* **Orchestration:** LangGraph / LangChain Core
* **Intelligence:** Google Gemini 2.5 Flash
* **Search / Tooling:** Tavily API (Optimized for LLM context windows)
* **Data Validation:** Pydantic (v2)
* **Environment:** Python 3.10+, `uv`, `python-dotenv`

## 🚀 Quick Start

1. Clone the repository.
2. Ensure you have [uv](https://github.com/astral-sh/uv) installed.
3. Sync the environment:
   ```bash
   uv sync

```

4. Create a `.env` file in the root directory:
GOOGLE_API_KEY=your_gemini_key
TAVILY_API_KEY=your_tavily_key

```


5. Ignite the agent:
```bash
uv run python main.py

```



