from fastapi import FastAPI

from routes.query import router as query_router

app = FastAPI()
app.include_router(query_router)

