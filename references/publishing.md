# Publishing and installation

Publish the skill from a clean public GitHub repository. Keep the skill at the repository root so a repository URL is sufficient for installation.

Recommended repository contents:

```text
threads-sticker-to-wechat/
  .gitignore
  LICENSE
  README.md
  SKILL.md
  agents/openai.yaml
  references/publishing.md
  scripts/pack_only.py
  tests/test_pack_only.py
```

Before creating a release:

1. Run the skill validator against the repository root.
2. Run `python -m unittest discover -s tests -v`.
3. Confirm the repository contains no downloaded stickers, ZIP archives, captured page data, cookies, credentials, absolute local paths, or WeChat account data.
4. Install the repository into a clean Codex environment and run one public Threads post end to end.
5. Tag the tested commit as the release; use a pre-release tag when browser behavior has not been verified recently.

Users can ask Codex to install the GitHub repository with `skill-installer`, then invoke `$threads-sticker-to-wechat` with a public Threads post URL.

State these limits on the repository page:

- A browser capability that can render Threads and access current media resources is required.
- Public posts are processed by default.
- The final deliverable is one flat ZIP containing validated GIF, WebP, or PNG sticker files.
- Deduplication is exact by SHA-256; visually similar files may remain.
- The skill does not automatically add files to WeChat personal favorites.
- Users are responsible for copyright and redistribution permission.
