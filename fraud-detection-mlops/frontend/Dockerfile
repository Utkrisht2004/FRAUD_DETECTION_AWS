FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir gradio requests
COPY ui.py .
EXPOSE 7860
CMD ["python", "ui.py"]