import sys
import os

# Add the project directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
#print("project root -> ",pr)
sys.path.append(project_root)

from fastapi import FastAPI
from utils import auth, routes
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from database.setup import check_and_create_database


app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await check_and_create_database()
        yield
    finally:
        print("Startup completed!")

app = FastAPI(lifespan=lifespan)


app.include_router(routes.router)
app.include_router(auth.router)