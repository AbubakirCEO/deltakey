import os

TOKEN = "8683133632:AAGagr__2eD8a9jyBcgGVW8trQtLx4zNzyE"
ADMIN_ID = 0  # o'z Telegram ID'ingiz (ixtiyoriy)

BYPASS_URL = "http://127.0.0.1:2233/delta"  # delta-bypass server manzili
LINK_FILE = "link.txt"  # yangi havola shu faylga yoziladi

DEFAULT_KEY_LINK = "https://auth.platorelay.com/a?d=6sF6xR2QHSqhaQv7MqjvuFbP3xvQHHGrVgNG7YD9bxI60PjHnZsp9yFwCGVcoCvcGJr7g8nEpv6jKWMNUtPUp7LyQReplZNCUKrkTV2NZAn2LFZ0LTicX1RJf6xSrXcgvK1qX0ZcBy5a3LGDz8zKjMoXRhrGHLbjp2GctfRCdYzrc265ziZRVFoWyv15F8f5cWfcpRqNw6bxXrIdKHltGdbl7Qu53CSSnjjGR9rUGKzaCGSuWll0tvNYtUDL4yVMmtrl0UtSdmmytQGwkhMgvGjc7aihXGaIOQ9jYuphq5gPc0bGZwcwOD2fuQypd4ZO8iNYQNBgnaVBivjlhZ0rEIuRcs5OmvOG57SMZSD4Ijkk1LxqAxF51bvBXiv7JnjttRy7DecTkG140WVu3Rzz91OtXxmCi08QIux8UNYsy7Mqauh4BGB4ko9Ha1cT9KOaXsCn5jzA24v4o1NNHjipq1KLYCuJxlxSKhQFwsA38aUK70h3ghg"

def get_key_link():
    if os.path.exists(LINK_FILE):
        with open(LINK_FILE, "r", encoding="utf-8") as f:
            link = f.read().strip()
            if link:
                return link
    return DEFAULT_KEY_LINK
