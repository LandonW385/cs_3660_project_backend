class User:
    def __init__(self, username: str, name: str, password_hash: str, coins: int = 0) -> None:
        self.username = username
        self.name = name
        self.password_hash = password_hash
        self.coins = coins