---
description: Deep-scan any codebase and generate a comprehensive architecture.md reference document that serves as the starting point for any AI agent or developer
---

# Generate Architecture Document

A **language-agnostic deep-scan skill** that scrapes an entire codebase — regardless of language, framework, or scale — and produces a comprehensive `architecture.md`. This document becomes the **single starting reference** for any coding agent or developer to understand the project deeply before making changes.

## When to Use

- Starting work on any project (new or existing)
- User explicitly asks for architecture documentation
- Onboarding onto an unfamiliar codebase
- Before any major refactoring or feature addition

## Philosophy

This is a **deep search engine for codebases**. The goal is NOT surface-level documentation — it's a thorough investigation that maps every component, API boundary, data flow, state machine, and design decision. Critically, it also builds a **complete code index** — every file, every class, every function — so any AI agent can instantly locate the right code without searching. The output should let any agent immediately understand the project well enough to make production-quality changes.

---

## Step 1: Detect the Tech Stack

Before scanning, identify the project type by checking for these marker files. Check ALL of them — projects often combine multiple stacks.

### Build System / Language Detection

| Marker File(s) | Stack | Scan Focus |
|----------------|-------|------------|
| `CMakeLists.txt`, `Makefile`, `*.cpp`, `*.h` | **C / C++** | Headers (public API), static/shared libs, link order, pkg-config deps |
| `package.json`, `tsconfig.json` | **Node.js / TypeScript** | `src/` components, routes, API handlers, middleware, `package.json` scripts |
| `vite.config.*`, `next.config.*`, `webpack.config.*` | **React / Vue / Angular** | Component tree, pages/routes, state management, API calls, styling system |
| `setup.py`, `pyproject.toml`, `requirements.txt`, `Pipfile` | **Python** | Modules, classes, decorators, CLI entry points, ORM models |
| `manage.py`, `settings.py` | **Django** | Apps, models, views, URLs, middleware, management commands |
| `go.mod`, `go.sum` | **Go** | Packages, interfaces, `cmd/` entry points, internal vs exported |
| `Cargo.toml` | **Rust** | Crates, modules, traits, `src/bin/` vs `src/lib.rs` |
| `pom.xml`, `build.gradle` | **Java / Kotlin** | Packages, Spring beans, controllers, services, repositories |
| `Dockerfile`, `docker-compose.yml` | **Containerized** | Services, networks, volumes, build stages |
| `.github/workflows/`, `.gitlab-ci.yml` | **CI/CD** | Pipeline stages, deploy targets |
| `terraform/`, `*.tf` | **Infrastructure** | Resources, modules, variables |

Run `list_dir` on the project root first, then check for these markers to determine the scanning strategy.

---

## Step 2: Deep Scan the Codebase

Execute these scans in order. **Adapt to the detected stack** — not all scans apply to every project.

### 2.1 Structure Scan

```
list_dir on project root → identify all top-level directories
Recursively list_dir on each source directory — GO DEEP (4-5 levels)
For each source directory, also run find_by_name with file extensions
  to get the COMPLETE file list
```

**Goal:** Build a complete mental model of the directory tree including EVERY source file.

> ⚠️ **CRITICAL:** Do NOT stop at top-level directories. You must drill into
> EVERY subdirectory until you reach individual source files. A directory tree
> that only shows folders and a few files is INCOMPLETE and UNACCEPTABLE.
> Use `find_by_name` with extension filters to ensure you capture every file.
> For example, for frontend frameworks (Angular/React/Vue):
> - List every `.ts`, `.tsx`, `.html`, `.css`, `.scss` file in every component directory
> - List every service, hook, utility, and state management file
>
> For backend/systems code (C++, Python, Go, Java, Rust):
> - C++: List every `.h` AND `.cpp` file, not just headers
> - Python: List every `.py` file including `__init__.py` and utility modules
> - Go: List every `.go` file in the package
> - Config: List every `CMakeLists.txt`, `pom.xml`, or `Cargo.toml` in subdirectories

### 2.2 Entry Point Scan

