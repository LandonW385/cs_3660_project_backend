from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from services.music_queue_service import MusicQueueService
from repositories.user_repository import UserRepository  # Import the user repository

router = APIRouter(prefix="/api/music-queue", tags=["Music Queue"])

class TrackRequest(BaseModel):
    song: str
    artist: str
    albumArt: str
    duration: int
    votes: int = 0

@router.get("/coins")
def get_user_coins(request: Request):
    """
    Retrieve the user's coin count.
    """
    try:
        username = request.headers.get("X-Username")  # Use a custom header to identify the user
        print(f"Received X-Username header: {username}")  # Debug statement

        if not username:
            raise HTTPException(status_code=400, detail="Username is required")

        # Fetch user data from the repository
        user_data = UserRepository.get_user_by_username(username)
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")

        # Return the coin count
        return {"coins": user_data.coins}  # Access the coins attribute directly
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{store_id}")
def get_store_data(store_id: int):
    return MusicQueueService.get_store_data(store_id)

@router.post("/{store_id}/queue")
def add_to_queue(store_id: int, track: TrackRequest):
    try:
        MusicQueueService.add_to_queue(store_id, track.dict())
        return {"message": "Track added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{store_id}/skip")
def skip_song(store_id: int, request: Request):
    """
    Skip the currently playing song in the store's queue.
    """
    try:
        username = request.headers.get("X-Username")  # Use X-Username to identify the user
        if not username:
            raise HTTPException(status_code=400, detail="Username is required")

        # Fetch the user's coin balance
        user_data = UserRepository.get_user_by_username(username)
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")

        if user_data.coins < 10:  # Require 10 coins to skip
            raise HTTPException(status_code=400, detail="Not enough coins to skip the song")

        # Deduct coins and save the user data
        user_data.coins -= 10
        UserRepository.save_user_data(username, user_data)

        # Perform the skip action
        result = MusicQueueService.skip_song(store_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{store_id}/play-next/{song_index}")
def play_next(store_id: int, song_index: int, request: Request):
    """
    Move a song to the front of the queue to play next.
    """
    try:
        username = request.headers.get("X-Username")  # Use X-Username to identify the user
        if not username:
            raise HTTPException(status_code=400, detail="Username is required")

        # Fetch the user's coin balance
        user_data = UserRepository.get_user_by_username(username)
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")

        if user_data.coins < 5:  # Require 15 coins to play next
            raise HTTPException(status_code=400, detail="Not enough coins to play the next song")

        # Deduct coins and save the user data
        user_data.coins -= 5
        UserRepository.save_user_data(username, user_data)

        # Perform the play next action
        result = MusicQueueService.play_next(store_id, song_index)
        return result
    except IndexError:
        raise HTTPException(status_code=404, detail="Song not found in the queue")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{store_id}/listeners/increment")
def increment_listeners(store_id: int, request: Request):
    try:
        session_id = request.headers.get("X-Session-ID")
        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID is required")
        return MusicQueueService.increment_listeners(store_id, session_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{store_id}/listeners/decrement")
def decrement_listeners(store_id: int, request: Request):
    try:
        session_id = request.headers.get("X-Session-ID")
        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID is required")
        return MusicQueueService.decrement_listeners(store_id, session_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{store_id}/vote/{vote_type}")
def vote_now_playing(store_id: int, vote_type: str, request: Request):
    try:
        session_id = request.headers.get("X-Session-ID")
        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID is required")
        if vote_type not in ["upvote", "downvote"]:
            raise HTTPException(status_code=400, detail="Invalid vote type")
        return MusicQueueService.vote_now_playing(store_id, session_id, vote_type)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

