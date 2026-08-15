import os
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Any

class VaultContext:
    def __init__(self, content_dir: str):
        self.content_dir = Path(content_dir)
        self.files: Dict[str, Dict[str, Any]] = {} # rel_path -> metadata
        self.inlinks: Dict[str, Set[str]] = defaultdict(set) # target_name/stem -> set of source stems
        self._build_index()

    def _build_index(self):
        for p in self.content_dir.rglob("*.md"):
            if p.name.startswith("."):
                continue
            rel_path = p.relative_to(self.content_dir).as_posix()
            folder = p.parent.relative_to(self.content_dir).as_posix()
            if folder == ".":
                folder = ""
            
            content = ""
            try:
                content = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                pass

            # Extract outgoing wikilinks: [[link]] or [[link|alias]]
            # Ignore images ![[...]]
            raw_links = re.findall(r'(?<!\!)\[\[([^\]\|]+)(?:\|[^\]]+)?\]\]', content)
            outgoing = set()
            for l in raw_links:
                target_stem = Path(l).stem
                outgoing.add(target_stem)

            self.files[rel_path] = {
                "rel_path": rel_path,
                "folder": folder,
                "stem": p.stem,
                "name": p.name,
                "outgoing": outgoing,
                "content": content,
            }

        # Build inlinks
        for rel_path, meta in self.files.items():
            source_stem = meta["stem"]
            for target_stem in meta["outgoing"]:
                self.inlinks[target_stem].add(source_stem)

    def get_inlinks_for(self, stem: str) -> List[str]:
        return sorted(list(self.inlinks.get(stem, set())))

def evaluate_dataview_block(query_str: str, vault: VaultContext, current_file: str) -> str:
    lines = [line.strip() for line in query_str.strip().split("\n") if line.strip()]
    if not lines:
        return ""

    first_line = lines[0].upper()
    full_query = " ".join(lines)

    # 1. Check if it's the specific Subnotes Table Query
    # TABLE rows.file.link as Subnotes FROM "04_Archives/Subnotes" ... GROUP BY incoming
    if "FROM \"04_ARCHIVES/SUBNOTES\"" in full_query.upper() and ("INCOMING" in full_query.upper() or "INLINKS" in full_query.upper()):
        return _render_subnotes_table(vault)

    # 2. Check if it's the Folder Summary Table Query
    # TABLE rows.file.link AS "노트 목록", length(rows) AS "문서 수" ... GROUP BY file.folder
    if "GROUP BY FILE.FOLDER" in full_query.upper() or ("노트 목록" in full_query and "문서 수" in full_query):
        return _render_folder_summary_table(vault)

    # 3. Generic LIST query: LIST [FROM "folder"] [WHERE ...]
    if first_line.startswith("LIST"):
        return _render_generic_list(lines, vault)

    # 4. Generic TABLE query: TABLE [cols] [FROM "folder"] [WHERE ...]
    if first_line.startswith("TABLE"):
        return _render_generic_table(lines, vault)

    return ""

def _render_folder_summary_table(vault: VaultContext) -> str:
    # Target folders: Root, 01_Projects, 02_Areas, 04_Archives
    folder_groups = defaultdict(list)
    
    target_folders = ["", "01_Projects", "02_Areas", "04_Archives"]
    
    for rel_path, meta in sorted(vault.files.items(), key=lambda x: x[0]):
        folder = meta["folder"]
        # Only direct children of the target folders
        if folder in target_folders:
            folder_groups[folder].append(meta)

    rows = []
    headers = "| 영역 | 노트 목록 | 문서 수 |"
    divider = "| :--- | :--- | :---: |"
    rows.append(headers)
    rows.append(divider)

    folder_display_order = [
        ("", "최상위 (루트)"),
        ("01_Projects", "01_Projects"),
        ("02_Areas", "02_Areas"),
        ("04_Archives", "04_Archives")
    ]

    for folder_key, display_name in folder_display_order:
        files = folder_groups.get(folder_key, [])
        if not files:
            continue
        count = len(files)
        links = []
        for f in sorted(files, key=lambda x: x["stem"]):
            # Format as [[folder/file\|file]]
            stem = f["stem"]
            rel = f["rel_path"][:-3]
            links.append(f"[[{rel}\\|{stem}]]")
        
        note_list_str = "<br>".join([f"• {l}" for l in links])
        folder_col = f"**{display_name}**" if folder_key else display_name
        rows.append(f"| {folder_col} | {note_list_str} | {count} |")

    return "\n".join(rows)

