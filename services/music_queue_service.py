from datetime import datetime
from repositories.music_queue_repository import MusicQueueRepository
from fastapi import HTTPException

class MusicQueueService:
    DOWNVOTE_THRESHOLD = 5  # Define the threshold for skipping a song

    @staticmethod
    def get_store_data(store_id: int):
        # Fetch the store data
        store_data = MusicQueueRepository.get_store_data(store_id)

        # Ensure the listeners field exists
        if "listeners" not in store_data:
            store_data["listeners"] = 0

        # Auto-start the first song in the queue if "Now Playing" is empty
        if not store_data.get("now_playing") and store_data.get("queue"):
            first_song = store_data["queue"].pop(0)  # Remove the first song from the queue
            first_song["progress"] = 0
            first_song["last_updated"] = datetime.now().isoformat()
            store_data["now_playing"] = first_song

        # Update the timer to handle progress and song transitions
        now_playing = store_data.get("now_playing")
        if now_playing:
            # Ensure "progress" exists in the now_playing object
            if "progress" not in now_playing:
                now_playing["progress"] = 0  # Initialize progress if missing

            # Ensure "duration" exists in the now_playing object
            if "duration" not in now_playing:
                raise KeyError("'duration' field is missing in the 'now_playing' object")

            last_updated = datetime.fromisoformat(now_playing.get("last_updated", datetime.now().isoformat()))
            elapsed_time = (datetime.now() - last_updated).total_seconds()

            # Update progress
            now_playing["progress"] += int(elapsed_time)
            now_playing["last_updated"] = datetime.now().isoformat()

            # If the song is finished, move to the next song
            if now_playing["progress"] >= now_playing["duration"]:
                queue = store_data.get("queue", [])
                if queue:
                    next_song = queue.pop(0)
                    next_song["progress"] = 0
                    next_song["last_updated"] = datetime.now().isoformat()
                    store_data["now_playing"] = next_song
                else:
                    store_data["now_playing"] = None

                store_data["queue"] = queue

        # Save any changes to the store data
        MusicQueueRepository.save_store_data(store_id, store_data)

        return {
            "now_playing": store_data.get("now_playing"),
            "queue": store_data.get("queue", []),
            "listeners": store_data.get("listeners", 0)  # Include listeners count
        }

    @staticmethod
    def add_to_queue(store_id: int, track_data: dict):
        # Fetch the store data
        store_data = MusicQueueRepository.get_store_data(store_id)
        queue = store_data.get("queue", [])

        # Ensure the track_data contains the "duration" field
        if "duration" not in track_data:
            raise KeyError("'duration' field is missing in the track data")

        if not store_data["now_playing"]:
            # If nothing is playing, start playing the song immediately
            store_data["now_playing"] = track_data
            store_data["now_playing"]["progress"] = 0
            store_data["now_playing"]["last_updated"] = datetime.now().isoformat()
        else:
            # Otherwise, add the song to the queue
            queue.append(track_data)

        store_data["queue"] = queue
        MusicQueueRepository.save_store_data(store_id, store_data)

    @staticmethod
    def skip_song(store_id: int):
        # Fetch the store data
        store_data = MusicQueueRepository.get_store_data(store_id)
        queue = store_data.get("queue", [])

        # Skip the current song and move to the next one
        if queue:
            next_song = queue.pop(0)  # Remove the first song from the queue
            next_song["progress"] = 0
            next_song["last_updated"] = datetime.now().isoformat()
            store_data["now_playing"] = next_song
        else:
            # If the queue is empty, stop playing
            store_data["now_playing"] = None

        store_data["queue"] = queue
        MusicQueueRepository.save_store_data(store_id, store_data)

        return store_data

    @staticmethod
    def play_next(store_id: int, song_index: int):
        # Fetch the store data
        store_data = MusicQueueRepository.get_store_data(store_id)
        queue = store_data.get("queue", [])

        # Ensure the song index is valid
        if song_index < 0 or song_index >= len(queue):
            raise IndexError("Invalid song index")

        # Move the selected song to the front of the queue
        song_to_move = queue.pop(song_index)
        queue.insert(0, song_to_move)

        store_data["queue"] = queue
        MusicQueueRepository.save_store_data(store_id, store_data)

        return store_data

    @staticmethod
    def increment_listeners(store_id: int, session_id: str):
        # Fetch the store data
        store_data = MusicQueueRepository.get_store_data(store_id)

        # Ensure the listeners field exists
        if "listeners" not in store_data:
            store_data["listeners"] = 0
        if "active_sessions" not in store_data:
            store_data["active_sessions"] = set()

        # Add the session ID to the active sessions
        if session_id not in store_data["active_sessions"]:
            store_data["active_sessions"].add(session_id)
            store_data["listeners"] += 1

        # Save the updated store data
        MusicQueueRepository.save_store_data(store_id, store_data)

        return {"listeners": store_data["listeners"]}

    @staticmethod
    def decrement_listeners(store_id: int, session_id: str):
        # Fetch the store data
        store_data = MusicQueueRepository.get_store_data(store_id)

        # Ensure the listeners field exists
        if "listeners" not in store_data:
            store_data["listeners"] = 0
        if "active_sessions" not in store_data:
            store_data["active_sessions"] = set()

        # Remove the session ID from the active sessions
        if session_id in store_data["active_sessions"]:
            store_data["active_sessions"].remove(session_id)
            store_data["listeners"] = max(store_data["listeners"] - 1, 0)

        # Save the updated store data
        MusicQueueRepository.save_store_data(store_id, store_data)

        return {"listeners": store_data["listeners"]}

    @staticmethod
    def vote_now_playing(store_id: int, session_id: str, vote_type: str):
        # Fetch the store data
        store_data = MusicQueueRepository.get_store_data(store_id)

        # Ensure there is a song currently playing
        now_playing = store_data.get("now_playing")
        if not now_playing:
            raise HTTPException(status_code=400, detail="No song is currently playing")

        # Ensure the "voters" field exists in the now_playing object
        if "voters" not in now_playing:
            now_playing["voters"] = {}

        # Check if the user has already voted for this song
        if session_id in now_playing["voters"]:
            raise HTTPException(status_code=400, detail="You have already voted for this song")

        # Process the vote
        if vote_type == "upvote":
            now_playing["votes"] = now_playing.get("votes", 0) + 1
        elif vote_type == "downvote":
            now_playing["votes"] = now_playing.get("votes", 0) - 1
        else:
            raise HTTPException(status_code=400, detail="Invalid vote type")

        # Record the user's vote
        now_playing["voters"][session_id] = vote_type

        # Save the updated store data
        MusicQueueRepository.save_store_data(store_id, store_data)

        return store_data