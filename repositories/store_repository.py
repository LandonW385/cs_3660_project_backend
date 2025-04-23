import json
from models.store_model import StoreModel

class StoreRepository:
    @staticmethod
    def get_all_stores():
        try:
            with open("./db/stores.json", "r") as file:
                data = json.load(file)
                return [StoreModel(**store) for store in data["stores"]]
        except FileNotFoundError:
            raise Exception("Store database not found.")

    @staticmethod
    def search_stores(query: str):
        all_stores = StoreRepository.get_all_stores()
        return [
            store for store in all_stores
            if query.lower() in store.name.lower() or query.lower() in store.address.lower()
        ]