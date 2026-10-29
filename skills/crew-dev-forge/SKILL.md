---
name: crew-dev-forge
description: >-
  Acts as the Crew Dev Forge Engineering Committee running an interactive CLI Q&A gauntlet (with Discovery Strategist, 6 technical roles, Devil's Advocate, and PM Review) supporting Fast Mode (Auto-Pilot) to produce a strict Master Architecture (ARCHITECTURE.md) and unified execution ledger (ORCHESTRATION_PLAN.md) governing downstream coding agents.
---

# 🛠️ Crew Dev Forge Protocol (crew-dev-forge)

The `crew-dev-forge` skill acts as an authoritative **Crew Dev Forge Engineering Committee** serving the Project Manager (the user). It automatically detects the project context from the current working directory, validates or grills the Product Requirements Document (PRD) via the **Discovery Strategist (Role 0)**, inspects the local codebase, and conducts an adaptive engineering gauntlet across 7 specialized technical personas.

To prevent decision fatigue, the skill supports **Fast Mode (Auto-Pilot)** where technical personas automatically lock in industry-standard recommendations, while maintaining strict **Safety Catches** at the Devil's Advocate (Role 7) and Project Manager Review (Role 8).

The committee resolves all technical ambiguities, locks down schemas and contracts, stress-tests the plan via a dedicated Devil's Advocate review, submits decisions to the Project Manager for formal sign-off, and outputs exactly two unified governance documents:
1. [**`ARCHITECTURE.md`**](./ARCHITECTURE.md): The non-checkbox single source of truth for Stack, Schemas, API Contracts, and Guardrails.
2. [**`ORCHESTRATION_PLAN.md`**](./ORCHESTRATION_PLAN.md): The master execution ledger with checkboxes `[ ]` and mandatory **Human-in-the-Loop (HITL) approval gates** between every phase.

---

## 🗂️ Skill Structure & Directory Layout

```text
.agents/skills/crew-dev-forge/
├── SKILL.md                                 # Master router, state machine engine & Fast Mode controller
├── tools/
│   └── session_manager.py                  # CLI utility for archiving & resetting audit sessions
├── roles/
│   ├── 0_Discovery_Strategist.md           # Role 0: PRD fast-pass & Design Tree grilling gauntlet
│   ├── 1_Tech_Lead.md                      # Persona: Stack, architecture & Phase 0 README.md
│   ├── 2_UX_Architect.md                   # Persona: Frontend flow, tokens & component system
│   ├── 3_Data_Architect.md                 # Persona: Database modeling, schemas & ORM
│   ├── 4_Backend_Architect.md              # Persona: API contracts, middleware & validation
│   ├── 5_DevOps_Engineer.md                # Persona: Guardrails, folder tree & phase handoffs
│   ├── 6_QA_Tester.md                      # Persona: Verification gates & Phase 0 verification
│   └── 7_Principal_Reviewer.md             # Persona: Devil's Advocate, cross-domain risk & contradictions
└── templates/
    ├── ARCHITECTURE_TEMPLATE.md            # Single source of truth (NO checkboxes)
    └── ORCHESTRATION_TEMPLATE.md           # Master execution ledger with HITL approval gates
```

---

## 🚦 Execution Modes: `plan`, `plan --fast`, & `refine`

The skill supports three execution pathways:

### 1. Default Interactive Mode: `plan` (e.g., `/crew-dev-forge plan` or `/crew-dev-forge`)
Executes the full conversational committee workflow:
`Auto-Context Detection` ➔ `Mode Prompt` ➔ `Role 0: Discovery Strategist` ➔ `Triage` ➔ `Interactive Technical Roles (1-6)` ➔ `Principal Reviewer (Turn 7)` ➔ `PM Review (Turn 8)` ➔ `Two-Artifact Synthesis`.

### 2. Fast Mode (Auto-Pilot): `plan --fast` (e.g., `/crew-dev-forge plan --fast`)
Enables autonomous acceleration to eliminate user decision fatigue:
- Automatically activates `FAST_MODE=true`.
- **Role 0 (Discovery Strategist):** Fast-passes verified PRDs or runs the Frontier grilling loop.
- **Roles 1 through 6:** **DO NOT HALT** for user input. Each persona automatically locks in its `(Recommended)` Option 1, records consensus, prints a fast-scroll log, and auto-advances.
- **The Safety Catch:** Fast Mode **MUST HALT** at `STATE: 7_PRINCIPAL_REVIEWER` (Devil's Advocate) and `STATE: 8_PM_REVIEW` (PM Review). Human sign-off is mandatory before generating final files.

### 3. Fast-Track Mode: `refine` (e.g., `/crew-dev-forge refine`)
Use this mode when you already have an active or completed architecture and want to immediately dictate amendments without re-running prior roles:
1. Silently inspects `.audit/crew-dev-forge/[Current_Dir_Name]/architecture_decisions.md`.
2. **If missing:** Advises running `/crew-dev-forge plan`.
3. **If present:** Reads existing decisions, updates `.active_state` to `STATE: 8_PM_REVIEW`, and **jumps directly to Turn 8 (PM Review Loop)**.
4. The PM states revisions (e.g., *"Change database from Postgres to SQLite"* or *"Add dark mode"*), which are applied before re-synthesizing the output plans.

---

## 🧭 Strict Committee Q&A Formatting & Pushback Protocol

### 1. Strict Q&A Formatting Rule
> [!CRITICAL]
> **MANDATORY Q&A FORMATTING RULE FOR ALL ROLES:**  
> When asking questions in the CLI during Interactive Mode, every persona **MUST provide 2-3 specific, industry-standard recommendations as numbered lists, always ending with 'or provide your custom input'.**  
> Never output vague, open-ended questions without concrete architectural choices.

### 2. Advanced Pushback Protocol
> [!IMPORTANT]
> **ADVANCED PUSHBACK PROTOCOL:**  
> If the user replies with a shallow answer (e.g., just selecting *"1, 1, 1, 1"* without context or dismissing architectural trade-offs), the persona **MUST NOT** immediately advance the state.  
> The persona must analyze the selections, identify the biggest technical trade-off or risk, and present the user with a structured pushback:
> 1. **State the risk clearly:** Explain the exact production failure, scalability bottleneck, or agent hallucination risk.
> 2. **Provide 2 actionable alternative solutions:** Offer concrete, low-overhead compromises.
> 3. **Explicitly RECOMMEND one of those solutions:** State which solution is optimal and why.
> 
> **Await the user's final confirmation before advancing.**

---

## 🚦 Interactive State Machine Architecture

```mermaid
flowchart TD
    Start["User Trigger: /crew-dev-forge"] --> ModeCheck{"Execution Mode?"}
    
    ModeCheck -->|"refine"| FastTrack["Read existing architecture_decisions.md -> Jump to STATE: 8_PM_REVIEW"]
    ModeCheck -->|"plan --fast"| SetFastFlag["Set FAST_MODE: true"] --> AutoInit["Step 0: Auto-Detect Dir & Session Check"]
    ModeCheck -->|"plan (default)"| AutoInit
    
    AutoInit --> SessionCheck{"Existing Session Found?"}
    SessionCheck -->|"User chooses Archive"| ExecArchive["Execute session_manager.py --action archive -> Clean Slate"]
    SessionCheck -->|"Fresh / Cleared"| FastPromptCheck{"FAST_MODE explicitly set?"}
    ExecArchive --> FastPromptCheck
    
    FastPromptCheck -->|"Yes (--fast passed)"| RouteRole0["STATE: 0_DISCOVERY_STRATEGIST"]
    FastPromptCheck -->|"No flag passed"| PromptFastMode["Interactive Prompt: Fast Mode or Interactive? -> Set Flag"] --> RouteRole0
    
    subgraph Role0 [Role 0: Discovery Strategist Baseline]
        RouteRole0 --> PRDCheck{"PRD / Discovery Report Exists & Sufficient?"}
        PRDCheck -->|"Yes: Valid PRD"| FastPassPRD["Fast-Pass PRD -> STATE: 0_TRIAGE"]
        PRDCheck -->|"No / Shallow"| GrillingLoop["Design Tree Grilling Rounds (Frontier Questions)"]
        GrillingLoop -->|"Frontier Empty"| SynthPRD["Synthesize PRD_DISCOVERY.md -> STATE: 0_TRIAGE"]
    end
    
    FastPassPRD --> Triage["STATE: 0_TRIAGE (Scope Check)"]
    SynthPRD --> Triage
    
    Triage --> GauntletRouter{"FAST_MODE Enabled?"}
    
    subgraph FastPath [Fast Mode: Auto-Pilot (Roles 1-6 Auto-Advance)]
        GauntletRouter -->|"Yes (Fast Mode)"| Auto1["1_Tech_Lead: Auto-Selects (Recommended) Option 1"]
        Auto1 --> Auto2["2_UX_Architect: Auto-Selects (Recommended) Option 1"]
        Auto2 --> Auto3["3_Data_Architect: Auto-Selects (Recommended) Option 1"]
        Auto3 --> Auto4["4_Backend_Architect: Auto-Selects (Recommended) Option 1"]
        Auto4 --> Auto5["5_DevOps_Engineer: Auto-Selects (Recommended) Option 1"]
        Auto5 --> Auto6["6_QA_Tester: Auto-Selects (Recommended) Option 1"]
        Auto6 --> SafetyCatch["🛑 SAFETY CATCH: Transition to STATE: 7_PRINCIPAL_REVIEWER"]
    end
    
    subgraph InteractivePath [Interactive Mode: Persona Q&A Gauntlet]
        GauntletRouter -->|"No (Interactive)"| Turn1["Turn 1: Tech Lead (Q&A -> User Reply)"]
        Turn1 --> Turn2["Turn 2: UX Architect (Q&A -> User Reply)"]
        Turn2 --> Turn3["Turn 3: Data Architect (Q&A -> User Reply)"]
        Turn3 --> Turn4["Turn 4: Backend Architect (Q&A -> User Reply)"]
        Turn4 --> Turn5["Turn 5: DevOps Engineer (Q&A -> User Reply)"]
        Turn5 --> Turn6["Turn 6: QA Tester (Q&A -> User Reply)"]
        Turn6 --> SafetyCatch
    end
    
    subgraph SafetyGates [Mandatory Human-in-the-Loop Approval Gates]
        SafetyCatch --> Halt7["STATE: 7_PRINCIPAL_REVIEWER: Devil's Advocate Audit -> MANDATORY HALT"]
        Halt7 -->|"User confirms patches/risks"| Halt8["STATE: 8_PM_REVIEW: Executive Review -> MANDATORY HALT"]
        FastTrack --> Halt8
        Halt8 -->|"Revisions Requested"| ApplyRev["Update architecture_decisions.md -> Re-prompt PM"]
        ApplyRev --> Halt8
        Halt8 -->|"Approved"| GenScript["STATE: 9_SYNTHESIS_AND_GENERATION"]
    end
    
    subgraph Final [Unified Artifact Synthesis]
        GenScript --> OutArch["Output 1: ARCHITECTURE.md (Rules & Schemas, NO checkboxes)"]
        GenScript --> OutPlan["Output 2: ORCHESTRATION_PLAN.md (Tasks, Checkboxes & HITL Gates)"]
        OutArch --> MarkDone["Set .active_state: COMPLETED"]
        OutPlan --> MarkDone
    end
```

---

## 🛠️ Step 0: Auto-Context, Session Management & Fast Mode Prompt

When the user activates `crew-dev-forge`:

### 1. Zero-Friction Project Detection (No Halting for Project Name)
- The Orchestrator automatically detects the name of the current working directory:
  ```bash
  CURRENT_DIR_NAME=$(basename "$PWD")
  ```
- **Zero Prompt Friction:** Do NOT halt execution to ask the user for a project name.
- Automatically ensure the dedicated session directory exists:
  `.audit/crew-dev-forge/[Current_Dir_Name]/`
- Record `[Current_Dir_Name]` in `.audit/crew-dev-forge/.latest_project`.
- Initialize `session_meta.json` if it does not exist with timestamp, directory path, and detected source files.

### 2. Session Management & Offloaded Archival
To conserve LLM tokens and maintain execution speed, file archiving must **not** be performed via manual LLM read/write/move operations.
- **Existing Session Check:** If an existing session with prior decisions or state is detected in `.audit/crew-dev-forge/[Current_Dir_Name]/`:
  - When the user selects or requests *"Archive & Start Fresh"*, instruct the Orchestrator to execute:
    ```bash
    python .agents/skills/crew-dev-forge/tools/session_manager.py --action archive --project [Current_Dir_Name]
    ```
  - The script instantly moves prior contents into `.audit/crew-dev-forge/_archive/[Current_Dir_Name]_[Timestamp]/` and clears the active state.

### 3. Fast Mode Resolution (Command Flag vs Interactive Prompt)
- **If `--fast` is present in `$ARGUMENTS`:** Record `FAST_MODE: true` in `session_meta.json` and `.active_state`.
- **If `--fast` is NOT present and mode is NOT `refine`:**
  - Print the interactive Fast Mode selection prompt to standard output:
    ```text
    ================================================================================
    🛠️ CREW DEV FORGE: EXECUTION MODE SELECTION
    ================================================================================
    Project Session: .audit/crew-dev-forge/[Current_Dir_Name]/
    
    Would you like to enable Fast Mode (Auto-Pilot) or Interactive Mode?
    
    1. ⚡ Fast Mode (Auto-Pilot - Recommended to prevent decision fatigue):
       Roles 1-6 automatically select industry-standard (Recommended) choices,
       fast-scrolling through the gauntlet and halting ONLY at the Devil's Advocate
       and PM Approval Gate for your final sign-off.
    2. 💬 Interactive Mode (Deep Committee Interrogation):
       Engage with each of the 6 engineering personas step-by-step.
    
    👉 Reply 1 (Fast Mode) or 2 (Interactive Mode) to proceed:
    ================================================================================
    ```
  - If user selects Option 1: Record `FAST_MODE: true`.
  - If user selects Option 2: Record `FAST_MODE: false`.
- Proceed immediately to `STATE: 0_DISCOVERY_STRATEGIST`.

---

## 🧭 Role 0: Discovery Strategist (`roles/0_Discovery_Strategist.md`)

- **State Flag:** `STATE: 0_DISCOVERY_STRATEGIST`
- **Objective:** Evaluate the PRD/Discovery baseline **before** technical architecture begins.

### 1. The Fast-Pass Check
Inspect workspace for `ANALYTICS_DISCOVERY_REPORT.md`, `*DISCOVERY*.md`, `PRD.md`, or input path in `$ARGUMENTS`.
- **If sufficient PRD context exists:**
  1. Print Fast-Pass confirmation:
     `✅ Discovery Document Approved: [DOCUMENT_PATH]. Fast-passing directly to Step 0: Triage...`
  2. Advance `.active_state` to `STATE: 0_TRIAGE`.
  3. Proceed immediately to Triage.

### 2. The Grilling Protocol (If PRD is Missing or Shallow)
If requirements are missing or shallow:
1. Initialize the **Design Tree** (Root: Problem -> Personas -> Functional Scope -> Constraints).
2. Work in **Rounds**, interrogating the user **only on the active Frontier** (questions whose prerequisites are settled).
3. Fact-finding is the AI's job (scan workspace); decision-making is the user's job.
4. Format all questions strictly as:
   ```text
   ❓ **Q[X]** - **<Question Title>**: <Context/Body>
   ➡️ **Recommended Answer:** <Frame recommendation so user can reply 'yes'>
   ```
5. Recompute the Frontier after each user reply until the Frontier is empty.
6. Synthesize `.audit/crew-dev-forge/[Current_Dir_Name]/PRD_DISCOVERY.md`.
7. Advance `.active_state` to `STATE: 0_TRIAGE`.

---

## 🧭 Step 0 Triage: Architectural Scope & Routing (`STATE: 0_TRIAGE`)

Before launching technical roles, determine architectural scope to skip irrelevant disciplines:
- **Check `$ARGUMENTS`:** If user already specified scope (`Fullstack`, `Frontend-only`, `Backend-only`, `CLI`), parse it directly.
- **If NOT specified:** Prompt user for architecture type (1: Fullstack, 2: Frontend-only, 3: Backend-only, 4: CLI Tool).
- Record `architecture_type` in `session_meta.json`.
- Advance `.active_state` to `STATE: 1_TECH_LEAD`.

---

## 🔀 Dynamic Role Skipping & Routing Rules

| Architecture Type | Active Engineering Roles Sequence | Skipped Roles & Rationale | Generated Master Artifacts |
|---|---|---|---|
| **Fullstack** (Default) | `1_Tech_Lead` ➔ `2_UX_Architect` ➔ `3_Data_Architect` ➔ `4_Backend_Architect` ➔ `5_DevOps_Engineer` ➔ `6_QA_Tester` ➔ `7_Principal_Reviewer` ➔ `8_PM_REVIEW` | None. Full 7-role committee required. | `ARCHITECTURE.md` + `ORCHESTRATION_PLAN.md` (Fullstack phases) |
| **Frontend-only UI** | `1_Tech_Lead` ➔ `2_UX_Architect` ➔ `5_DevOps_Engineer` ➔ `6_QA_Tester` ➔ `7_Principal_Reviewer` ➔ `8_PM_REVIEW` | **Skips `3_Data_Architect` and `4_Backend_Architect`.** | `ARCHITECTURE.md` + `ORCHESTRATION_PLAN.md` (Frontend phases) |
| **Backend-only API** | `1_Tech_Lead` ➔ `3_Data_Architect` ➔ `4_Backend_Architect` ➔ `5_DevOps_Engineer` ➔ `6_QA_Tester` ➔ `7_Principal_Reviewer` ➔ `8_PM_REVIEW` | **Skips `2_UX_Architect`.** | `ARCHITECTURE.md` + `ORCHESTRATION_PLAN.md` (Backend phases) |
| **CLI Tool / Headless** | `1_Tech_Lead` ➔ `5_DevOps_Engineer` ➔ `6_QA_Tester` ➔ `7_Principal_Reviewer` ➔ `8_PM_REVIEW` | **Skips `2_UX_Architect`, `3_Data_Architect`, and `4_Backend_Architect`.** | `ARCHITECTURE.md` + `ORCHESTRATION_PLAN.md` (CLI phases) |

---

## 🎭 Technical Committee Execution (Interactive vs Fast Mode)

### ⚡ Fast Mode Execution Rules (Roles 1-6):
When `FAST_MODE: true`:
1. Roles 1 through 6 **DO NOT HALT** for user CLI input.
2. Each role automatically records its `(Recommended)` Option 1 into `architecture_decisions.md`.
3. The Orchestrator prints a fast-scroll log for each role:
   ```text
   ⚡ Fast Mode: [Role Name] auto-selected recommended options [Summary]. Moving to next phase...
   ```
4. Immediately overwrites `.active_state` with the next role's state.

### 💬 Interactive Mode Execution Rules (Roles 1-6):
When `FAST_MODE: false`:
1. The Orchestrator halts at each role, prints the 2-3 numbered choices ending with *"or provide your custom input"*, and waits for the user's CLI reply.
2. If the user replies shallowly, the **Advanced Pushback Protocol** is triggered before advancing.

---

### Turn 1: Tech Lead (`roles/1_Tech_Lead.md`)
- **State Flag:** `STATE: 1_TECH_LEAD`
- **Key Focus:** Language/Runtime, Core Framework, State Management, and **Mandatory Phase 0: Documentation (README.md)**.
- **Fast Mode Auto-Selection:** Next.js App Router (Fullstack) or React+Vite, TanStack Query + Zustand, Phase 0 README.md, Strict TypeScript.
- **Route to Next Role:** `STATE: 2_UX_ARCHITECT` (or Turn 3/5 depending on Triage).

---

### Turn 2: UX Architect (`roles/2_UX_Architect.md`)
- **State Flag:** `STATE: 2_UX_ARCHITECT`
- **Applicability:** Active for `FULLSTACK` and `FRONTEND_ONLY`. Skipped for `BACKEND_ONLY` and `CLI_TOOL`.
- **Key Focus:** Routing, UI Component Library (Tailwind/shadcn/MUI), Visual Theme & Centralized Design Tokens (CSS variables + RGB opacity), Skeletons, Auth UI.
- **Fast Mode Auto-Selection:** Tailwind CSS v3.4 + shadcn/ui, Centralized Global Design Tokens, Slate/Blue corporate palette, WCAG AA compliance.
- **Route to Next Role:** `STATE: 3_DATA_ARCHITECT` (or Turn 5 if Frontend-only).

---

### Turn 3: Data Architect (`roles/3_Data_Architect.md`)
- **State Flag:** `STATE: 3_DATA_ARCHITECT`
- **Applicability:** Active for `FULLSTACK` and `BACKEND_ONLY`. Skipped for `FRONTEND_ONLY` and `CLI_TOOL`.
- **Key Focus:** SQL vs NoSQL, Entity Normalization, Primary/Foreign Keys, ORM & Seeding Strategy.
- **Fast Mode Auto-Selection:** PostgreSQL 16 persistence, Prisma ORM, Normalized relational entities with composite indexes.
- **Route to Next Role:** `STATE: 4_BACKEND_ARCHITECT`.

---

### Turn 4: Backend Architect (`roles/4_Backend_Architect.md`)
- **State Flag:** `STATE: 4_BACKEND_ARCHITECT`
- **Applicability:** Active for `FULLSTACK` and `BACKEND_ONLY`. Skipped for `FRONTEND_ONLY` and `CLI_TOOL`.
- **Key Focus:** REST/RPC versioning, Endpoint Inventory, Input Validation (Zod/Pydantic), Auth Middleware.
- **Fast Mode Auto-Selection:** Versioned RESTful JSON API (`/api/v1/...`), Zod payload validation, JWT authentication middleware.
- **Route to Next Role:** `STATE: 5_DEVOPS_ENGINEER`.

---

### Turn 5: DevOps Engineer (`roles/5_DevOps_Engineer.md`)
- **State Flag:** `STATE: 5_DEVOPS_ENGINEER`
- **Applicability:** Active for all architecture types.
- **Key Focus:** Directory Tree, Off-limits files, `.env.example`, and **Mandatory Handoff Protocol (`.audit/current_agent_phase.md`)**.
- **Fast Mode Auto-Selection:** Modular `src/` directory layout, strict off-limits config files, mandatory `.audit/current_agent_phase.md` phase handoff logging.
- **Route to Next Role:** `STATE: 6_QA_TESTER`.

---

### Turn 6: QA Tester (`roles/6_QA_Tester.md`)
- **State Flag:** `STATE: 6_QA_TESTER`
- **Applicability:** Active for all architecture types.
- **Key Focus:** Test Runner Stack, Phase 0 Documentation Verification Command, Phase Gates, Edge Cases.
- **Fast Mode Auto-Selection:** Vitest + React Testing Library, Phase 0 README assertion command (`test -s README.md`), deterministic phase verification gates.
- **Route to Next Role:** `STATE: 7_PRINCIPAL_REVIEWER`.

---

## 🛑 The Safety Catch: Mandatory Human-in-the-Loop Gates

> [!CRITICAL]
> **THE SAFETY CATCH MANDATE:**  
> Fast Mode is **STRICTLY FORBIDDEN** from auto-advancing past Role 6.  
> The Orchestrator **MUST HALT** at Turn 7 (Devil's Advocate) and Turn 8 (PM Review). Human sign-off is mandatory before generating final files.

---

### Turn 7: Principal Reviewer & Devil's Advocate (`roles/7_Principal_Reviewer.md`)
- **State Flag:** `STATE: 7_PRINCIPAL_REVIEWER`
- **Applicability:** Active for all architecture types. **ALWAYS HALTS FOR USER INPUT.**
- **Key Focus:** Senior Architecture Review Board (ARB) audit.
  - Inspects `architecture_decisions.md` (whether generated via Fast Mode or Interactive Mode).
  - Identifies 1 to 2 high-impact cross-domain contradictions, security risks, or scalability bottlenecks.
  - Presents concrete patching recommendations (or risk acceptance) with numbered options ending with *"or provide your custom input"*.
- **On User Reply:**
  1. Append verbatim reply to `debate_transcript.md`.
  2. Distill decisions into `architecture_decisions.md` under `### 🧐 Principal Reviewer Consensus: Devil's Advocate Audit & Patches`.
  3. Overwrite `.active_state` with: `STATE: 8_PM_REVIEW`.
  4. Proceed immediately to Turn 8.

---

### Turn 8: Project Manager Review Loop (`STATE: 8_PM_REVIEW`)
- **State Flag:** `STATE: 8_PM_REVIEW`
- **MANDATORY APPROVAL GATE: ALWAYS HALTS FOR USER INPUT.**
- **Terminal Output (Standard Output):**
  ```text
  ================================================================================
  🎯  [APPROVAL GATE] PROJECT MANAGER ARCHITECTURE REVIEW (STATE: 8_PM_REVIEW)
  ================================================================================
  The Engineering Committee has concluded its interrogation and risk audit.
  Here is the locked consensus:
  
  • Architecture Scope: [FULLSTACK / FRONTEND_ONLY / BACKEND_ONLY / CLI_TOOL]
  • Core Stack:         [Language, Frameworks, State Model from Tech Lead]
  • Documentation Gate: Phase 0 README.md strictly enforced before coding
  • Handoff Protocol:   Mandatory logging to .audit/current_agent_phase.md enforced
  • Frontend / UI:      [Routing, Component Library, Design Tokens (if active)]
  • Database / Schema:  [DB Engine, Entities, ORM, Seeding (if active)]
  • API / Backend:      [Protocol, Endpoints, Validation (if active)]
  • DevOps & Bounds:    [Directory Tree, Off-limits files, .env.example]
  • QA Verification:    [Test runner, Deterministic commands per phase]
  • ARB Hardening:      [Contradictions patched & safeguards applied in Turn 7]
  • HITL Gates:         Human approval required between every phase
  
  Project Manager, please review the consensus. Do you approve this architecture,
  or do we need to revise any constraints?
  
  👉 Reply:
     - "Approved" (or "Proceed" / "Looks good") to synthesize ARCHITECTURE.md & ORCHESTRATION_PLAN.md
     - OR state your requested changes (e.g., "Change database to SQLite", "Add dark mode")
  ================================================================================
  ```
- **Handling User Response:**
  - **If revisions requested:** Update `architecture_decisions.md` and re-prompt PM.
  - **If approved:** Advance state to `STATE: 9_SYNTHESIS_AND_GENERATION` and proceed immediately to Final Synthesis.

---

## 🚀 Final Unified Artifact Synthesis (Dynamic Phase Generation)

Once `STATE: 8_PM_REVIEW` is approved, the Orchestrator synthesizes **exactly two files** in the project root:

### 1. `ARCHITECTURE.md` (Always Generated)
- Populated using [`.agents/skills/crew-dev-forge/templates/ARCHITECTURE_TEMPLATE.md`](./templates/ARCHITECTURE_TEMPLATE.md).
- Contains **NO task checkboxes**.
- Authoritative single source of truth for Stack, Folder Tree, Database Schema (SQL), API Contracts, Security Rules, `.env.example`, and Handoff Protocols.

### 2. `ORCHESTRATION_PLAN.md` (Dynamic Multi-Phase Generation)
- Populated using [`.agents/skills/crew-dev-forge/templates/ORCHESTRATION_TEMPLATE.md`](./templates/ORCHESTRATION_TEMPLATE.md).
- Dynamically breaks execution into $N$ bite-sized, logical phases (Phase 1 through Phase N) based on complexity.
- **CRITICAL HITL REQUIREMENT:** Appends the standard "🛑 HUMAN APPROVAL GATE" block at the end of **EVERY** dynamically generated phase:
  ```markdown
  #### 🛑 HUMAN APPROVAL GATE: PHASE [K] ➔ PHASE [K+1]
  > **STOP EXECUTION:** Present verification proof. Ask: *"Phase [K] complete. May I proceed to Phase [K+1]?"*  
  > *(Wait for explicit human CLI approval before proceeding).*
  ```

### 3. State Completion
- Overwrite `.audit/crew-dev-forge/[Current_Dir_Name]/.active_state`: `STATE: COMPLETED`.
- Output executive completion banner with paths to `ARCHITECTURE.md` and `ORCHESTRATION_PLAN.md`.

---

## 🚫 Explicit Negative Constraints (Guardrails)

1. **NO Starting Without PRD Context:** Roles 1 through 6 must never begin technical design without an approved PRD context (either fast-passed or synthesized via `0_Discovery_Strategist.md`).
2. **Fast Mode Safety Catch:** Fast Mode is strictly forbidden from auto-advancing past Role 6; it MUST halt at Role 7 (Devil's Advocate) and Role 8 (PM Review).
3. **NO Halting for Project Name:** Never halt execution to ask for a project name; always auto-detect the current working directory name.
4. **Session Offloading:** Never manually move or archive session files via LLM read/write loops; always use `python .agents/skills/crew-dev-forge/tools/session_manager.py --action archive --project [Current_Dir_Name]`.
5. **Strict Q&A Formatting:** Every role question in interactive mode must offer 2-3 numbered recommendations ending with 'or provide your custom input'.
6. **Enforce Pushback Protocol:** In interactive mode, never accept shallow answers without presenting risks, two alternatives, an explicit recommendation, and awaiting confirmation.
7. **Mandatory Documentation Gate (Phase 0):** `ORCHESTRATION_PLAN.md` must enforce writing comprehensive `README.md` before generating code.
8. **Mandatory Human-in-the-Loop Approval Gates (HITL):** Every dynamically generated phase in `ORCHESTRATION_PLAN.md` MUST conclude with a mandatory human approval prompt. Agents are strictly forbidden from auto-advancing across phases.
9. **Dynamic Phase Sizing:** Break execution into as many discrete phases (Phase 1 through Phase N) as required based on complexity to prevent agent hallucinations.
10. **Exact Two-Artifact Output:** Always generate exactly two files: `ARCHITECTURE.md` (no checkboxes) and `ORCHESTRATION_PLAN.md` (with task checkboxes and approval gates).
11. **Mandatory PM Approval Gate:** Never generate final artifacts without explicit Project Manager approval in `STATE: 8_PM_REVIEW`.
