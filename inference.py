import os
import requests
from openai import OpenAI

BASE_URL = "http://localhost:7860"

# ✅ Use hackathon provided proxy
client = OpenAI(
    base_url=os.environ["API_BASE_URL"],
    api_key=os.environ["API_KEY"]
)

def get_action_from_llm(email):
    prompt = f"Classify this email into one of: important, spam, work.\nEmail: {email}"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    output = response.choices[0].message.content.lower()

    if "spam" in output:
        return {"label": "spam"}
    elif "important" in output:
        return {"label": "important"}
    else:
        return {"label": "work"}


def run_task(task_name):
    print(f"[START] task={task_name}", flush=True)

    res = requests.post(f"{BASE_URL}/reset")
    data = res.json()

    total_reward = 0
    step_count = 0

    while True:
        email = data["observation"]["email"]

        # ✅ LLM decision
        action = get_action_from_llm(email)

        res = requests.post(f"{BASE_URL}/step", json=action)
        data = res.json()

        reward = data["reward"]
        done = data["done"]

        step_count += 1
        total_reward += reward

        print(f"[STEP] step={step_count} reward={reward}", flush=True)

        if done:
            break

    print(f"[END] task={task_name} score={total_reward} steps={step_count}", flush=True)


if __name__ == "__main__":
    run_task("easy")
    run_task("medium")
    run_task("hard")
