---
description: Intercept coding requests and enrich with semantic knowledge from the knowledge base
argument-hint: Coding request or task description
---

# Fellow - Context-Enriched Coding

Execute coding requests with intelligent context from the semantic knowledge base. Automatically retrieves relevant entities, workflows, patterns, and constraints to ensure architecture-consistent implementations.

## Objective

Transform a user's coding request into a context-enriched task by:
1. Analyzing the user's intent
2. Loading semantic knowledge from `.fellow-data/semantic/`
3. Retrieving relevant entities, workflows, and patterns
4. Extracting applicable architectural constraints and guardrails
5. Executing the coding task with full architectural awareness

---

## Arguments

- **$ARGUMENTS** (required): The coding request or task description
  - Examples:
    - "Add user authentication endpoint"
    - "Implement caching for the API"
    - "Refactor the payment processing module"
    - "Add validation to the user registration"

---

## Core Principles

- **Knowledge-Driven**: All suggestions grounded in the actual codebase architecture
- **Constraint-Aware**: Enforce architectural boundaries and design decisions
- **Pattern-Consistent**: Follow established patterns from the knowledge base
- **Non-Invasive**: Only suggest changes that align with existing architecture

---

## Execution Workflow

### Phase 0: Initialize Logging

**Goal**: Set up logging for this enrichment session

**Actions**:
1. Create a Python script to initialize logging:
   ```python
   import sys
   sys.path.insert(0, './hooks')
   from logger import get_logger

   logger = get_logger()
   # Store logger for use in final phase
   ```

2. Store the original user request for logging later

**Note**: Logging is enabled if `logging_enabled: true` in `.claude-plugin/hooks.json` or if `FELLOW_LOGGING` environment variable is set.

---

### Phase 1: Knowledge Base Loading

**Goal**: Load and validate the semantic knowledge base, auto-building if necessary

**Actions**:
1. Check if knowledge base exists at `.fellow-data/semantic/`

2. **If NOT found** (first time use):
   - Output informative message **to the conversation** (so it appears in chat):
     ```
     ⚠️  **Fellow Knowledge Base Not Found**

     This appears to be the first time using Fellow on this project.
     To enable context enrichment, Fellow needs to extract semantic knowledge
     from your codebase.

     **This will take 2-5 minutes** (one-time process).

     I can build the knowledge base now and then proceed with your request.

     Would you like me to build it?
     ```

   - **Important**: This message must appear in the chat interface, not just logs
   - The message is part of your response to the user
   - Wait for user confirmation before proceeding

3. **If user agrees to build**:
   - Execute the `/build-kb` command automatically:
     ```
     🔨 Building knowledge base for this project...

     [Launch /build-kb command]

     ✓ Knowledge base built successfully!

     Proceeding with your original request: "{user's request}"
     ```

4. **If user declines**:
   - Display message:
     ```
     ℹ️  Knowledge base build cancelled.

     To use Fellow later:
     1. Run `/build-kb` to extract knowledge (2-5 minutes)
     2. Then use `/fellow` or enable automatic enrichment

     Your request will proceed without enrichment.
     ```
   - Exit and pass through the original request unchanged

5. **If KB found** - Proceed with loading:
   - Load all knowledge files:
     - `factual_knowledge.json` - Entities and relationships
     - `procedural_knowledge.json` - Workflows and execution flows
     - `conceptual_knowledge.json` - Architecture and design patterns

6. **Validate loaded knowledge**:
   - Check metadata for completeness
   - Ensure all required sections present
   - Report any issues found

**Error Handling**:
- Corrupted files: "Knowledge base appears corrupted. Please re-run `/build-kb` to regenerate."
- Invalid format: "Knowledge base format is invalid. Please re-run `/build-kb`."
- Empty KB: "Knowledge base is empty. Project may not have recognizable code patterns."

---

### Phase 2: Intent Analysis

**Goal**: Understand what the user wants to accomplish

**Actions**:
1. Parse the user's request ($ARGUMENTS)

2. Identify the primary intent category:
   - **Create**: Add new functionality (endpoints, modules, classes, functions)
   - **Modify**: Change existing functionality (refactor, optimize, enhance)
   - **Fix**: Repair bugs or issues
   - **Validate**: Add validation or constraints
   - **Test**: Add or modify tests
   - **Document**: Add or update documentation

