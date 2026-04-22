from fastapi import FastAPI

print("Hello World")
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}