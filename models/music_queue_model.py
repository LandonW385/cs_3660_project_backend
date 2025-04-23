from pydantic import BaseModel
from typing import List

class Track(BaseModel):
    song: str  # Song name
    artist: str  # Artist name(s)
    albumArt: str  # Album art URL
    duration: int  # Duration in seconds
    votes: int = 0  # Default votes to 0

class MusicQueue(BaseModel):
    store_id: int
    queue: List[Track]  # List of tracks in the queue
    current_track_index: int = 0  # Index of the currently playing track
    current_track_progress: int = 0  # Progress of the current track in seconds