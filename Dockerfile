
FROM manimcommunity/manim:stable

# Install FastAPI, uvicorn, and python-multipart using the correct Python environment
RUN python -m pip install --no-cache-dir fastapi uvicorn python-multipart streamlit google-generativeai

WORKDIR /app

COPY main.py .

RUN mkdir -p /app/artifacts

EXPOSE 8000

# Start FastAPI server
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

