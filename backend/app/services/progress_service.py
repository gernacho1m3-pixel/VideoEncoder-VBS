progress = {}


def set_progress(task_id: str, value: int):
    progress[task_id] = value


def get_progress(task_id: str):
    return progress.get(task_id, 0)


def remove_progress(task_id: str):
    progress.pop(task_id, None)