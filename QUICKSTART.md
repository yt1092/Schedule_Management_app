# クイックスタートガイド

Schedule Management アプリを素早く起動して使い始めるための手順です。

## 前提条件確認

```bash
# Python バージョン確認（3.8以上推奨）
python --version

# Node.js バージョン確認（14以上推奨）
node --version
npm --version
```

## 方法1: ローカル開発（最も簡単）

### ステップ1: バックエンド起動（ターミナル1）

```bash
cd app
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

✅ `http://127.0.0.1:8000/docs` が表示されたら成功

### ステップ2: フロントエンド起動（ターミナル2）

```bash
cd frontend
npm install
REACT_APP_API_URL=http://localhost:8000 npm start
```

✅ ブラウザが自動で開いたら成功

### ステップ3: テスト

```bash
# 新しいターミナルで実行
python test_api.py
```

## 方法2: APIテスト（curl コマンド）

### 登録
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123456"}'
```

### ログイン
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123456"}'
```

## ブラウザでのテスト

1. `http://localhost:3000` を開く
2. 「登録」をクリック
3. メールアドレス（例: test@example.com）
4. パスワード（6文字以上、例: password123）
5. 「登録」をクリック
6. 「ログイン」をクリック
7. 登録したアカウント情報でログイン
8. タスクを追加してみる

## よくあるエラーと解決方法

### ❌ "Connection refused" エラー
→ バックエンド（FastAPI）が起動していない
```bash
cd app && uvicorn main:app --reload
```

### ❌ "CORS error" エラー
→ フロントエンドが正しいAPIサーバーに接続していない
```bash
# 環境変数が正しく設定されているか確認
echo $REACT_APP_API_URL
# 出力: http://localhost:8000 であることを確認
```

### ❌ ポート 3000 / 8000 が使用中
→ 別のアプリケーションがポートを使用している
```bash
# 別のポートで起動
REACT_APP_API_URL=http://localhost:8001 npm start
uvicorn main:app --reload --port 8001
```

### ❌ "ModuleNotFoundError" エラー
→ 依存パッケージがインストールされていない
```bash
cd app
pip install -r requirements.txt
```

## デプロイ方法

### バックエンドデプロイ（Railway）

1. [Railway](https://railway.app) にアカウント作成・ログイン
2. 「New Project」→「Deploy from GitHub repo」
3. このリポジトリを選択
4. 自動デプロイが開始される
5. デプロイ完了後、URL（例: `https://your-app.railway.app`）を取得

### フロントエンドデプロイ（Vercel）

1. [Vercel](https://vercel.com) にアカウント作成・ログイン
2. 「New Project」→「Import Git Repository」
3. このリポジトリを選択
4. 設定:
   - **Framework Preset**: React
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
   - **Environment Variables**:
     - `REACT_APP_API_URL`: RailwayのバックエンドURL（例: `https://your-app.railway.app`）
5. 「Deploy」をクリック
6. デプロイ完了後、URL（例: `https://your-app.vercel.app`）を取得

### デプロイ後の確認

1. VercelのURLを開く
2. ユーザー登録・ログイン
3. タスク追加・削除
4. カレンダービュー切り替え

## トラブルシューティング（デプロイ）

### ❌ バックエンドが起動しない
- Railwayのログを確認
- `requirements.txt` が正しいか確認
- Pythonバージョンが3.8以上か確認

### ❌ フロントエンドがAPIに接続できない
- Vercelの環境変数 `REACT_APP_API_URL` が正しいURLか確認
- RailwayのURLに `/api` が付かないよう注意（例: `https://your-app.railway.app`）

### ❌ カレンダーが表示されない
- `npm install` が実行されたか確認
- `react-calendar` が `package.json` に追加されているか確認

## 次のステップ

- Renderへのデプロイ → [RENDER_SETUP.md](./RENDER_SETUP.md)
- APIドキュメント → http://localhost:8000/docs (Swagger UI)
- 詳細情報 → [README.md](./README.md)

## 開発ツール

### Swagger UI (API ドキュメント & テスト)
```
http://localhost:8000/docs
```

### ReDoc (API ドキュメント)
```
http://localhost:8000/redoc
```

### React Developer Tools
ChromeウェブストアからReact Developer Toolsをインストール

### VS Code デバッグ
`.vscode/launch.json` を設定してブレークポイントを使用可能

## よく使うコマンド

```bash
# バックエンド停止（Ctrl+C）
# フロントエンド停止（Ctrl+C）

# 全ファイルをビルド（デプロイ用）
cd frontend && npm run build

# SQLiteデータベースをリセット
rm app/test.db
```

## サポート

質問や問題がある場合、まず [RENDER_SETUP.md](./RENDER_SETUP.md) のトラブルシューティングを確認してください。
