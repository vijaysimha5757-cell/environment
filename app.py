from fastapi import FastAPI, Request
from env import EmailEnv

app = FastAPI()
env = EmailEnv()

@app.post("/reset")
async def reset():
    obs = env.reset()
    return {
        "observation": obs,
        "reward": 0.0,
        "done": False,
        "info": {}
    }

@app.post("/step")
async def step(request: Request):
    data = await request.json()

    obs, reward, done, info = env.step(data)

    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/")
def root():
    return {"message": "OpenEnv Email Environment Running"}
