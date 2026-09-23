# Threads 表情搬运助手

把公开 Threads 帖子主贴中的表情媒体提取出来，排除普通照片和回复区媒体，精确去重后生成一个纯表情 ZIP，方便发送到微信文件传输助手并手动添加。

## 能做什么

- 接收公开的 `threads.com` 或 `threads.net` 帖子链接。
- 优先识别主贴中的 GIF、Giphy、Tenor、WebP 和透明 PNG 表情。
- 排除普通轮播照片、引用帖截图、头像、图标、回复区和相关帖子媒体。
- 按文件内容进行 SHA-256 精确去重。
- 最终只交付一个扁平 ZIP，内部文件按 `sticker-001.gif` 的形式编号。

## 不会做什么

- 不要求或保存 Threads Cookie、密码及登录凭据。
- 不修改微信文件、数据库或收藏数据。
- 不会自动把表情加入微信；最后仍需在手机微信中长按表情并选择“添加”。
- 不保证拆分一张已经合成好的表情拼图。
- 不进行视觉近似去重；只删除内容完全相同的文件。

## 安装到 Codex

将本仓库链接交给 Codex，并要求使用 `skill-installer` 安装：

```text
请使用 skill-installer 安装这个 Skill：
https://github.com/<你的GitHub用户名>/threads-sticker-to-wechat
```

安装后新建一个任务，并发送：

```text
使用 $threads-sticker-to-wechat，把这个帖子里的表情整理成微信收藏包：
https://www.threads.com/@账号/post/帖子ID
```

## 运行要求

- Codex，以及能够渲染 Threads 并读取当前页面媒体资源的浏览器能力。
- Python 3.10 或更高版本；打包脚本仅使用 Python 标准库。
- 默认处理公开帖子。受登录或地区限制的内容可能无法提取。

## 输出与安全

输出 ZIP 仅包含通过签名检查的 GIF、WebP 或 PNG 文件。脚本默认拒绝覆盖已有 ZIP；只有显式使用 `--force` 才会替换同名文件。

本仓库采用 MIT License。该许可只覆盖仓库中的代码与文档，不授予任何第三方表情素材的版权。请仅下载和使用你有权处理的内容，不要未经授权重新分发他人的完整表情包。
