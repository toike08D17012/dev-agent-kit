---
name: pytest-safe-runner
description: "このワークスペースでは、常に scripts/pre-commit/pytest.sh を使って pytest を安全に実行します。Docker 外の依存関係差異を避けたい場合や、pytest の終了コード 5 を成功扱いにしたい場合に使います。"
argument-hint: "すべてのテストを実行するか、対象のテストファイルのパスを指定してください"
user-invocable: true
disable-model-invocation: false
---

# Pytest Safe Runner

## 利用する場面

* このリポジトリのテストを、実行環境ごとの差異による依存関係の不具合なしに実行したい。
* `pytest` を実行しようとしていて、Docker 上で一貫した挙動が必要だ。
* `pytest` の終了コード `5`（テストが収集されなかった）を成功として扱いたい。

## 実行手順

1. 必要であればリポジトリのルートに移動する。
2. 直接 `pytest` を実行せず、プロジェクトのスクリプトを使う。
3. 次のどちらかを選ぶ。
* すべてのテストを実行する。
  * コマンド: bash ./scripts/pre-commit/pytest.sh
* 特定のテスト対象を実行する。
  * コマンド: bash ./scripts/pre-commit/pytest.sh tests/test_smoke.py

4. このスクリプトは常に `docker/run-docker.sh pytest` 経由でテストを実行する。
* `docker` が利用できない場合は、明示的なエラーで即座に失敗する。
5. 結果を確認する。
* 終了コード `0` は成功を意味する。
* 終了コード `5` はスクリプト側で成功に正規化される。
* それ以外の 0 以外のコードは失敗として報告する。

## 必須の動作

* このワークスペースで通常のテスト実行を行うときは、素の `pytest` を直接実行しない。
* ホスト側の依存関係のずれを最小化するため、CI に近いローカル検証ではこの手順を優先する。
* pytest 実行にローカルのフォールバック経路を追加しない。

## 完了確認

* 実行したテストコマンドがラッパースクリプトのコマンドになっている。
* 全件実行の場合: bash ./scripts/pre-commit/pytest.sh
* 対象指定実行の場合: bash ./scripts/pre-commit/pytest.sh tests/<target_file>.py
* 最終状態が、正規化後のスクリプト終了挙動に基づいて成功か失敗かを明確に示している。
* 失敗した場合は、短いエラー要約と具体的な次の修正対象を含める。

## 例となる依頼文

* プロジェクトの pytest ラッパーで安全にテストを実行して。
* 安全な pytest 手順で tests/test_smoke.py だけを実行して。
* 依存関係の影響を受けにくい pytest スクリプトで現在のブランチを確認して。
