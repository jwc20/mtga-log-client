import time
import requests

def poll_server(task_id: str, interval: int = 2):
    url = f"http://127.0.0.1:8000/task-status/{task_id}"
    while True:
        response = requests.get(url)
        data = response.json()
        print(f"Polled Task Status: {data}")
        if data.get("status") == "completed":
            print("Task completed!")
            break
        time.sleep(interval)

if __name__ == "__main__":
    task_id = "1234"
    print(f"Starting to poll for task {task_id}...")
    poll_server(task_id)