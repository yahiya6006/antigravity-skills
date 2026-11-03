#!/usr/bin/env python3
"""
Session Manager for crew-dev-forge skill.
CLI tool to manage, archive, resume, export, and check project audit sessions.
"""

import os
import sys
import json
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
        choices=["archive", "status", "list", "resume", "export", "inspect-stack", "export-adrs", "check"],
        default="archive",
        help="Action to perform (default: archive)",
    )
    parser.add_argument(
        "--project",
        "-p",
        default="",
        help="Project name (usually current directory name)",
    )
    parser.add_argument(
        "--project-root",
        "-r",
        default=".",
        help="Root directory of the workspace project (default: current working directory)",
    )
    parser.add_argument(
        "--audit-dir",
        "-d",
        default=".audit/crew-dev-forge",
        help="Path to crew-dev-forge audit directory (default: .audit/crew-dev-forge)",
    )
    return parser.parse_args()


def resolve_paths(project_root: str, audit_dir: str, project_name: str):
    root_path = Path(project_root).resolve()
    audit_base = Path(audit_dir)
    if not audit_base.is_absolute():
        audit_path = (root_path / audit_base).resolve()
    else:
        audit_path = audit_base.resolve()

    project_dir = audit_path / project_name if project_name else audit_path
    return root_path, audit_path, project_dir


def archive_session(project_name: str, project_root: str, audit_dir: str) -> int:
    if not project_name:
        print("[session_manager] Error: --project is required for archive action.", file=sys.stderr)
        return 1

    _, audit_path, project_dir = resolve_paths(project_root, audit_dir, project_name)
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

    project_dir.mkdir(parents=True, exist_ok=True)

    active_state_file = project_dir / ".active_state"
    if active_state_file.exists():
        active_state_file.unlink(missing_ok=True)

    print(
        f"[session_manager] ✅ Archived {moved_count} items for project '{project_name}' to:\n"
        f"                  {target_archive}\n"
        f"[session_manager] Active session cleared. Ready for fresh execution."
    )
    return 0


def status_session(project_name: str, project_root: str, audit_dir: str) -> int:
    if not project_name:
        print("[session_manager] Error: --project is required for status action.", file=sys.stderr)
        return 1

    _, _, project_dir = resolve_paths(project_root, audit_dir, project_name)
    state_file = project_dir / ".active_state"
    meta_file = project_dir / "session_meta.json"

    if not project_dir.exists():
        print(f"[session_manager] No active session found for '{project_name}'.")
        return 0

    state = state_file.read_text().strip() if state_file.exists() else "UNINITIALIZED"
    meta_info = {}
    if meta_file.exists():
        try:
            meta_info = json.loads(meta_file.read_text())
        except Exception:
            pass

    files = [f.name for f in project_dir.iterdir() if f.is_file()]
    print(f"[session_manager] Project: {project_name}")
    print(f"[session_manager] Path: {project_dir}")
    print(f"[session_manager] Current State: {state}")
    print(f"[session_manager] Fast Mode: {meta_info.get('fast_mode', 'Unknown')}")
    print(f"[session_manager] Architecture Type: {meta_info.get('architecture_type', 'Unknown')}")
    print(f"[session_manager] Tracked Files ({len(files)}): {', '.join(files) if files else 'None'}")
    return 0


def resume_session(project_name: str, project_root: str, audit_dir: str) -> int:
    if not project_name:
        print("[session_manager] Error: --project is required for resume action.", file=sys.stderr)
        return 1

    _, _, project_dir = resolve_paths(project_root, audit_dir, project_name)
    state_file = project_dir / ".active_state"
    meta_file = project_dir / "session_meta.json"
    decisions_file = project_dir / "architecture_decisions.md"

    if not project_dir.exists() or not state_file.exists():
        print(json.dumps({
            "project": project_name,
            "resumable": False,
            "reason": "No active session or .active_state found"
        }, indent=2))
        return 0

    state = state_file.read_text().strip()
    meta_info = {}
    if meta_file.exists():
        try:
            meta_info = json.loads(meta_file.read_text())
        except Exception:
            pass

    completed_roles = []
    if decisions_file.exists():
        content = decisions_file.read_text()
        role_headers = [
            ("0_Discovery_Strategist", "### 🧭 Discovery Strategist"),
            ("0_Triage", "### 🧭 Triage Consensus"),
            ("1_Tech_Lead", "### 🏛️ Tech Lead Consensus"),
            ("2_UX_Architect", "### 🎨 UX Architect Consensus"),
            ("3_Data_Architect", "### 🗄️ Data Architect Consensus"),
            ("4_Backend_Architect", "### ⚙️ Backend Architect Consensus"),
            ("5_DevOps_Engineer", "### 🛡️ DevOps Engineer Consensus"),
            ("6_QA_Tester", "### 🧪 QA Tester Consensus"),
            ("7_Principal_Reviewer", "### 🧐 Principal Reviewer Consensus"),
            ("8_PM_Review", "### 🚀 Turn 8 Refinements Ledger"),
        ]
        for role_id, header in role_headers:
            if header in content:
                completed_roles.append(role_id)

    result = {
        "project": project_name,
        "active_state": state,
        "is_completed": state == "STATE: COMPLETED",
        "resumable": state != "STATE: COMPLETED" and state != "UNINITIALIZED",
        "fast_mode": meta_info.get("fast_mode", False),
        "architecture_type": meta_info.get("architecture_type", "FULLSTACK"),
        "completed_roles": completed_roles,
        "session_meta_exists": meta_file.exists(),
        "decisions_file_exists": decisions_file.exists(),
    }

    print(json.dumps(result, indent=2))
    return 0


