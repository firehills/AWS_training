from fastapi import FastAPI, Request


app = FastAPI()

@app.get("/")
async def root():
    return {"message":"You've found the home page!"}


