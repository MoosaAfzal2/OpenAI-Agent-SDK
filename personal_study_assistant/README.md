# Personal Study Assistant

## Project Overview

The **Personal Study Assistant** is an AI-powered tool designed to optimize study routines by leveraging multiple specialized agents. These agents work collaboratively to assist with scheduling, research, and summarization tasks, ensuring an efficient and streamlined study experience.

### Key Agents

- **Scheduler Agent**: Develops personalized study plans based on user-defined goals and deadlines.
- **Research Agent**: Gathers academic resources, including articles, videos, and papers.
- **Summarizer Agent**: Creates concise summaries of the gathered resources for quick review.

### Objectives

- Master the orchestration of multiple agents with distinct roles.
- Utilize the Responses API for web searches and file processing.
- Implement seamless task delegation and communication between agents.

### Features

1. **Agent Functionality**:
    - **Scheduler Agent**: Plans study schedules tailored to user inputs.
    - **Research Agent**: Fetches relevant academic materials.
    - **Summarizer Agent**: Produces brief, actionable summaries.

2. **User Inputs**:
    - A simple interface for entering study goals, topics, and deadlines.

3. **Tool Integration**:
    - Real-time web search using the Responses API.
    - Text processing for web results and uploaded files (e.g., PDFs).

4. **Agent Collaboration**:
    - Smooth task handoffs between Scheduler, Research, and Summarizer agents.

5. **Content Filtering**:
    - Exclude non-academic sources.
    - Limit summaries to concise, relevant information.

## Installation

To set up the **Personal Study Assistant**, follow these steps:

1. **Install Python**:
    - Ensure you have Python 3.8 or higher installed on your system. You can download it from [python.org](https://www.python.org/).

2. **Install `uv`**:
    - Use the following command to install the `uv` package:
      ```bash
      pip install uv
      ```

3. **Clone the Repository**:
    - Clone the project repository to your local machine:
      ```bash
      git clone https://github.com/your-repo/Agentic-AI/OpenAI-Agent-SDK.git
      cd personal_study_assistant
      ```

4. **Install Dependencies**:
    - Navigate to the project directory and install the required dependencies:
      ```bash
      pip install -r requirements.txt
      ```

5. **Run the Application**:
    - Start the project using one of the following commands:
      ```bash
      uv run personal-study-assistant
      ```
      OR
      ```bash
      uv run personal-study-assistant-app
      ```

You are now ready to use the **Personal Study Assistant**!