def list_sessions(project_root: str, audit_dir: str) -> int:
    _, audit_path, _ = resolve_paths(project_root, audit_dir, "")
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


def export_decisions(project_name: str, project_root: str, audit_dir: str) -> int:
    if not project_name:
        print("[session_manager] Error: --project is required for export action.", file=sys.stderr)
        return 1

    root_path, _, project_dir = resolve_paths(project_root, audit_dir, project_name)
    decisions_file = project_dir / "architecture_decisions.md"

    if not decisions_file.exists():
        print(f"[session_manager] Error: {decisions_file} does not exist.", file=sys.stderr)
        return 1

    export_path = root_path / f"ARCHITECTURE_DECISIONS_{project_name}.md"
    shutil.copy2(str(decisions_file), str(export_path))
    print(f"[session_manager] ✅ Exported architectural decisions to: {export_path}")
    return 0


def inspect_stack(project_name: str, project_root: str, audit_dir: str) -> int:
    root_path, _, project_dir = resolve_paths(project_root, audit_dir, project_name)
    project_dir.mkdir(parents=True, exist_ok=True)

    inspection = {
        "project_name": project_name,
        "scanned_at": datetime.now().isoformat(),
        "is_greenfield": True,
        "frontend": None,
        "backend": None,
        "database": None,
        "styling": None,
        "detected_manifests": [],
    }

    # 1. Frontend inspection
    pkg_files = [p for p in root_path.glob("**/package.json") if "node_modules" not in str(p) and ".next" not in str(p) and "dist" not in str(p)]
    if pkg_files:
        inspection["is_greenfield"] = False
        f_pkg = pkg_files[0]
        inspection["detected_manifests"].append(str(f_pkg.relative_to(root_path)))
        try:
            data = json.loads(f_pkg.read_text(encoding="utf-8"))
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            inspection["frontend"] = {
                "manifest": str(f_pkg.relative_to(root_path)),
                "framework": "Next.js" if "next" in deps else ("React" if "react" in deps else ("Vue" if "vue" in deps else "Unknown")),
                "build_tool": "Vite" if "vite" in deps else ("Next.js" if "next" in deps else ("Webpack" if "webpack" in deps else "Unknown")),
                "state_management": [d for d in ["zustand", "@tanstack/react-query", "redux", "@reduxjs/toolkit", "recoil", "jotai"] if d in deps],
                "styling_framework": [d for d in ["tailwindcss", "@radix-ui", "lucide-react", "@mui/material", "@mantine/core", "framer-motion"] if any(x in d for x in [d])],
                "typescript": "typescript" in deps or (f_pkg.parent / "tsconfig.json").exists(),
            }
        except Exception:
            pass

    # 2. Backend inspection
    req_files = [p for p in root_path.glob("**/requirements.txt") if "venv" not in str(p) and ".venv" not in str(p)]
    pyproject_files = [p for p in root_path.glob("**/pyproject.toml") if "venv" not in str(p)]
    if req_files or pyproject_files:
        inspection["is_greenfield"] = False
        b_deps = []
        manifest_rel = ""
        if req_files:
            manifest_rel = str(req_files[0].relative_to(root_path))
            inspection["detected_manifests"].append(manifest_rel)
            b_deps = [line.strip().split("==")[0].split(">=")[0].strip().lower() for line in req_files[0].read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip() and not line.startswith("#")]
        elif pyproject_files:
            manifest_rel = str(pyproject_files[0].relative_to(root_path))
            inspection["detected_manifests"].append(manifest_rel)
            b_deps = [line.strip().lower() for line in pyproject_files[0].read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip()]

        inspection["backend"] = {
            "manifest": manifest_rel,
            "framework": "FastAPI" if any("fastapi" in d for d in b_deps) else ("Django" if any("django" in d for d in b_deps) else ("Flask" if any("flask" in d for d in b_deps) else "Python")),
            "orm_db": [d for d in ["sqlalchemy", "tortoise-orm", "alembic", "prisma", "peewee"] if any(d in x for x in b_deps)],
            "validation": [d for d in ["pydantic", "marshmallow"] if any(d in x for x in b_deps)],
            "test_runner": [d for d in ["pytest", "unittest"] if any(d in x for x in b_deps)],
        }

    # 3. Database inspection
    db_files = [p for p in root_path.glob("**/*.db") if "venv" not in str(p) and ".git" not in str(p)] + \
               [p for p in root_path.glob("**/*.sqlite*") if "venv" not in str(p) and ".git" not in str(p)]
    if db_files:
        inspection["is_greenfield"] = False
        inspection["database"] = {
            "engine": "SQLite",
            "files": [str(p.relative_to(root_path)) for p in db_files[:5]],
        }
    elif any(root_path.glob("**/schema.prisma")):
        inspection["database"] = {"engine": "Prisma Managed", "files": ["schema.prisma"]}

    # 4. Styling & centralized tokens inspection
    css_files = [p for p in root_path.glob("**/*.css") if "node_modules" not in str(p) and "dist" not in str(p)]
    for c in css_files:
        try:
            txt = c.read_text(encoding="utf-8", errors="ignore")
            if ":root" in txt or "--primary" in txt:
                inspection["styling"] = {
                    "centralized_tokens": True,
                    "token_file": str(c.relative_to(root_path)),
                }
                break
        except Exception:
            pass

    out_file = project_dir / "codebase_inspection.json"
    out_file.write_text(json.dumps(inspection, indent=2))

    print(f"[session_manager] 🔍 Pre-Flight Codebase Fact-Finding Complete:")
    print(f"  • Project Mode: {'Existing Codebase' if not inspection['is_greenfield'] else 'Greenfield (Clean Slate)'}")
    if inspection.get("frontend"):
        f = inspection["frontend"]
        print(f"  • Frontend: {f.get('framework')} ({f.get('build_tool')}) | State: {', '.join(f.get('state_management', [])) or 'None'} | TypeScript: {f.get('typescript')}")
    if inspection.get("backend"):
        b = inspection["backend"]
        print(f"  • Backend: {b.get('framework')} | ORM: {', '.join(b.get('orm_db', [])) or 'None'} | Validation: {', '.join(b.get('validation', [])) or 'None'}")
    if inspection.get("database"):
        d = inspection["database"]
        print(f"  • Database: {d.get('engine')} ({len(d.get('files', []))} file(s) found)")
    if inspection.get("styling"):
        s = inspection["styling"]
        print(f"  • Design Tokens: Centralized CSS tokens detected in {s.get('token_file')}")
    print(f"[session_manager] ✅ Saved pre-flight report to: {out_file}")
    return 0


