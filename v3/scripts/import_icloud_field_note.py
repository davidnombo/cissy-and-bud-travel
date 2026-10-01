#!/usr/bin/env python3
"""Import one public iCloud shared album into a Field Note rotation pool."""

import argparse
import json
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def album_token(url):
    return url.split("#", 1)[-1]


def initial_host(token):
    digits = token[1:2] if token.startswith("A") else token[1:3]
    partition = 0
    for char in digits:
        partition = partition * 62 + ALPHABET.index(char)
    return f"p{partition:02d}-sharedstreams.icloud.com"


def post(state, path, payload):
    for _ in range(4):
        request = urllib.request.Request(
            f"https://{state['host']}/{state['token']}/sharedstreams/{path}",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        )
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            data = json.loads(error.read() or b"{}")
            redirect = data.get("X-Apple-MMe-Host") or error.headers.get("X-Apple-MMe-Host")
            if redirect:
                state["host"] = redirect
                continue
            raise
    raise RuntimeError("Too many iCloud host redirects")


def find_photos(value):
    if isinstance(value, list):
        if any(isinstance(item, dict) and item.get("photoGuid") for item in value):
            return [item for item in value if isinstance(item, dict) and item.get("photoGuid")]
        for item in value:
            result = find_photos(item)
            if result:
                return result
    if isinstance(value, dict):
        for item in value.values():
            result = find_photos(item)
            if result:
                return result
    return []


def asset_source(assets, photo):
    items = assets.get("items", {})
    choices = [item for item in (photo.get("derivatives") or {}).values() if item.get("checksum") in items]
    if not choices:
        raise RuntimeError(f"No downloadable asset for {photo['photoGuid']}")
    # Prefer a web-sized source at or above 1800px; otherwise use the largest derivative.
    choices.sort(key=lambda item: max(int(item.get("width") or 0), int(item.get("height") or 0)))
    choice = next((item for item in choices if max(int(item.get("width") or 0), int(item.get("height") or 0)) >= 1800), choices[-1])
    asset = items[choice["checksum"]]
    location = asset["url_location"]
    location_data = assets.get("locations", {}).get(location, {})
    host = (location_data.get("hosts") or [location])[0]
    return f"{location_data.get('scheme', 'https')}://{host}{asset['url_path']}", choice


def plain_caption(photo):
    return (photo.get("caption") or "").strip()


def safe_name(index, photo, extension):
    guid = photo["photoGuid"].split("-", 1)[0].lower()
    return f"{index:02d}-{guid}.{extension}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    parser.add_argument("album_url")
    args = parser.parse_args()
    token = album_token(args.album_url)
    state = {"token": token, "host": initial_host(token)}
    photos = find_photos(post(state, "webstream", {"streamCtag": None}))
    assets = post(state, "webasseturls", {"photoGuids": [photo["photoGuid"] for photo in photos]})
    destination = ROOT / "assets/photos/field-notes" / args.slug
    destination.mkdir(parents=True, exist_ok=True)
    pool = []
    image_metadata = json.loads((ROOT / "content/images.json").read_text())

    expected = set()
    for index, photo in enumerate(photos, 1):
        url, derivative = asset_source(assets, photo)
        with urllib.request.urlopen(url, timeout=120) as response:
            source = response.read()
            content_type = response.headers.get_content_type()
        extension = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}.get(content_type, "jpg")
        filename = safe_name(index, photo, extension)
        expected.add(filename)
        output = destination / filename
        output.write_bytes(source)
        width = int(derivative.get("width") or 0)
        height = int(derivative.get("height") or 0)
        caption = plain_caption(photo)
        alt = caption or "California Expedition photograph"
        relative = f"field-notes/{args.slug}/{filename}"
        pool.append({
            "src": relative,
            "alt": alt,
            "caption": caption or "Untitled — California Expedition",
        })
        image_metadata[relative] = {
            "width": width,
            "height": height,
            "photoGuid": photo["photoGuid"],
            "dateCreated": photo.get("dateCreated") or photo.get("batchDateCreated"),
            "expedition": args.slug,
        }
        print(f"{index:02d}/{len(photos)} {filename} {caption}")

    for old in destination.iterdir():
        if not old.is_file():
            continue
        if old.name not in expected:
            old.unlink()
            image_metadata.pop(f"field-notes/{args.slug}/{old.name}", None)

    pools_path = ROOT / "content/field-note-photos.json"
    pools = json.loads(pools_path.read_text())
    pools[args.slug] = pool
    pools_path.write_text(json.dumps(pools, indent=2, ensure_ascii=False) + "\n")
    (ROOT / "content/images.json").write_text(json.dumps(image_metadata, indent=2, ensure_ascii=False) + "\n")
    print(f"Imported {len(pool)} photos into {args.slug}")


if __name__ == "__main__":
    main()
