from fastapi import APIRouter, Depends, HTTPException
from services.spotify_service import SpotifyService

from config import settings

router = APIRouter(prefix="/api/spotify", tags=["Spotify"])

# Dependency injection
def get_spotify_service():
    return SpotifyService(settings.client_id, settings.client_secret)

@router.get("/search")
def search_tracks(query: str, service: SpotifyService = Depends(get_spotify_service)):
    try:
        return service.search_tracks(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))