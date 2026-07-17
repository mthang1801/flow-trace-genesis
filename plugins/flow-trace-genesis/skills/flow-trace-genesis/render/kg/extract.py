#!/usr/bin/env python3
"""extract.py — sinh graph.json cho section knowledge-graph từ GitNexus (script-first, ~0 token).

Usage:
  python3 render/kg/extract.py --doc docs/flows/<slug> \
      --repo <gitnexus-repo> --seeds "ClassA,MethodB@path-substring" \
      [--repo <repo2> --seeds "..."] [--hops 2] [--cap 200] [--gitnexus-version 1.6.4-rc.4]

- Mỗi cặp --repo/--seeds là một subgraph (gitnexus cypher chạy per-repo); các subgraph
  merge vào một graph.json, node id prefix theo repo. Cross-repo edge KHÔNG có ở v1.
- Seeds = symbol từ bảng bước (đã Read) → đánh dấu verified=true; node mở rộng k-hop
  là candidate. Seed dạng "Name@sub" lọc thêm filePath chứa "sub" khi tên trùng.
- Chỉ dùng cú pháp Kuzu đã test thật: labels(n), label(r), r.type, n.id/n.name/n.filePath/
  n.startLine. KHÔNG dùng type(r) (không tồn tại trong Kuzu).
- Version drift: index tạo bởi gitnexus khác storage-version sẽ lỗi "Database file version" —
  khi đó pin --gitnexus-version đúng bản đã analyze (hoặc re-analyze).
"""
import argparse, json, os, re, subprocess, sys
from datetime import date

EDGE_TYPES = ["CALLS", "HAS_METHOD", "IMPLEMENTS", "METHOD_IMPLEMENTS", "EXTENDS",
              "METHOD_OVERRIDES", "HANDLES_ROUTE", "DEFINES"]
NODE_LABELS = ["Class", "Method", "Function", "Interface", "Route"]
# CLI gitnexus cắt stdout ở 64KB (đo thật 2026-07-18) → giữ mỗi query nhỏ:
# chỉ RETURN id (tự parse label/file/name từ id), chunk nhỏ, LIMIT vừa.
CHUNK = 20
HOP_LIMIT = 150


def run_cypher(version, repo, query):
    cmd = ["npx", "-y", f"gitnexus@{version}", "cypher", "-r", repo, query]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    # JSON có thể lẫn warning (FTS extension...) và đôi lúc nằm bên stderr — gộp cả hai.
    out = (p.stdout + "\n" + p.stderr).strip()
    m = re.search(r'(\{.*\}|\[.*\])', out, re.S)
    if not m:
        sys.exit(f"[kg] output lạ từ gitnexus (repo {repo}, {len(out)} bytes)\n"
                 f"HEAD: {out[:200]}\nTAIL: {out[-200:]}")
    data = json.loads(m.group(0))
    if isinstance(data, list):  # CLI trả [] khi 0 rows
        return []
    if "error" in data:
        hint = ""
        if "Database file version" in data["error"]:
            hint = " → index được analyze bằng gitnexus khác storage-version; pin --gitnexus-version đúng bản đó hoặc re-analyze."
        sys.exit(f"[kg] cypher error (repo {repo}): {data['error']}{hint}")
    return parse_md_table(data.get("markdown", ""))


def parse_md_table(md):
    rows = []
    lines = [l for l in md.split("\n") if l.strip().startswith("|")]
    if len(lines) < 2:
        return rows
    header = [c.strip() for c in lines[0].strip().strip("|").split("|")]
    for line in lines[2:]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == len(header):
            rows.append(dict(zip(header, cells)))
    return rows


def q(s):
    return s.replace("\\", "\\\\").replace("'", "\\'")


def labels_pred(var):
    lst = ", ".join(f"'{l}'" for l in NODE_LABELS)
    return f"label({var}) IN [{lst}]"


def resolve_seeds(version, repo, seeds):
    resolved, missing = {}, []
    for seed in seeds:
        name, _, sub = seed.partition("@")
        rows = run_cypher(version, repo,
            f"MATCH (n) WHERE n.name = '{q(name)}' AND {labels_pred('n')} "
            f"RETURN n.id AS id, labels(n) AS l, n.name AS name, n.filePath AS fp, n.startLine AS sl LIMIT 25")
        if sub:
            rows = [r for r in rows if sub in r.get("fp", "")]
        if not rows:
            missing.append(seed)
        for r in rows:
            resolved[r["id"]] = r
    return resolved, missing


