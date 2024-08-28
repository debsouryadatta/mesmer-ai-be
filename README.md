### Support Chatbot Backend

- Few notes on how I built it:
    - I have started up an fastApi server which is running on a docker container on my vps
    - For the Generative AI part, I have used groq library with the GROQ Api key
    - Implemented tool calling using latest groq tool calling models
    - Using groq's streaming response feature to send a streaming response to the frontend
    - Chat history is stored in a postgres database, if the user visits next time, the responses will be based on the previous chat history

