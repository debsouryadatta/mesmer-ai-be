FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir fastapi uvicorn python-dotenv faiss-cpu sqlmodel psycopg2-binary python-multipart beautifulsoup4 langchain-cohere groq requests passlib pyjwt

COPY . .

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload", "--port=5000"]