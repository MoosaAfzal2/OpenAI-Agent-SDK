# Research Bot

This is a simple example of a multi-agent research bot.

## How to Run

### 🔧 CLI mode

Run the research bot from the terminal:

```bash
uv run research_bot
```

### 🖥️ Streamlit mode

Launch the Streamlit web app:

```bash
uv run streamlit run src/research_bot/main.py
```

---

## Installation (with [`uv`](https://github.com/astral-sh/uv))

Make sure you have `uv` installed:

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

Then install dependencies:

```bash
uv pip install
```

Set up your `.env` file with the required API keys:

```env
OPENAI_API_KEY=your-openai-key (optional, used for tracing/debugging purposes)
TAVILY_API_KEY=your-tavily-key
GEMINI_API_KEY=your-gemini-key
```

---

## Architecture

The flow is:

1. User enters their research topic
2. `planner_agent` comes up with a plan to search the web for information. The plan is a list of search queries, with a search term and a reason for each query.
3. For each search item, we run a `search_agent`, which uses the Web Search tool to search for that term and summarize the results. These all run in parallel.
4. Finally, the `writer_agent` receives the search summaries, and creates a written report.

---

## Suggested Improvements

If you're building your own research bot, some ideas to add to this are:

1. **Retrieval**: Add support for fetching relevant information from a vector store. You could use the File Search tool for this.
2. **Image and file upload**: Allow users to attach PDFs or other files, as baseline context for the research.
3. **More planning and thinking**: Models often produce better results given more time to think. Improve the planning process to come up with a better plan, and add an evaluation step so that the model can choose to improve its results, search for more stuff, etc.
4. **Code execution**: Allow running code, which is useful for data analysis.

---

## Requirements

- Python 3.12+
- [`uv`](https://github.com/astral-sh/uv)

---

## License

MIT
