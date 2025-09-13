#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Các hàm tiện ích cho bot Telegram HUTECH
"""

import uuid
import logging
import json
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

def generate_uuid() -> str:
    """
    Tạo một UUID mới cho thiết bị
    
    Returns:
        UUID dưới dạng string
    """
    return str(uuid.uuid4()).upper()

def format_user_info(user_info: Dict[str, Any]) -> str:
    """
    Định dạng thông tin người dùng để hiển thị
    
    Args:
        user_info: Thông tin người dùng
        
    Returns:
        Chuỗi đã định dạng
    """
    if not user_info:
        return "Không có thông tin người dùng"
    
    formatted_info = "📋 Thông tin người dùng:\n\n"
    
    if "ho_ten" in user_info:
        formatted_info += f"👤 Họ và tên: {user_info['ho_ten']}\n"
    
    if "username" in user_info:
        formatted_info += f"🆔 Tài khoản: {user_info['username']}\n"
    
    if "email" in user_info:
        formatted_info += f"📧 Email: {user_info['email']}\n"
    
    if "so_dien_thoai" in user_info:
        formatted_info += f"📱 Số điện thoại: {user_info['so_dien_thoai']}\n"
    
    if "contact_id" in user_info:
        formatted_info += f"🔢 Contact ID: {user_info['contact_id']}\n"
    
    return formatted_info

def format_response_data(response_data: Dict[str, Any], max_length: int = 1000) -> str:
    """
    Định dạng dữ liệu response để hiển thị
    
    Args:
        response_data: Dữ liệu response
        max_length: Độ dài tối đa của chuỗi trả về
        
    Returns:
        Chuỗi đã định dạng
    """
    if not response_data:
        return "Không có dữ liệu"
    
    try:
        # Chuyển đổi dữ liệu thành JSON string với định dạng đẹp
        json_str = json.dumps(response_data, indent=2, ensure_ascii=False)
        
        # Cắt bớt nếu quá dài
        if len(json_str) > max_length:
            json_str = json_str[:max_length] + "\n... (dữ liệu bị cắt bớt)"
        
        return f"```json\n{json_str}\n```"
    
    except Exception as e:
        logger.error(f"Error formatting response data: {e}")
        return f"Lỗi định dạng dữ liệu: {str(e)}"

def safe_json_loads(json_str: str) -> Optional[Dict[str, Any]]:
    """
    Tải JSON string một cách an toàn
    
    Args:
        json_str: Chuỗi JSON
        
    Returns:
        Dict hoặc None nếu có lỗi
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error loading JSON: {e}")
        return None

def format_timestamp(timestamp: Optional[str] = None) -> str:
    """
    Định dạng timestamp thành chuỗi dễ đọc
    
    Args:
        timestamp: Timestamp (nếu None, sử dụng thời gian hiện tại)
        
    Returns:
        Chuỗi thời gian đã định dạng
    """
    if timestamp:
        try:
            # Cố gắng parse timestamp
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except:
            # Nếu không parse được, sử dụng thời gian hiện tại
            dt = datetime.now()
    else:
        dt = datetime.now()
    
    return dt.strftime("%d/%m/%Y %H:%M:%S")

def mask_sensitive_data(data: str, mask_char: str = "*") -> str:
    """
    Che giấu dữ liệu nhạy cảm
    
    Args:
        data: Dữ liệu cần che giấu
        mask_char: Ký tự dùng để che giấu
        
    Returns:
        Chuỗi đã được che giấu
    """
    if not data or len(data) < 3:
        return mask_char * len(data) if data else ""
    
    # Giữ lại 2 ký tự đầu và 2 ký tự cuối, che giấu phần còn lại
    return data[:2] + mask_char * (len(data) - 4) + data[-2:]

def validate_phone_number(phone: str) -> bool:
    """
    Kiểm tra số điện thoại có hợp lệ không
    
    Args:
        phone: Số điện thoại cần kiểm tra
        
    Returns:
        True nếu hợp lệ, False nếu không
    """
    if not phone:
        return False
    
    # Loại bỏ các ký tự không phải số
    clean_phone = ''.join(c for c in phone if c.isdigit())
    
    # Kiểm tra độ dài (số điện thoại Việt Nam thường có 10 hoặc 11 số)
    return len(clean_phone) in (10, 11)

def validate_email(email: str) -> bool:
    """
    Kiểm tra email có hợp lệ không
    
    Args:
        email: Email cần kiểm tra
        
    Returns:
        True nếu hợp lệ, False nếu không
    """
    if not email:
        return False
    
    # Kiểm tra cơ bản
    return '@' in email and '.' in email.split('@')[-1]

def create_success_message(message: str) -> str:
    """
    Tạo thông báo thành công với emoji
    
    Args:
        message: Nội dung thông báo
        
    Returns:
        Chuỗi thông báo đã định dạng
    """
    return f"✅ {message}"

def create_error_message(message: str) -> str:
    """
    Tạo thông báo lỗi với emoji
    
    Args:
        message: Nội dung thông báo
        
    Returns:
        Chuỗi thông báo đã định dạng
    """
    return f"❌ {message}"

def create_info_message(message: str) -> str:
    """
    Tạo thông báo thông tin với emoji
    
    Args:
        message: Nội dung thông báo
        
    Returns:
        Chuỗi thông báo đã định dạng
    """
    return f"ℹ️ {message}"

def create_warning_message(message: str) -> str:
    """
    Tạo thông báo cảnh báo với emoji
    
    Args:
        message: Nội dung thông báo
        
    Returns:
        Chuỗi thông báo đã định dạng
    """
    return f"⚠️ {message}"

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Cắt bớt văn bản nếu quá dài
    
    Args:
        text: Văn bản cần cắt bớt
        max_length: Độ dài tối đa
        suffix: Hậu tố khi bị cắt bớt
        
    Returns:
        Chuỗi đã được cắt bớt (nếu cần)
    """
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def escape_markdown(text: str) -> str:
    """
    Escape các ký tự đặc biệt trong Markdown
    
    Args:
        text: Văn bản cần escape
        
    Returns:
        Chuỗi đã được escape
    """
    if not text:
        return ""
    
    # Các ký tự cần escape trong Markdown
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    
    return text