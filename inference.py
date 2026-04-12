import requests

BASE_URL = "http://localhost:7860"

def run_env():
    # Reset environment
    res = requests.post(f"{BASE_URL}/reset")
    data = res.json()

    total_reward = 0

    for _ in range(3):
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

        total_reward += data["reward"]

        if data["done"]:
            break

    print("Final Score:", total_reward)


if __name__ == "__main__":
    run_env()
