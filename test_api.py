#!/usr/bin/env python3
"""
Schedule Management App - ローカルテストスクリプト
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    """APIエンドポイントをテスト"""
    
    print("=" * 60)
    print("Schedule Management API - テスト開始")
    print("=" * 60)
    
    # テスト用の認証情報
    test_email = "test@example.com"
    test_password = "test123456"
    
    # 1. ユーザー登録テスト
    print("\n[1] ユーザー登録テスト")
    print(f"登録メール: {test_email}")
    
    register_data = {
        "email": test_email,
        "password": test_password
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json=register_data
        )
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ 登録成功")
            print(f"   ユーザーID: {user_data['id']}")
            print(f"   メール: {user_data['email']}")
            user_id = user_data['id']
        else:
            print(f"❌ 登録失敗: {response.status_code}")
            print(f"   エラー: {response.json()}")
            return
            
    except requests.exceptions.ConnectionError:
        print("❌ API サーバーに接続できません")
        print("   バックエンドが起動しているか確認してください")
        print("   起動コマンド: cd app && uvicorn main:app --reload")
        return
    
    # 2. ログインテスト
    print("\n[2] ログインテスト")
    
    login_data = {
        "email": test_email,
        "password": test_password
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data
        )
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ ログイン成功")
            print(f"   ユーザーID: {user_data['id']}")
        else:
            print(f"❌ ログイン失敗: {response.status_code}")
            print(f"   エラー: {response.json()}")
            return
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        return
    
    # 3. タスク作成テスト
    print("\n[3] タスク作成テスト")
    
    task_data = {
        "user_id": str(user_id),
        "title": "テストタスク1",
        "priority": 1,
        "deadline": "2026-02-15T10:00:00"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/tasks/",
            params=task_data
        )
        
        if response.status_code == 200:
            task = response.json()
            print(f"✅ タスク作成成功")
            print(f"   タスクID: {task['id']}")
            print(f"   タイトル: {task['title']}")
            print(f"   優先度: {task['priority']}")
            task_id = task['id']
        else:
            print(f"❌ タスク作成失敗: {response.status_code}")
            print(f"   エラー: {response.json()}")
            return
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        return
    
    # 4. タスク一覧取得テスト
    print("\n[4] タスク一覧取得テスト")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/tasks/",
            params={"user_id": str(user_id)}
        )
        
        if response.status_code == 200:
            tasks = response.json()
            print(f"✅ タスク取得成功")
            print(f"   取得件数: {len(tasks)}")
            for i, task in enumerate(tasks, 1):
                print(f"   {i}. {task['title']} (ID: {task['id']})")
        else:
            print(f"❌ タスク取得失敗: {response.status_code}")
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        return
    
    # 5. タスク削除テスト
    print("\n[5] タスク削除テスト")
    
    try:
        response = requests.delete(
            f"{BASE_URL}/api/tasks/{task_id}"
        )
        
        if response.status_code == 200:
            print(f"✅ タスク削除成功")
        else:
            print(f"❌ タスク削除失敗: {response.status_code}")
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        return
    
    # テスト完了
    print("\n" + "=" * 60)
    print("✅ すべてのテストが完了しました！")
    print("=" * 60)

if __name__ == "__main__":
    test_api()
