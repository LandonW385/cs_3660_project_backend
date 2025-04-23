import json
from datetime import datetime, timedelta

class MusicQueueRepository:
    @staticmethod
    def get_store_data(store_id: int):
        try:
            with open("./db/music_queues.json", "r") as file:
                data = json.load(file)
                return data["stores"].get(str(store_id), {"now_playing": None, "queue": []})
        except FileNotFoundError:
            return {"now_playing": None, "queue": []}

    @staticmethod
    def save_store_data(store_id: int, store_data: dict):
        try:
            with open("./db/music_queues.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {"stores": {}}

        data["stores"][str(store_id)] = store_data

        with open("./db/music_queues.json", "w") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def update_timer(store_id: int):
        store_data = MusicQueueRepository.get_store_data(store_id)
        now_playing = store_data.get("now_playing")

        if now_playing:
            # Calculate elapsed time
            last_updated = datetime.fromisoformat(now_playing.get("last_updated", datetime.now().isoformat()))
            elapsed = (datetime.now() - last_updated).total_seconds()

            # Update progress
            now_playing["progress"] += int(elapsed)
            now_playing["last_updated"] = datetime.now().isoformat()

            # If the song is finished, move to the next song
            if now_playing["progress"] >= now_playing["duration"]:
                queue = store_data.get("queue", [])
                if queue:
                    store_data["now_playing"] = queue.pop(0)
                    store_data["now_playing"]["progress"] = 0
                    store_data["now_playing"]["last_updated"] = datetime.now().isoformat()
                else:
                    store_data["now_playing"] = None

                store_data["queue"] = queue

        MusicQueueRepository.save_store_data(store_id, store_data)