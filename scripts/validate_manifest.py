#!/usr/bin/env python3
"""使用Python标准库校验军师Android更新清单。"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


MANIFEST_PATH = Path(__file__).resolve().parents[1] / "update" / "stable.json"
EXPECTED_REPOSITORY = "JJames646/junshi-android-releases"
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
SHA256_PATTERN = re.compile(r"^[a-fA-F0-9]{64}$")


def fail(message: str) -> None:
    print(f"更新清单校验失败：{message}", file=sys.stderr)
    raise SystemExit(1)


def require_type(value: object, expected_type: type, field: str) -> None:
    if not isinstance(value, expected_type):
        fail(f"{field} 类型不正确")


def main() -> None:
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"无法读取JSON：{error}")

    if manifest.get("schemaVersion") != 1:
        fail("schemaVersion 必须为 1")
    if manifest.get("channel") != "stable":
        fail("channel 必须为 stable")
    if manifest.get("repository") != EXPECTED_REPOSITORY:
        fail(f"repository 必须为 {EXPECTED_REPOSITORY}")

    latest = manifest.get("latest")
    if latest is None:
        print("更新清单有效：尚未发布首个Android正式版本")
        return

    require_type(latest, dict, "latest")
    required_fields = {
        "versionCode",
        "versionName",
        "minimumVersionCode",
        "tag",
        "downloadUrl",
        "fileSize",
        "sha256",
        "releaseNotes",
        "publishedAt",
    }
    missing_fields = sorted(required_fields - latest.keys())
    if missing_fields:
        fail(f"latest 缺少字段：{', '.join(missing_fields)}")

    version_code = latest["versionCode"]
    minimum_version_code = latest["minimumVersionCode"]
    if not isinstance(version_code, int) or version_code < 1:
        fail("versionCode 必须是大于0的整数")
    if not isinstance(minimum_version_code, int) or minimum_version_code < 1:
        fail("minimumVersionCode 必须是大于0的整数")
    if minimum_version_code > version_code:
        fail("minimumVersionCode 不能大于 versionCode")

    version_name = latest["versionName"]
    if not isinstance(version_name, str) or not SEMVER_PATTERN.fullmatch(
        version_name
    ):
        fail("versionName 必须使用 x.y.z 格式")
    if latest["tag"] != f"v{version_name}":
        fail("tag 必须等于 v + versionName")

    parsed_url = urlparse(latest["downloadUrl"])
    expected_prefix = f"/{EXPECTED_REPOSITORY}/releases/download/{latest['tag']}/"
    if (
        parsed_url.scheme != "https"
        or parsed_url.netloc != "github.com"
        or not parsed_url.path.startswith(expected_prefix)
        or not parsed_url.path.endswith(".apk")
    ):
        fail("downloadUrl 必须指向本仓库对应标签下的HTTPS APK")

    if not isinstance(latest["fileSize"], int) or latest["fileSize"] < 1:
        fail("fileSize 必须是大于0的整数")
    if not isinstance(latest["sha256"], str) or not SHA256_PATTERN.fullmatch(
        latest["sha256"]
    ):
        fail("sha256 必须是64位十六进制字符串")
    if (
        not isinstance(latest["releaseNotes"], list)
        or not latest["releaseNotes"]
        or not all(
            isinstance(note, str) and note.strip()
            for note in latest["releaseNotes"]
        )
    ):
        fail("releaseNotes 必须包含至少一条非空更新说明")

    print(
        "更新清单有效："
        f"{latest['versionName']}（versionCode {latest['versionCode']}）"
    )


if __name__ == "__main__":
    main()
