from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "🚀 API online com FastAPI e Hypercorn no Render!"}
