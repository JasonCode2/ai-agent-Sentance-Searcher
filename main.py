from fastapi import FastAPI
from agent import run_agent

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Agent running"}

@app.post("/chat")
def chat(query: str):
    result = run_agent(query)
    return {"response": result}