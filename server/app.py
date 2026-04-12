from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

# ---------------- ENV ----------------
class EmailEnv:
    def __init__(self):
        self.tasks = [
            ("Meeting at 10 AM", "important"),
            ("Win money now!!!", "spam"),
            ("Client follow-up required", "work")
        ]
        self.index = 0
        self.done = False

    def reset(self):
        self.index = 0
        self.done = False
        return {"email": self.tasks[self.index][0]}

    def step(self, action):
        correct_label = self.tasks[self.index][1]

        reward = 1.0 if action.get("label") == correct_label else 0.0

        self.index += 1
        if self.index >= len(self.tasks):
            self.done = True

        return {"email": self.tasks[self.index-1][0]}, reward, self.done, {}


env = EmailEnv()

# ---------------- API ----------------
@app.post("/reset")
async def reset():
    return {
        "observation": env.reset(),
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

# ---------------- MAIN FUNCTION ----------------
def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

# REQUIRED ENTRY POINT
if __name__ == "__main__":
    main()
