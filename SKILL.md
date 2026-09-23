---
name: threads-sticker-to-wechat
description: Extract sticker-like media from the main post of a public Threads URL, remove exact duplicates, and create one flat ZIP for manual collection in WeChat. Use when a user asks to download, move, batch-process, or prepare Threads stickers for WeChat. Exclude ordinary photos and never claim to automate WeChat favorites.
---

# Threads Sticker to WeChat

Turn one public Threads post URL into one clean, deduplicated sticker ZIP. Optimize for speed. The final WeChat “添加” action remains manual.

## Workflow

1. Accept a public `threads.com` or `threads.net` post URL. Do not request cookies, credentials, or login.
2. Prefer the Codex in-app browser and its page-asset inspection capability. Open the URL hidden, allow share links to redirect, then inspect the rendered target post with one DOM evaluation and one asset inventory.
3. Interpret “表情包 / stickers” narrowly. Select inline GIFs, Giphy or Tenor resources, animated WebP files, or clearly sticker-like transparent images from the main post only.
4. When the main post contains explicit GIF, Giphy, or Tenor resources, select those and exclude ordinary carousel photos, quoted-post screenshots, avatars, logos, reaction icons, tracking pixels, and media from replies or related posts. Never package every asset on the page.
5. Download all high-confidence sticker assets in one browser operation. Skip preview and confirmation when classification is unambiguous.
6. Run `scripts/pack_only.py --input <download-dir> --output <final.zip>`. The script validates GIF, WebP, and PNG signatures, removes exact SHA-256 duplicates, and creates a flat ZIP containing only numbered sticker files. Choose a fresh output path; use `--force` only when the user has authorized replacing that exact ZIP.
7. Verify the ZIP entry count. Return only the ZIP link plus the number and formats of stickers; do not create or mention auxiliary files.

## Ambiguous posts

- If no explicit animated or sticker resources are present, inspect only media rendered inside the main post. Ask one concise question only when ordinary photos and stickers cannot be distinguished reliably.
- If the post contains one collage rather than separate stickers, explain that individual stickers cannot be recovered losslessly and offer the collage instead.
- If a media URL expires, reopen the post and acquire a current URL. Never replay stale asset identifiers.

## Boundaries

- Process public posts by default. Use an authenticated browser only when the user separately authorizes it.
- Download only content the user is entitled to use. Remind users not to redistribute copyrighted sticker packs without permission.
- Never edit, decrypt, inject, or copy files into WeChat storage or databases.
- Never promise bulk addition to personal WeChat favorites. This skill automates extraction and packaging, not the final collection action.
- Preserve animation. Do not convert animated media to static images.

For repository publication and installation guidance, read [references/publishing.md](references/publishing.md).
