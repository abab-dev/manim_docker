# Manim Code Conversion Pipeline

This project provides a pipeline for converting natural language descriptions into Manim code, and then rendering the resulting animation. It consists of a FastAPI backend for code generation and rendering, and a Streamlit frontend for user interaction.

## Overview

The pipeline works as follows:

1.  The user provides a text description of the desired animation through the Streamlit frontend.
2.  The frontend sends this description to the FastAPI backend, along with the desired scene name.
3.  The FastAPI backend uses a language model (Gemini) to generate Manim code based on the description.
4.  The generated code is saved to a file, and Manim is used to render the animation.
5.  The rendered animation (as a video file) is made available for download.
6.  Logs from the Manim rendering process are streamed back to the frontend.

## Components

*   **FastAPI Backend (`main.py`):**  Handles the code generation and rendering logic. It exposes endpoints for converting text descriptions to Manim code and downloading the resulting video.
*   **Streamlit Frontend (`frontend/streamlit_app.py`):** Provides a user interface for submitting text descriptions and viewing the generated animations.
*   **Manim:** The core animation engine used to render the generated code.

## Setup

### Prerequisites

*   Python 3.9+
*   Poetry
*   FFmpeg

### Backend Setup

1.  Navigate to the project root directory.
2.  Create a virtual environment (optional but recommended):

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
3.  Install dependencies using Poetry:

    ```bash
    poetry install
    ```
4.  Activate the Poetry shell:

    ```bash
    poetry shell
    ```
5.  Set the `GOOGLE_API_KEY` environment variable:

    ```bash
    export GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
    ```

    Replace `"YOUR_GEMINI_API_KEY"` with your actual Gemini API key.
6.  Run the FastAPI backend:

    ```bash
    python main.py
    ```

### Frontend Setup

1.  Navigate to the `frontend` directory:

    ```bash
    cd frontend
    ```
2.  Create a virtual environment (optional but recommended):

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
3.  Install dependencies using Poetry:

    ```bash
    poetry install
    ```
4.  Activate the Poetry shell:

    ```bash
    poetry shell
    ```
5.  Set the `GOOGLE_API_KEY` environment variable in `frontend/streamlit_app.py`:

    ```python
    GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY"
    ```

    Replace `"YOUR_GEMINI_API_KEY"` with your actual Gemini API key.
6.  Run the Streamlit frontend:

    ```bash
    streamlit run streamlit_app.py
    ```

## Usage

1.  Open the Streamlit frontend in your browser (usually at `http://localhost:8501`).
2.  Enter a text description of the animation you want to create in the provided text box.
3.  Enter a name for the Manim scene.
4.  Click the "Generate Code" button.
5.  The frontend will send the description to the backend, which will generate the Manim code and render the animation.
6.  The logs from the Manim rendering process will be displayed in the Streamlit app.
7.  Once the rendering is complete, a download link will be provided to download the generated video.

## Configuration

*   **`GOOGLE_API_KEY`:**  The API key for the Gemini language model.  This needs to be set in both the backend and the frontend.
*   **`FASTAPI_URL`:**  The URL of the FastAPI backend.  This is configured in the frontend (`frontend/streamlit_app.py`).  The default value is `http://localhost:8000/convert/`.
*   **`ARTIFACTS_DIR`:** The directory where the generated video files are stored on the backend (`main.py`). The default value is `/app/artifacts`.

## Notes

*   Ensure that FFmpeg is installed and available in your system's PATH. Manim relies on FFmpeg for video encoding.
*   The quality of the generated code depends on the clarity and detail of the text description provided.
*   The first time you run the `streamlit_app.py`, it may take a few minutes to download the necessary dependencies.
