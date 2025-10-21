# API Generator Chatbot

A conversational AI tool that assists developers in generating API endpoints using FastAPI, based on natural language descriptions.

## 🧠 Overview

The API Generator Chatbot leverages OpenAI's GPT-3.5-turbo model to interpret user prompts and generate corresponding FastAPI code. This tool is designed to streamline the process of creating RESTful APIs by translating human-readable requirements into functional code snippets.

## ⚙️ Features

* **Natural Language Processing**: Understands user prompts to generate API code.
* **FastAPI Integration**: Generates code compatible with FastAPI framework.
* **Modular Code Generation**: Supports generation of models, routes, and utility functions.
* **Template-Based Responses**: Uses predefined templates to structure the generated code.

## 🛠️ Technologies Used

* **Backend**: Python, FastAPI
* **AI Model**: OpenAI GPT-3.5-turbo
* **Frontend**: Streamlit (for user interface)
* **Code Templates**: Jinja2 for templating
* **Data Storage**: Local file storage

## 🚀 Getting Started

### Prerequisites

* Python 3.8+
* OpenAI API Key
* Required Python packages (listed below)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/bhavi018/api-generator-chatbot.git
   cd api-generator-chatbot
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:

   * Create an `.env` file in the project root.
   * Add your API key:

     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

4. Run the application:

   ```bash
   streamlit run streamlit_app.py
   ```

   This will start the application and open it in your default web browser.

## 🧩 Project Structure

* `main.py`: Core application logic and API endpoint definitions.
* `models.py`: Data models for request and response handling.
* `storage.py`: Functions for saving and retrieving generated code.
* `utils.py`: Utility functions for various tasks.
* `streamlit_app.py`: Streamlit interface for user interaction.
* `templates/`: Directory containing code templates for FastAPI components.
* `fastapi_openapi.json`: OpenAPI schema for the generated API.

## 💡 Usage

1. Open the application in your browser.
2. Enter a natural language prompt describing the desired API functionality.
3. The chatbot will process the prompt and generate the corresponding FastAPI code.
4. Review the generated code and copy it to your project.


Feel free to customize this README further based on additional features or specific instructions related to your project.
