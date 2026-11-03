---
name: crew-dev-forge
description: >-
  Acts as the Crew Dev Forge Engineering Committee running an interactive CLI Q&A gauntlet (with Discovery Strategist, 6 technical roles, Devil's Advocate, and PM Review) supporting Fast Mode (Auto-Pilot) to produce a strict Master Architecture (ARCHITECTURE.md) and unified execution ledger (ORCHESTRATION_PLAN.md) governing downstream coding agents.
---

# 🛠️ Crew Dev Forge Protocol (crew-dev-forge)

The `crew-dev-forge` skill acts as an authoritative **Crew Dev Forge Engineering Committee** serving the Project Manager (the user). It automatically detects the project context from the current working directory, validates or grills the Product Requirements Document (PRD) via the **Discovery Strategist (Role 0)**, inspects the local codebase, and conducts an adaptive engineering gauntlet across 7 specialized technical personas.

To prevent decision fatigue, the skill supports **Fast Mode (Auto-Pilot)** where technical personas automatically lock in industry-standard recommendations, while maintaining strict **Safety Catches** at the Devil's Advocate (Role 7) and Project Manager Review (Role 8).

> [!CRITICAL]
> **PLANNING-ONLY DIRECTIVE (ZERO CODE WRITING):**  
> `crew-dev-forge` is **EXCLUSIVELY A PLANNING, ARCHITECTURE, AND GOVERNANCE COMMITTEE**.  
> The Orchestrator and all personas are **STRICTLY FORBIDDEN** from modifying, creating, or editing any application source code files (`.py`, `.ts`, `.tsx`, `.js`, etc.) or executing build/runtime commands. This skill outputs **ONLY** architectural governance files in `.audit/crew-dev-forge/` and the two master governance artifacts (`ARCHITECTURE.md` and `ORCHESTRATION_PLAN.md`).

The committee resolves all technical ambiguities, locks down schemas and contracts, stress-tests the plan via a dedicated Devil's Advocate review, submits decisions to the Project Manager for formal sign-off, and outputs exactly two unified governance documents:
1. [**`ARCHITECTURE.md`**](./ARCHITECTURE.md): The non-checkbox single source of truth for Stack, Schemas, API Contracts, and Guardrails.
2. [**`ORCHESTRATION_PLAN.md`**](./ORCHESTRATION_PLAN.md): The master execution ledger with checkboxes `[ ]` and mandatory **Human-in-the-Loop (HITL) approval gates** between every phase.

---

## 🗂️ Skill Structure & Directory Layout

```text
.agents/skills/crew-dev-forge/
├── SKILL.md                                 # Master router, state machine engine & Fast Mode controller
├── tools/
│   └── session_manager.py                  # CLI utility for session lifecycle, archive, status, resume & check
├── roles/
│   ├── 0_Discovery_Strategist.md           # Role 0: PRD fast-pass & Design Tree grilling gauntlet
│   ├── 1_Tech_Lead.md                      # Persona: Stack, architecture & Phase 0 README.md
│   ├── 2_UX_Architect.md                   # Persona: Frontend flow, tokens & component system
│   ├── 3_Data_Architect.md                 # Persona: Database modeling, schemas & ORM
│   ├── 4_Backend_Architect.md              # Persona: API contracts, middleware & validation
│   ├── 5_DevOps_Engineer.md                # Persona: Guardrails, folder tree & phase handoffs
│   ├── 6_QA_Tester.md                      # Persona: Verification gates & Phase 0 verification
│   └── 7_Principal_Reviewer.md             # Persona: Devil's Advocate, cross-domain risk & refine mini-audit
└── templates/
    ├── ARCHITECTURE_TEMPLATE.md            # Single source of truth (NO checkboxes)
    └── ORCHESTRATION_TEMPLATE.md           # Master execution ledger with HITL approval gates
```

---

## 🚦 Execution Modes & Strict Invocation Parsing

Parse `$ARGUMENTS` using these strict routing rules:

| Invocation Command | Target Execution Pathway | Description |
|---|---|---|
| `/crew-dev-forge` or `/crew-dev-forge plan` | **Default Interactive Mode** | Full conversational committee gauntlet across all active personas with mandatory Q&A and pushback. |
| `/crew-dev-forge plan --fast` | **Fast Mode (Auto-Pilot)** | Autonomous acceleration for Roles 1-6 auto-selecting `(Recommended)` defaults; halts strictly at Role 7 & Role 8. |
| `/crew-dev-forge refine` | **Fast-Track Refinement** | Jumps directly to Turn 8 (PM Review) with version snapshotting and mini-ARB stress-test. |
| `/crew-dev-forge escalate [Reason]` | **Emergency Mini-ARB Escalation** | Bi-directional bridge for coding agents/user when code execution hits a major roadblock; jumps directly to Turn 7 (Devil's Advocate) for micro-arbitration. |
| *Any unrecognized argument* | **Usage Help Banner** | Halts immediately and displays allowed commands. |

### Unrecognized Command Fallback:
If an unrecognized argument is passed, output:
```text
================================================================================
❌ CREW DEV FORGE: UNRECOGNIZED COMMAND
================================================================================
Available execution modes:
  • /crew-dev-forge plan               - Full interactive committee gauntlet
  • /crew-dev-forge plan --fast        - Auto-pilot with mandatory safety catches
  • /crew-dev-forge refine             - Fast-track amendments for existing architecture
  • /crew-dev-forge escalate [Reason]  - Emergency Mini-ARB audit for coding blockers
================================================================================
```

---

## 🧭 Strict Committee Q&A Formatting & Pushback Protocol

### 1. The Dual-Stage Interactive CLI Protocol (Chat Markdown + `ask_question`)

> [!CRITICAL]
> **MANDATORY DUAL-STAGE CLI INTERACTION PROTOCOL (ALL ROLES & PROMPTS):**  
> To deliver a superior user experience with intuitive arrow-key navigation while preventing information loss or cramped terminal screens, all interactive questions, safety catches, and review prompts MUST strictly follow this **Two-Stage Presentation Protocol**:
> 
> 1. **Stage 1: Full-Context Markdown Presentation (Chat Stream):**  
>    - The persona or orchestrator **MUST FIRST** output the complete, rich Markdown briefing directly into the visible chat message before or alongside invoking any interactive prompt.
>    - This message **MUST** contain:
>      - Persona introduction and technical context.
>      - Deep architectural trade-offs, rationale, and specific codebase file references with clickable markdown links using the `file://` scheme.
>      - Detailed question descriptions with formatted numbered recommendations and sub-bullets.
>    - **NEVER** invoke `ask_question` with empty message content (`content: None`) or without printing the detailed context first. The Project Manager must always be able to read the full technical context, trade-offs, and file pointers directly on screen.
> 
> 2. **Stage 2: Ergonomic Interactive Selection (`ask_question` Tool):**  
>    - Use the interactive `ask_question` tool to provide the user with keyboard arrow-key navigation (`↑`/`↓`) and custom typing support.
>    - **Option Text Formatting:** Keep option strings **concise, punchy, and human-readable** (e.g., `"(Recommended) 1. Decoupled Modern Stack: React 18 + Vite + Tailwind + FastAPI"`, `"2. Unified Node/TS Fullstack"`, `"3. Custom alternative"`).
>    - **NO Text Squeezing:** Do NOT cram multi-sentence paragraphs, code blocks, or raw Markdown syntax into the `options` array of `ask_question`. The rich explanations live in Stage 1 Markdown; the interactive selector in Stage 2 acts as a clean, rapid decision steering wheel.
> 
> 3. **Paced Question Pacing (Roles 1–6):**  
>    - Do NOT dump 4 complex questions with 12–16 dense options into a single squeezed interactive widget.
>    - Present the full 4-question technical brief in the Stage 1 Markdown, and in Stage 2 present questions either:
>      - Grouped into two focused interactive pairs (e.g., Q1 & Q2 on Stack/State, followed by Q3 & Q4 on Governance/Verification), OR
>      - A single consolidated approval selector where Option 1 selects the persona's recommended consensus across all 4 questions (with Option 2 for custom overrides or individual question adjustments).
> 
> 4. **Zero-Blind-Decisions Mandate (Role 7 Devil's Advocate & Role 8 PM Review):**  
>    - At Turn 7 (Devil's Advocate), the complete Architecture Review Board (ARB) audit report—including **[RISK 1]** and **[RISK 2]** with explicit **Descriptions**, **File Links (`file://...`)**, and **Blast Radius** consequences—MUST be printed in the Stage 1 Markdown before triggering the approval selector.
>    - At Turn 8 (PM Review), the complete Executive Review consensus summary banner MUST be printed in the Stage 1 Markdown before prompting for final sign-off.
>    - **Never prompt the user to approve hardening patches or accept risks without the specific issues visible on screen.**

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
    Start["User Trigger: /crew-dev-forge"] --> ParseMode{"Parse Command"}
    
    ParseMode -->|"refine"| CheckExistRefine{"architecture_decisions.md exists?"}
    CheckExistRefine -->|"No"| AdvisePlan["Print: Run /crew-dev-forge plan first -> Halt"]
    CheckExistRefine -->|"Yes"| RefineSetup["Version Snapshot -> STATE: 8_PM_REVIEW"] --> Halt8
    
    ParseMode -->|"escalate"| CheckExistEscalate{"architecture_decisions.md exists?"}
    CheckExistEscalate -->|"No"| AdvisePlanEscalate["Print: Run /crew-dev-forge plan first -> Halt"]
    CheckExistEscalate -->|"Yes"| EscalateSetup["Log Blocker -> STATE: 7_PRINCIPAL_REVIEWER"] --> Halt7
    
    ParseMode -->|"plan / plan --fast"| AutoDetect["Step 0: Detect Project & Session State"]
    
    AutoDetect --> StateInspect{".active_state Status?"}
    
    StateInspect -->|"STATE: COMPLETED"| CompletedPrompt{"Prompt User: Completed Session"}
    CompletedPrompt -->|"1. Refine"| RefineSetup
    CompletedPrompt -->|"2. Archive & Reset"| ExecArchive["Execute session_manager.py archive"] --> FreshStart["Clean Slate"]
    CompletedPrompt -->|"3. Cancel"| AbortHalt["Halt execution safely"]
    
    StateInspect -->|"In-Progress (e.g. STATE: 3_DATA_ARCHITECT)"| ResumePrompt{"Prompt User: In-Progress Session"}
    ResumePrompt -->|"1. Resume"| LoadDecisions["Load decisions & fast_mode -> Resume at [CURRENT_STATE]"]
    ResumePrompt -->|"2. Archive & Reset"| ExecArchive
    ResumePrompt -->|"3. Cancel"| AbortHalt
    
    StateInspect -->|"UNINITIALIZED / Fresh"| FreshStart
    ExecArchive --> FreshStart
    
    FreshStart --> FastPromptCheck{"--fast flag in args?"}
    FastPromptCheck -->|"Yes"| SetFastTrue["Set fast_mode: true in session_meta.json"] --> RouteRole0["STATE: 0_DISCOVERY_STRATEGIST"]
    FastPromptCheck -->|"No"| PromptFastMode["Interactive Prompt: Fast Mode or Interactive?"] --> SetFastFlag["Record fast_mode in session_meta.json"] --> RouteRole0
    
    subgraph Role0 [Role 0: Discovery Strategist Baseline]
        RouteRole0 --> PRDCheck{"PRD / Discovery Report Exists?"}
        PRDCheck -->|"Yes: Valid PRD"| FastPassPRD["Fast-Pass PRD -> Persist to debate_transcript.md"]
        PRDCheck -->|"No / Shallow"| GrillingLoop["Design Tree Grilling Rounds (Frontier Questions)"]
        GrillingLoop -->|"Frontier Empty"| SynthPRD["Synthesize PRD_DISCOVERY.md"]
        FastPassPRD --> Triage["STATE: 0_TRIAGE (Scope Check)"]
        SynthPRD --> Triage
        Triage --> PersistTriage["Persist Triage Consensus to decisions & transcript"]
    end
    
    PersistTriage --> GauntletRouter{"fast_mode Enabled?"}
    
    subgraph FastPath [Fast Mode: Auto-Pilot (Roles 1-6 Auto-Advance)]
        GauntletRouter -->|"Yes"| Auto1["1_Tech_Lead: Auto-Selects (Recommended) 1"]
        Auto1 --> Auto2["2_UX_Architect: Auto-Selects (Recommended) 1"]
        Auto2 --> Auto3["3_Data_Architect: Auto-Selects (Recommended) 1"]
        Auto3 --> Auto4["4_Backend_Architect: Auto-Selects (Recommended) 1"]
        Auto4 --> Auto5["5_DevOps_Engineer: Auto-Selects (Recommended) 1"]
        Auto5 --> Auto6["6_QA_Tester: Auto-Selects (Recommended) 1"]
        Auto6 --> SafetyCatch["🛑 SAFETY CATCH: Transition to STATE: 7_PRINCIPAL_REVIEWER"]
    end
    
    subgraph InteractivePath [Interactive Mode: Persona Q&A Gauntlet]
        GauntletRouter -->|"No"| Turn1["Turn 1: Tech Lead (Q&A -> User Reply -> Persist)"]
        Turn1 --> Turn2["Turn 2: UX Architect (Q&A -> User Reply -> Persist)"]
        Turn2 --> Turn3["Turn 3: Data Architect (Q&A -> User Reply -> Persist)"]
        Turn3 --> Turn4["Turn 4: Backend Architect (Q&A -> User Reply -> Persist)"]
        Turn4 --> Turn5["Turn 5: DevOps Engineer (Q&A -> User Reply -> Persist)"]
        Turn5 --> Turn6["Turn 6: QA Tester (Q&A -> User Reply -> Persist)"]
        Turn6 --> SafetyCatch
    end
    
    subgraph SafetyGates [Mandatory Human-in-the-Loop Approval Gates]
        SafetyCatch --> Halt7["STATE: 7_PRINCIPAL_REVIEWER: Devil's Advocate Audit -> MANDATORY HALT"]
        Halt7 -->|"User confirms patches/risks"| Halt8["STATE: 8_PM_REVIEW: Executive Review -> MANDATORY HALT"]
        Halt8 -->|"Revisions Requested"| ApplyRev["Record Refinements in decisions ledger"]
        ApplyRev --> MiniARB{"Mini-ARB Check: Cross-Domain Conflicts?"}
        MiniARB -->|"Conflicts Detected"| FlagARB["Present 1-2 Risks to PM -> Await Confirmation"] --> Halt8
        MiniARB -->|"Clean"| Halt8
        Halt8 -->|"Approved"| GenScript["STATE: 9_SYNTHESIS_AND_GENERATION"]
    end
    
    subgraph Final [Unified Artifact Synthesis & Validation]
        GenScript --> OutArch["Output 1: ARCHITECTURE.md (Rules & Schemas, NO checkboxes)"]
        GenScript --> OutPlan["Output 2: ORCHESTRATION_PLAN.md (Tasks, Checkboxes & HITL Gates)"]
        OutArch --> ValidateTemplates["Validate: Zero unresolved {{...}} placeholders"]
        OutPlan --> ValidateTemplates
        ValidateTemplates --> RecordTerminal["Record Session Completion in debate_transcript.md"]
        RecordTerminal --> MarkDone["Set .active_state: COMPLETED & sync session_meta.json"]
    end
```

---

## 🛠️ Step 0: Auto-Context, Session Lifecycle & Resume Protocols

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

### 1b. Automated Pre-Flight Codebase Fact-Finding (Stack Discovery)
Before initiating the committee gauntlet or prompting for technical stack decisions, the Orchestrator MUST execute the automated codebase inspector:
```bash
python .agents/skills/crew-dev-forge/tools/session_manager.py --action inspect-stack --project [Current_Dir_Name]
```
- This automatically detects:
  - Frontend manifests (`package.json`, `tsconfig.json`) -> Framework (React, Next.js, Vite), state engines (Zustand, TanStack Query), UI libraries (Tailwind, Lucide, Radix, Framer Motion), and TypeScript strictness.
  - Backend manifests (`requirements.txt`, `pyproject.toml`) -> Framework (FastAPI, Django, Flask), ORM (SQLAlchemy), validation (Pydantic), and test runners (PyTest).
  - Database persistence (`catalog.db`, `session.db`, SQLite, Prisma schemas).
  - Styling & Design Tokens (presence of `:root` or CSS variables in `globals.css` / `index.css`).
- Outputs structured facts to `.audit/crew-dev-forge/[Current_Dir_Name]/codebase_inspection.json`.
- **Pre-Flight Fact-Finding Rule:** When `codebase_inspection.json` contains detected tools, Roles 1 through 3 MUST NOT ask redundant questions like *"What language/framework?"*. Instead, acknowledge the detected stack automatically and frame questions as a confirmation or focused delta inquiry.

### 1c. Bi-Directional Execution Escalation Pathway (/crew-dev-forge escalate)
If the user or a downstream autonomous coding agent invokes `/crew-dev-forge escalate [Reason]`:
1. Check that `.audit/crew-dev-forge/[Current_Dir_Name]/architecture_decisions.md` exists. (If missing, advise running `/crew-dev-forge plan` first).
2. Append the escalation event and blocker description to `debate_transcript.md`:
   ```markdown
   ---
   ## 🚨 Escalation Event: Coding Implementation Blocker
   - **Triggered By:** Execution Agent / User
   - **Blocker Summary:** [Reason provided in $ARGUMENTS]
   - **Timestamp:** [ISO-8601]
   ```
3. Overwrite `.active_state` with `STATE: 7_PRINCIPAL_REVIEWER` and set `"active_state": "STATE: 7_PRINCIPAL_REVIEWER"` in `session_meta.json`.
4. Jump directly to **Turn 7 (Principal Reviewer / Devil's Advocate)**. The Devil's Advocate conducts an emergency Mini-ARB audit focusing specifically on the blocker, presents hardening solutions to the user, and updates `architecture_decisions.md` and `ORCHESTRATION_PLAN.md` with targeted amendments.

### 2. Completed Session Re-Entry Protocol
Before prompting for execution mode, inspect `.audit/crew-dev-forge/[Current_Dir_Name]/.active_state`:
- **If `.active_state` exists and equals `STATE: COMPLETED`:**
  DO NOT drop into Role 0 or start the planning gauntlet automatically.  
  Execute the **Dual-Stage Protocol**: Output the following interactive selection banner to standard output (Stage 1 Markdown), then prompt with `ask_question` using clean concise options (Stage 2):
  ```text
  ================================================================================
  🛠️ CREW DEV FORGE: COMPLETED ARCHITECTURE SESSION DETECTED
  ================================================================================
  Project Session: .audit/crew-dev-forge/[Current_Dir_Name]/
  Current Status:  STATE: COMPLETED
  Artifacts:       ARCHITECTURE.md and ORCHESTRATION_PLAN.md already generated
  
  An architecture session has already been completed for this project.
  How would you like to proceed?
  
  1. 🔄 Refine Existing Architecture:
     Jump directly to PM Review (Turn 8) to dictate amendments, run a mini-ARB
     audit, and update master governance documents without re-running prior roles.
  2. 🗄️  Archive & Start Fresh:
     Safely archive current audit logs and decisions to _archive/ and begin a
     brand new architecture committee gauntlet from scratch.
  3. 🚫 Cancel:
     Exit cleanly without modifying any files.
  
  👉 Reply 1 (Refine), 2 (Archive & Fresh), or 3 (Cancel) to proceed:
  ================================================================================
  ```
  - **User selects 1:** Advance to Fast-Track Refine Pathway (`STATE: 8_PM_REVIEW`).
  - **User selects 2:** Execute archival tool:
    ```bash
    python .agents/skills/crew-dev-forge/tools/session_manager.py --action archive --project [Current_Dir_Name]
    ```
    Initialize clean `session_meta.json` and proceed with fresh `plan` mode.
  - **User selects 3:** Print `[crew-dev-forge] Session preserved. Halting.` and stop.

### 3. In-Progress Session Resume Protocol
- **If `.active_state` exists, is NOT `COMPLETED`, and is NOT empty:**
  An interrupted or paused session has been detected.  
  Read `session_meta.json` and `architecture_decisions.md` to identify completed roles.  
  Execute the **Dual-Stage Protocol**: Output the resume banner to standard output (Stage 1 Markdown), then prompt with `ask_question` using clean concise options (Stage 2):
  ```text
  ================================================================================
  🛠️ CREW DEV FORGE: IN-PROGRESS SESSION DETECTED
  ================================================================================
  Project Session: .audit/crew-dev-forge/[Current_Dir_Name]/
  Last State:      [ACTIVE_STATE]
  Mode:            [Fast Mode / Interactive Mode]
  
  1. ▶️  Resume Session:
     Continue the committee gauntlet from [ACTIVE_STATE]. All prior decisions
     in architecture_decisions.md are preserved.
  2. 🗄️  Archive & Start Fresh:
     Archive partial progress and begin a clean session from scratch.
  3. 🚫 Cancel:
     Exit cleanly without modifying any files.
  
  👉 Reply 1 (Resume), 2 (Archive & Fresh), or 3 (Cancel) to proceed:
  ================================================================================
  ```
  - **User selects 1:** Load cumulative decisions from `architecture_decisions.md`, restore `fast_mode` flag from `session_meta.json`, and jump directly to the persona corresponding to `[ACTIVE_STATE]`.
  - **User selects 2:** Execute `session_manager.py --action archive` and restart.
  - **User selects 3:** Halt execution.

### 4. Fresh Session Initialization
If no active session exists or after an archive action:
- Initialize `session_meta.json` with:
  ```json
  {
    "timestamp": "[ISO-8601]",
    "project_name": "[Current_Dir_Name]",
    "directory": "[Current_Working_Dir]",
    "active_state": "STATE: 0_DISCOVERY_STRATEGIST",
    "architecture_type": "FULLSTACK",
    "fast_mode": false,
    "refinement_version": 0,
    "completed_roles": []
  }
  ```
- **Fast Mode Resolution:**
  - If `--fast` is in `$ARGUMENTS`: Set `"fast_mode": true` in `session_meta.json`.
  - If `--fast` is not in `$ARGUMENTS` and mode is not `refine`: Execute the **Dual-Stage Protocol**: Print the interactive mode selection prompt to standard output (Stage 1 Markdown), then prompt with `ask_question` using clean concise options (Stage 2):
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
    - Reply 1: Set `"fast_mode": true` in `session_meta.json`.
    - Reply 2: Set `"fast_mode": false` in `session_meta.json`.
- Proceed immediately to `STATE: 0_DISCOVERY_STRATEGIST`.

### 5. Universal Abort / Cancel Mechanism
If the user replies `ABORT` or `CANCEL` (case-insensitive) at any CLI prompt during any role:
1. Append `[SESSION PAUSED BY USER]` to `debate_transcript.md`.
2. Overwrite `.active_state` with `[CURRENT_STATE]_PAUSED`.
3. Update `session_meta.json` with `"active_state": "[CURRENT_STATE]_PAUSED"`.
4. Output: `[crew-dev-forge] Session safely paused at [CURRENT_STATE]. Resume anytime by running /crew-dev-forge plan.` and halt.

---

## 🔄 State Transition Bookkeeping & Pre-Advancement Validation

> [!CRITICAL]
> **STATE SYNCHRONIZATION DIRECTIVE (MANDATORY ACROSS ALL ROLES):**  
> State must NEVER desynchronize. Whenever advancing from role $N$ to role $N+1$:
> 1. **Pre-Advancement Validation:** Inspect `architecture_decisions.md` to confirm the current role's consensus section header (e.g., `### 🏛️ Tech Lead Consensus`) is present and non-empty. If missing, DO NOT ADVANCE; re-prompt or distill decisions.
> 2. **Active State Overwrite:** Overwrite `.audit/crew-dev-forge/[Current_Dir_Name]/.active_state` with the new state string.
> 3. **Metadata Sync:** Update `.audit/crew-dev-forge/[Current_Dir_Name]/session_meta.json`:
>    - Set `"active_state"` to the new state.
>    - Append the completed role name to `"completed_roles"` (if not already present).
>    - Set `"updated_at"` to the current timestamp.

---

## 🧠 Context Budget Management & Role Isolation Directive

To prevent LLM context exhaustion, instruction degradation, and behavioral drift during long gauntlets:
1. **Targeted State Loading:** When activating each persona, the Orchestrator MUST load ONLY:
   - The current role's instruction file (`roles/[X]_[Name].md`)
   - The distilled `architecture_decisions.md`
   - `session_meta.json`  
   Do NOT re-read raw unparsed workbooks or the full cumulative `debate_transcript.md`.
2. **Incremental Transcript Persistence:** Append each persona's debate and pushback exchanges to `debate_transcript.md` immediately upon completing that turn, then flush raw conversation details from working context.
3. **Role Isolation:** Each persona acts solely within its designated discipline. Personas must NEVER re-litigate decisions settled by prior personas unless raising an explicit contradiction during Role 7.

---

## 🧭 Role 0: Discovery Strategist (`roles/0_Discovery_Strategist.md`)

- **State Flag:** `STATE: 0_DISCOVERY_STRATEGIST`
- **Objective:** Establish the product requirements baseline before technical architecture begins.

### 1. The Fast-Pass Check
Inspect workspace for `ANALYTICS_DISCOVERY_REPORT.md`, `*DISCOVERY*.md`, `PRD.md`, or input path in `$ARGUMENTS`.
- **If sufficient PRD context exists:**
  1. Print Fast-Pass confirmation:
     `✅ Discovery Document Approved: [DOCUMENT_PATH]. Fast-passing directly to Step 0: Triage...`
  2. Log approval to `debate_transcript.md`.
  3. Overwrite `.active_state` with `STATE: 0_TRIAGE` and sync `session_meta.json`.
  4. Proceed directly to Triage.

### 2. The Grilling Protocol (If PRD is Missing or Shallow)
If requirements are missing or shallow:
1. Initialize the **Design Tree** (Root: Problem -> Personas -> Functional Scope -> Constraints).
2. Interrogate the user in concise **Rounds** on the active **Frontier**.
3. Format questions strictly:
   ```text
   ❓ **Q[X]** - **<Question Title>**: <Context/Body>
   ➡️ **Recommended Answer:** <Recommendation framed for 'yes'>
   ```
4. Recompute the Frontier after each user reply until empty.
5. Synthesize `.audit/crew-dev-forge/[Current_Dir_Name]/PRD_DISCOVERY.md`.
6. Advance state to `STATE: 0_TRIAGE` and sync `session_meta.json`.

---

## 🧭 Step 0 Triage: Architectural Scope & Routing (`STATE: 0_TRIAGE`)

Determine architectural scope to skip irrelevant disciplines:
- **Check `$ARGUMENTS`:** Parse `Fullstack`, `Frontend-only`, `Backend-only`, or `CLI` if supplied.
- **If NOT specified:** Prompt user for architecture type (1: Fullstack, 2: Frontend-only, 3: Backend-only, 4: CLI Tool).
- **Mandatory Triage Persistence:**
  1. Record `architecture_type` in `session_meta.json`.
  2. Record the consensus in `architecture_decisions.md`:
     ```markdown
     ### 🧭 Triage Consensus: Architectural Scope
     - **Architecture Type:** [FULLSTACK / FRONTEND_ONLY / BACKEND_ONLY / CLI_TOOL]
     - **Active Role Sequence:** [Active roles list]
     - **Skipped Disciplines:** [Skipped roles list and rationale]
     ```
  3. Log triage consensus to `debate_transcript.md`.
- Overwrite `.active_state` with `STATE: 1_TECH_LEAD` and sync `session_meta.json`.

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
When `fast_mode: true` in `session_meta.json`:
1. Roles 1 through 6 **DO NOT HALT** for user CLI input.
2. Each role automatically records its `(Recommended)` Option 1 into `architecture_decisions.md`.
3. The Orchestrator prints a fast-scroll log:
   ```text
   ⚡ Fast Mode: [Role Name] auto-selected recommended options [Summary]. Moving to next phase...
   ```
4. Perform pre-advancement validation, overwrite `.active_state`, and sync `session_meta.json`.

### 💬 Interactive Mode Execution Rules (Roles 1-6):
When `fast_mode: false` in `session_meta.json`:
1. The Orchestrator halts at each role and strictly executes the **Dual-Stage Interactive CLI Protocol**:
   - **Stage 1 (Chat Stream):** Emits the full persona introduction, architectural rationale, code references with `file://` links, and the complete Question Battery with detailed numbered recommendations into the visible chat message.
   - **Stage 2 (Interactive Selector):** Invokes `ask_question` with clean, concise option labels (referencing the Stage 1 options) to enable ergonomic arrow-key navigation without terminal text wrapping or squeezing.
2. **Mandatory Completion Gate:** The persona **MUST NOT** advance until the user answers all questions for that role.
3. If the user replies shallowly, the **Advanced Pushback Protocol** is triggered before advancing.
4. Record decisions in `architecture_decisions.md`, log to `debate_transcript.md`, validate, overwrite `.active_state`, and sync `session_meta.json`.

---

### Turn 1: Tech Lead (`roles/1_Tech_Lead.md`)
- **State Flag:** `STATE: 1_TECH_LEAD`
- **Key Focus:** Language/Runtime, Core Framework, State Management, and **Mandatory Phase 0: Documentation (README.md)**.
- **Route to Next Role:** `STATE: 2_UX_ARCHITECT` (or Turn 3/5 depending on Triage).

---

### Turn 2: UX Architect (`roles/2_UX_Architect.md`)
- **State Flag:** `STATE: 2_UX_ARCHITECT`
- **Applicability:** Active for `FULLSTACK` and `FRONTEND_ONLY`. Skipped for `BACKEND_ONLY` and `CLI_TOOL`.
- **Key Focus:** Routing, UI Component Library, Centralized Design Tokens (globals.css + config bridge), Skeletons, Auth UI.
- **Route to Next Role:** `STATE: 3_DATA_ARCHITECT` (or Turn 5 if Frontend-only).

---

### Turn 3: Data Architect (`roles/3_Data_Architect.md`)
- **State Flag:** `STATE: 3_DATA_ARCHITECT`
- **Applicability:** Active for `FULLSTACK` and `BACKEND_ONLY`. Skipped for `FRONTEND_ONLY` and `CLI_TOOL`.
- **Key Focus:** SQL vs NoSQL, Entity Normalization, Primary/Foreign Keys, ORM & Seeding Strategy.
- **Route to Next Role:** `STATE: 4_BACKEND_ARCHITECT`.

---

### Turn 4: Backend Architect (`roles/4_Backend_Architect.md`)
- **State Flag:** `STATE: 4_BACKEND_ARCHITECT`
- **Applicability:** Active for `FULLSTACK` and `BACKEND_ONLY`. Skipped for `FRONTEND_ONLY` and `CLI_TOOL`.
- **Key Focus:** REST/RPC versioning, Endpoint Inventory, Input Validation (Zod/Pydantic), Auth Middleware.
- **Route to Next Role:** `STATE: 5_DEVOPS_ENGINEER`.

---

### Turn 5: DevOps Engineer (`roles/5_DevOps_Engineer.md`)
- **State Flag:** `STATE: 5_DEVOPS_ENGINEER`
- **Applicability:** Active for all architecture types.
- **Key Focus:** Directory Tree, Off-limits files, `.env.example`, and **Mandatory Handoff Protocol (`.audit/current_agent_phase.md`)**.
- **Route to Next Role:** `STATE: 6_QA_TESTER`.

---

### Turn 6: QA Tester (`roles/6_QA_Tester.md`)
- **State Flag:** `STATE: 6_QA_TESTER`
- **Applicability:** Active for all architecture types.
- **Key Focus:** Test Runner Stack, Phase 0 Documentation Verification Command, Phase Gates, Edge Cases.
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
  - Audits `architecture_decisions.md` for cross-domain contradictions, security traps, and scalability bottlenecks.
  - **MANDATORY ARB AUDIT VISIBILITY (Stage 1):** MUST output the complete ARB Audit Report directly in the chat message containing persona introduction, explicit `[RISK 1]` and `[RISK 2]` descriptions, code references with `file://` links, and blast radius analysis. Never call `ask_question` with empty message text.
  - **Interactive Hardening Gate (Stage 2):** Invokes `ask_question` with streamlined hardening options:
    1. `(Recommended) 1. Apply Full ARB Hardening: (Apply Patches 1 & 2 to eliminate detected risks)`
    2. `2. Partial Hardening: (Apply Patch 1 only)`
    3. `3. Accept identified risks as intentional technical debt for V1 MVP`
- **On User Reply:**
  1. Append verbatim reply to `debate_transcript.md`.
  2. Distill decisions into `architecture_decisions.md` under `### 🧐 Principal Reviewer Consensus: Devil's Advocate Audit & Patches`.
  3. Overwrite `.active_state` with `STATE: 8_PM_REVIEW` and sync `session_meta.json`.
  4. Proceed immediately to Turn 8.

---

### Turn 8: Project Manager Review Loop (`STATE: 8_PM_REVIEW`)
- **State Flag:** `STATE: 8_PM_REVIEW`
- **MANDATORY APPROVAL GATE: ALWAYS HALTS FOR USER INPUT.**
- **Dual-Stage PM Review:**
  1. **Stage 1 (Chat Stream):** Print the Executive Architecture Review Banner to standard output:
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
  2. **Stage 2 (Interactive Approval Selector):** Invoke `ask_question` with clean choices:
     - `(Recommended) Approved: Proceed to synthesize ARCHITECTURE.md & ORCHESTRATION_PLAN.md`
     - `Request changes or revise constraints (provide details)`

#### Handling PM Revisions & The Refinement Mini-ARB Check:
If the PM requests changes:
1. **Snapshot Prior State (Versioning):**
   - Increment `"refinement_version"` in `session_meta.json`.
   - Copy current `architecture_decisions.md` to `architecture_decisions_v[N].md`.
2. **Record Amendments:**
   - Append changes under `### 🚀 Turn 8 Refinements Ledger v[N] (YYYY-MM-DD HH:MM)` in `architecture_decisions.md`.
3. **Mini-ARB Devil's Advocate Stress-Test:**
   - Evaluate whether the requested changes introduce cross-domain contradictions with earlier locked decisions.
   - If conflicts exist: Output 1-2 specific risks and request confirmation before re-prompting PM.
   - If no conflicts: Update consensus and re-prompt PM for final sign-off.
4. **When Approved:**
   - Advance `.active_state` to `STATE: 9_SYNTHESIS_AND_GENERATION` and sync `session_meta.json`.
   - Proceed immediately to Final Synthesis.

---

## 🚀 Final Unified Artifact Synthesis & Template Validation

Once `STATE: 8_PM_REVIEW` is approved, synthesize **exactly two files** in the project root:

### 1. `ARCHITECTURE.md` (Always Generated)
- Populated using [`.agents/skills/crew-dev-forge/templates/ARCHITECTURE_TEMPLATE.md`](./templates/ARCHITECTURE_TEMPLATE.md).
- Contains **NO task checkboxes**.
- Authoritative single source of truth for Stack, Folder Tree, Schemas, API Contracts, Security Rules, `.env.example`, and Handoff Protocols.
- If non-fullstack, mark inactive layers cleanly as `N/A - [Scope] Scope`.

### 2. `ORCHESTRATION_PLAN.md` (Dynamic Multi-Phase Generation)
- Populated using [`.agents/skills/crew-dev-forge/templates/ORCHESTRATION_TEMPLATE.md`](./templates/ORCHESTRATION_TEMPLATE.md).
- Dynamically breaks execution into $N$ bite-sized, logical phases based on complexity.
- **CRITICAL HITL REQUIREMENT:** Appends the standard "🛑 HUMAN APPROVAL GATE" block at the end of **EVERY** phase:
  ```markdown
  #### 🛑 HUMAN APPROVAL GATE: PHASE [K] ➔ PHASE [K+1]
  > **STOP EXECUTION:** Present verification proof. Ask: *"Phase [K] complete. May I proceed to Phase [K+1]?"*  
  > *(Wait for explicit human CLI approval before proceeding).*
  ```

### 3. Automated Architecture Decision Records (ADR) Export Engine
Upon synthesizing the master artifacts, the Orchestrator MUST execute the automated ADR export engine:
```bash
python .agents/skills/crew-dev-forge/tools/session_manager.py --action export-adrs --project [Current_Dir_Name]
```
- Parses all consensus sections from `architecture_decisions.md` and generates structured, versioned ADR files in `docs/adr/`:
  - `docs/adr/0001-scope-and-triage.md`
  - `docs/adr/0002-core-stack-and-state.md`
  - `docs/adr/0003-frontend-tokens-and-layout.md`
  - `docs/adr/0004-database-and-orm.md`
  - `docs/adr/0005-api-contracts-and-validation.md`
  - `docs/adr/0006-devops-and-handoffs.md`
  - `docs/adr/0007-verification-gates-and-testing.md`
  - `docs/adr/0008-arb-devil-advocate-hardening.md`
  - `docs/adr/README.md` (Master Table of Contents)

### 4. Post-Synthesis Template Placeholder & Schema Syntax Validation
Before marking the session complete:
1. Scan `ARCHITECTURE.md` and `ORCHESTRATION_PLAN.md` for unresolved `{{...}}` tags.
2. Verify that all markdown code fences (```) are syntactically closed.
3. Verify that all shell verification commands in `ORCHESTRATION_PLAN.md` reference real paths (e.g., `backend/venv/bin/pytest`, `npm run build`).
4. If any placeholder remains unresolved: Resolve it immediately using data from `architecture_decisions.md` or replace with an explicit, clean specification.

### 5. Terminal State Completion & Transcript Closure
1. Append final completion block to `debate_transcript.md`:
   ```markdown
   ---
   ## 📝 Session Completion Record
   - **PM Approval:** Approved
   - **Artifacts Generated:** ARCHITECTURE.md, ORCHESTRATION_PLAN.md
   - **Completion Timestamp:** [ISO-8601]
   - **Final State:** STATE: COMPLETED
   ```
2. Overwrite `.active_state`: `STATE: COMPLETED`.
3. Update `session_meta.json` with `"active_state": "STATE: COMPLETED"`.
4. Output executive completion banner with paths to `ARCHITECTURE.md` and `ORCHESTRATION_PLAN.md`.

---

## 🚫 Explicit Negative Constraints (Guardrails)

1. **Planning-Only Skill Boundary:** This skill is STRICTLY a planning and architecture committee simulation. The Orchestrator and all role personas are ABSOLUTELY FORBIDDEN from:
   - Creating, editing, or modifying ANY application source code files (`.py`, `.ts`, `.tsx`, `.js`, `.jsx`, `.css`, `.html`, etc.).
   - Running code execution commands (`npm run dev`, `pip install`, test execution, or modifying project codebase).
   - Making ANY changes outside of `.audit/crew-dev-forge/` and the two root governance files (`ARCHITECTURE.md` and `ORCHESTRATION_PLAN.md`).  
   If the user asks for code changes during the workflow, respond:  
   *"This skill is a planning-only committee. Code implementation should be performed after the architecture and orchestration plan are approved, using the generated ORCHESTRATION_PLAN.md as the execution guide."*
2. **NO Starting Without PRD Context:** Roles 1 through 6 must never begin technical design without an approved PRD context (either fast-passed or synthesized via `0_Discovery_Strategist.md`).
3. **Fast Mode Safety Catch:** Fast Mode is strictly forbidden from auto-advancing past Role 6; it MUST halt at Role 7 (Devil's Advocate) and Role 8 (PM Review).
4. **NO Halting for Project Name:** Never halt execution to ask for a project name; always auto-detect the current working directory name.
5. **Session Offloading:** Never manually move or archive session files via LLM read/write loops; always use `python .agents/skills/crew-dev-forge/tools/session_manager.py --action archive --project [Current_Dir_Name]`.
6. **Strict Q&A Formatting & Dual-Stage Protocol:** Every role question in interactive mode must offer 2-3 numbered recommendations ending with 'or provide your custom input'. The Orchestrator and all personas are STRICTLY FORBIDDEN from invoking `ask_question` with empty message content or without first presenting the detailed context, risk analysis, and trade-offs in visible chat Markdown (Zero-Blind-Decisions rule).
7. **Enforce Pushback Protocol:** In interactive mode, never accept shallow answers without presenting risks, two alternatives, an explicit recommendation, and awaiting confirmation.
8. **Mandatory Documentation Gate (Phase 0):** `ORCHESTRATION_PLAN.md` must enforce writing comprehensive `README.md` before generating code.
9. **Mandatory Human-in-the-Loop Approval Gates (HITL):** Every dynamically generated phase in `ORCHESTRATION_PLAN.md` MUST conclude with a mandatory human approval prompt. Agents are strictly forbidden from auto-advancing across phases.
10. **Dynamic Phase Sizing:** Break execution into as many discrete phases (Phase 1 through Phase N) as required based on complexity to prevent agent hallucinations.
11. **Exact Two-Artifact Output:** Always generate exactly two files: `ARCHITECTURE.md` (no checkboxes) and `ORCHESTRATION_PLAN.md` (with task checkboxes and approval gates).
12. **Mandatory PM Approval Gate:** Never generate final artifacts without explicit Project Manager approval in `STATE: 8_PM_REVIEW`.
