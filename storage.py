from pathlib import Path
import pickle


def save_data(data, filename: str):
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(data, f)


def load_data(filename: str):
    path = Path(filename)
    if path.exists():
        with open(path, "rb") as f:
            return pickle.load(f)
    return None
