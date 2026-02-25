FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN playwright install chromium
RUN playwright install-deps
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