3. Extract key components from the request:
   - **Target entities**: Which entities are involved? (e.g., "User", "AuthService")
   - **Target workflows**: Which workflows are affected? (e.g., "authentication flow")
   - **Target patterns**: Which patterns should be used? (e.g., "Repository Pattern")
   - **Keywords**: Important technical terms (e.g., "caching", "validation", "async")

4. Determine scope:
   - **Single file**: Changes isolated to one file
   - **Single module**: Changes within one module
   - **Cross-module**: Changes span multiple modules
   - **Architectural**: Changes affect overall architecture

**Output**: Structured intent analysis with category, components, and scope

---

### Phase 3: Knowledge Retrieval

**Goal**: Retrieve relevant knowledge from the KB based on intent

**Actions**:

#### 3.1 Retrieve Relevant Entities (from factual_knowledge.json)

1. Search for entities mentioned in the request:
   - By exact name match
   - By keyword match in purpose/description
   - By category match

2. For each matched entity, extract:
   - Entity definition (type, purpose, attributes, methods)
   - Relationships to other entities
   - Business rules and invariants
   - Source location (file and line numbers)

3. Retrieve related entities:
   - Dependencies (entities this depends on)
   - Dependents (entities that depend on this)
   - One hop away in relationship graph

#### 3.2 Retrieve Relevant Workflows (from procedural_knowledge.json)

1. Search for workflows related to the request:
   - By name match
   - By keyword match in purpose/description
   - By entry point or steps containing target entities

2. For each matched workflow, extract:
   - Workflow steps with file locations
   - Data flow and transformations
   - Control flow and conditions
   - Error handling patterns
   - Design patterns used

#### 3.3 Retrieve Relevant Patterns and Decisions (from conceptual_knowledge.json)

1. Identify applicable design patterns:
   - Patterns already used in target modules
   - Patterns recommended for the intent type
   - Patterns mentioned in the request

2. Extract relevant design decisions:
   - Decisions affecting target modules
   - Decisions related to the intent category
   - Rationale and trade-offs

3. Extract architectural layers:
   - Which layer does this change belong to?
   - What are the layer dependencies?
   - What are the layer constraints?

#### 3.4 Extract Applicable Constraints (from conceptual_knowledge.json)

1. Identify constraints that apply to this request:
   - **Security constraints**: If request involves auth, data access, API endpoints
   - **Performance constraints**: If request involves caching, database, HTTP
   - **Resource management**: If request involves connections, streams, cleanup
   - **Data validation**: If request involves user input, API parameters
   - **Configuration**: If request involves settings, environment
   - **Architectural**: Always apply
   - **API Integration**: If request involves external APIs

2. For each applicable constraint, extract:
   - Constraint description
   - Rationale
   - Enforcement mechanism
   - Violation consequences

**Output**: Structured knowledge package with entities, workflows, patterns, and constraints

---

### Phase 4: Guardrail Generation

**Goal**: Generate specific coding guardrails based on retrieved knowledge

**Actions**:

1. **Architectural Guardrails**:
   - Layer boundaries to respect
   - Dependencies allowed/forbidden
   - Module boundaries to maintain

2. **Pattern Guardrails**:
   - Design patterns to follow
   - Existing patterns to maintain consistency with
   - Anti-patterns to avoid

3. **Constraint Guardrails**:
   - Security requirements (auth, validation, sanitization)
   - Performance requirements (caching, connection pooling)
   - Resource management requirements (cleanup, lifecycle)
   - Data validation requirements (schema, types, bounds)

4. **Consistency Guardrails**:
   - Naming conventions from existing entities
   - Code structure patterns from existing modules
   - Error handling patterns from existing workflows

**Output**: Structured guardrails organized by category

---

### Phase 5: Context Enrichment

**Goal**: Create enriched context for the coding task

**Actions**:

