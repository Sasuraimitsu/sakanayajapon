#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub リポジトリの description / topics を一括設定するスクリプト。

Claude の実行環境からは GitHub の「リポジトリ設定の書き込み」がプロキシで遮断されるため
（Repository settings writes are not permitted through this proxy）、
このスクリプトを手元の PC で実行してください。

── 使い方 ────────────────────────────────────────────────
  1. Personal Access Token を用意する
     https://github.com/settings/tokens?type=beta
     Repository access: All repositories
     Permissions → Repository permissions → Metadata: Read and write (topics に必要)
                                          → Administration: Read and write (description / archive に必要)

  2. 確認（何も変更しない。まずこれを実行して差分を見る）
     export GITHUB_TOKEN=github_pat_xxxxxxxx
     python3 apply-repo-metadata.py

  3. 適用
     python3 apply-repo-metadata.py --apply

  4. Archive（任意・読み取り専用化。--apply と併用）
     python3 apply-repo-metadata.py --apply --archive

── 注意 ────────────────────────────────────────────────
  * Archive したリポジトリは GitHub の画面から手動で解除できます（元に戻せます）。
  * ただし sakanayajapon-air は「価格を含む script.js を先に削除してから」Archive してください。
    Archive しても公開状態は続き、誰でも価格を読めるためです。
