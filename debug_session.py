#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session Cookie 调试工具
用于查看 Session 中包含的信息
"""

import sys
import base64
import re


def decode_session(session_cookie: str):
    """解码并分析 Session Cookie"""
    print('=' * 60)
    print('Session Cookie 分析')
    print('=' * 60)
    print(f'Session 长度: {len(session_cookie)} 字符')
    print(f'Session 开头: {session_cookie[:50]}...')
    print()

    try:
        # 尝试 Base64 解码
        print('[1] 尝试 Base64 解码...')

        # 移除可能的填充问题
        padding = len(session_cookie) % 4
        if padding:
            session_cookie_padded = session_cookie + '=' * (4 - padding)
        else:
            session_cookie_padded = session_cookie

        decoded = base64.b64decode(session_cookie_padded)
        print(f'✅ 解码成功，长度: {len(decoded)} 字节')

        # 尝试不同的编码
        print('\n[2] 尝试解析内容...')

        # UTF-8
        try:
            decoded_utf8 = decoded.decode('utf-8')
            print(f'\n📝 UTF-8 解码 (前 500 字符):')
            print(f'{decoded_utf8[:500]}')
            print()
        except UnicodeDecodeError:
            print('⚠️  UTF-8 解码失败')

        # 忽略错误的解码
        decoded_ignore = decoded.decode('utf-8', errors='ignore')
        print(f'📝 UTF-8 解码（忽略错误，前 500 字符）:')
        print(f'{decoded_ignore[:500]}')
        print()

        # 查找可能的用户信息
        print('[3] 搜索用户信息...')

        patterns = {
            'linuxdo_数字': r'linuxdo[_-](\d+)',
            'user_数字': r'user[_-](\d+)',
            '"id": 数字': r'"id"[:\s]+(\d+)',
            'userid: 数字': r'userid[:\s]+(\d+)',
            '纯数字（3位以上）': r'\b(\d{3,})\b',
        }

        found_any = False
        for name, pattern in patterns.items():
            matches = re.findall(pattern, decoded_ignore, re.IGNORECASE)
            if matches:
                print(f'  ✅ {name}: {matches}')
                found_any = True

        if not found_any:
            print('  ⚠️  未找到明显的用户ID模式')

        # 显示所有可打印字符
        print('\n[4] 可打印字符:')
        printable = ''.join(c for c in decoded_ignore if c.isprintable())
        print(f'{printable[:300]}...')

    except Exception as e:
        print(f'❌ 解码失败: {e}')

    print('\n' + '=' * 60)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('使用方法：')
        print('  python debug_session.py <SESSION_COOKIE>')
        print('')
        print('示例：')
        print('  python debug_session.py MTc2NzQxMzYzM3xEWDhFQVFMX2...')
        sys.exit(1)

    session_cookie = sys.argv[1]
    decode_session(session_cookie)