1. **Build Context Document** with the following sections:

   **A. Task Summary**
   - Original request
   - Intent analysis (category, scope, components)
   - Affected entities and workflows

   **B. Relevant Entities**
   - List of entities with:
     - Name, type, purpose
     - Key attributes and methods
     - Relationships
     - Source location (for reference)

   **C. Relevant Workflows**
   - List of workflows with:
     - Name, type, purpose
     - Entry points
     - Key steps
     - Patterns used

   **D. Applicable Design Patterns**
   - List of patterns with:
     - Pattern name
     - Current usage in codebase
     - How to apply to this task

   **E. Architectural Context**
   - Target layer
   - Layer dependencies and constraints
   - Module boundaries

   **F. Coding Guardrails**
   - MUST follow (critical constraints)
   - SHOULD follow (recommended practices)
   - MUST NOT do (violations)

   **G. Related Design Decisions**
   - Decisions affecting this task
   - Rationale and trade-offs

2. **Format Context** for clarity:
   - Use markdown formatting
   - Include code locations as references
   - Highlight critical constraints
   - Group related items

**Output**: Complete enriched context document

---

### Phase 6: Task Execution

**Goal**: Execute the coding task with full context

**Actions**:

1. **Present Context to User** (summary):
   ```
   📋 Context Loaded from Knowledge Base

   Relevant Entities: X entities found
   Relevant Workflows: Y workflows found
   Applicable Constraints: Z constraints apply
   Design Patterns: P patterns to follow

   Key Guardrails:
   - [List 3-5 most critical guardrails]
   ```

2. **Execute with Context**:
   - Use TodoWrite to plan the implementation
   - Keep context in mind while coding
   - Reference specific entities, workflows, patterns from KB
   - Enforce guardrails throughout implementation
   - Verify against constraints before completion

3. **Validation**:
   - Check implementation against guardrails
   - Verify architectural boundaries respected
   - Ensure patterns followed consistently
   - Confirm constraints satisfied

4. **Completion Report**:
   ```
   ✓ Task completed with architectural awareness

   Implementation Details:
   - Entities modified: [list]
   - Patterns applied: [list]
   - Constraints verified: [list]
   - Files changed: [list]
   ```

---

### Phase 7: Log Enrichment Results

**Goal**: Log the enrichment event for analysis and debugging

**Actions**:
1. Create a logging script using the Fellow logger:
   ```python
   import sys
   import os
   sys.path.insert(0, './hooks')
   from logger import get_logger

   logger = get_logger()

   # Log the enrichment event
   logger.log_enrichment_event(
       original_prompt="$ARGUMENTS",
       is_coding_request=True,
       intent="[detected intent category]",
       confidence=1.0,  # Manual command = 100% confidence
       kb_found=True,
       kb_path=".fellow-data/semantic/",
       entities_found=[count of entities retrieved],
       workflows_found=[count of workflows retrieved],
       constraints_found=[count of constraints applied],
       enriched_prompt="[full enriched context that was used]",
       source="command"
   )
   ```

2. Store logs in `.fellow-data/logs/` (or Fellow plugin logs if project logs unavailable)

3. Log files created:
   - `enrichment_YYYY-MM-DD.jsonl` - Machine-readable JSON logs
   - `enrichment_YYYY-MM-DD.log` - Human-readable logs with full context

**Note**: Logging is enabled if `logging_enabled: true` in `.claude-plugin/hooks.json` or if `FELLOW_LOGGING=1` environment variable is set.

---

## Knowledge Base Structure Reference

The command expects knowledge base files in this structure:

```
.fellow-data/semantic/
├── factual_knowledge.json
│   ├── metadata
│   ├── entities[]
│   │   ├── name, type, category, purpose
│   │   ├── attributes[], methods[]
│   │   ├── relationships[]
│   │   ├── invariants[], business_rules[]
│   │   └── grounding (file, line_start, line_end)
│   └── entity_relationships[]
│
├── procedural_knowledge.json
│   ├── metadata
│   └── workflows[]
│       ├── name, type, purpose
│       ├── entry_point (file, line, function)
│       ├── steps[] (with file/line references)
│       ├── data_flow, control_flow
│       ├── error_handling
│       └── pattern
│
└── conceptual_knowledge.json
    ├── metadata
    ├── architecture_style
    ├── layers[]
    │   ├── name, responsibility
    │   ├── components, dependencies
    │   └── constraints
    ├── modules[]
    │   ├── name, path, responsibility
    │   ├── patterns_used[], dependencies[]
    │   └── complexity
    ├── design_patterns[]
    │   ├── pattern, usage, locations
    │   ├── rationale, benefits, trade_offs
    │   └── examples[]
    ├── design_decisions[]
    │   ├── decision, rationale
    │   ├── alternatives_considered[]
    │   ├── trade_offs, impact
    │   └── evidence_location
    └── constraints[]
        ├── type, constraint
        ├── rationale, enforcement
        └── violations
```

