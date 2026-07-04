import threading

tasks = {}


def run_background(task_id, target, *args):

    thread = threading.Thread(
        target=target,
        args=args,
        daemon=True
    )

    tasks[task_id] = thread
    thread.start()