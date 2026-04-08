from fastapi import FastAPI, Request

app = FastAPI()

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

# ---------------- API ----------------

@app.post("/reset")
async def reset():
    return {
        "observation": env.reset(),
        "reward": 0,
        "done": False,
        "info": {}
    }

@app.post("/step")
async def step(request: Request):
    data = await request.json()
    action = data.get("action", 0)

    obs, reward, done = env.step(action)

    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": {}
    }
