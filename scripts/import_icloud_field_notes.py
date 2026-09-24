#!/usr/bin/env python3
"""Import selected photos from public iCloud Shared Albums for Field Notes."""
from __future__ import annotations

import io
import json
import shutil
from pathlib import Path
from typing import Any

import requests
from PIL import Image, ImageOps

ALBUMS = {
    "mighty-v-passage": "D2H1XGFpZnWBxDZ",
    "northwest-hotlap": "D2Lv3J2ZSUym_d83sgEOnFyRxIQCAEQARogQoSddYqLP_nAK6QDIaVF6OYYmgLY2_VmygyQgKygoyA",
    "great-western-loop": "D2R5qXGF1G0Ie5BC1MQsIzda5cfiZnIDCnKw_LJOdR2S3jLHQpRqxNzjqHo3yn5FzInrHKth6JYA",
    "socoex": "B1l5qXGF1HoYy8ppFd3wL5nq5prbmzRRO6rkh6gcWMuW30IRSRNofIIjPNlYFWMAIGbOFhXuh12A",
    "east-side-passage": "B115qXGF1Hnrd_5XbhG4Cj3irOM-5osK6LPFItvqpyjxQppWX4ipj9Lmy3oW_PxEXg9X7-Yk7pIA",
}
OUT = Path("assets/photos/field-notes")
BASE62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Mozilla/5.0", "Accept": "application/json"})


def partition(token: str) -> int:
    digits = token[1:2] if token.startswith("A") else token[1:3]
    value = 0
    for ch in digits:
        value = value * 62 + BASE62.index(ch)
    return value


def post(token: str, path: str, payload: dict[str, Any], host: str | None = None) -> tuple[dict[str, Any], str]:
    host = host or f"p{partition(token):02d}-sharedstreams.icloud.com"
    for _ in range(4):
        url = f"https://{host}/{token}/sharedstreams/{path}"
        response = SESSION.post(url, json=payload, timeout=60)
        if response.status_code in (330, 421):
            try:
                redirect = response.json().get("X-Apple-MMe-Host")
            except Exception:
                redirect = None
            redirect = redirect or response.headers.get("X-Apple-MMe-Host")
            if redirect and redirect != host:
                host = redirect
                continue
        response.raise_for_status()
        return response.json(), host
    raise RuntimeError(f"Unable to resolve iCloud host for {token}")


def find_photos(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        if data and all(isinstance(x, dict) for x in data) and any("photoGuid" in x for x in data):
            return [x for x in data if isinstance(x, dict) and x.get("photoGuid")]
        for value in data:
            found = find_photos(value)
            if found:
                return found
    elif isinstance(data, dict):
        for key in ("photos", "items", "photoList"):
            if key in data:
                found = find_photos(data[key])
                if found:
                    return found
        for value in data.values():
            found = find_photos(value)
            if found:
                return found
    return []


def derivative_options(photo: dict[str, Any]) -> list[dict[str, Any]]:
    options: list[dict[str, Any]] = []
    derivatives = photo.get("derivatives") or {}
    iterable = derivatives.values() if isinstance(derivatives, dict) else derivatives
    if not isinstance(iterable, (list, tuple, type({}.values()))):
        return options
    for item in iterable:
        if not isinstance(item, dict):
            continue
        checksum = item.get("checksum")
        if checksum:
            options.append({"checksum": checksum, "width": int(item.get("width") or 0), "height": int(item.get("height") or 0)})
    return options


def select_indices(count: int, limit: int = 8) -> list[int]:
    if count <= limit:
        return list(range(count))
    return sorted({round(i * (count - 1) / (limit - 1)) for i in range(limit)})


def asset_url(asset: dict[str, Any], response: dict[str, Any]) -> str:
    location = asset["url_location"]
    location_data = response.get("locations", {}).get(location, {})
    scheme = location_data.get("scheme", "https")
    host = (location_data.get("hosts") or [location])[0]
    return f"{scheme}://{host}{asset['url_path']}"


def save_web_jpeg(raw: bytes, destination: Path) -> None:
    with Image.open(io.BytesIO(raw)) as source:
        image = ImageOps.exif_transpose(source).convert("RGB")
        image.thumbnail((1800, 1350), Image.Resampling.LANCZOS)
        destination.parent.mkdir(parents=True, exist_ok=True)
        image.save(destination, "JPEG", quality=84, optimize=True, progressive=True)


def import_album(slug: str, token: str) -> list[dict[str, Any]]:
    stream, host = post(token, "webstream", {"streamCtag": None})
    photos = find_photos(stream)
    photos.sort(key=lambda p: (p.get("dateCreated") or p.get("batchDateCreated") or 0, p.get("photoGuid", "")))
    chosen = [photos[i] for i in select_indices(len(photos))]
    guids = [p["photoGuid"] for p in chosen]
    urls, _ = post(token, "webasseturls", {"photoGuids": guids}, host)
    items = urls.get("items", {})

    directory = OUT / slug
    if directory.exists():
        shutil.rmtree(directory)
    directory.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, Any]] = []

    for number, photo in enumerate(chosen, 1):
        options = derivative_options(photo)
        available = [o for o in options if o["checksum"] in items]
        if not available:
            continue
        large_enough = [o for o in available if o["width"] >= 1400]
        selected = min(large_enough, key=lambda o: o["width"]) if large_enough else max(available, key=lambda o: o["width"])
        source_url = asset_url(items[selected["checksum"]], urls)
        raw = SESSION.get(source_url, timeout=120).content
        filename = f"{number:02d}.jpg"
        save_web_jpeg(raw, directory / filename)
        manifest.append({
            "src": f"assets/photos/field-notes/{slug}/{filename}",
            "photoGuid": photo["photoGuid"],
            "dateCreated": photo.get("dateCreated") or photo.get("batchDateCreated"),
            "width": selected["width"],
            "height": selected["height"],
        })
    return manifest


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, Any] = {}
    for slug, token in ALBUMS.items():
        print(f"Importing {slug}…")
        manifest[slug] = import_album(slug, token)
        print(f"  saved {len(manifest[slug])} photos")
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
