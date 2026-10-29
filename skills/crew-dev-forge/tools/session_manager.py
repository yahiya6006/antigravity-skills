#!/usr/bin/env python3
"""
Session Manager for crew-dev-forge skill.
Lightweight CLI tool to manage, archive, and reset project audit sessions.
"""

import os
import sys
import shutil
import argparse
from datetime import datetime
from pathlib import Path


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Session manager for crew-dev-forge audit sessions."
    )
    parser.add_argument(
        "--action",
        choices=["archive", "status", "list"],
        default="archive",
        help="Action to perform (default: archive)",
    )
    parser.add_argument(
        "--project",
        "-p",
        required=True,
        help="Project name (usually current directory name)",
    )
    parser.add_argument(
        "--audit-dir",
        "-d",
        default=".audit/crew-dev-forge",
        help="Path to crew-dev-forge audit directory (default: .audit/crew-dev-forge)",
    )
    return parser.parse_args()


def archive_session(project_name: str, audit_base: str) -> int:
    audit_path = Path(audit_base).resolve()
    project_dir = audit_path / project_name
    archive_base = audit_path / "_archive"

    if not project_dir.exists():
        project_dir.mkdir(parents=True, exist_ok=True)
        print(f"[session_manager] Project directory did not exist. Initialized fresh: {project_dir}")
        return 0

    items = list(project_dir.iterdir())
    if not items:
        print(f"[session_manager] Session directory is already clean: {project_dir}")
        return 0

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target_archive = archive_base / f"{project_name}_{timestamp}"
    target_archive.mkdir(parents=True, exist_ok=True)

    moved_count = 0
    for item in items:
        try:
            dest = target_archive / item.name
            shutil.move(str(item), str(dest))
            moved_count += 1
        except Exception as e:
            print(f"[session_manager] Warning: Failed to move {item.name}: {e}", file=sys.stderr)

    # Ensure clean project directory remains ready for fresh session
    project_dir.mkdir(parents=True, exist_ok=True)

    # Remove lingering active state file if any
    active_state_file = project_dir / ".active_state"
    if active_state_file.exists():
        active_state_file.unlink(missing_ok=True)

    print(
        f"[session_manager] ✅ Archived {moved_count} items for project '{project_name}' to:\n"
        f"                  {target_archive}\n"
        f"[session_manager] Active session cleared. Ready for fresh execution."
    )
    return 0


def status_session(project_name: str, audit_base: str) -> int:
    audit_path = Path(audit_base).resolve()
    project_dir = audit_path / project_name
    state_file = project_dir / ".active_state"

    if not project_dir.exists():
        print(f"[session_manager] No active session found for '{project_name}'.")
        return 0

    state = state_file.read_text().strip() if state_file.exists() else "UNINITIALIZED"
    files = [f.name for f in project_dir.iterdir() if f.is_file()]
    print(f"[session_manager] Project: {project_name}")
    print(f"[session_manager] Path: {project_dir}")
    print(f"[session_manager] Current State: {state}")
    print(f"[session_manager] Tracked Files ({len(files)}): {', '.join(files) if files else 'None'}")
    return 0


def list_sessions(audit_base: str) -> int:
    audit_path = Path(audit_base).resolve()
    if not audit_path.exists():
        print(f"[session_manager] Audit base directory does not exist: {audit_path}")
        return 0

    projects = [p.name for p in audit_path.iterdir() if p.is_dir() and not p.name.startswith("_") and not p.name.startswith(".")]
    archives = []
    archive_dir = audit_path / "_archive"
    if archive_dir.exists():
        archives = [a.name for a in archive_dir.iterdir() if a.is_dir()]

    print(f"[session_manager] Active Projects ({len(projects)}): {', '.join(projects) if projects else 'None'}")
    print(f"[session_manager] Archived Sessions ({len(archives)}): {', '.join(archives) if archives else 'None'}")
    return 0


def main():
    args = parse_arguments()
    if args.action == "archive":
        sys.exit(archive_session(args.project, args.audit_dir))
    elif args.action == "status":
        sys.exit(status_session(args.project, args.audit_dir))
    elif args.action == "list":
        sys.exit(list_sessions(args.audit_dir))
    else:
        print(f"[session_manager] Unknown action: {args.action}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
