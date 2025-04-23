from pydantic import BaseModel

class Store(BaseModel):
    id: int
    name: str
    address: str
    lat: float
    lng: float