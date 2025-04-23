from fastapi import APIRouter, Depends
from services.store_service import StoreService
from schemas.store_schema import Store

router = APIRouter(prefix="/api/stores", tags=["Store Locator"])

@router.get("/", response_model=list[Store])
def get_all_stores():
    return StoreService.get_all_stores()

@router.get("/search", response_model=list[Store])
def search_stores(query: str):
    return StoreService.search_stores(query)