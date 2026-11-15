import csv

from agent import run_agent, load_config, TOOLS
from task_set import TASKS


def evaluate(output_path="results.csv"):
    config = load_config()
    rows = []

    for task in TASKS:
        print(f"\n=== {task['id']}: {task['goal']} ===")
        result = run_agent(task["goal"], config, TOOLS)

        if result is None:
            answer, steps = "", config["step_budget"]
        else:
            answer, steps, _ = result

        try:
            passed = bool(task["correct_answer_check"](answer))
        except Exception as e:
            print(f"[{task['id']}] answer check failed: {e}")
            passed = False

        print(f"[{task['id']}] passed={passed} steps={steps}")
        rows.append({
            "id": task["id"],
            "goal": task["goal"],
            "answer": answer,
            "passed": passed,
            "steps": steps,
        })

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "goal", "answer", "passed", "steps"])
        writer.writeheader()
        writer.writerows(rows)

    return rows


if __name__ == "__main__":
    evaluate()