def expand(version, repo, frontier_ids, edge_types):
    """Một hop, hai chiều. Chỉ lấy id (nhẹ) — label/file/name parse từ id."""
    results = []
    et = ", ".join(f"'{t}'" for t in edge_types)
    ret = f"RETURN a.id AS aid, r.type AS rt, b.id AS bid LIMIT {HOP_LIMIT}"
    ids = sorted(frontier_ids)
    for i in range(0, len(ids), CHUNK):
        chunk = ", ".join(f"'{q(x)}'" for x in ids[i:i + CHUNK])
        for pred in (f"a.id IN [{chunk}]", f"b.id IN [{chunk}]"):
            results += run_cypher(version, repo,
                f"MATCH (a)-[r]->(b) WHERE {pred} AND r.type IN [{et}] "
                f"AND {labels_pred('a')} AND {labels_pred('b')} {ret}")
    return results


def parse_id(nid):
    """id dạng 'Label:filePath:Name[#n]' → (label, file, name)."""
    first = nid.find(":")
    last = nid.rfind(":")
    if first < 0 or last <= first:
        return "Node", "", nid
    return nid[:first], nid[first + 1:last], re.sub(r"#\d+$", "", nid[last + 1:])


def first_label(raw):
    m = re.findall(r"[A-Za-z]+", raw or "")
    return m[0] if m else "Node"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc", required=True)
    ap.add_argument("--repo", action="append", required=True)
    ap.add_argument("--seeds", action="append", required=True)
    ap.add_argument("--hops", type=int, default=2)
    ap.add_argument("--cap", type=int, default=200)
    # 1.6.6 đọc được cả storage v40 lẫn v41 (test 2026-07-18); bản cũ hơn chỉ đọc v40.
    ap.add_argument("--gitnexus-version", default=os.environ.get("GITNEXUS_VERSION", "1.6.6"))
    args = ap.parse_args()
    if len(args.repo) != len(args.seeds):
        sys.exit("[kg] số --repo phải bằng số --seeds (mỗi repo một danh sách seeds)")

    nodes, edges, all_missing, truncated = {}, {}, [], False
    for repo, seeds_str in zip(args.repo, args.seeds):
        seeds = [s.strip() for s in seeds_str.split(",") if s.strip()]
        seed_nodes, missing = resolve_seeds(args.gitnexus_version, repo, seeds)
        all_missing += [f"{repo}:{s}" for s in missing]
        for nid, r in seed_nodes.items():
            key = f"{repo}::{nid}"
            nodes[key] = {"id": key, "name": r["name"], "label": first_label(r["l"]),
                          "file": r.get("fp", ""), "line": r.get("sl", ""), "repo": repo, "verified": True}
        frontier = set(seed_nodes)
        seen = set(seed_nodes)
        for _ in range(args.hops):
            if not frontier or len(nodes) >= args.cap:
                truncated = truncated or len(nodes) >= args.cap
                break
            rows = expand(args.gitnexus_version, repo, frontier, EDGE_TYPES)
            nxt = set()
            for r in rows:
                for side in ("aid", "bid"):
                    nid = r[side]
                    key = f"{repo}::{nid}"
                    if key not in nodes:
                        if len(nodes) >= args.cap:
                            truncated = True
                            continue
                        lab, fp, nm = parse_id(nid)
                        nodes[key] = {"id": key, "name": nm, "label": lab,
                                      "file": fp, "line": "", "repo": repo, "verified": False}
                        nxt.add(nid)
                ka, kb = f"{repo}::{r['aid']}", f"{repo}::{r['bid']}"
                if ka in nodes and kb in nodes:
                    ek = f"{ka}->{kb}:{r['rt']}"
                    edges[ek] = {"source": ka, "target": kb, "type": r["rt"],
                                 "verified": nodes[ka]["verified"] and nodes[kb]["verified"]}
            frontier = nxt - seen
            seen |= nxt

    out = {
        "nodes": sorted(nodes.values(), key=lambda n: n["id"]),
        "edges": sorted(edges.values(), key=lambda e: (e["source"], e["target"], e["type"])),
        "meta": {"generated": str(date.today()), "gitnexus_version": args.gitnexus_version,
                 "repos": args.repo, "hops": args.hops, "cap": args.cap,
                 "truncated": truncated, "seeds_missing": all_missing},
    }
    path = os.path.join(args.doc.rstrip("/"), "graph.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"[kg] ✓ {path}: {len(out['nodes'])} nodes, {len(out['edges'])} edges"
          + (" (TRUNCATED tại cap)" if truncated else "")
          + (f" · seeds không thấy: {all_missing}" if all_missing else ""))


if __name__ == "__main__":
    main()
