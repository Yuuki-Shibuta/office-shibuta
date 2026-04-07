#!/usr/bin/env python3
"""
しぶた行政書士事務所 ブログビルダー

_posts/ フォルダ内の .txt ファイルを読み取り、
blog/ フォルダに HTML ページを自動生成するスクリプト。

使い方:
    python3 build_blog.py

テキストファイルの書式:
    タイトル: 記事のタイトル
    日付: 2026-04-06
    概要: 記事の概要
    ---
    本文（空行で段落分け、【】で見出し、・で箇条書き）
"""

import os
import re
import glob
from datetime import datetime

# パス設定
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_DIR = os.path.join(BASE_DIR, '_posts')
BLOG_DIR = os.path.join(BASE_DIR, 'blog')
SITEMAP_PATH = os.path.join(BASE_DIR, 'sitemap.xml')
SITE_URL = 'https://www.office-shibuta.com'


def parse_post(filepath):
    """テキストファイルを読み取り、メタ情報と本文を分離する"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- で区切る
    parts = content.split('---', 1)
    if len(parts) < 2:
        print(f"  警告: {filepath} に --- 区切りがありません。スキップします。")
        return None

    header = parts[0].strip()
    body = parts[1].strip()

    # ヘッダーからメタ情報を抽出
    meta = {}
    for line in header.split('\n'):
        line = line.strip()
        if ':' in line:
            key, value = line.split(':', 1)
            meta[key.strip()] = value.strip()

    # 必須フィールドチェック
    if 'タイトル' not in meta or '日付' not in meta:
        print(f"  警告: {filepath} にタイトルまたは日付がありません。スキップします。")
        return None

    # ファイル名からスラッグ生成
    filename = os.path.basename(filepath)
    slug = os.path.splitext(filename)[0]

    return {
        'title': meta['タイトル'],
        'date': meta['日付'],
        'description': meta.get('概要', ''),
        'body': body,
        'slug': slug,
        'filepath': filepath,
    }


def text_to_html(text):
    """簡易テキスト → HTML変換"""
    lines = text.split('\n')
    html_parts = []
    in_list = False
    paragraph_lines = []

    def flush_paragraph():
        if paragraph_lines:
            p_text = '<br>'.join(paragraph_lines)
            html_parts.append(f'<p>{p_text}</p>')
            paragraph_lines.clear()

    def close_list():
        nonlocal in_list
        if in_list:
            html_parts.append('</ul>')
            in_list = False

    for line in lines:
        line = line.rstrip()

        # 空行 → 段落区切り
        if not line:
            flush_paragraph()
            close_list()
            continue

        # 【見出し】 → h3
        match = re.match(r'^【(.+?)】(.*)$', line)
        if match:
            flush_paragraph()
            close_list()
            heading = match.group(1)
            rest = match.group(2).strip()
            html_parts.append(f'<h3>{heading}</h3>')
            if rest:
                paragraph_lines.append(rest)
            continue

        # ・箇条書き → ul/li
        if line.startswith('・') or line.startswith('- '):
            flush_paragraph()
            if not in_list:
                html_parts.append('<ul>')
                in_list = True
            item = line.lstrip('・').lstrip('- ').strip()
            html_parts.append(f'<li>{item}</li>')
            continue

        # 通常テキスト
        close_list()
        paragraph_lines.append(line)

    # 残りを処理
    flush_paragraph()
    close_list()

    return '\n'.join(html_parts)


def generate_post_html(post):
    """記事ページのHTMLを生成"""
    body_html = text_to_html(post['body'])
    date_display = post['date'].replace('-', '.')

    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{post['title']} | しぶた行政書士事務所ブログ</title>
    <meta name="description" content="{post['description']}">
    <link rel="canonical" href="{SITE_URL}/blog/{post['slug']}.html">

    <meta property="og:title" content="{post['title']}｜しぶた行政書士事務所ブログ">
    <meta property="og:description" content="{post['description']}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{SITE_URL}/blog/{post['slug']}.html">
    <meta property="og:site_name" content="しぶた行政書士事務所">
    <meta property="og:locale" content="ja_JP">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=Noto+Serif+JP:wght@300;400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../style.css">
</head>
<body>

<header class="solid">
    <div class="container">
        <a href="../index.html" class="logo-mini"><span class="accent">しぶた</span>行政書士事務所</a>
        <button class="hamburger" onclick="toggleNav()" aria-label="メニュー">
            <span></span><span></span><span></span>
        </button>
        <nav id="mainNav">
            <a href="../about.html">事務所案内</a>
            <a href="../services.html">サービス一覧</a>
            <a href="../blog/">ブログ</a>
            <a href="../about.html#faq">よくある質問</a>
            <a href="../index.html#contact" class="nav-contact">無料相談はこちら</a>
        </nav>
    </div>
</header>

<section class="page-hero">
    <div class="container">
        <h1>{post['title']}</h1>
        <p>{date_display}</p>
        <div class="breadcrumb">
            <a href="../index.html">トップ</a> ／ <a href="../blog/">ブログ</a> ／ {post['title']}
        </div>
    </div>
</section>

<section class="section">
    <div class="container">
        <article class="blog-article">
            <div class="blog-meta">
                <time datetime="{post['date']}">{date_display}</time>
            </div>
            <div class="blog-body">
                {body_html}
            </div>
        </article>
        <div class="blog-back">
            <a href="../blog/" class="btn btn-navy">← ブログ一覧に戻る</a>
        </div>
    </div>
</section>

<footer>
    <div class="container">
        <div class="footer-grid">
            <div class="footer-info">
                <h4>しぶた行政書士事務所</h4>
                <p>〒030-0861<br>
                青森県青森市長島2丁目13-1<br>
                リージャス アクア青森スクエア6階<br><br>
                TEL: <a href="tel:070-4697-7033" style="color:var(--gold);">070-4697-7033</a><br>
                営業時間：平日 10:00〜17:00</p>
            </div>
            <div class="footer-links">
                <h4>ページ一覧</h4>
                <ul>
                    <li><a href="../index.html">トップ</a></li>
                    <li><a href="../services.html">サービス一覧</a></li>
                    <li><a href="../about.html">事務所案内</a></li>
                    <li><a href="../blog/">ブログ</a></li>
                    <li><a href="../about.html#office">アクセス</a></li>
                    <li><a href="../index.html#contact">お問い合わせ</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            &copy; 2026 しぶた行政書士事務所. All rights reserved.
        </div>
    </div>
</footer>

<script>
    function toggleNav() {{ document.getElementById('mainNav').classList.toggle('open'); }}
    document.querySelectorAll('#mainNav a').forEach(a => {{
        a.addEventListener('click', () => {{ document.getElementById('mainNav').classList.remove('open'); }});
    }});
</script>

</body>
</html>'''


def generate_index_html(posts):
    """ブログ一覧ページのHTMLを生成"""
    # 日付の新しい順にソート
    posts_sorted = sorted(posts, key=lambda p: p['date'], reverse=True)

    cards = ''
    for post in posts_sorted:
        date_display = post['date'].replace('-', '.')
        cards += f'''
            <a href="{post['slug']}.html" class="blog-list-item">
                <div class="blog-list-date">{date_display}</div>
                <div class="blog-list-content">
                    <h3>{post['title']}</h3>
                    <p>{post['description']}</p>
                </div>
                <div class="blog-list-arrow">→</div>
            </a>'''

    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ブログ | しぶた行政書士事務所</title>
    <meta name="description" content="しぶた行政書士事務所のブログ。相続・遺言、建設業許可、法人設立など、暮らしとビジネスに役立つ情報をお届けします。">
    <link rel="canonical" href="{SITE_URL}/blog/">

    <meta property="og:title" content="ブログ｜しぶた行政書士事務所">
    <meta property="og:description" content="相続・遺言、建設業許可、法人設立など、暮らしとビジネスに役立つ情報をお届けします。">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{SITE_URL}/blog/">
    <meta property="og:site_name" content="しぶた行政書士事務所">
    <meta property="og:locale" content="ja_JP">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=Noto+Serif+JP:wght@300;400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../style.css">
</head>
<body>

<header class="solid">
    <div class="container">
        <a href="../index.html" class="logo-mini"><span class="accent">しぶた</span>行政書士事務所</a>
        <button class="hamburger" onclick="toggleNav()" aria-label="メニュー">
            <span></span><span></span><span></span>
        </button>
        <nav id="mainNav">
            <a href="../about.html">事務所案内</a>
            <a href="../services.html">サービス一覧</a>
            <a href="../blog/">ブログ</a>
            <a href="../about.html#faq">よくある質問</a>
            <a href="../index.html#contact" class="nav-contact">無料相談はこちら</a>
        </nav>
    </div>
</header>

<section class="page-hero">
    <div class="container">
        <h1>ブログ</h1>
        <p>暮らしとビジネスに役立つ情報をお届けします</p>
        <div class="breadcrumb">
            <a href="../index.html">トップ</a> ／ ブログ
        </div>
    </div>
</section>

<section class="section">
    <div class="container">
        <div class="blog-list">{cards}
        </div>
    </div>
</section>

<footer>
    <div class="container">
        <div class="footer-grid">
            <div class="footer-info">
                <h4>しぶた行政書士事務所</h4>
                <p>〒030-0861<br>
                青森県青森市長島2丁目13-1<br>
                リージャス アクア青森スクエア6階<br><br>
                TEL: <a href="tel:070-4697-7033" style="color:var(--gold);">070-4697-7033</a><br>
                営業時間：平日 10:00〜17:00</p>
            </div>
            <div class="footer-links">
                <h4>ページ一覧</h4>
                <ul>
                    <li><a href="../index.html">トップ</a></li>
                    <li><a href="../services.html">サービス一覧</a></li>
                    <li><a href="../about.html">事務所案内</a></li>
                    <li><a href="../blog/">ブログ</a></li>
                    <li><a href="../about.html#office">アクセス</a></li>
                    <li><a href="../index.html#contact">お問い合わせ</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            &copy; 2026 しぶた行政書士事務所. All rights reserved.
        </div>
    </div>
</footer>

<script>
    function toggleNav() {{ document.getElementById('mainNav').classList.toggle('open'); }}
    document.querySelectorAll('#mainNav a').forEach(a => {{
        a.addEventListener('click', () => {{ document.getElementById('mainNav').classList.remove('open'); }});
    }});
</script>

</body>
</html>'''


def update_sitemap(posts):
    """sitemap.xml にブログ記事を追加"""
    urls = [
        ('/', '1.0'),
        ('/services.html', '0.9'),
        ('/about.html', '0.8'),
        ('/blog/', '0.8'),
    ]
    for post in sorted(posts, key=lambda p: p['date'], reverse=True):
        urls.append((f"/blog/{post['slug']}.html", '0.6'))

    today = datetime.now().strftime('%Y-%m-%d')
    entries = ''
    for url, priority in urls:
        entries += f'''    <url>
        <loc>{SITE_URL}{url}</loc>
        <lastmod>{today}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>{priority}</priority>
    </url>
'''

    sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{entries}</urlset>
'''
    with open(SITEMAP_PATH, 'w', encoding='utf-8') as f:
        f.write(sitemap)
    print(f'  sitemap.xml を更新しました（{len(urls)} ページ）')


def main():
    print('=== ブログビルダー ===')
    print()

    # _posts ディレクトリの確認
    if not os.path.exists(POSTS_DIR):
        os.makedirs(POSTS_DIR)
        print(f'  _posts/ フォルダを作成しました')

    # blog ディレクトリの確認
    if not os.path.exists(BLOG_DIR):
        os.makedirs(BLOG_DIR)
        print(f'  blog/ フォルダを作成しました')

    # テキストファイルを読み込み
    txt_files = glob.glob(os.path.join(POSTS_DIR, '*.txt'))
    if not txt_files:
        print('  _posts/ フォルダに .txt ファイルがありません。')
        print('  記事を _posts/ に置いてから再実行してください。')
        return

    print(f'  {len(txt_files)} 件の記事ファイルを発見')
    print()

    # 記事をパース
    posts = []
    for filepath in txt_files:
        filename = os.path.basename(filepath)
        print(f'  処理中: {filename}')
        post = parse_post(filepath)
        if post:
            posts.append(post)

    if not posts:
        print('  有効な記事がありません。')
        return

    print()

    # 各記事のHTMLを生成
    for post in posts:
        output_path = os.path.join(BLOG_DIR, f"{post['slug']}.html")
        html = generate_post_html(post)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  生成: blog/{post["slug"]}.html')

    # 一覧ページを生成
    index_html = generate_index_html(posts)
    index_path = os.path.join(BLOG_DIR, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_html)
    print(f'  生成: blog/index.html')

    # サイトマップを更新
    update_sitemap(posts)

    print()
    print(f'=== 完了！{len(posts)} 件の記事を生成しました ===')


if __name__ == '__main__':
    main()
