from repositories.store_repository import StoreRepository

class StoreService:
    @staticmethod
    def get_all_stores():
        return StoreRepository.get_all_stores()

    @staticmethod
    def search_stores(query: str):
        return StoreRepository.search_stores(query)