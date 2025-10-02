#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Các hàm tiện ích cho bot Telegram HUTECH
"""

import uuid
import logging

logger = logging.getLogger(__name__)

def generate_uuid() -> str:
    """
    Tạo một UUID mới cho thiết bị
    
    Returns:
        UUID dưới dạng string
    """
    return str(uuid.uuid4()).upper()