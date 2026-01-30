#!/usr/bin/env python3
"""
Schedule Management - トラブルシューティング診断
"""

import subprocess
import sys
import os

def check_python_packages():
    """必要なPythonパッケージが正しくインストールされているか確認"""
    print("\n" + "="*60)
    print("🔍 Python パッケージ確認")
    print("="*60)
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'passlib',
        'bcrypt',
        'pydantic',
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  不足しているパッケージ: {', '.join(missing_packages)}")
        print("以下のコマンドで修正してください:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_api_connection():
    """APIサーバーに接続できるか確認"""
    print("\n" + "="*60)
    print("🔍 API サーバー接続確認")
    print("="*60)
    
    try:
        import requests
        response = requests.get("http://localhost:8000/api", timeout=2)
        print(f"✅ API サーバーが起動しています")
        print(f"   レスポンス: {response.json()}")
        return True
    except requests.exceptions.ConnectionError:
        print(f"❌ API サーバーに接続できません")
        print(f"   バックエンドが起動していない可能性があります")
        print(f"   起動コマンド: cd app && uvicorn main:app --reload")
        return False
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def check_database():
    """データベースへのアクセスを確認"""
    print("\n" + "="*60)
    print("🔍 データベース確認")
    print("="*60)
    
    try:
        os.chdir('app')
        from db import SessionLocal, engine
        from models import User
        
        # DB接続テスト
        db = SessionLocal()
        user_count = db.query(User).count()
        db.close()
        
        print(f"✅ データベース接続OK")
        print(f"   ユーザー数: {user_count}")
        return True
    except Exception as e:
        print(f"❌ データベースエラー: {e}")
        return False

def test_registration():
    """登録APIをテスト"""
    print("\n" + "="*60)
    print("🔍 ユーザー登録 API テスト")
    print("="*60)
    
    try:
        import requests
        
        test_data = {
            "email": "diagnostic@test.com",
            "password": "test123456"
        }
        
        response = requests.post(
            "http://localhost:8000/api/auth/register",
            json=test_data,
            timeout=5
        )
        
        if response.status_code == 200:
            print(f"✅ 登録 API が正常に動作しています")
            print(f"   レスポンス: {response.json()}")
            return True
        else:
            print(f"❌ API エラー (ステータス: {response.status_code})")
            print(f"   レスポンス: {response.json()}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"❌ タイムアウト - API が応答していません")
        return False
    except requests.exceptions.ConnectionError:
        print(f"❌ 接続エラー - API サーバーが起動していません")
        return False
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("Schedule Management - トラブルシューティング診断")
    print("="*60)
    
    # チェック実行
    pkg_ok = check_python_packages()
    api_ok = check_api_connection()
    db_ok = False
    reg_ok = False
    
    if api_ok:
        db_ok = check_database()
        reg_ok = test_registration()
    
    # 結果サマリー
    print("\n" + "="*60)
    print("📊 診断結果")
    print("="*60)
    
    results = {
        "Pythonパッケージ": pkg_ok,
        "APIサーバー": api_ok,
        "データベース": db_ok,
        "登録API": reg_ok
    }
    
    for item, status in results.items():
        symbol = "✅" if status else "❌"
        print(f"{symbol} {item}")
    
    # 推奨アクション
    print("\n" + "="*60)
    print("💡 推奨アクション")
    print("="*60)
    
    if not pkg_ok:
        print("1️⃣  パッケージをインストール:")
        print("    cd app && pip install -r requirements.txt")
    
    if not api_ok:
        print("2️⃣  バックエンドを起動:")
        print("    cd app && uvicorn main:app --reload")
    
    if api_ok and not reg_ok:
        print("3️⃣  バックエンドのターミナルでエラーを確認してください")

if __name__ == "__main__":
    main()
