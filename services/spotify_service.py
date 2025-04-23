from repositories.spotify_repository import SpotifyRepository

class SpotifyService:
    def __init__(self, client_id: str, client_secret: str):
        self.repository = SpotifyRepository(client_id, client_secret)

    def get_track_details(self, track_id: str):
        track_data = self.repository.get_track(track_id)
        return {
            "title": track_data["name"],
            "artist": ", ".join(artist["name"] for artist in track_data["artists"]),
            "albumArt": track_data["album"]["images"][0]["url"] if track_data["album"]["images"] else None,
            "duration": track_data["duration_ms"] // 1000  # Convert milliseconds to seconds
        }

    def search_tracks(self, query: str):
        tracks = self.repository.search_tracks(query)
        unique_tracks = []
        track_set = set()

        for track in tracks:
            track_identifier = f"{track['name']}-{track['artists'][0]['name']}"
            if track_identifier not in track_set:
                track_set.add(track_identifier)
                unique_tracks.append({
                    "name": track["name"],
                    "artists": [artist["name"] for artist in track["artists"]],
                    "albumArt": track["album"]["images"][0]["url"] if track["album"]["images"] else "",
                    "duration_ms": track["duration_ms"],
                })

        return unique_tracks