#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
恢复个性化配置文件
"""

import os
import json
import shutil

# 需要恢复的配置文件列表
CONFIG_FILES = [
    'blog.config.js',
    'site.config.js',
    'theme.config.js',
    # 添加其他需要保留的配置文件
]

def restore_configs():
    """
    从临时目录恢复所有配置文件
    """
    backup_dir = '.config_backup'
    
    # 检查备份目录是否存在
    if not os.path.exists(backup_dir):
        print("备份目录不存在，无法恢复配置")
        return
    
    # 恢复每个配置文件
    for config_file in CONFIG_FILES:
        backup_file = os.path.join(backup_dir, config_file)
        if os.path.exists(backup_file):
            shutil.copy2(backup_file, config_file)
            print(f"已恢复: {config_file}")
    
    # 清理备份目录
    shutil.rmtree(backup_dir)
    print("备份目录已清理")

if __name__ == "__main__":
    restore_configs()
