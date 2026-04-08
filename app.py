import gradio as gr
from fastapi import FastAPI, Request

# ---------------- ENV ----------------
class EVEnvironment:
    def __init__(self):
        self.reset()

    def reset(self):
        self.battery = 80
        self.distance = 50
        self.done = False
        return self.get_state()

    def step(self, action):
        if self.done:
            return self.get_state(), 0, self.done

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

        return self.get_state(), reward, self.done

    def get_state(self):
        return {"battery": self.battery, "distance": self.distance}


env = EVEnvironment()

# ---------------- FASTAPI ----------------
app = FastAPI()

@app.post("/reset")
async def reset():
    return {"state": env.reset()}

@app.post("/step")
async def step(request: Request):
    data = await request.json()
    action = data.get("action", 0)

    state, reward, done = env.step(action)

    return {
        "state": state,
        "reward": reward,
        "done": done
    }

# ---------------- GRADIO UI ----------------
def take_action(action):
    try:
        action = int(action)
    except:
        return "❌ Enter 0 or 1"

    state, reward, done = env.step(action)

    return f"{state} | Reward: {reward} | Done: {done}"


ui = gr.Interface(
    fn=take_action,
    inputs=gr.Textbox(label="Enter Action (0=Drive, 1=Charge)"),
    outputs="text",
    title="🚗 EV Simulator"
)

# 🔥 THIS IS THE KEY LINE
app = gr.mount_gradio_app(app, ui, path="/")
