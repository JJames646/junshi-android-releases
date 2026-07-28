# 军师 Android 更新仓库

这个仓库只负责发布军师 Android 安装包、版本清单和知识包更新，不存放用户数据、API Key、Android 签名证书或应用源代码。

## APP 使用的更新入口

- 稳定版清单：`https://raw.githubusercontent.com/JJames646/junshi-android-releases/main/update/stable.json`
- 正式安装包：GitHub Releases
- 当前状态：仓库已经初始化，首个 Android 正式版发布前 `latest` 保持为 `null`

APP 启动后每天最多自动检查一次稳定版清单。用户忽略某个版本后，该版本不再自动弹出；设置页的“检查更新”始终可以手动检查，并且不会受忽略记录限制。出现更高的 `versionCode` 时，APP会重新提示。

## Release 资源命名

每个正式版本使用 `v{versionName}` 标签，例如 `v1.0.1`，并至少包含：

```text
junshi-v1.0.1.apk
update.json
SHA256SUMS.txt
```

APK必须使用与首个正式版本相同的应用ID和签名证书，并且新版 `versionCode` 必须递增。

## 发布顺序

1. 构建并签名APK。
2. 计算APK的SHA-256。
3. 创建GitHub Release并上传完整资源。
4. 验证APK下载地址可访问。
5. 最后更新 `update/stable.json`，让APP发现新版本。

完整步骤见 [发布检查清单](docs/RELEASE_CHECKLIST.md)。

更新清单的本机校验命令：

```bash
python3 scripts/validate_manifest.py
```

GitHub Actions校验模板已保存在 `docs/workflows/`。当前GitHub登录凭据没有修改工作流的权限，因此模板尚未启用，不影响版本清单和Release下载功能。

## 安全要求

- 禁止提交 `.jks`、`.keystore`、密码、Token和任何 `.env` 文件。
- 签名证书至少保留两份离线加密备份。
- APP下载APK后必须校验SHA-256，再交给Android系统安装器。
- 更新失败不能阻止用户进入APP或读取本机数据。
