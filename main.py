from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import auth_route, task_route, friend_route, group_route

app = FastAPI(
    title="Online Shop API",
    version="1.0.0",
    description="FastAPI asosida qurilgan professional onlayn do'kon API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_route.auth_router, tags=["Authentication"])
app.include_router(task_route.task_router, tags=["task CRUD"])
app.include_router(friend_route.friend_router, tags=["friend CRUD"])
app.include_router(group_route.group_router, tags=["Group-> add_member, add_task"])

# Asosiy sahifa
@app.get("/")
async def root():
    return {"message": "Welcome to the Online Shop API!"}