def _render_subnotes_table(vault: VaultContext) -> str:
    # Find all files in 04_Archives/Subnotes
    subnotes = [m for m in vault.files.values() if m["folder"].startswith("04_Archives/Subnotes")]
    
    # All known hub notes (stems) in 01_Projects, 02_Areas, 03_Resources, 04_Archives
    known_hubs = {m["stem"]: m for m in vault.files.values() if not m["folder"].startswith("04_Archives/Subnotes")}

    # Group subnotes by incoming link (parent hub note that links to this subnote)
    groups = defaultdict(list)

    for sub in subnotes:
        incoming_stems = vault.inlinks.get(sub["stem"], set())
        # Also check if subnote itself links to a hub
        if not incoming_stems:
            incoming_stems = {s for s in sub["outgoing"] if s in known_hubs}

        matched_parents = [known_hubs[stem] for stem in incoming_stems if stem in known_hubs]
        if matched_parents:
            for p in matched_parents:
                groups[p["stem"]].append(sub)
        else:
            groups["참조 없음"].append(sub)

    # Sort groups
    rows = []
    rows.append("| 분류 | Subnotes |")
    rows.append("| :--- | :--- |")

    for group_name in sorted(groups.keys(), key=lambda x: (x == "참조 없음", x)):
        subs = sorted(groups[group_name], key=lambda s: s["stem"])
        sub_links = []
        for s in subs:
            rel = s["rel_path"][:-3]
            sub_links.append(f"• [[{rel}\\|{s['stem']}]]")
        
        sub_list_str = "<br>".join(sub_links)
        
        if group_name in known_hubs:
            hub = known_hubs[group_name]
            hub_rel = hub["rel_path"][:-3]
            category_col = f"[[{hub_rel}\\|{group_name}]]"
        else:
            category_col = group_name

        rows.append(f"| {category_col} | {sub_list_str} |")

    return "\n".join(rows)

def _render_generic_list(lines: List[str], vault: VaultContext) -> str:
    folder_match = re.search(r'FROM\s+["\']([^"\']+)["\']', " ".join(lines), re.IGNORECASE)
    folder_filter = folder_match.group(1) if folder_match else ""
    
    matched_files = []
    for rel_path, meta in vault.files.items():
        if folder_filter and not meta["folder"].startswith(folder_filter):
            continue
        matched_files.append(meta)

    if not matched_files:
        return "*노트가 없습니다.*"

    items = []
    for m in sorted(matched_files, key=lambda x: x["stem"]):
        rel = m["rel_path"][:-3]
        items.append(f"- [[{rel}|{m['stem']}]]")
    return "\n".join(items)

def _render_generic_table(lines: List[str], vault: VaultContext) -> str:
    folder_match = re.search(r'FROM\s+["\']([^"\']+)["\']', " ".join(lines), re.IGNORECASE)
    folder_filter = folder_match.group(1) if folder_match else ""
    
    matched_files = []
    for rel_path, meta in vault.files.items():
        if folder_filter and not meta["folder"].startswith(folder_filter):
            continue
        matched_files.append(meta)

    if not matched_files:
        return "*노트가 없습니다.*"

    rows = []
    rows.append("| 노트 | 위치 |")
    rows.append("| :--- | :--- |")
    for m in sorted(matched_files, key=lambda x: x["stem"]):
        rel = m["rel_path"][:-3]
        folder_display = m["folder"] if m["folder"] else "루트"
        rows.append(f"| [[{rel}|{m['stem']}]] | {folder_display} |")
    return "\n".join(rows)

def convert_dataview_queries_in_vault(content_dir: str):
    vault = VaultContext(content_dir)
    # Match dataview blocks with optional callout '>' prefix on each line
    pattern = re.compile(r'((?:^[ \t]*>[ \t]*)?)```dataview[ \t]*\n([\s\S]*?)\n\1```', re.MULTILINE | re.IGNORECASE)

    for rel_path, meta in vault.files.items():
        content = meta["content"]
        if "```dataview" not in content:
            continue

        def replacer(match):
            prefix = match.group(1) # e.g. "> " or ""
            query = match.group(2)
            # Remove leading '>' from inside the query lines if callout
            clean_query_lines = []
            for line in query.split("\n"):
                clean_line = re.sub(r'^[ \t]*>[ \t]?', '', line)
                clean_query_lines.append(clean_line)
            clean_query = "\n".join(clean_query_lines)

            converted = evaluate_dataview_block(clean_query, vault, rel_path)
            if converted:
                if prefix:
                    # Apply prefix to every converted line
                    prefixed_lines = [f"{prefix}{line}" if line else prefix.rstrip() for line in converted.split("\n")]
                    return "\n".join(prefixed_lines)
                return converted
            return match.group(0) # fallback to original

        new_content = pattern.sub(replacer, content)
        if new_content != content:
            file_path = Path(content_dir) / rel_path
            file_path.write_text(new_content, encoding="utf-8")
            print(f"  [Dataview Evaluated] Converted query in {rel_path}")

if __name__ == "__main__":
    import sys
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "content"
    convert_dataview_queries_in_vault(target_dir)