---

## Usage Examples

### Example 1: Add New Endpoint

```bash
/fellow Add a POST endpoint for user registration with email and password
```

**Context Retrieved**:
- **Entities**: User, AuthService, ValidationService
- **Workflows**: User authentication workflow
- **Patterns**: Repository Pattern, Service Layer Pattern
- **Constraints**: Security (password hashing), validation (email format), error handling

**Guardrails Applied**:
- MUST hash passwords before storage
- MUST validate email format
- MUST use existing AuthService pattern
- MUST follow API layer conventions
- MUST NOT access database directly from endpoint

---

### Example 2: Refactor Module

```bash
/fellow Refactor the payment processing to use the Strategy pattern
```

**Context Retrieved**:
- **Entities**: PaymentProcessor, PaymentMethod classes
- **Workflows**: Payment processing workflow
- **Patterns**: Strategy Pattern (definition and usage), Factory Pattern
- **Constraints**: Transaction consistency, error handling, logging

**Guardrails Applied**:
- MUST maintain transaction consistency
- MUST preserve existing interface contracts
- SHOULD use Factory Pattern for strategy instantiation
- MUST maintain error handling patterns
- MUST NOT change external API contracts

---

### Example 3: Add Caching

```bash
/fellow Add caching to the tool listing API with 60-second TTL
```

**Context Retrieved**:
- **Entities**: ToolService, HttpClientService
- **Workflows**: Tool list retrieval workflow
- **Patterns**: Cache-Aside Pattern (existing usage example)
- **Constraints**: Performance (caching strategy), Resource management (cache cleanup)

**Guardrails Applied**:
- SHOULD follow existing Cache-Aside Pattern in ToolService
- MUST implement cache expiration (TTL)
- MUST handle cache misses gracefully
- SHOULD add cache statistics tracking
- MUST consider thread-safety for cache access

---

## Error Handling

### Missing Knowledge Base
```
❌ Knowledge base not found

The semantic knowledge base is required for context-enriched coding.

To create the knowledge base, run:
  /build-kb

This will analyze the codebase and extract:
- Entities and relationships
- Workflows and patterns
- Architecture and constraints
```

### Corrupted Knowledge Base
```
❌ Knowledge base corrupted or incomplete

File: .fellow-data/semantic/[file].json
Issue: [description]

To regenerate the knowledge base, run:
  /build-kb
```

### No Relevant Knowledge Found
```
⚠️  Limited context available

No directly relevant entities or workflows found in the knowledge base.

Proceeding with general architectural guidance:
- Architecture style: [from KB]
- Design principles: [from KB]
- General constraints: [from KB]
```

---

## Implementation Notes

### Knowledge Retrieval Strategy

**Entity Matching**:
1. Exact name match (case-insensitive)
2. Keyword match in purpose/description
3. Category/type match
4. Relationship graph traversal

**Workflow Matching**:
1. Name/purpose keyword match
2. Entry point entity match
3. Step entity match
4. Pattern match

**Constraint Filtering**:
1. Type-based (security, performance, etc.)
2. Keyword-based (if request mentions specific concerns)
3. Layer-based (based on target layer)
4. Always include architectural constraints

### Context Presentation

**Priority Levels**:
- **Critical**: Security, data integrity, breaking changes
- **Important**: Performance, architectural boundaries, patterns
- **Recommended**: Conventions, best practices, consistency

**Formatting**:
- Use clear section headers
- Include code references (file:line)
- Highlight MUST vs SHOULD vs MAY
- Keep guardrails actionable and specific

---

## Notes

- **First Run**: Requires `/build-kb` to be run first
- **KB Updates**: If codebase changes significantly, re-run `/build-kb`
- **Context Size**: May be large for complex requests - focus on most relevant items
- **Extensibility**: Can be enhanced with additional knowledge types in future
