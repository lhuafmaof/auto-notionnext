#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
备份个性化配置文件
"""

import os
import json
import shutil

# 需要备份的配置文件列表
CONFIG_FILES = [
    'blog.config.js',
    'site.config.js',
    'theme.config.js',
    # 添加其他需要保留的配置文件
]

def backup_configs():
    """
    备份所有配置文件到临时目录
    """
    backup_dir = '.config_backup'
    
    # 创建备份目录
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # 备份每个配置文件
    for config_file in CONFIG_FILES:
        if os.path.exists(config_file):
            shutil.copy2(config_file, os.path.join(backup_dir, config_file))
            print(f"已备份: {config_file}")

if __name__ == "__main__":
    backup_configs()
