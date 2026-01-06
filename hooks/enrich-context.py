#!/usr/bin/env python3
"""
Fellow Context Enrichment Hook

Automatically enriches coding requests with semantic knowledge from the knowledge base.

This script:
1. Analyzes user prompts to detect coding requests
2. Loads semantic knowledge from .fellow-data/semantic/
3. Retrieves relevant entities, workflows, patterns, and constraints
4. Generates enriched context with architectural guardrails
5. Outputs enriched prompt for Claude to process

Hook Type: user-prompt-submit
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Import logger
try:
    from logger import get_logger
except ImportError:
    # Fallback if logger not available
    class DummyLogger:
        def log_enrichment_event(self, *args, **kwargs):
            pass
        def log_error(self, *args, **kwargs):
            pass
    def get_logger():
        return DummyLogger()


# Coding request detection patterns
CODING_KEYWORDS = {
    'create': ['add', 'create', 'implement', 'build', 'write', 'generate', 'make'],
    'modify': ['update', 'modify', 'change', 'enhance', 'improve', 'optimize', 'refactor'],
    'fix': ['fix', 'repair', 'debug', 'resolve', 'correct'],
    'delete': ['delete', 'remove', 'clean up', 'eliminate'],
    'test': ['test', 'validate', 'verify', 'check'],
}

CODE_ENTITIES = [
    'endpoint', 'api', 'route', 'handler', 'function', 'method', 'class',
    'service', 'component', 'module', 'interface', 'model', 'entity',
    'controller', 'middleware', 'utility', 'helper', 'decorator', 'hook'
]


def detect_coding_request(prompt: str) -> Tuple[bool, str, float]:
    """
    Detect if a prompt is a coding request.

    Returns:
        (is_coding_request, intent_category, confidence)
    """
    prompt_lower = prompt.lower()

    # Check for coding keywords
    intent_category = None
    keyword_found = False

    for category, keywords in CODING_KEYWORDS.items():
        if any(keyword in prompt_lower for keyword in keywords):
            intent_category = category
            keyword_found = True
            break

    # Check for code entity mentions
    entity_found = any(entity in prompt_lower for entity in CODE_ENTITIES)

    # Check for imperative mood (commands)
    imperative_patterns = [
        r'^(add|create|implement|build|write|update|modify|fix|refactor|delete|remove)',
        r'^(can you|could you|please|would you).*(add|create|implement|update|fix)',
    ]
    imperative_found = any(re.search(pattern, prompt_lower) for pattern in imperative_patterns)

    # Calculate confidence
    confidence = 0.0
    if keyword_found:
        confidence += 0.4
    if entity_found:
        confidence += 0.3
    if imperative_found:
        confidence += 0.3

    is_coding_request = confidence >= 0.5

    if not intent_category and is_coding_request:
        intent_category = 'create'  # Default

    return is_coding_request, intent_category or 'unknown', confidence


def find_knowledge_base(start_dir: Optional[Path] = None) -> Optional[Path]:
    """
    Find the knowledge base directory.

    Searches upward from start_dir for .fellow-data/semantic/
    """
    if start_dir is None:
        start_dir = Path.cwd()

    current = start_dir
    for _ in range(10):  # Search up to 10 levels
        kb_dir = current / '.fellow-data' / 'semantic'
        if kb_dir.exists() and kb_dir.is_dir():
            return kb_dir
        if current.parent == current:  # Reached root
            break
        current = current.parent

    return None


def load_knowledge_base(kb_dir: Path) -> Optional[Dict[str, Any]]:
    """Load all knowledge base files."""
    try:
        kb = {}

        factual_file = kb_dir / 'factual_knowledge.json'
        if factual_file.exists():
            with open(factual_file, 'r') as f:
                kb['factual'] = json.load(f)

        procedural_file = kb_dir / 'procedural_knowledge.json'
        if procedural_file.exists():
            with open(procedural_file, 'r') as f:
                kb['procedural'] = json.load(f)

        conceptual_file = kb_dir / 'conceptual_knowledge.json'
        if conceptual_file.exists():
            with open(conceptual_file, 'r') as f:
                kb['conceptual'] = json.load(f)

        if not kb:
            return None

        return kb

    except Exception as e:
        print(f"Warning: Failed to load knowledge base: {e}", file=sys.stderr)
        return None


def extract_relevant_entities(prompt: str, kb: Dict[str, Any], max_entities: int = 5) -> List[Dict]:
    """Extract entities relevant to the prompt."""
    if 'factual' not in kb or 'entities' not in kb['factual']:
        return []

    entities = kb['factual']['entities']
    prompt_lower = prompt.lower()

    # Score entities by relevance
    scored_entities = []
    for entity in entities:
        score = 0

        # Exact name match
        if entity.get('name', '').lower() in prompt_lower:
            score += 10

        # Purpose match (keywords)
        purpose = entity.get('purpose', '').lower()
        purpose_words = set(purpose.split())
        prompt_words = set(prompt_lower.split())
        common_words = purpose_words & prompt_words
        score += len(common_words) * 2

        # Category match
        category = entity.get('category', '')
        if 'auth' in prompt_lower and 'auth' in entity.get('name', '').lower():
            score += 5
        if 'service' in prompt_lower and category == 'technical_entity':
            score += 3

        if score > 0:
            scored_entities.append((score, entity))

    # Sort by score and return top N
    scored_entities.sort(reverse=True, key=lambda x: x[0])
    return [entity for score, entity in scored_entities[:max_entities]]


def extract_relevant_workflows(prompt: str, kb: Dict[str, Any], max_workflows: int = 3) -> List[Dict]:
    """Extract workflows relevant to the prompt."""
    if 'procedural' not in kb or 'workflows' not in kb['procedural']:
        return []

    workflows = kb['procedural']['workflows']
    prompt_lower = prompt.lower()

    # Score workflows by relevance
    scored_workflows = []
    for workflow in workflows:
        score = 0

        # Name match
        if workflow.get('name', '').lower().replace('_', ' ') in prompt_lower:
            score += 10

        # Purpose/description match
        purpose = workflow.get('purpose', '').lower()
        if any(word in purpose for word in prompt_lower.split()):
            score += 5

        # Type match
        workflow_type = workflow.get('type', '')
        if 'endpoint' in prompt_lower and workflow_type == 'request_handler':
            score += 5

        if score > 0:
            scored_workflows.append((score, workflow))

    scored_workflows.sort(reverse=True, key=lambda x: x[0])
    return [workflow for score, workflow in scored_workflows[:max_workflows]]


def extract_applicable_constraints(intent: str, kb: Dict[str, Any]) -> List[Dict]:
    """Extract architectural constraints applicable to the intent."""
    if 'conceptual' not in kb or 'constraints' not in kb['conceptual']:
        return []

    constraints = kb['conceptual']['constraints']

    # Filter by intent type
    applicable = []
    for constraint in constraints:
        constraint_type = constraint.get('type', '').lower()

        # Security constraints always apply
        if constraint_type == 'security':
            applicable.append(constraint)

        # Architectural constraints always apply
        elif constraint_type == 'architectural':
            applicable.append(constraint)

        # Performance constraints for optimization/refactoring
        elif constraint_type == 'performance' and intent in ['modify', 'create']:
            applicable.append(constraint)

        # Data validation for create/modify
        elif constraint_type == 'data validation' and intent in ['create', 'modify']:
            applicable.append(constraint)

    return applicable[:10]  # Limit to 10 most relevant


def generate_enriched_context(
    prompt: str,
    intent: str,
    entities: List[Dict],
    workflows: List[Dict],
    constraints: List[Dict],
    kb: Dict[str, Any]
) -> str:
    """Generate enriched context to prepend to the user's prompt."""

    context_parts = []

    context_parts.append("📋 **Context from Knowledge Base**")
    context_parts.append("")

    # Relevant Entities
    if entities:
        context_parts.append("**Relevant Entities:**")
        for entity in entities:
            name = entity.get('name', 'Unknown')
            purpose = entity.get('purpose', 'No description')
            entity_type = entity.get('type', 'unknown')
            grounding = entity.get('grounding', {})
            file_path = grounding.get('file', 'unknown')

            context_parts.append(f"- **{name}** ({entity_type}): {purpose}")
            context_parts.append(f"  Location: `{file_path}`")

        context_parts.append("")

    # Relevant Workflows
    if workflows:
        context_parts.append("**Relevant Workflows:**")
        for workflow in workflows:
            name = workflow.get('name', 'Unknown')
            purpose = workflow.get('purpose', 'No description')
            entry_point = workflow.get('entry_point', {})
            entry_file = entry_point.get('file', 'unknown')

            context_parts.append(f"- **{name}**: {purpose}")
            context_parts.append(f"  Entry: `{entry_file}`")

        context_parts.append("")

    # Applicable Constraints
    if constraints:
        context_parts.append("**Architectural Guardrails (MUST follow):**")
        for constraint in constraints[:5]:  # Top 5
            constraint_type = constraint.get('type', 'Unknown')
            constraint_text = constraint.get('constraint', 'No description')
            rationale = constraint.get('rationale', '')

            context_parts.append(f"- [{constraint_type}] {constraint_text}")
            if rationale:
                context_parts.append(f"  Rationale: {rationale}")

        context_parts.append("")

    # Architecture Style
    if 'conceptual' in kb and 'architecture_style' in kb['conceptual']:
        arch_style = kb['conceptual']['architecture_style']
        style_name = arch_style.get('primary_style', 'Unknown')
        context_parts.append(f"**Architecture Style:** {style_name}")
        context_parts.append("")

    # Design Patterns
    if 'conceptual' in kb and 'design_patterns' in kb['conceptual']:
        patterns = kb['conceptual']['design_patterns']
        if patterns:
            pattern_names = [p.get('pattern', '') for p in patterns[:3]]
            context_parts.append(f"**Design Patterns in Use:** {', '.join(pattern_names)}")
            context_parts.append("")

    context_parts.append("---")
    context_parts.append("")
    context_parts.append("**User Request:**")
    context_parts.append(prompt)

    return '\n'.join(context_parts)


