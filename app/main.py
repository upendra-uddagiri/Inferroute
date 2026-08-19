from fastapi import FastAPI
app = FastAPI(
    title="InferRoute",
    version="1.0.0"
)
@app.get("/")
def root():
    return {
        "message": "InferRoute is running"
    }