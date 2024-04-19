# In authentication.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.db_session import SessionLocal
from app.models.user import User
from .security import verify_password, create_access_token, get_current_user

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    #print("db -> ", db)
    try:
        yield db
    finally:
        db.close()

def authenticate_user(db: Session, email: str, password: str):
    
    try:
        user = db.query(User).filter(User.email == email).first()
        #print("user in authenticate_user -> ", user.email)
        #print("not user -> ", not user)
        if not user:
            #print("in if not user")
            return None  # User not found
        else:
            #print("\ndb password in authenticate user -> ", user.hashed_password)
            #print("not verify_user_password -> ", verify_password(password, user.hashed_password))
            if not verify_password(password, user.hashed_password):
                #print("in not verify_user_password -> ", verify_password(password, user.hashed_password))
                return None  # Incorrect password
        return user
    except Exception as e:
        print("Error during authentication:", e)
        return None


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    #print("user authenticate_user -> ", user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}

@router.get("/protected")
async def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": "This is a protected route", "username": current_user}