def main():
    """Main entry point for the hook."""

    # Initialize logger
    logger = get_logger()

    # Get user prompt from command line or stdin
    if len(sys.argv) > 1:
        user_prompt = ' '.join(sys.argv[1:])
    else:
        user_prompt = sys.stdin.read().strip()

    if not user_prompt:
        print("No prompt provided", file=sys.stderr)
        sys.exit(1)

    # Step 1: Detect if it's a coding request
    is_coding, intent, confidence = detect_coding_request(user_prompt)

    if not is_coding:
        # Not a coding request - pass through unchanged
        logger.log_enrichment_event(
            original_prompt=user_prompt,
            is_coding_request=False,
            intent=intent,
            confidence=confidence,
            kb_found=False,
            kb_path=None,
            entities_found=0,
            workflows_found=0,
            constraints_found=0,
            enriched_prompt=user_prompt,
            source="hook"
        )
        print(user_prompt)
        sys.exit(0)

    # Step 2: Find knowledge base
    kb_dir = find_knowledge_base()
    if not kb_dir:
        # No KB found - prepend warning message to prompt so it appears in chat
        warning_message = """⚠️  **Fellow Knowledge Base Not Found**

Fellow detected a coding request but couldn't find a knowledge base for this project.

**To enable context enrichment:**
1. Build the knowledge base: `/build-kb`
   (Takes 2-5 minutes for first extraction)

**Or continue without enrichment:**
Your request will proceed without Fellow's architectural context.

---

**Original Request:**
"""

        # Log the event
        logger.log_enrichment_event(
            original_prompt=user_prompt,
            is_coding_request=True,
            intent=intent,
            confidence=confidence,
            kb_found=False,
            kb_path=None,
            entities_found=0,
            workflows_found=0,
            constraints_found=0,
            enriched_prompt=user_prompt,
            source="hook"
        )

        # Output warning + original prompt to stdout (appears in chat)
        print(warning_message + user_prompt)
        sys.exit(0)

    # Step 3: Load knowledge base
    kb = load_knowledge_base(kb_dir)
    if not kb:
        # KB invalid or empty - pass through unchanged
        logger.log_enrichment_event(
            original_prompt=user_prompt,
            is_coding_request=True,
            intent=intent,
            confidence=confidence,
            kb_found=True,
            kb_path=str(kb_dir),
            entities_found=0,
            workflows_found=0,
            constraints_found=0,
            enriched_prompt=user_prompt,
            source="hook"
        )
        print(user_prompt)
        sys.exit(0)

    # Step 4: Extract relevant knowledge
    entities = extract_relevant_entities(user_prompt, kb)
    workflows = extract_relevant_workflows(user_prompt, kb)
    constraints = extract_applicable_constraints(intent, kb)

    # If no relevant knowledge found, pass through
    if not entities and not workflows and not constraints:
        logger.log_enrichment_event(
            original_prompt=user_prompt,
            is_coding_request=True,
            intent=intent,
            confidence=confidence,
            kb_found=True,
            kb_path=str(kb_dir),
            entities_found=0,
            workflows_found=0,
            constraints_found=0,
            enriched_prompt=user_prompt,
            source="hook"
        )
        print(user_prompt)
        sys.exit(0)

    # Step 5: Generate enriched context
    enriched_prompt = generate_enriched_context(
        user_prompt,
        intent,
        entities,
        workflows,
        constraints,
        kb
    )

    # Log enrichment event
    logger.log_enrichment_event(
        original_prompt=user_prompt,
        is_coding_request=True,
        intent=intent,
        confidence=confidence,
        kb_found=True,
        kb_path=str(kb_dir),
        entities_found=len(entities),
        workflows_found=len(workflows),
        constraints_found=len(constraints),
        enriched_prompt=enriched_prompt,
        source="hook"
    )

    # Output enriched prompt
    print(enriched_prompt)


if __name__ == '__main__':
    main()
