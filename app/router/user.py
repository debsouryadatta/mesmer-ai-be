import traceback
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.db import get_session
from app.lib.auth import create_access_token, get_current_user, hash_password, verify_password
from app.models import SigninPayload, SignupPayload, User



user_router = APIRouter(
    prefix="/api/user",
    tags=["user"],
    responses={404: {"description": "Not found"}}
)

# Sign up
@user_router.post("/signup")
async def signup(signup_payload: SignupPayload, session = Depends(get_session)):
    try:
        user = session.query(User).filter(User.email == signup_payload.email).first()
        if user:
            return JSONResponse(content={"success": False, "message": "User already exists"}, status_code=400)
        user = User(name=signup_payload.name, email=signup_payload.email, password=hash_password(signup_payload.password))
        session.add(user)
        session.commit()
        return JSONResponse(content={"success": True, "message": "User created successfully"}, status_code=201)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    

# Sign in
@user_router.post("/signin")
async def signin(signin_payload: SigninPayload, session = Depends(get_session)):
    try:
        user = session.query(User).filter(User.email == signin_payload.email).first()
        if not user:
            return JSONResponse(content={"success": False, "message": "Wrong credentials"}, status_code=404)
        if not verify_password(signin_payload.password, user.password):
            return JSONResponse(content={"success": False, "message": "Wrong credentials"}, status_code=404)
        
        access_token = create_access_token(data={"sub": user.email, "name": user.name})
        return JSONResponse(content={"success": True, "access_token": access_token}, status_code=200)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    


@user_router.get("/me")
async def me(current_user: str = Depends(get_current_user), session = Depends(get_session)):
    try:
        user = session.query(User).filter(User.email == current_user).first()
        if not user:
            return JSONResponse(content={"success": False, "message": "User not found"}, status_code=404)
        return JSONResponse(content={"success": True, "name": user.name, "email": user.email}, status_code=200)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
        
        
        
        
