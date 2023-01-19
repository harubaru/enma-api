import os
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline

from models import Completion

app = FastAPI(
    title="Enma Inference API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

args = {
    "model": os.getenv("INFERENCE_MODEL", "../distilgpt2"),
    "device": int(os.getenv("INFERENCE_DEVICE", 0)),
    "port": int(os.getenv("INFERENCE_PORT", 8080))
}

model = pipeline("text-generation", model=args["model"], device=args["device"])

@app.post("/completion")
async def completion(completion: Completion):
    try:
        return model(
            completion.prompt,
            max_new_tokens=completion.max_new_tokens,
            temperature=completion.temperature,
            top_p=completion.top_p,
            top_k=completion.top_k,
            repetition_penalty=completion.repetition_penalty,
            do_sample=completion.do_sample,
            penalty_alpha=completion.penalty_alpha,
            num_return_sequences=completion.num_return_sequences,
            stop_sequence=completion.stop_sequence
        )
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(
        "inference:app",
        host="0.0.0.0",
        port=args["port"]
    )