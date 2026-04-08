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
api = FastAPI()

@api.post("/reset")
def reset():
    return {"state": env.reset()}

@api.post("/step")
def step(data: dict):
    action = data.get("action", 0)
    state, reward, done = env.step(action)
    return {
        "state": state,
        "reward": reward,
        "done": done
    }

# ---------------- GRADIO ----------------
def take_action(action):
    try:
        action = int(action)
    except:
        return "❌ Enter 0 or 1"

    state, reward, done = env.step(action)

    return f"{state} | Reward: {reward} | Done: {done}"


def reset_game():
    return str(env.reset())


ui = gr.Interface(
    fn=take_action,
    inputs=gr.Textbox(label="Enter Action (0=Drive, 1=Charge)"),
    outputs="text",
    title="🚗 EV Simulator"
)

# ---------------- RUN BOTH ----------------
def run_api():
    uvicorn.run(api, host="127.0.0.1", port=8000)

threading.Thread(target=run_api, daemon=True).start()

ui.launch()
