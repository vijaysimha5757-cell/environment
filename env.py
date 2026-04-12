from pydantic import BaseModel

class Observation(BaseModel):
    email: str

class Action(BaseModel):
    label: str

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
        return Observation(email=self.tasks[self.index][0]).dict()

    def step(self, action):
        correct_label = self.tasks[self.index][1]

        if action["label"] == correct_label:
            reward = 1.0
        else:
            reward = 0.0

        self.index += 1

        if self.index >= len(self.tasks):
            self.done = True

        obs = {"email": self.tasks[self.index-1][0]}

        return obs, reward, self.done, {}

    def state(self):
        return {"index": self.index}
