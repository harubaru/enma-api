import os
import uvicorn
import yaml
import aiohttp
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import Completion, Feedback

app = FastAPI(
    title="Enma API Gateway"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

args = {
    "config": os.getenv("GATEWAY_CONF", "gateway-conf.yaml"),
    "port": int(os.getenv("GATEWAY_PORT", 80))
}

with open(args["config"], "r") as f:
    config = yaml.safe_load(f)

@app.get("/engines")
async def engines():
    all_engines = []
    for engine in config["models"].keys():
        all_engines.append({
            "name": engine,
            "author": config["models"][engine]["author"],
            "description": config["models"][engine]["description"]
        })
    return {"engines": all_engines}

@app.post("/completion")
async def completion(completion: Completion):
    if completion.engine is None:
        raise Exception("Engine not specified")
    engine_endpoint = config["models"][completion.engine]["url"]
    async with aiohttp.ClientSession() as session:
        async with session.post(engine_endpoint, json=completion.dict()) as resp:
            return await resp.json()

@app.post("/feedback")
async def feedback(f_: Feedback):
    with open('feedback.jsonl', 'a') as f:
        f.write(f'{f_.json()}\n')
    return "OK"

@app.get("/")
async def root():
    return "Sometimes I dream about cheese."

if __name__ == "__main__":
    uvicorn.run(
        "gateway:app",
        host="0.0.0.0",
        port=args["port"]
    )
