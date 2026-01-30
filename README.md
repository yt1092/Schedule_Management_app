# Schedule Management App

スケジュール管理アプリケーション。ユーザー登録・ログイン機能とタスク管理が統合されています。

## 機能

- ✅ ユーザー登録（メール＆パスワード）
- ✅ ユーザーログイン
- ✅ タスク作成・削除
- ✅ タスク優先度設定（高・中・低）
- ✅ タスク期限設定
- ✅ 期限切れ・緊急タスクのハイライト表示

## 技術スタック

### フロントエンド
- React 19
- CSS3

### バックエンド
- FastAPI
- SQLAlchemy
- PassLib (パスワードハッシング)
- Pydantic

### データベース
- SQLite（開発環境）
- PostgreSQL（本番環境 - Render）

## インストール・セットアップ

### 前提条件
- Python 3.8以上
- Node.js 14以上

### バックエンド セットアップ

```bash
# 依存パッケージをインストール
cd app
pip install -r requirements.txt

# .env ファイルを作成（オプション）
cp .env.example .env

# サーバー起動
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### フロントエンド セットアップ

```bash
# 依存パッケージをインストール
cd frontend
npm install

# 開発サーバー起動
REACT_APP_API_URL=http://localhost:8000 npm start
```

ブラウザで http://localhost:3000 を開きます。

## Render デプロイ

[RENDER_SETUP.md](./RENDER_SETUP.md) を参照してください。

## プロジェクト構造

```
Schedule_Management_app/
├── app/                          # バックエンド (FastAPI)
│   ├── main.py                   # メインアプリケーション
│   ├── models.py                 # SQLAlchemy モデル
│   ├── db.py                     # データベース接続設定
│   ├── requirements.txt           # Python 依存パッケージ
│   ├── .env.example              # 環境変数テンプレート
│   └── __pycache__/              # キャッシュ
│
├── frontend/                      # フロントエンド (React)
│   ├── public/                    # 静的ファイル
│   ├── src/
│   │   ├── App.js                # メインコンポーネント
│   │   ├── App.css               # アプリケーションスタイル
│   │   ├── APP.css               # メインスタイル
│   │   ├── Login.js              # ログイン/登録コンポーネント
│   │   ├── Login.css             # ログインスタイル
│   │   ├── index.js              # エントリーポイント
│   │   └── ...
│   ├── package.json              # npm 依存パッケージ
│   └── build/                    # ビルド出力
│
├── RENDER_SETUP.md               # Render デプロイガイド
└── README.md                     # このファイル
```

## API エンドポイント

### 認証

#### ユーザー登録
```
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**レスポンス:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "message": "ユーザー登録が完了しました"
}
```

#### ログイン
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**レスポンス:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "message": "ログインしました"
}
```

### タスク管理

#### タスク作成
```
POST /api/tasks/?user_id=1&title=タスク名&priority=1&deadline=2026-02-10T10:00:00
```

#### タスク一覧取得
```
GET /api/tasks/?user_id=1
```

#### タスク削除
```
DELETE /api/tasks/{task_id}
```

## セキュリティ情報

- パスワードは bcrypt でハッシング化されています
- メールアドレスはユニーク制約があります
- パスワードは6文字以上が必須です

## 使用方法

1. **アカウント作成**: ログイン画面の「登録」ボタンでメールアドレスとパスワードを入力
2. **ログイン**: 作成したアカウントでログイン
3. **タスク追加**: 「新しいタスクを追加」セクションでタスク情報を入力
4. **タスク管理**: タスク一覧でタスクを確認・削除可能
5. **ログアウト**: ヘッダーの「ログアウト」ボタンをクリック

## トラブルシューティング

### "psycopg2" エラー
PostgreSQL接続時に発生します。`psycopg2-binary` をインストール：
```bash
pip install psycopg2-binary
```

### CORS エラー
フロントエンドからAPIへのアクセスが拒否されています。
- `REACT_APP_API_URL` 環境変数が正しいか確認
- APIサーバーが起動しているか確認

### ポート競合エラー
別のアプリケーションがポートを使用しています。別のポートを指定：
```bash
uvicorn main:app --reload --port 8001
```

## ライセンス

MIT License

## 作成者

Schedule Management Development Team