"""

import argparse
import json
import sys
import urllib.error
import urllib.request

OWNER = "Sasuraimitsu"
API = "https://api.github.com"

# (リポジトリ名, description, topics, Archive対象か)
#   description を None にすると、そのリポジトリの description は変更しない。
#   topics を None にすると、topics は変更しない。
REPOS = [
    # ── SAKANAYA JAPON ────────────────────────────────────────
    ("sakanayajapon",
     "SAKANAYA JAPON 個人向け公式サイト（カンボジア・プノンペンの魚屋／鮮魚・刺身の宅配）",
     ["sakanaya-japon", "cambodia", "seafood", "website", "github-pages"],
     False),
    ("sakanayajapon-air",
     "【旧版】法人向け商品カタログの試作。後継は sakanaya-japon/sakanaya-productlist",
     ["sakanaya-japon", "deprecated", "product-catalog"],
     True),   # ★ 先に価格データを削除してから Archive すること
    ("sakanaya-punch",
     "SAKANAYA JAPON 勤怠打刻システム（QRキオスク＋PIN認証／GASバックエンド）",
     ["sakanaya-japon", "attendance", "google-apps-script", "qrcode", "internal-tool"],
     False),
    ("sakanaya-productlist",
     "【移転案内】商品カタログは sakanaya-japon/sakanaya-productlist へ移転しました",
     ["sakanaya-japon", "redirect-notice"],
     False),  # 案内期間（3か月目安）の終了後に Archive

    # ── JCFS（カンボジア漁港開発） ──────────────────────────────
    ("JCFS",
     "JCFS カンボジア漁港開発プロジェクト 公式サイト（日本製FRP漁船の導入・インパクト投資）",
     ["jcfs", "cambodia", "fishery", "impact-investing", "website"],
     False),
    ("JCFS-sub",
     "JCFS プロジェクト 投資家向けページ（ガバナンス・セキュリティ・漁船モデル紹介）",
     ["jcfs", "cambodia", "fishery", "investor-relations"],
     False),
    ("jcfs-all",
     "JCFS プロトコル 1ページ紹介サイト",
     ["jcfs", "cambodia", "fishery", "landing-page"],
     False),

    # ── METIS ────────────────────────────────────────────────
    ("metis-order-web",
     "METIS B2B受注サイト（system5 フロントエンド）",
     ["metis", "b2b", "order-system", "website"],
     False),
    ("metis-photos",
     None,  # 既存の英語 description が適切なため変更しない
     ["metis", "images", "assets"],
     False),

    # ── その他 ────────────────────────────────────────────────
    ("ISEC",
     "伊勢志摩水産物輸出促進協議会 公式サイト（三重県志摩市）",
     ["iseshima", "seafood", "export", "website"],
     False),
    ("smallearthtrading",
     "SMALL EARTH TRADING Co.,ltd 公式サイト（輸送サービス案内・手続きの流れ・FAQ）",
     ["logistics", "cambodia", "website"],
     False),
    ("cambodia-products",
     "カンボジア産品の通販サイト（ニャムガウスープ・塩漬けライム・乾燥ハーブ）",
     ["cambodia", "ec", "food", "website"],
     False),
    ("acledasupport",
     "ACLEDA銀行 口座開設サポート案内（日本語／英語）",
     ["cambodia", "banking", "guide", "website"],
     False),
    ("privacy-policy",
     "各サービス共通のプライバシーポリシー掲載ページ",
     ["privacy-policy", "legal"],
     False),
]


def request(token, method, path, payload=None):
    """GitHub API を叩き、(成功したか, HTTPステータス, メッセージ) を返す。

    ネットワーク障害を「成功」と誤表示しないよう、例外は必ず失敗として扱う。
    """
    url = f"{API}{path}"
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if data is not None:
        req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            return True, res.status, ""
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            msg = json.loads(body).get("message", body)
        except json.JSONDecodeError:
            msg = body
        return False, e.code, msg
    except urllib.error.URLError as e:
        return False, 0, f"ネットワークエラー: {e.reason}"
    except OSError as e:
        return False, 0, f"通信に失敗しました: {e}"


def main():
    parser = argparse.ArgumentParser(description="リポジトリの description / topics を一括設定する")
    parser.add_argument("--apply", action="store_true",
                        help="実際に変更を適用する（省略時は確認のみで何も変更しない）")
    parser.add_argument("--archive", action="store_true",
                        help="Archive 対象に指定したリポジトリを読み取り専用化する（--apply と併用）")
    parser.add_argument("--token", default=None,
                        help="Personal Access Token（省略時は環境変数 GITHUB_TOKEN）")
    args = parser.parse_args()

    import os
    token = args.token or os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        print("エラー: トークンがありません。export GITHUB_TOKEN=... を設定するか --token を指定してください。",
              file=sys.stderr)
        return 2

    if not args.apply:
        print("=== 確認モード（何も変更しません）===")
        print("実際に反映するには --apply を付けて再実行してください。\n")

    failures = []
    changed = 0

    for name, desc, topics, archivable in REPOS:
        print(f"── {OWNER}/{name}")

        if desc is not None:
            print(f"   description: {desc}")
            if args.apply:
                ok, status, msg = request(token, "PATCH", f"/repos/{OWNER}/{name}",
                                          {"description": desc})
                if ok:
                    changed += 1
                else:
                    print(f"   ✗ description 失敗 (HTTP {status}): {msg}")
                    failures.append((name, "description", status, msg))

        if topics is not None:
            print(f"   topics:      {', '.join(topics)}")
            if args.apply:
                ok, status, msg = request(token, "PUT", f"/repos/{OWNER}/{name}/topics",
                                          {"names": topics})
                if ok:
                    changed += 1
                else:
                    print(f"   ✗ topics 失敗 (HTTP {status}): {msg}")
                    failures.append((name, "topics", status, msg))

        if archivable:
            if args.archive and args.apply:
                print("   archive:     実行します")
                ok, status, msg = request(token, "PATCH", f"/repos/{OWNER}/{name}",
                                          {"archived": True})
                if ok:
                    changed += 1
                else:
                    print(f"   ✗ archive 失敗 (HTTP {status}): {msg}")
                    failures.append((name, "archive", status, msg))
            else:
                print("   archive:     対象（--archive を付けると実行）")

    print()
    if not args.apply:
        print("確認モードのため、変更は行われていません。")
        return 0

    if failures:
        print(f"完了しましたが {len(failures)} 件のエラーがあります:")
        for name, kind, status, msg in failures:
            print(f"  - {name} / {kind}: HTTP {status} {msg}")
        print("\nHTTP 403 の場合はトークンの権限不足です。")
        print("Administration: Read and write / Metadata: Read and write を確認してください。")
        return 1

    print(f"{changed} 件の設定を適用しました。エラーはありません。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