def export_adrs(project_name: str, project_root: str, audit_dir: str) -> int:
    import re
    if not project_name:
        print("[session_manager] Error: --project is required for export-adrs action.", file=sys.stderr)
        return 1

    root_path, _, project_dir = resolve_paths(project_root, audit_dir, project_name)
    decisions_file = project_dir / "architecture_decisions.md"

    if not decisions_file.exists():
        print(f"[session_manager] Error: {decisions_file} does not exist.", file=sys.stderr)
        return 1

    adr_dir = root_path / "docs" / "adr"
    adr_dir.mkdir(parents=True, exist_ok=True)

    text = decisions_file.read_text(encoding="utf-8")
    raw_sections = [s.strip() for s in text.split("\n### ") if s.strip()]

    role_slug_map = {
        "triage": ("0001", "scope-and-triage", "Scope and Architecture Type"),
        "tech lead": ("0002", "core-stack-and-state", "Core Tech Stack and State Management"),
        "ux architect": ("0003", "frontend-tokens-and-layout", "Frontend Layout and Design Tokens"),
        "data architect": ("0004", "database-and-orm", "Database Schema, Normalization, and ORM"),
        "backend architect": ("0005", "api-contracts-and-validation", "API Contracts, Versioning, and Validation"),
        "devops engineer": ("0006", "devops-and-handoffs", "Directory Layout, Guardrails, and Phase Handoffs"),
        "qa tester": ("0007", "verification-gates-and-testing", "Verification Gates, Phase Commands, and Test Runners"),
        "principal reviewer": ("0008", "arb-devil-advocate-hardening", "Architecture Review Board Hardening & Safeguards"),
        "refinements": ("0009", "pm-review-amendments", "Project Manager Refinements and Versioned Amendments"),
    }

    adr_entries = []
    counter = 1

    for section in raw_sections:
        lines = section.splitlines()
        first_line = lines[0] if lines else ""
        lower_header = first_line.lower()

        # Skip document title block
        if "architecture decisions ledger" in lower_header or first_line.startswith("# "):
            continue

        slug = None
        title = None
        num_str = f"{counter:04d}"

        for key, (mapped_num, mapped_slug, mapped_title) in role_slug_map.items():
            if key in lower_header:
                num_str = mapped_num
                slug = mapped_slug
                title = mapped_title
                break

        if not slug:
            clean_title = re.sub(r"[^a-zA-Z0-9 ]", "", first_line).strip()
            slug = clean_title.lower().replace(" ", "-")[:30]
            title = first_line

        filename = f"{num_str}-{slug}.md"
        adr_file = adr_dir / filename

        body = "\n".join(lines[1:]).strip()
        adr_content = f"""# {num_str}. {title}

**Status:** Accepted  
**Date:** {datetime.now().strftime('%Y-%m-%d')}  
**Committee:** Crew Dev Forge Architecture Review Board  
**Scope / Role:** {first_line}

---

## 🏛️ Context & Architectural Trade-offs
Derived through multi-role consensus in `architecture_decisions.md` for project `{project_name}`.

## 🎯 Decision
{body}

## ⚖️ Consequences & Implementation Bounds
- Downstream autonomous coding agents MUST adhere strictly to these constraints.
- Verified before phase transitions using deterministic verification commands in `ORCHESTRATION_PLAN.md`.
"""
        adr_file.write_text(adr_content, encoding="utf-8")
        adr_entries.append((num_str, title, filename))
        counter += 1

    readme_lines = [
        "# 📚 Architecture Decision Records (ADR Ledger)",
        "",
        f"**Project:** {project_name}  ",
        f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
        "**Governance:** Crew Dev Forge Engineering Committee  ",
        "",
        "| ADR ID | Decision Title | Status | File Reference |",
        "|---|---|:---:|---|",
    ]
    for num, title, fname in adr_entries:
        readme_lines.append(f"| ADR {num} | {title} | `Accepted` | [{fname}](./{fname}) |")

    (adr_dir / "README.md").write_text("\n".join(readme_lines) + "\n", encoding="utf-8")
    print(f"[session_manager] ✅ Exported {len(adr_entries)} ADRs to {adr_dir}/")
    return 0


