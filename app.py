import gradio as gr
from fastapi import FastAPI
import uvicorn
import threading

# ---------------- ENV ----------------
class EVEnvironment:
    def __init__(self):
        self.reset()

    def reset(self):
        self.battery = 80
        self.distance = 50
        self.done = False
        return {"battery": self.battery, "distance": self.distance}

    def step(self, action):
        if self.done:
            return self.reset(), 0, self.done

        if action == 0:
            self.distance -= 10
            self.battery -= 15
        elif action == 1:
            self.battery += 20
            self.battery = min(self.battery, 100)

        if self.distance <= 0:
            reward = 10
            self.done = True
        elif self.battery <= 0:
            reward = -10
            self.done = True
        else:
            reward = 1

        return {"battery": self.battery, "distance": self.distance}, reward, self.done


env = EVEnvironment()

# ---------------- FASTAPI ----------------
app = FastAPI()

@app.post("/reset")
async def reset():
    return {"state": env.reset()}

@app.post("/step")
async def step(data: dict):
    action = data.get("action", 0)
    state, reward, done = env.step(action)
    return {"state": state, "reward": reward, "done": done}

# ---------------- GRADIO ----------------
def take_action(action):
    try:
        action = int(action)
    except:
        return "❌ Enter 0 or 1"

    state, reward, done = env.step(action)
    return f"{state} | Reward: {reward} | Done: {done}"


def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Run API in background
threading.Thread(target=run_api, daemon=True).start()

# Run UI
gr.Interface(
    fn=take_action,
    inputs="text",
    outputs="text",
    title="🚗 EV Simulator"
).launch()
