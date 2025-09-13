#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Handler xử lý đăng nhập vào hệ thống HUTECH
"""

import json
import logging
import aiohttp
from typing import Dict, Any, Optional

from config.config import Config

logger = logging.getLogger(__name__)

class LoginHandler:
    def __init__(self, db_manager, cache_manager):
        self.db_manager = db_manager
        self.cache_manager = cache_manager
        self.config = Config()
    
    async def handle_login(self, telegram_user_id: int, username: str, password: str, device_uuid: str) -> Dict[str, Any]:
        """
        Xử lý đăng nhập vào hệ thống HUTECH
        
        Args:
            telegram_user_id: ID của người dùng trên Telegram
            username: Tên tài khoản HUTECH
            password: Mật khẩu tài khoản HUTECH
            device_uuid: UUID của thiết bị
            
        Returns:
            Dict chứa kết quả đăng nhập
        """
        try:
            # Tạo request data
            request_data = {
                "diuu": device_uuid,
                "username": username,
                "password": password
            }
            
            # Gọi API đăng nhập
            response_data = await self._call_login_api(request_data)
            
            # Kiểm tra kết quả đăng nhập
            if response_data and "token" in response_data:
                # 1. Lưu thông tin người dùng và cập nhật trạng thái đăng nhập
                user_saved = await self.db_manager.save_user(telegram_user_id, username, password, device_uuid)
                
                # 2. Sau đó mới lưu response đăng nhập
                response_saved = await self._save_login_response(telegram_user_id, response_data)

                if user_saved and response_saved:
                    # 3. Xóa cache cũ của người dùng để đảm bảo dữ liệu mới được lấy
                    await self.cache_manager.clear_user_cache(telegram_user_id)
                    
                    return {
                        "success": True,
                        "message": "Đăng nhập thành công",
                        "data": response_data
                    }
                else:
                    # Nếu một trong hai bước lưu thất bại, coi như đăng nhập thất bại
                    await self.db_manager.set_user_login_status(telegram_user_id, False) # Đảm bảo trạng thái là logout
                    return {
                        "success": False,
                        "message": "🚫 *Lỗi*\n\nKhông thể lưu thông tin đăng nhập. Vui lòng thử lại sau.",
                        "data": None,
                        "show_back_button": True
                    }
            else:
                return {
                    "success": False,
                    "message": "🚫 *Đăng nhập thất bại*\n\nTài khoản hoặc mật khẩu không đúng. Vui lòng kiểm tra lại.",
                    "data": response_data,
                    "show_back_button": True
                }
        
        except Exception as e:
            logger.error(f"Login error for user {telegram_user_id}: {e}")
            return {
                "success": False,
                "message": f"🚫 *Lỗi*\n\nĐã xảy ra lỗi trong quá trình đăng nhập: {str(e)}",
                "data": None,
                "show_back_button": True
            }
    
    async def _call_login_api(self, request_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Gọi API đăng nhập của HUTECH
        
        Args:
            request_data: Dữ liệu request
            
        Returns:
            Response data từ API hoặc None nếu có lỗi
        """
        try:
            url = f"{self.config.HUTECH_API_BASE_URL}{self.config.HUTECH_LOGIN_ENDPOINT}"
            headers = self.config.HUTECH_STUDENT_HEADERS.copy()
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    headers=headers,
                    json=request_data
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        logger.error(f"Login API error: {response.status} - {error_text}")
                        return {
                            "error": True,
                            "status_code": response.status,
                            "message": error_text
                        }
        
        except aiohttp.ClientError as e:
            logger.error(f"HTTP client error: {e}")
            return {
                "error": True,
                "message": f"Lỗi kết nối: {str(e)}"
            }
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return {
                "error": True,
                "message": f"Lỗi phân tích dữ liệu: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {
                "error": True,
                "message": f"Lỗi không xác định: {str(e)}"
            }
    
    async def _save_login_response(self, telegram_user_id: int, response_data: Dict[str, Any]) -> bool:
        """
        Lưu response từ API đăng nhập vào database
        
        Args:
            telegram_user_id: ID của người dùng trên Telegram
            response_data: Dữ liệu response từ API
            
        Returns:
            True nếu lưu thành công, False nếu có lỗi
        """
        try:
            return await self.db_manager.save_login_response(telegram_user_id, response_data)
        except Exception as e:
            logger.error(f"Error saving login response for user {telegram_user_id}: {e}")
            return False
    
    async def get_user_token(self, telegram_user_id: int) -> Optional[str]:
        """
        Lấy token của người dùng từ database
        
        Args:
            telegram_user_id: ID của người dùng trên Telegram
            
        Returns:
            Token của người dùng hoặc None nếu không tìm thấy
        """
        try:
            # Lấy response đăng nhập gần nhất của người dùng
            response_data = await self.db_manager.get_user_login_response(telegram_user_id)
            
            if response_data and "token" in response_data:
                return response_data["token"]
            
            return None
        
        except Exception as e:
            logger.error(f"Error getting token for user {telegram_user_id}: {e}")
            return None
    
    async def get_user_device_uuid(self, telegram_user_id: int) -> Optional[str]:
        """
        Lấy device UUID của người dùng từ database
        
        Args:
            telegram_user_id: ID của người dùng trên Telegram
            
        Returns:
            Device UUID của người dùng hoặc None nếu không tìm thấy
        """
        try:
            user = await self.db_manager.get_user(telegram_user_id)
            if user:
                return user.get("device_uuid")
            return None
        
        except Exception as e:
            logger.error(f"Error getting device UUID for user {telegram_user_id}: {e}")
            return None
    
    async def get_user_info(self, telegram_user_id: int) -> Optional[Dict[str, Any]]:
        """
        Lấy thông tin người dùng từ response đăng nhập gần nhất
        
        Args:
            telegram_user_id: ID của người dùng trên Telegram
            
        Returns:
            Thông tin người dùng hoặc None nếu không tìm thấy
        """
        try:
            # Lấy response đăng nhập gần nhất của người dùng
            response_data = await self.db_manager.get_user_login_response(telegram_user_id)
            
            if response_data:
                
                # Trích xuất thông tin người dùng từ response
                user_info = {}
                
                if "username" in response_data:
                    user_info["username"] = response_data["username"]
                
                if "data" in response_data and isinstance(response_data["data"], dict):
                    data = response_data["data"]
                    if "email" in data:
                        user_info["email"] = data["email"]
                    if "ho_ten" in data:
                        user_info["ho_ten"] = data["ho_ten"]
                    if "so_dien_thoai" in data:
                        user_info["so_dien_thoai"] = data["so_dien_thoai"]
                
                if "old_login_info" in response_data and isinstance(response_data["old_login_info"], dict):
                    old_info = response_data["old_login_info"]
                    if "result" in old_info and isinstance(old_info["result"], dict):
                        result = old_info["result"]
                        if "Ho_Ten" in result:
                            user_info["ho_ten"] = result["Ho_Ten"]
                        if "email" in result:
                            user_info["email"] = result["email"]
                        if "contact_id" in result:
                            user_info["contact_id"] = result["contact_id"]
                
                if "contact_id" in response_data:
                    user_info["contact_id"] = response_data["contact_id"]
                
                return user_info if user_info else None
            
            return None
        
        except Exception as e:
            logger.error(f"Error getting user info for user {telegram_user_id}: {e}")
            return None