Find ALL entry points — how the application starts and what drives it:

| Stack | Entry Points to Find |
|-------|---------------------|
| **C/C++** | `grep_search` for `int main(` across all `.cpp` files |
| **Python** | `grep_search` for `if __name__`, `@app.route`, `@click.command`, `entry_points` in setup.py |
| **React** | Read `src/App.tsx` or `src/App.jsx`, check router config, `src/main.tsx` |
| **Next.js** | Scan `pages/` or `app/` directory (file-based routing) |
| **Django** | Read `urls.py` files (all of them), `settings.py` INSTALLED_APPS |
| **Go** | Scan `cmd/*/main.go`, `main.go` at root |
| **Rust** | Read `src/main.rs`, `src/bin/*.rs`, check `[[bin]]` in Cargo.toml |
| **Java** | `grep_search` for `public static void main`, `@SpringBootApplication` |

### 2.3 Public API / Interface Scan

Map every public API surface — what external consumers see:

| Stack | How to Scan |
|-------|------------|
| **C/C++** | Read all `include/*.h` files — structs, classes, function declarations |
| **Python** | Read `__init__.py` files for exports, class definitions, `@dataclass`, type hints |
| **TypeScript** | Read `index.ts` barrel exports, interface/type files, `.d.ts` declarations |
| **React** | Read component props (interfaces), context providers, custom hooks |
| **Django** | Read serializers, viewsets, URL patterns |
| **Go** | Scan exported types (capitalized) in package-level files |
| **Rust** | Read `pub` items in `lib.rs` and module `mod.rs` files |
| **REST API** | Find route definitions, OpenAPI/Swagger specs, handler functions |
| **GraphQL** | Read schema files (`.graphql`, `typeDefs`) |

### 2.4 Data Model Scan

Find ALL data definitions — schemas, models, types:

| Stack | Where to Look |
|-------|--------------|
| **SQL** | `*.sql` files, migration directories, schema DDL in source code |
| **Django** | `models.py` in each app |
| **SQLAlchemy** | Model classes inheriting `Base` or `db.Model` |
| **Prisma** | `schema.prisma` |
| **TypeORM** | `@Entity()` decorated classes |
| **Mongoose** | `Schema` definitions |
| **Go** | Struct definitions with `db` or `json` tags |
| **Rust** | `#[derive(Serialize)]` structs, diesel schema |
| **Proto** | `.proto` files |

### 2.5 Dependency Scan

Map internal AND external dependencies:

**Internal:** Which component imports/includes which? Look at import statements across all files.

**External (from manifests):**
| Stack | Manifest |
|-------|---------|
| **C/C++** | `CMakeLists.txt` (FetchContent, find_package), `pkg-config` |
| **Python** | `requirements.txt`, `pyproject.toml`, `Pipfile`, `setup.cfg` |
| **Node.js** | `package.json` (dependencies + devDependencies) |
| **Go** | `go.mod` |
| **Rust** | `Cargo.toml` [dependencies] |
| **Java** | `pom.xml` or `build.gradle` |

**Vendored / header-only deps (often missed — check explicitly):**
- `grep_search` for `#include` directives that reference non-system, non-project headers (e.g. `"nlohmann/json.hpp"`, `"httplib.h"`, `"stb_image.h"`)
- Check for `third_party/`, `vendor/`, `extern/`, `deps/` directories
- Look inside `CMakeLists.txt` for `add_subdirectory` of external libs
- These are real dependencies that MUST appear in the External Dependencies table

### 2.6 Configuration Scan

Find ALL configuration sources:

- Environment variables (`grep_search` for `os.environ`, `process.env`, `os.Getenv`, `std::getenv`)
- Config files (`.json`, `.yaml`, `.toml`, `.env`, `.ini`)
- CLI flags / argument parsing
- Feature flags
- Default values and fallbacks

### 2.7 State & Flow Scan

Identify stateful components:

- State machines (enums with transitions, Redux reducers, FSM patterns)
- Event handlers / callbacks / signal handlers
- Async flows (promises, futures, channels, queues)
- Lifecycle hooks (React useEffect, Django signals, Spring @PostConstruct)

