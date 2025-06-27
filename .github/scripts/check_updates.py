#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查NotionNext原仓库是否有更新，并通过Dify API发送通知
"""

import os
import json
import subprocess
import requests
import sys

# 获取环境变量
DIFY_API_KEY = os.environ.get('DIFY_API_KEY')
DIFY_API_ENDPOINT = os.environ.get('DIFY_API_ENDPOINT')

def get_latest_commit(repo_url, branch='main'):
    """
    获取指定仓库最新的commit信息
    
    Args:
        repo_url: 仓库URL
        branch: 分支名称
        
    Returns:
        最新commit的SHA值和日期
    """
    result = subprocess.run(
        ['git', 'ls-remote', repo_url, f'refs/heads/{branch}'],
        capture_output=True, text=True, check=True
    )
    if result.stdout:
        commit_sha = result.stdout.split()[0]
        return commit_sha
    return None

def read_last_synced_commit():
    """
    读取上次同步的commit信息
    
    Returns:
        上次同步的commit SHA，如果不存在则返回None
    """
    try:
        with open('.last_synced_commit', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_current_commit(commit_sha):
    """
    保存当前同步的commit信息
    
    Args:
        commit_sha: 当前commit的SHA值
    """
    with open('.last_synced_commit', 'w') as f:
        f.write(commit_sha)

def notify_via_dify(message):
    """
    通过Dify API发送通知
    
    Args:
        message: 通知消息内容
    """
    headers = {
        'Authorization': f'Bearer {DIFY_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'inputs': {
            'message': message
        },
        'response_mode': 'blocking'
    }
    
    try:
        response = requests.post(
            f'{DIFY_API_ENDPOINT}/chat-messages',
            headers=headers,
            json=data
        )
        response.raise_for_status()
        print(f"通知已发送: {message}")
    except Exception as e:
        print(f"发送通知失败: {e}")

def main():
    # 原仓库URL
    upstream_url = 'https://github.com/original-author/notionnext.git'
    
    # 获取最新commit
    latest_commit = get_latest_commit(upstream_url)
    last_synced_commit = read_last_synced_commit()
    
    has_updates = latest_commit != last_synced_commit
    
    # 设置GitHub Actions输出变量
    print(f"::set-output name=has_updates::{str(has_updates).lower()}")
    
    if has_updates:
        # 发送通知
        message = f"NotionNext原仓库有更新！\n最新commit: {latest_commit[:8]}\n是否需要同步更新？"
        notify_via_dify(message)
        
        # 保存当前commit信息
        save_current_commit(latest_commit)
        
        print("检测到更新，已发送通知")
    else:
        print("没有检测到新的更新")

if __name__ == "__main__":
    main()
