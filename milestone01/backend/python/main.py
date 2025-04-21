from fastapi import FastAPI, Request


app = FastAPI()

@app.get("/")
async def root():
    return {"message":"You've found Phils home page!"}

@app.get("/health")
async def health():
    return {"status":"Alive!"}
