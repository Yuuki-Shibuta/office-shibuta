# しぶた行政書士事務所 ホームページ制作プロジェクト

## プロジェクト概要
- しぶた行政書士事務所のホームページをWIXから脱却し、自前のサイトに移行する
- 姉妹プロジェクト「そうさぽ青森」（sousapo-site/）で脱WIXを完了済み。同じ手法で進める

## オーナー情報
- **事務所名**：しぶた行政書士事務所
- **代表**：澁田優希（しぶた ゆうき）
- **住所**：〒030-0861 青森県青森市長島2丁目13-1 リージャス アクア青森スクエア6階
- **電話番号**：070-4697-7033
- **メール**：sousapo.aomori@gmail.com
- **営業時間**：午前10時〜午後5時（土日祝除く）
- **現在のWIXサイト**：https://www.office-shibuta.com/
- **WIXサイトのページ構成**：トップ、ご相談一覧、ブログ、ごあいさつ、他（複数ページ）

## 運営している事業
- **しぶた行政書士事務所**（本体）：相続・遺言、終活サポート、建設業許可、各種許認可申請、契約書作成、法人設立
- **そうさぽ青森**（相続特化サービス）：相続サポートセンター青森。同事務所内で運営する団体名。独自サイトあり（sousapo-aomori.com）

## 技術環境（すでに構築済み）
- **GitHubアカウント**：Yuuki-Shibuta（GitHub Pages利用可能）
- **GitHub CLI**：`/tmp/gh_install/gh_2.89.0_macOS_arm64/bin/gh`（認証済み）
- **Cloudflareアカウント**：登録済み（そうさぽ青森のドメイン移管で使用中）
- **Apple Business**：しぶた行政書士事務所で登録済み
- **Bing Places**：しぶた行政書士事務所で登録済み
- **Googleビジネスプロフィール**：オーナー登録済み
- **Homebrew**：未インストール（sudoが必要で断念）
- **git**：`/usr/bin/git` インストール済み
- **Python3 + Pillow**：利用可能（画像生成に使用）

## そうさぽ青森で得た知見・オーナーの好み

### デザインの好み
- 温かみのある色合いが好き（ベージュ・オレンジ系）
- 丸ゴシック系フォント（Zen Maru Gothic）が好評だった
- ソコスト（soco-st.com）のイラストスタイルが気に入っている
- ヒーローバナーは横幅いっぱいが良い
- 中央テキスト＋両サイドにイラストを散りばめるレイアウトが好評
- SVGコードで人物を描くのは品質に限界がある → 外部のイラスト素材を使うべき
- デザインセンスに厳しい（規則正しい配置、中央両脇の画像配置はNG）

### ヒーローバナーについて
- しぶた行政書士事務所では**写真を使いたい**（そうさぽはイラストだった）
- ただし事務所の写真は持っていない
- **フリー写真素材**（Unsplash等）で青森の風景や法律イメージの写真を使う方針
- ファーストビューでの印象を大事にしたい

### 技術的な注意点
- オーナーは技術者ではない。すべて平易な日本語で説明する
- ファイルの上書き前は確認を取る（CLAUDE.mdの安全ルール）
- 削除コマンドは実行しない
- パッケージ追加は事前説明と承認が必要
- WIXサイトはJavaScriptで動的レンダリングされるため、WebFetchでは内容を取得できない。ブラウザ経由（スクショ）で確認する必要がある

### SEO/MEO対策で実施すべきこと
- メタタグ（title, description, keywords, OGP）
- 構造化データ（LegalService型 + FAQPage型）
- sitemap.xml / robots.txt
- 画像の遅延読み込み（loading="lazy"）
- 電話番号はtel:リンク、メールはmailto:リンク
- Google Search Consoleへの登録（ドメイン移管完了後）
- GBPへのサービス詳細登録・定期投稿
- NAP（名称・住所・電話番号）の表記統一

### 使える無料素材サイト
- **ソコスト**（soco-st.com）：シンプルなイラスト、商用無料
- **いらすとや**（irasutoya.com）：かわいい系イラスト、商用無料（20点まで）
- **Unsplash**（unsplash.com）：高品質写真、商用無料
- **unDraw**（undraw.co）：フラットデザインSVG、商用無料

### GitHub Pagesでの公開手順（実績あり）
1. ローカルでサイト作成
2. `git init` → `git add` → `git commit`
3. `gh repo create [名前] --public --source=. --push`
4. GitHub Pages有効化：`gh api repos/Yuuki-Shibuta/[名前]/pages -X POST -f "build_type=legacy" -f "source[branch]=main" -f "source[path]=/"`
5. 空コミットでビルドトリガー
6. ドメイン移管（WIX → Cloudflare）→ DNS設定 → CNAME追加

### ドメイン移管の手順（実績あり）
1. WIX管理画面で「ドメインを移管する」→ 認証コード取得
2. Cloudflareで「ドメインの移管」→ 認証コード入力
3. WIXからのメールで移管承認
4. CloudflareのDNSにGitHub PagesのAレコード4つ + CNAMEを設定
   - A: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
   - CNAME: www → yuuki-shibuta.github.io
5. サイトにCNAMEファイルを追加してpush

## そうさぽ青森の状況（参考）
- サイト：sousapo-site/ フォルダに格納
- 公開URL：https://yuuki-shibuta.github.io/sousapo-aomori/
- ドメイン移管：WIX → Cloudflare 進行中（2026年4月9〜11日頃完了見込み）
- 移管完了後にやること：CNAME設定を戻す、Google Search Console登録
