#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quản lý cơ sở dữ liệu PostgreSQL cho bot Telegram HUTECH
"""

import json
import logging
import asyncpg
from typing import Dict, Any, Optional, List

from src.config.config import Config

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.config = Config()
        self.pool = None

    async def connect(self):
        """Khởi tạo connection pool đến PostgreSQL."""
        if not self.pool:
            try:
                self.pool = await asyncpg.create_pool(
                    dsn=self.config.POSTGRES_URL,
                    min_size=5,
                    max_size=20
                )
                logger.info("Đã kết nối thành công đến PostgreSQL và tạo connection pool.")
                await self._init_database()
            except Exception as e:
                logger.error(f"Lỗi không thể kết nối đến PostgreSQL: {e}")
                raise

    async def close(self):
        """Đóng connection pool."""
        if self.pool:
            await self.pool.close()
            logger.info("Đã đóng connection pool của PostgreSQL.")

    async def _init_database(self) -> None:
        """Khởi tạo cơ sở dữ liệu và tạo các bảng nếu chưa tồn tại."""
        async with self.pool.acquire() as conn:
            try:
                await conn.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        telegram_user_id BIGINT UNIQUE NOT NULL,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL,
                        device_uuid TEXT NOT NULL,
                        is_logged_in BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                await conn.execute('''
                    CREATE TABLE IF NOT EXISTS login_responses (
                        id SERIAL PRIMARY KEY,
                        telegram_user_id BIGINT NOT NULL REFERENCES users(telegram_user_id) ON DELETE CASCADE,
                        response_data JSONB NOT NULL,
                        created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(telegram_user_id)
                    )
                ''')
                
                # Các bảng khác sẽ được tạo tương tự khi cần
                # Ví dụ cho tkb_responses
                logger.info("Database initialized successfully")
            except Exception as e:
                logger.error(f"Lỗi khởi tạo database: {e}")
                raise

    async def save_user(self, telegram_user_id: int, username: str, password: str, device_uuid: str) -> bool:
        """Lưu hoặc cập nhật thông tin người dùng."""
        query = '''
            INSERT INTO users (telegram_user_id, username, password, device_uuid, is_logged_in, updated_at)
            VALUES ($1, $2, $3, $4, TRUE, CURRENT_TIMESTAMP)
            ON CONFLICT (telegram_user_id) DO UPDATE SET
                username = EXCLUDED.username,
                password = EXCLUDED.password,
                device_uuid = EXCLUDED.device_uuid,
                is_logged_in = TRUE,
                updated_at = CURRENT_TIMESTAMP
        '''
        try:
            async with self.pool.acquire() as conn:
                await conn.execute(query, telegram_user_id, username, password, device_uuid)
            logger.info(f"User {telegram_user_id} saved successfully")
            return True
        except Exception as e:
            logger.error(f"Error saving user {telegram_user_id}: {e}")
            return False

    async def save_login_response(self, telegram_user_id: int, response_data: Dict[str, Any]) -> bool:
        """Lưu response từ API đăng nhập."""
        query = '''
            INSERT INTO login_responses (telegram_user_id, response_data, created_at)
            VALUES ($1, $2, CURRENT_TIMESTAMP)
            ON CONFLICT (telegram_user_id) DO UPDATE SET
                response_data = EXCLUDED.response_data,
                created_at = CURRENT_TIMESTAMP
        '''
        try:
            async with self.pool.acquire() as conn:
                await conn.execute(query, telegram_user_id, json.dumps(response_data))
            logger.info(f"Login response for user {telegram_user_id} saved successfully")
            return True
        except Exception as e:
            logger.error(f"Error saving login response for user {telegram_user_id}: {e}")
            return False

    async def get_user(self, telegram_user_id: int) -> Optional[Dict[str, Any]]:
        """Lấy thông tin người dùng."""
        query = "SELECT telegram_user_id, username, password, device_uuid, is_logged_in FROM users WHERE telegram_user_id = $1"
        try:
            async with self.pool.acquire() as conn:
                user_data = await conn.fetchrow(query, telegram_user_id)
            if user_data:
                return dict(user_data)
            return None
        except Exception as e:
            logger.error(f"Error getting user {telegram_user_id}: {e}")
            return None

    async def is_user_logged_in(self, telegram_user_id: int) -> bool:
        """Kiểm tra xem người dùng đã đăng nhập chưa."""
        user = await self.get_user(telegram_user_id)
        return user is not None and user.get("is_logged_in", False)

    async def set_user_login_status(self, telegram_user_id: int, is_logged_in: bool) -> bool:
        """Cập nhật trạng thái đăng nhập của người dùng."""
        query = "UPDATE users SET is_logged_in = $1, updated_at = CURRENT_TIMESTAMP WHERE telegram_user_id = $2"
        try:
            async with self.pool.acquire() as conn:
                await conn.execute(query, is_logged_in, telegram_user_id)
            logger.info(f"User {telegram_user_id} login status updated to {is_logged_in}")
            return True
        except Exception as e:
            logger.error(f"Error updating login status for user {telegram_user_id}: {e}")
            return False
            
    async def get_user_login_response(self, telegram_user_id: int) -> Optional[Dict[str, Any]]:
        """Lấy response đăng nhập gần nhất của người dùng."""
        query = "SELECT response_data FROM login_responses WHERE telegram_user_id = $1"
        try:
            async with self.pool.acquire() as conn:
                record = await conn.fetchrow(query, telegram_user_id)
            if record and record['response_data']:
                return json.loads(record['response_data'])
            return None
        except Exception as e:
            logger.error(f"Error getting login response for user {telegram_user_id}: {e}")
            return None

    async def delete_user(self, telegram_user_id: int) -> bool:
        """Xóa người dùng và tất cả dữ liệu liên quan (sử dụng ON DELETE CASCADE)."""
        query = "DELETE FROM users WHERE telegram_user_id = $1"
        try:
            async with self.pool.acquire() as conn:
                await conn.execute(query, telegram_user_id)
            logger.info(f"User {telegram_user_id} and all related data deleted successfully")
            return True
        except Exception as e:
            logger.error(f"Error deleting user {telegram_user_id}: {e}")
            return False

    async def get_all_logged_in_users(self) -> List[int]:
        """Lấy danh sách ID của tất cả người dùng đang đăng nhập."""
        query = "SELECT telegram_user_id FROM users WHERE is_logged_in = TRUE"
        try:
            async with self.pool.acquire() as conn:
                records = await conn.fetch(query)
            return [record['telegram_user_id'] for record in records]
        except Exception as e:
            logger.error(f"Error getting all logged in users: {e}")
            return []
