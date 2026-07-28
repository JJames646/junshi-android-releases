# Android正式版本发布检查清单

## 发布前

- [ ] 应用ID与上一版完全相同
- [ ] 使用同一份正式签名证书
- [ ] `versionCode` 大于上一版
- [ ] `versionName` 使用 `x.y.z` 格式
- [ ] 本机数据库升级不会删除用户资料、聊天记录和测试结果
- [ ] APP启动检查失败时仍能正常进入
- [ ] 设置页可以绕过“忽略此版本”并手动检查

## 构建资源

- [ ] 生成正式签名APK：`junshi-v{versionName}.apk`
- [ ] 计算SHA-256
- [ ] 记录APK字节大小
- [ ] 准备更新说明
- [ ] 生成本次Release使用的 `update.json`
- [ ] 生成 `SHA256SUMS.txt`

## 发布GitHub Release

- [ ] 创建标签 `v{versionName}`
- [ ] 上传APK
- [ ] 上传 `update.json`
- [ ] 上传 `SHA256SUMS.txt`
- [ ] 确认Release不是Draft
- [ ] 确认APK下载地址可以访问

## 开放APP更新

- [ ] 更新 `update/stable.json`
- [ ] 运行 `python3 scripts/validate_manifest.py`
- [ ] 提交并推送到 `main`
- [ ] 确认本机更新清单校验通过
- [ ] 使用旧版APP测试自动更新提示
- [ ] 测试“忽略此版本”
- [ ] 测试设置页手动检查仍能发现被忽略版本
- [ ] 测试安装后本机数据仍然存在

## 回滚

如果新版存在严重问题，不要删除历史Release。把 `update/stable.json` 恢复为上一可用版本并重新校验。已经安装新版的用户不能通过普通覆盖安装降级，因此数据库迁移和发布前测试仍然是首要保护措施。

## 启用GitHub自动校验

当前登录凭据未授权修改GitHub Actions工作流，因此自动校验文件暂存于 `docs/workflows/validate-update-manifest.yml.example`。完成GitHub的 `workflow` 权限授权后，将它复制为 `.github/workflows/validate-update-manifest.yml` 即可启用。