def check_skill_integrity() -> int:
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent

    required_files = [
        skill_dir / "SKILL.md",
        skill_dir / "roles" / "0_Discovery_Strategist.md",
        skill_dir / "roles" / "1_Tech_Lead.md",
        skill_dir / "roles" / "2_UX_Architect.md",
        skill_dir / "roles" / "3_Data_Architect.md",
        skill_dir / "roles" / "4_Backend_Architect.md",
        skill_dir / "roles" / "5_DevOps_Engineer.md",
        skill_dir / "roles" / "6_QA_Tester.md",
        skill_dir / "roles" / "7_Principal_Reviewer.md",
        skill_dir / "templates" / "ARCHITECTURE_TEMPLATE.md",
        skill_dir / "templates" / "ORCHESTRATION_TEMPLATE.md",
        skill_dir / "tools" / "session_manager.py",
    ]

    all_ok = True
    print(f"[session_manager] 🔍 Auditing skill installation at: {skill_dir}")
    for rf in required_files:
        if rf.exists() and rf.stat().st_size > 0:
            print(f"  [OK] {rf.relative_to(skill_dir)}")
        else:
            print(f"  [MISSING/EMPTY] {rf.relative_to(skill_dir)}", file=sys.stderr)
            all_ok = False

    if all_ok:
        print("[session_manager] ✅ All skill components verified.")
        return 0
    else:
        print("[session_manager] ❌ Integrity check failed.", file=sys.stderr)
        return 1


def main():
    args = parse_arguments()
    if args.action == "archive":
        sys.exit(archive_session(args.project, args.project_root, args.audit_dir))
    elif args.action == "status":
        sys.exit(status_session(args.project, args.project_root, args.audit_dir))
    elif args.action == "resume":
        sys.exit(resume_session(args.project, args.project_root, args.audit_dir))
    elif args.action == "list":
        sys.exit(list_sessions(args.project_root, args.audit_dir))
    elif args.action == "export":
        sys.exit(export_decisions(args.project, args.project_root, args.audit_dir))
    elif args.action == "inspect-stack":
        sys.exit(inspect_stack(args.project, args.project_root, args.audit_dir))
    elif args.action == "export-adrs":
        sys.exit(export_adrs(args.project, args.project_root, args.audit_dir))
    elif args.action == "check":
        sys.exit(check_skill_integrity())
    else:
        print(f"[session_manager] Unknown action: {args.action}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