### 2.8 Error Handling Scan

Map error handling patterns:

- Exception/error types defined in the project
- Global error handlers (middleware, error boundaries, panic handlers)
- Retry logic, circuit breakers, fallback behavior
- Logging patterns (`grep_search` for log/print/console statements)

### 2.9 Security Scan

Identify security-related code:

- Authentication (JWT, OAuth, session, API keys)
- Authorization (RBAC, middleware guards, decorators)
- Encryption (at rest, in transit)
- Secret management (vault, env vars, encrypted files)
- Input validation and sanitization

### 2.10 Test Scan

Map the testing strategy:

- Test framework(s) used
- Test directory structure
- Unit vs integration vs e2e tests
- Test utilities, fixtures, factories
- Coverage configuration

### 2.11 Event & Message Broker Scan

Identify event-driven components:
- Event buses (Kafka, RabbitMQ, SQS, SNS, Redis Pub/Sub)
- Topics, queues, and channels
- Producers and Consumers (which components publish, which subscribe)
- Event schema registries if applicable
- WebSocket / Server-Sent Events (SSE) hubs

### 2.12 Caching Scan

Identify caching strategies:
- Distributed caches (Redis, Memcached)
- In-memory caches (Guava, LRU caches)
- Web caches (CDN rules, Edge caching, Varnish)
- Decorators or annotations (e.g., `@Cacheable`)
- Invalidation logic triggers

### 2.13 Observability Scan

Identify telemetry and monitoring:
- Logging frameworks (Log4j, Winston, Serilog, Zap)
- Log formatters (JSON, text) and correlation IDs
- Metrics exporters (Prometheus, Datadog StatsD, OpenTelemetry)
- Distributed tracing setup
- Health check endpoints (`/healthz`, `/metrics`)

### 2.14 Symbol Index Scan (Code Index)

This is the **most important scan for AI agent effectiveness**. For every source file in the project, extract the complete list of classes, functions, methods, and key constants.

**How to scan:**

Use `view_file_outline` on every source file (not configs, not assets). This returns all classes and functions with their line ranges. For each file, record:

- File path (relative to project root)
- Every class / struct / interface / enum defined
- Every function / method with its signature (name + params + return type)
- Line range for each symbol

**Scanning by stack:**

| Stack | Files to Scan | What to Extract |
|-------|--------------|----------------|
| **C/C++** | All `.h` and `.cpp` files | Classes, structs, free functions, methods, enums, typedefs |
| **Python** | All `.py` files (skip `__pycache__`) | Classes, functions, methods, decorators, module-level constants |
| **TypeScript/JS** | All `.ts`, `.tsx`, `.js`, `.jsx` files | Components, hooks, functions, interfaces, types, classes, exported constants |
| **Go** | All `.go` files (skip `*_test.go` but note test files separately) | Structs, interfaces, functions, methods (receiver type noted) |
| **Rust** | All `.rs` files | Structs, enums, traits, impl blocks, functions |
| **Java/Kotlin** | All `.java`, `.kt` files | Classes, interfaces, methods, enums |

**Efficiency tips:**
- Use `find_by_name` with file extension filters to get the full file list first
- Process files in directory order (component by component)
- For large projects (100+ files), batch by component/module
- Skip generated files, vendor directories, node_modules, build output

**Output format for the Code Index section:**

Group by component/directory. For each file, create a compact table:

```
### `component/src/service.cpp`
| Symbol | Type | Line | Description |
|--------|------|------|-------------|
| `ServiceClass` | class | 15-120 | Main service implementation |
| `ServiceClass::init` | method | 25-40 | Initializes connection pool |
| `ServiceClass::process` | method | 42-89 | Core processing loop |
| `helperFunc` | function | 95-120 | Utility for parsing input |
```

The Description column should be a concise one-line explanation derived from reading the function body or its doc comment. If the function purpose is obvious from its name, the description can simply restate it.

---

## Step 3: Write the Architecture Document

