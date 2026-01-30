# Schedule Management App - Render PostgreSQL 設定ガイド

## Renderでの設定方法

### 1. PostgreSQLデータベース作成

1. [Render.com](https://render.com) にアクセス
2. ダッシュボードから「New +」→「PostgreSQL」を選択
3. 下記情報を設定：
   - Name: `schedule-management-db`
   - Database: `schedule_db`
   - User: `schedule_user`
   - Region: 自分の地域を選択
4. 「Create Database」をクリック

### 2. 接続情報の取得

作成後、以下の情報をコピー：
- External Database URL (PostgreSQL の接続文字列)

### 3. バックエンド環境変数設定

Renderでバックエンドサービスを作成し、環境変数に以下を追加：

```
DATABASE_URL=postgresql://[user]:[password]@[host]/[database]
```

例:
```
DATABASE_URL=postgresql://schedule_user:your_password@host.render.com:5432/schedule_db
```

### 4. ローカル開発環境での設定

プロジェクトルートに `.env` ファイルを作成：

```
DATABASE_URL=postgresql://schedule_user:your_password@localhost:5432/schedule_db
```

### 5. 必要なパッケージのインストール

```bash
cd app
pip install -r requirements.txt
```

### 6. バックエンド起動（開発環境）

```bash
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 7. フロントエンド起動（開発環境）

```bash
cd frontend
npm install
REACT_APP_API_URL=http://localhost:8000 npm start
```

## デプロイ手順

### Renderへのデプロイ

1. GitHub にコードをプッシュ
2. Render ダッシュボードで「New +」→「Web Service」を選択
3. リポジトリを接続
4. 以下を設定：
   - Name: `schedule-management-api`
   - Environment: `Python 3`
   - Build Command: `cd app && pip install -r requirements.txt`
   - Start Command: `cd app && uvicorn main:app --host 0.0.0.0 --port $PORT`
5. 環境変数 `DATABASE_URL` を追加
6. 「Create Web Service」をクリック

## テスト用APIエンドポイント

### ユーザー登録
```
POST http://localhost:8000/api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

### ログイン
```
POST http://localhost:8000/api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

## トラブルシューティング

### PostgreSQL接続エラー
- CONNECTION_URL が正しいか確認
- ファイアウォール設定を確認
- Renderダッシュボードでデータベースが起動しているか確認

### CORS エラー
- フロントエンド環境変数 `REACT_APP_API_URL` が正しく設定されているか確認

### パスワードハッシング関連エラー
- `bcrypt` が正しくインストールされているか確認
- `pip install --upgrade bcrypt`
