import aiosqlite
from typing import List, Optional, Dict
from pathlib import Path
from datetime import datetime



class Database:
    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
        self._initialized = False

    async def initialize(self):
        """Инициализировать базу данных и создать таблицы"""
        if self._initialized:
            return

        async with aiosqlite.connect(self.db_path) as db:
            # Создаем таблицу для связи user_id -> thread_id
            await db.execute("""
                CREATE TABLE IF NOT EXISTS user_threads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    thread_id TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    UNIQUE(user_id, thread_id)
                )
            """)
            await db.commit()

        self._initialized = True

    async def add_thread_to_user(self, user_id: str, thread_id: str):
        """Добавить thread_id к user_id"""
        await self.initialize()

        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute("""
                    INSERT INTO user_threads (user_id, thread_id, created_at)
                    VALUES (?, ?, ?)
                """, (user_id, thread_id, datetime.now().isoformat()))
                await db.commit()
            except aiosqlite.IntegrityError:
                # Уже существует, игнорируем
                pass

    async def get_user_threads(self, user_id: str) -> List[Dict[str, str]]:
        """Получить список thread_id для user_id"""
        await self.initialize()

        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT thread_id, created_at FROM user_threads
                WHERE user_id = ?
                ORDER BY created_at DESC
            """, (user_id,)) as cursor:
                rows = await cursor.fetchall()
                return [{"thread_id": row[0], "created_at": row[1]} for row in rows]

    async def remove_thread_from_user(self, user_id: str, thread_id: str):
        """Удалить thread_id у user_id"""
        await self.initialize()

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                DELETE FROM user_threads
                WHERE user_id = ? AND thread_id = ?
            """, (user_id, thread_id))
            await db.commit()

    async def user_has_thread(self, user_id: str, thread_id: str) -> bool:
        """Проверить, есть ли у user_id доступ к thread_id"""
        await self.initialize()

        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT COUNT(*) FROM user_threads
                WHERE user_id = ? AND thread_id = ?
            """, (user_id, thread_id)) as cursor:
                row = await cursor.fetchone()
                return row[0] > 0