Create `architecture.md` at the location specified by the user (default: project root).

### Rules

1. **Every claim must be verified against source code** — never guess
2. **Omit sections that don't apply** — a React SPA won't have systemd services
3. **Use tables for structured data** — APIs, configs, schemas, dependencies
4. **Use Mermaid for visual relationships** — architecture diagrams, state machines, sequence flows
5. **Annotate the directory tree** — add `# comment` for every significant file/directory
6. **Document WHY, not just WHAT** — design decisions need rationale
7. **Keep it current-state** — document what IS, not what should be

### Document Structure

Use these sections. **Skip sections that don't apply.** Order can vary based on project type.

```markdown
# [Project Name] — Architecture Reference

> **Purpose of this document:** This is the single reference for any developer
> or AI agent before starting work on the `[project]` project. It covers the
> project structure, all components, data models, build system, deployment,
> and key design decisions.

## Table of Contents

A clickable navigation index listing every section and subsection in the
document. Use markdown anchor links. Include all top-level `##` sections
and nested `###` subsections indented as a sub-list.

Example:
- [1. Project Overview](#1-project-overview)
- [2. Architecture Diagram](#2-architecture-diagram)
- [4. Components — Detail](#4-components--detail)
  - [4.1 Component A](#41-component-a)
  - [4.2 Component B](#42-component-b)
- ...

> ⚠️ **MANDATORY:** Every generated architecture.md MUST include a Table
> of Contents immediately after the purpose block. This enables fast
> navigation in large documents. Update the TOC whenever sections are
> added or removed.

---

## 1. Project Overview

- What the project does (bullet list of capabilities)
- Tech stack summary (languages, frameworks, database, runtime)
- Build system and package manager
- Version management strategy

---

## 2. Architecture Diagram

Mermaid graph showing all components, their relationships, external
dependencies, and data flow directions. 

> ⚠️ Ensure the diagram includes message brokers (Kafka/RabbitMQ), 
> caching layers (Redis), and 3rd-party integrations (Stripe/Auth0),
> not just the app and the database. Use subgraphs to group related
> components.

---

## 3. Directory Structure

Annotated tree with inline # comments explaining every significant
directory AND every source file. This is the "map" for navigating
the codebase.

> ⚠️ **DEPTH REQUIREMENT:** The tree MUST go down to individual source
> files, not just directories. For every directory that contains source
> code, list EVERY file in it. This includes:
> - **C/C++:** Both headers AND implementation files (`.h` + `.cpp`)
> - **Frontend (Angular/React):** All component files (`.ts` + `.tsx` + `.html` + `.css`)
> - **Python/Django:** All module files (`models.py`, `views.py`, `serializers.py`)
> - **Go/Rust/Java:** All source files (`.go`, `.rs`, `.java`)
> - Configuration and test files alongside their source files
>
> A tree that only shows directories and a few selected files is
> INCOMPLETE. If a directory has 5 files, list all 5.
>
> Example of CORRECT depth (C++):
> ```text
> common/streamutils/
> ├── include/
> │   └── StreamService.h      # StreamResult, ImageResult structs + StreamService class
> ├── src/
> │   └── StreamService.cpp    # Pipeline management, teardown, pad-added callbacks
> └── CMakeLists.txt           # Links gstreamer-1.0, gstreamer-app-1.0
> ```
>
> Example for Angular:
> ```text
> features/dashboard/
> ├── dashboard.component.ts    # Main dashboard controller, tab switching
> ├── dashboard.component.html  # Template with chart containers
> ├── dashboard.component.css   # Dashboard-specific styles
> ├── dashboard.module.ts       # Module declaration, imports PrimeNG
> └── dashboard-routing.module.ts # Child routes for dashboard tabs
> ```

---

## 4. Components / Modules — Detail

For EACH component, in dependency order (dependencies first):

### 4.N [Component Name]

- Purpose (1-2 sentences)
- **Public API surface** — MUST be a table, not prose:

| Method / Function | Params | Returns | Description |
|-------------------|--------|---------|-------------|
| `methodName` | `(arg1: type, arg2: type)` | `ReturnType` | What it does |

- **Internal architecture** — key classes, patterns, important private methods
- **Dependencies** on other components
- **External library dependencies**

> ⚠️ **NO PROSE-ONLY SECTIONS.** Every component that has methods MUST
> include a method-level table. A section that says "ServerService: The
> central hub for all backend communication" without listing its methods
> is INCOMPLETE.
>
> For UI frameworks (Angular/React/Vue), list EVERY public method in services and hooks.
> For backend code (C++, Python, Go), list EVERY public method or exported function.
> Do NOT use prose when a table can show the exact API.

---

## 5. Data Model & Storage

### 5.1 Database Schema
- Database / storage engine
- Connection / credential management
- Schema tables with columns, types, constraints, indexes
- For ORMs: model class locations and relationships

> ⚠️ **MANDATORY ERD:** If using a relational database, you MUST 
> include a Mermaid `erDiagram` showing tables and relationships.

### 5.2 Caching Strategy
- What data is cached (Redis/Memcached vs CDN vs LocalStorage)
- Cache invalidation triggers and TTLs

### 5.3 Migrations & Seeding
- How schema changes are managed (Flyway, Alembic, Prisma)
- Development seeding strategy

---

## 6. Build System

- Build commands table (command → effect)
- Dependency acquisition (package manager, vendored, fetched)
- Build artifacts (what gets produced)
- Environment-specific builds (dev, staging, prod)

---

## 7. Deployment

- Deployment strategy (containers, packages, serverless, static hosting)
- Installation / startup flow (Mermaid diagram)
- Service management (systemd, Docker Compose, k8s, PM2, etc.)
- Environment configuration

---

## 8. Key File Paths

Table of important file paths on the installed/running system.
Config files, data directories, logs, sockets, PID files, etc.

---

## 9. Namespaces / Package Structure

Table mapping logical names to components.
For Python: packages. For JS/TS: module paths. For Go: packages.
For C++: namespaces. For Java: packages.

---

## 10. Design Decisions & Conventions

Numbered list with rationale:
1. **Decision title** — explanation of why

Include coding conventions, naming patterns, architectural patterns
(MVC, hexagonal, event-driven, etc.)

---

## 11. External Integrations

### 11.1 Library Dependencies (NPM/Pip/Maven/etc)
Table: name, version, acquisition method, which component uses it.

### 11.2 External 3rd-Party Services
Table of external APIs the app talks to (e.g., Stripe, Twilio, SendGrid, Auth0).
| Service | Purpose | Auth Method | Which component calls it |

---

## 12. State Machines / State Management

For each stateful component, include ALL THREE of:

**A) Mermaid stateDiagram-v2** — visual state transitions

**B) State meaning table** — what each state represents:
| State | Meaning | Filesystem / DB / Memory |
|-------|---------|-------------------------|
| ... | ... | ... |

**C) Behavior context table** — what happens in each state:
| State | Main Loop Behaviour | User-Facing Effect |
|-------|--------------------|-----------------|
| ... | What the code does in this state | What the user/UI sees |

> ⚠️ Do NOT omit the behavior table. The state diagram shows
> transitions but the behavior table shows what each state DOES.
> Both are required for any AI agent to understand the runtime.

For React/Vue: document state management (Redux, Zustand, Pinia,
Context, etc.) with store structure and reducer/action inventory.

---

## 13. Real-Time & Event-Driven Flows

For event-driven architectures and real-time sockets:
- Topic/Queue inventory (Kafka, RabbitMQ, SQS, Redis Pub/Sub)
- Event schema/payload descriptions
- Producer/Consumer matrix (which component publishes what, who listens)
- WebSocket / Server-Sent Events (SSE) connection hubs and message types

---

## 14. API Reference

Explicitly separate the APIs into categories:

### 14.1 External (Public-Facing) APIs
- REST/GraphQL endpoints exposed to frontends or 3rd parties
- Endpoint table (method, path, auth, request, response schemas)
- Rate limiting and versioning strategy

### 14.2 Internal (Microservice-to-Microservice) APIs
- Internal gRPC, REST, or RPC calls
- Service mesh routing if applicable

### 14.3 Incoming Webhooks
- Endpoints designed to receive data from 3rd parties (e.g., Stripe webhooks)
- Signature validation / security mechanism

## 15. Cross-Cutting Concerns

Document shared infrastructure code that affects multiple components:
- Middleware / Interceptors / Guards (authentication, logging, tracing)
- Logging formatters (JSON structure, correlation IDs)
- Global exception filters mapping to HTTP codes
- Public function/class reference
- Usage examples

---

## 15. Inter-Service / Inter-Component Communication

For multi-service or multi-agent architectures:
- Communication protocols (HTTP, gRPC, WebSocket, message queue)
- Mermaid diagram showing connections
- Responsibility matrix

---

## 16. Configuration Reference

Table of all configuration options:
key, type, default, required, description.
Include env vars, config file keys, CLI flags.

---

## 17. Error Handling

- Philosophy and patterns
- Error taxonomy table (component → error type → handling)
- Retry / recovery logic
- Logging conventions

---

## 18. Security Model

> ⚠️ This section must be GRANULAR. Do NOT condense into a summary.
> Break into dedicated sub-sections for each security domain.

### 18.1 Overview Diagram
Mermaid graph showing all encrypted artifacts, key flows, and
trust boundaries. Separate "At Rest" and "In Transit" subgraphs.

### 18.2 At-Rest Encryption
For each encrypted file/artifact:
- File path
- Algorithm and key size (e.g. AES-256-GCM)
- Key derivation method (hardware-bound, env var, KMS, etc.)
- Binary format (e.g. `[IV(12)] + [Tag(16)] + [Ciphertext]`)
- Tamper detection mechanism

### 18.3 In-Transit Encryption
For each API / network channel:
- Protocol (HTTPS, mTLS, gRPC-TLS, etc.)
- Payload encryption (if any, beyond TLS)
- Key exchange mechanism
- Request/response format

### 18.4 Identity Binding / Anti-Replay
If the system binds files or tokens to specific devices/users:
- How identity is established
- How binding is enforced
- What happens on mismatch (rejection, breach state, etc.)

### 18.5 Authentication & Authorization
- Auth mechanism (JWT, OAuth, API key, session, etc.)
- Authorization model (RBAC, ABAC, middleware guards)
- Token lifecycle (issuance, refresh, revocation)

### 18.6 API Endpoints (if applicable)
Table of all API endpoints with their security characteristics:
| Endpoint | Method | Auth | Encryption | Purpose |

---

## 19. Testing Strategy

- Framework(s) used
- Test structure (unit, integration, e2e)
- How to run tests
- Key test utilities / fixtures
- Coverage requirements

---

## 20. Monitoring & Observability

- Metrics endpoints (`/metrics`, `/healthz`)
- Tracing integration (Datadog, OpenTelemetry, Jaeger)
- APM setup and key tags injected
- Alerting rules (if defined in code, e.g., Prometheus `AlertManager` rules)

---

## 21. Code Index

Complete per-file inventory of every class, function, and method in the
codebase. This is the "search index" that lets any AI agent jump
directly to the right file and line without exploring.

Group files by component/module. For each file:

### [Component Name]

#### `relative/path/to/file.ext`
| Symbol | Type | Line | Description |
|--------|------|------|-------------|
| `ClassName` | class | 10-85 | One-line purpose |
| `ClassName.method` | method | 20-45 | What it does |
| `freeFunction` | function | 90-110 | What it does |

Rules for the Code Index:
1. **Every source file** must appear (skip generated, vendor, build, node_modules)
2. **Every public symbol** must be listed — private/internal are optional
   but recommended for key files
3. **Line ranges** must be accurate (from view_file_outline)
4. **Descriptions** should be one line — enough for an agent to decide
   whether to read the full function
5. **Group by component** — mirrors the directory/module structure
6. For large projects, this section can be split into a separate
   `code_index.md` file linked from the architecture doc

> ⚠️ **ANTI-SHORTCUT RULES:**
> - Do NOT reduce the Code Index to a bullet list of file names.
>   Every file MUST have a symbol table with Type, Line, Description columns.
> - Do NOT write "Core API and state management" as the only entry for a
>   service file. List EVERY method in that service.
> - Do NOT skip files because they seem "obvious" from the directory tree.
>   The Code Index is the EXHAUSTIVE function-level map.
>
> A Code Index entry like this is WRONG:
> ```
> ### Services
> - `server.service.ts`: Core API and state management.
> - `auth.service.ts`: Authentication and user profiles.
> ```
>
> The CORRECT format is:
> ```
> ### Services
> #### `src/app/Services/server.service.ts`
> | Symbol | Type | Line | Description |
> |--------|------|------|-------------|
> | `ServerService` | class | 15-450 | Central API + state management service |
> | `ServerService.getViolations` | method | 45-62 | Fetch paginated violations for camera |
> | `ServerService.updateROI` | method | 64-85 | Update region of interest config |
> | `ServerService.getDashboardStats` | method | 87-110 | Aggregate dashboard metrics |
> | `violationSubject$` | property | 20 | BehaviorSubject for real-time violation updates |
> ```
```

---

## Quality Checklist

Before delivering, verify:

- [ ] **MANDATORY**: A Table of Contents is present immediately after the purpose block
- [ ] Every component mentioned actually exists in the codebase
- [ ] All API signatures match the actual source code
- [ ] Data models match actual schema / migration files
- [ ] **MANDATORY**: If relational DB is used, an ERD is included
- [ ] **MANDATORY**: External APIs (Stripe, etc.) are distinct from npm/pip packages
- [ ] **MANDATORY**: Caching layers and message brokers are documented if present
- [ ] Build commands are accurate (run them if possible)
- [ ] Dependency versions match manifest files
- [ ] File paths exist and are correct
- [ ] Mermaid diagrams have no syntax errors (quote labels with special characters)
- [ ] No placeholder / todo text remains (unless genuinely unknown)
- [ ] Irrelevant sections are omitted entirely
- [ ] The document is self-contained — a new agent can understand the project from this alone
- [ ] Internal cross-references are consistent (component names match throughout)

## Style Rules

1. **Tables over prose** — structured data belongs in tables
2. **Mermaid over text descriptions** — visual relationships are faster to parse
3. **Annotated trees over flat lists** — directory structure needs context
4. **Backticks everywhere** — file names, function names, config keys, CLI commands
5. **Horizontal rules** between major sections for visual separation
6. **No opinions** — document what IS, not what should be
7. **Dependency order** — document dependencies before dependents
8. **Quote Mermaid labels** — `id["Label (info)"]` not `id[Label (info)]`

## Depth Enforcement — Common Failure Modes

The following are the most common ways this skill produces shallow output.
**Actively guard against each one:**

| Failure Mode | What Goes Wrong | How to Fix |
|-------------|-----------------|------------|
| **Shallow directory tree** | Only directories shown, not files | Use `find_by_name` with extensions to list EVERY source file |
| **Prose-only components** | "ServerService handles all API calls" | Add method table: method, params, returns, description |
| **Bullet-list Code Index** | Just file names with one-line descriptions | Must be symbol tables per file with Type, Line, Description |
| **Missing implementation files** | Only headers or main files shown | Tree must list all types (`.cpp`, `.py`, `.html`, `.css`) |
| **Skipped sections** | 10+ sections omitted as "not applicable" | Only omit if genuinely N/A; most projects have 12+ applicable sections |
| **One-liner feature modules** | "Dashboard: displays metrics" | List every component, every route, every service used |
| **Missing vendored deps** | nlohmann/json, httplib not listed | Grep for non-system includes/imports |
| **No method counts** | Component listed but methods not enumerated | Use `view_file_outline` on EVERY source file |
| **Config keys incomplete** | Only 2-3 config keys listed | Read the full config file/schema and list every key |
