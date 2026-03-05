from fastapi import FastAPI

app = FastAPI(title="AI Carousel Generator")

@app.get("/")
def root():
    return {"status": "ok"}
