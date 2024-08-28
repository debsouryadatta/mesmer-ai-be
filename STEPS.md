### Steps of Dev:

1. pip install poetry(on the python env) never do it in the system, faced a big fat kde error.

2. `poetry new app`, `cd app`

3. `poetry add fastapi uvicorn sqlmodel`

4. `poetry add pydantic typing-extensions langchain chromadb`

5. `poetry add pysqlite3-binary=0.5.2`

6. `poetry run uvicorn app.main:app --reload`

7. `poetry add python-dotenv langchain_openai langchain_core langchain_community langchain pypdf faiss-cpu`

8. Adding USER_AGENT, OPENAI_API_KEY, DATABASE_URL in the .env file

9. Switching to Postgres, having problem with the pysqlite3-binary at the production.

<!-- Pinecone -->
10. `pip install pinecone-client` , Adding PINECONE_API_KEY in .env

11. `pip install --upgrade langchain langchain-pinecone pinecone-client`

12. `pip install python-multipart` for file upload

13. `pip install openai-function-call`