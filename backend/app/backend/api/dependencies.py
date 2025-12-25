from app.backend.services.storage import Database

async def get_db() -> Database:
    database = Database()
    await database.initialize()
    return database