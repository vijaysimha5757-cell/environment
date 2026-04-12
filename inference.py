import requests

BASE_URL = "http://localhost:7860"

def run_task(task_name):
    print(f"[START] task={task_name}", flush=True)

    res = requests.post(f"{BASE_URL}/reset")
    data = res.json()

    total_reward = 0
    step_count = 0

    while True:
        email = data["observation"]["email"]

        # Simple rule-based agent
        if "win" in email.lower():
            action = {"label": "spam"}
        elif "meeting" in email.lower():
            action = {"label": "important"}
        else:
            action = {"label": "work"}

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
    # Run all 3 tasks
    run_task("easy")
    run_task("medium")
    run_task("hard")
