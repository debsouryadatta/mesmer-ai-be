from contextlib import asynccontextmanager
import traceback
from fastapi import Depends, FastAPI
from fastapi.responses import StreamingResponse

from app.db import create_table, get_session
from app.lib.groq import get_response_from_groq
from app.models import User, Payload
from fastapi.middleware.cors import CORSMiddleware


# Creating a context manager so that we can connect to db & create tables before starting the app
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating Tables")
    create_table()
    # initialize_chatbot_resources()
    print("Tables Created")
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Chatbot BE",
    description="APIs for chatbot application",
)

origins = [
    "http://localhost:5173",
    "*",
    "https://support-chatbot-brown.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/get_response")
async def get_response(payload: Payload, session = Depends(get_session)):
    async def generate_response():
        try:
            user = session.query(User).filter(User.id == payload.user_id).first()
            if not user:
                yield "User not found"
                return

            chat_history = [*user.chat_history]
            full_response = ""

            async for chunk in get_response_from_groq(payload.user_input, chat_history):
                print(chunk)
                if chunk:  # Only process non-empty chunks
                    full_response += chunk
                    yield chunk

            # Update chat history in the user object
            new_user_message = {"role": "user", "content": payload.user_input}
            new_assistant_message = {"role": "assistant", "content": full_response}
            
            updated_chat_history = user.chat_history + [new_user_message, new_assistant_message]
            
            # Update the user in the database
            user.chat_history = updated_chat_history
            session.add(user)
            session.commit()
            session.refresh(user)

        except Exception as e:
            traceback.print_exc()
            yield f"Error: {str(e)}"

    return StreamingResponse(generate_response(), media_type="text/plain")



@app.post("/register")
async def register(user_info: User, session = Depends(get_session)):
    user = User(
        name=user_info.name,
        email=user_info.email,
        chat_history=[]
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"success": True, "user_id": user.id}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host = "0.0.0.0", port=5000, reload=True)
