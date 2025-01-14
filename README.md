
## 使い方

クローン後は`emv.sample`を複製して`.env`へリネームしてください。
`.env`の中に`TARGET_URL="記事一覧ページURL"`を追加した後に、`./src/`の中のソースを編集してください。
```sh
# Dockerイメージのビルド
docker compose build --no-cache \
        --build-arg UID=$(id -u) \
        --build-arg GID=$(id -g) \
        --build-arg USERNAME=$(whoami)

# 起動
docker compose up -d

# コンテナのshellに入る
docker exec -it app sh

# Pythonスクリプトの実行
task docker:run

# 停止
task docker:stop
```

以下メモ
---

## ローカルでセットアップ
```sh
# uv
curl -LsSf https://astral.sh/uv/install.sh
uv version
> uv 0.4.22

# task
sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d
task -v
> Task version: v3.39.0 (h1:Loe6ppP1x38Puv1M2wigp91bH/garCt0vLWkJsiTWNI=)
```

## dockerでセットアップ
```sh
# Taskがインストール済みなら
task docker:build
task docker:sh

# Taskが未インストールなら
docker compose build --no-cache \
        --build-arg UID=$(id -u) \
        --build-arg GID=$(id -g) \
        --build-arg USERNAME=$(whoami)

docker compose up -d
docker exec -it コンテナ名 sh
```

## 仮想環境、実行
```sh
task new                  # 仮想環境セットアップ
source .venv/bin/activate # 仮想環境に入る
task run                  # pythonスクリプトの実行
```

### メモ
```sh
# 仮想環境に入る
source .venv/bin/activate

# 仮想環境から抜ける
deactivate
```
