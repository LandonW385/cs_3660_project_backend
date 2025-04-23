from fastapi import APIRouter, Depends, HTTPException
from services.spotify_service import SpotifyService

router = APIRouter(prefix="/api/spotify", tags=["Spotify"])

# Dependency injection
def get_spotify_service():
    CLIENT_ID = "4cbffe00e5fe460fa91ba32907d19114"
    CLIENT_SECRET = "35701f26a07947549a6a4f8919ca59ad"
    return SpotifyService(CLIENT_ID, CLIENT_SECRET)

@router.get("/search")
def search_tracks(query: str, service: SpotifyService = Depends(get_spotify_service)):
    try:
        return service.search_tracks(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))