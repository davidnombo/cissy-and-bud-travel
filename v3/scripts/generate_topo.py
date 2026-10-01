#!/usr/bin/env python3
"""Generate a seamless, terrain-like contour wallpaper from one elevation field."""

from __future__ import annotations

import math
from collections import defaultdict
from pathlib import Path


WIDTH, HEIGHT = 1200.0, 900.0
COLS, ROWS = 181, 136
LEVELS = 15


def elevation(x: float, y: float) -> float:
    """Periodic domain-warped terrain with ridges, valleys, and saddles."""
    u = math.tau * x
    v = math.tau * y
    wu = u + 0.42 * math.sin(2 * v) + 0.16 * math.sin(3 * u - v)
    wv = v + 0.34 * math.sin(2 * u) - 0.14 * math.sin(u + 3 * v)
    return (
        1.10 * math.sin(wu)
        + 0.88 * math.cos(wv)
        + 0.62 * math.sin(2 * wu + wv)
        + 0.46 * math.cos(wu - 3 * wv)
        + 0.29 * math.sin(4 * wu - 2 * wv)
        + 0.22 * math.cos(3 * wu + 5 * wv)
        + 0.14 * math.sin(7 * wu + 3 * wv)
    )


def interpolate(a, b, va, vb, level):
    ratio = 0.5 if va == vb else (level - va) / (vb - va)
    return (a[0] + ratio * (b[0] - a[0]), a[1] + ratio * (b[1] - a[1]))


def key(point):
    return (round(point[0], 3), round(point[1], 3))


def join_segments(segments):
    adjacency = defaultdict(list)
    points = {}
    for index, (a, b) in enumerate(segments):
        ka, kb = key(a), key(b)
        points[ka], points[kb] = a, b
        adjacency[ka].append((index, kb))
        adjacency[kb].append((index, ka))

    unused = set(range(len(segments)))
    paths = []
    while unused:
        seed = next(iter(unused))
        a, b = segments[seed]
        start = key(a)
        if len(adjacency[key(b)]) == 1:
            start = key(b)
        elif len(adjacency[start]) == 2:
            endpoints = [k for k in (key(a), key(b)) if len(adjacency[k]) == 1]
            if endpoints:
                start = endpoints[0]

        chain = [points[start]]
        current = start
        while True:
            choices = [(idx, other) for idx, other in adjacency[current] if idx in unused]
            if not choices:
                break
            idx, other = choices[0]
            unused.remove(idx)
            current = other
            chain.append(points[current])
            if current == start:
                break
        paths.append(chain)
    return paths


def main():
    values = [
        [elevation(i / (COLS - 1), j / (ROWS - 1)) for i in range(COLS)]
        for j in range(ROWS)
    ]
    flat = sorted(value for row in values for value in row)
    low = flat[int(len(flat) * 0.06)]
    high = flat[int(len(flat) * 0.94)]
    levels = [low + (high - low) * i / (LEVELS - 1) for i in range(LEVELS)]
    dx, dy = WIDTH / (COLS - 1), HEIGHT / (ROWS - 1)
    svg_paths = []

    for level_index, level in enumerate(levels):
        segments = []
        for j in range(ROWS - 1):
            for i in range(COLS - 1):
                p = [
                    (i * dx, j * dy),
                    ((i + 1) * dx, j * dy),
                    ((i + 1) * dx, (j + 1) * dy),
                    (i * dx, (j + 1) * dy),
                ]
                z = [values[j][i], values[j][i + 1], values[j + 1][i + 1], values[j + 1][i]]
                edges = []
                for edge, (a, b) in enumerate(((0, 1), (1, 2), (2, 3), (3, 0))):
                    if (z[a] < level) != (z[b] < level):
                        edges.append((edge, interpolate(p[a], p[b], z[a], z[b], level)))
                if len(edges) == 2:
                    segments.append((edges[0][1], edges[1][1]))
                elif len(edges) == 4:
                    by_edge = dict(edges)
                    center_high = sum(z) / 4 >= level
                    if center_high == (z[0] >= level):
                        pairs = ((0, 1), (2, 3))
                    else:
                        pairs = ((0, 3), (1, 2))
                    segments.extend((by_edge[a], by_edge[b]) for a, b in pairs)

        for path in join_segments(segments):
            if len(path) < 2:
                continue
            d = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in path)
            line_class = " index" if level_index % 5 == 0 else ""
            svg_paths.append(f'  <path class="contour{line_class}" d="{d}"/>')

    output = Path(__file__).resolve().parents[1] / "assets" / "topo-terrain.svg"
    output.write_text(
        "\n".join(
            [
                '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900">',
                '  <g fill="none" stroke="#617064" stroke-width="0.72" stroke-linecap="round" stroke-linejoin="round" opacity="0.32">',
                *svg_paths,
                "  </g>",
                "</svg>",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Wrote {output} with {len(svg_paths)} continuous contour paths")


if __name__ == "__main__":
    main()
