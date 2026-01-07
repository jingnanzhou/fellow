#!/usr/bin/env python3
"""
Merge delta knowledge with existing knowledge base for incremental updates.

This tool handles the knowledge base merge operation during incremental extraction,
combining newly extracted knowledge (delta files) with the existing knowledge base.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


def load_json(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Load and parse a JSON file.

    Args:
        file_path: Path to the JSON file

    Returns:
        Parsed JSON data, or None if file doesn't exist or can't be parsed
    """
    try:
        if not file_path.exists():
            return None
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"⚠️  Warning: Could not load {file_path.name}: {e}", file=sys.stderr)
        return None


def write_json(file_path: Path, data: Dict[str, Any]) -> None:
    """
    Write data to a JSON file with proper formatting.

    Args:
        file_path: Path where to write the JSON file
        data: Dictionary to write as JSON
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except OSError as e:
        print(f"❌ Error writing {file_path.name}: {e}", file=sys.stderr)
        sys.exit(1)


def get_changed_files_from_metadata(metadata: Dict[str, Any]) -> List[str]:
    """
    Extract the list of changed files from metadata.

    Args:
        metadata: Extraction metadata dictionary

    Returns:
        List of changed file paths
    """
    changed_files = []

    # Get from statistics
    if "changed_files" in metadata:
        changed_files = metadata["changed_files"]

    # Fallback: get from file registry with recent timestamps
    if not changed_files and "file_registry" in metadata:
        last_extraction = metadata.get("last_full_extraction", "")
        for file_path, file_info in metadata["file_registry"].items():
            if file_info.get("last_analyzed", "") > last_extraction:
                changed_files.append(file_path)

    return changed_files


def merge_factual_knowledge(
    existing: Dict[str, Any],
    delta: Dict[str, Any],
    changed_files: List[str]
) -> tuple[Dict[str, Any], Dict[str, int]]:
    """
    Merge factual knowledge (entities and relationships).

    Strategy: Remove entities from changed files, add new entities

    Args:
        existing: Existing factual knowledge
        delta: Delta factual knowledge from changed files
        changed_files: List of changed file paths

    Returns:
        Tuple of (merged factual knowledge, statistics dict)
    """
    # Convert changed files to set for faster lookup
    changed_files_set = set(changed_files)

    # Remove entities from changed files
    filtered_entities = [
        entity for entity in existing.get("entities", [])
        if entity.get("grounding", {}).get("file") not in changed_files_set
    ]

    entities_removed = len(existing.get("entities", [])) - len(filtered_entities)

    # Add newly extracted entities
    delta_entities = delta.get("entities", [])
    merged_entities = filtered_entities + delta_entities

    # Update relationships: Remove old relationships involving changed files
    existing_relationships = existing.get("entity_relationships", [])
    filtered_relationships = [
        rel for rel in existing_relationships
        if (rel.get("source_entity", {}).get("grounding", {}).get("file") not in changed_files_set and
            rel.get("target_entity", {}).get("grounding", {}).get("file") not in changed_files_set)
    ]

    # Add new relationships from delta
    delta_relationships = delta.get("entity_relationships", [])
    merged_relationships = filtered_relationships + delta_relationships

    relationships_updated = (len(existing_relationships) - len(filtered_relationships) +
                            len(delta_relationships))

    # Update metadata
    updated_metadata = existing.get("metadata", {}).copy()
    updated_metadata["last_update"] = datetime.utcnow().isoformat() + "Z"
    updated_metadata["extraction_method"] = "incremental"

    # Recalculate summary statistics
    summary = {
        "total_entities": len(merged_entities),
        "total_relationships": len(merged_relationships),
        "entity_types": {},
        "last_updated": updated_metadata["last_update"]
    }

    # Count entity types
    for entity in merged_entities:
        entity_type = entity.get("type", "unknown")
        summary["entity_types"][entity_type] = summary["entity_types"].get(entity_type, 0) + 1

    # Create merged factual knowledge
    merged = {
        "metadata": updated_metadata,
        "entities": merged_entities,
        "entity_relationships": merged_relationships,
        "summary": summary
    }

    stats = {
        "entities_removed": entities_removed,
        "entities_added": len(delta_entities),
        "relationships_updated": relationships_updated
    }

    return merged, stats


def workflow_affected_by_changed_files(workflow: Dict[str, Any], changed_files: List[str]) -> bool:
    """
    Check if a workflow is affected by changed files.

    A workflow is affected if:
    - Its entry point is in a changed file
    - Any of its steps are in changed files

    Args:
        workflow: Workflow dictionary
        changed_files: List of changed file paths

    Returns:
        True if workflow is affected, False otherwise
    """
    changed_files_set = set(changed_files)

    # Check entry point
    entry_point = workflow.get("entry_point", {})
    if entry_point.get("file") in changed_files_set:
        return True

    # Check steps
    steps = workflow.get("steps", [])
    for step in steps:
        if step.get("grounding", {}).get("file") in changed_files_set:
            return True

    return False


def merge_procedural_knowledge(
    existing: Dict[str, Any],
    delta: Dict[str, Any],
    changed_files: List[str]
) -> tuple[Dict[str, Any], Dict[str, int]]:
    """
    Merge procedural knowledge (workflows).

    Strategy: Update workflows affected by changed files

    Args:
        existing: Existing procedural knowledge
        delta: Delta procedural knowledge from changed files
        changed_files: List of changed file paths

    Returns:
        Tuple of (merged procedural knowledge, statistics dict)
    """
    # Filter out workflows affected by changed files
    existing_workflows = existing.get("workflows", [])
    filtered_workflows = [
        wf for wf in existing_workflows
        if not workflow_affected_by_changed_files(wf, changed_files)
    ]

    workflows_removed = len(existing_workflows) - len(filtered_workflows)

    # Add newly extracted/updated workflows
    delta_workflows = delta.get("workflows", [])
    merged_workflows = filtered_workflows + delta_workflows

    # Update metadata
    updated_metadata = existing.get("metadata", {}).copy()
    updated_metadata["last_update"] = datetime.utcnow().isoformat() + "Z"
    updated_metadata["extraction_method"] = "incremental"

    # Recalculate summary
    summary = {
        "total_workflows": len(merged_workflows),
        "workflow_types": {},
        "last_updated": updated_metadata["last_update"]
    }

    # Count workflow types
    for workflow in merged_workflows:
        wf_type = workflow.get("type", "unknown")
        summary["workflow_types"][wf_type] = summary["workflow_types"].get(wf_type, 0) + 1

    # Create merged procedural knowledge
    merged = {
        "metadata": updated_metadata,
        "workflows": merged_workflows,
        "summary": summary
    }

    stats = {
        "workflows_removed": workflows_removed,
        "workflows_added": len(delta_workflows),
        "workflows_updated": workflows_removed  # workflows removed were updated
    }

    return merged, stats


def merge_conceptual_knowledge(
    existing: Dict[str, Any],
    delta: Optional[Dict[str, Any]]
) -> tuple[Dict[str, Any], str]:
    """
    Merge conceptual knowledge (architecture).

    Strategy:
    - If delta exists: Use delta (architectural changes detected)
    - If no delta: Keep existing (no architectural changes)

    Args:
        existing: Existing conceptual knowledge
        delta: Delta conceptual knowledge (may be None)

    Returns:
        Tuple of (merged conceptual knowledge, status message)
    """
    if delta is not None:
        # Architectural changes detected
        updated = delta.copy()
        if "metadata" not in updated:
            updated["metadata"] = {}
        updated["metadata"]["update_type"] = "architectural_change"
        updated["metadata"]["last_update"] = datetime.utcnow().isoformat() + "Z"
        status = "Architectural changes detected"
    else:
        # No architectural changes
        updated = existing.copy()
        if "metadata" not in updated:
            updated["metadata"] = {}
        updated["metadata"]["update_type"] = "no_change"
        updated["metadata"]["last_update"] = datetime.utcnow().isoformat() + "Z"
        status = "No architectural changes"

    return updated, status


def merge_knowledge_bases(kb_dir: Path, changed_files: List[str]) -> Dict[str, Any]:
    """
    Perform the full knowledge base merge operation.

    Args:
        kb_dir: Path to the knowledge base directory (.fellow-data/semantic/)
        changed_files: List of changed file paths

    Returns:
        Dictionary with merge statistics
    """
    print("📦 Loading existing knowledge base...")

    # Load existing knowledge base
    existing_factual = load_json(kb_dir / "factual_knowledge.json")
    existing_procedural = load_json(kb_dir / "procedural_knowledge.json")
    existing_conceptual = load_json(kb_dir / "conceptual_knowledge.json")

    if not all([existing_factual, existing_procedural, existing_conceptual]):
        print("❌ Error: Could not load existing knowledge base", file=sys.stderr)
        print("   Required files:", file=sys.stderr)
        print("   - factual_knowledge.json", file=sys.stderr)
        print("   - procedural_knowledge.json", file=sys.stderr)
        print("   - conceptual_knowledge.json", file=sys.stderr)
        sys.exit(1)

    print("📦 Loading delta knowledge...")

    # Load delta knowledge
    delta_factual = load_json(kb_dir / "factual_knowledge_delta.json")
    delta_procedural = load_json(kb_dir / "procedural_knowledge_delta.json")
    delta_conceptual = load_json(kb_dir / "conceptual_knowledge_delta.json")

    if not delta_factual or not delta_procedural:
        print("❌ Error: Could not load delta knowledge files", file=sys.stderr)
        print("   Required files:", file=sys.stderr)
        print("   - factual_knowledge_delta.json", file=sys.stderr)
        print("   - procedural_knowledge_delta.json", file=sys.stderr)
        sys.exit(1)

    print(f"🔄 Merging knowledge for {len(changed_files)} changed files...")

    # Merge factual knowledge
    merged_factual, factual_stats = merge_factual_knowledge(
        existing_factual, delta_factual, changed_files
    )

    # Merge procedural knowledge
    merged_procedural, procedural_stats = merge_procedural_knowledge(
        existing_procedural, delta_procedural, changed_files
    )

    # Merge conceptual knowledge
    merged_conceptual, conceptual_status = merge_conceptual_knowledge(
        existing_conceptual, delta_conceptual
    )

    print("💾 Writing merged knowledge base...")

    # Write merged knowledge base
    write_json(kb_dir / "factual_knowledge.json", merged_factual)
    write_json(kb_dir / "procedural_knowledge.json", merged_procedural)
    write_json(kb_dir / "conceptual_knowledge.json", merged_conceptual)

    print("🧹 Cleaning up delta files...")

    # Clean up delta files
    for delta_file in ["factual_knowledge_delta.json",
                       "procedural_knowledge_delta.json",
                       "conceptual_knowledge_delta.json"]:
        delta_path = kb_dir / delta_file
        if delta_path.exists():
            delta_path.unlink()

    # Return merge statistics
    return {
        "factual": factual_stats,
        "procedural": procedural_stats,
        "conceptual": {"status": conceptual_status}
    }


def print_merge_statistics(stats: Dict[str, Any]) -> None:
    """
    Print merge statistics in a user-friendly format.

    Args:
        stats: Merge statistics dictionary
    """
    print()
    print("✅ Knowledge Base Updated (Incremental)")
    print()
    print("📊 Merge Statistics:")
    print()

    # Factual knowledge stats
    factual = stats.get("factual", {})
    print("  Factual Knowledge:")
    print(f"    • Entities removed: {factual.get('entities_removed', 0)} (from changed files)")
    print(f"    • Entities added: {factual.get('entities_added', 0)} (new extraction)")
    print(f"    • Relationships updated: {factual.get('relationships_updated', 0)}")
    print()

    # Procedural knowledge stats
    procedural = stats.get("procedural", {})
    print("  Procedural Knowledge:")
    print(f"    • Workflows updated: {procedural.get('workflows_updated', 0)}")
    print(f"    • Workflows added: {procedural.get('workflows_added', 0)}")
    print()

    # Conceptual knowledge stats
    conceptual = stats.get("conceptual", {})
    print("  Conceptual Knowledge:")
    print(f"    • Status: {conceptual.get('status', 'Unknown')}")
    print()


def main():
    """Main entry point for the merge-knowledge tool."""
    if len(sys.argv) < 2:
        print("Usage: merge_knowledge.py <target-project-path>", file=sys.stderr)
        print("", file=sys.stderr)
        print("Merges delta knowledge with existing knowledge base for incremental updates.", file=sys.stderr)
        sys.exit(1)

    # Get target project path
    target_path = Path(sys.argv[1]).resolve()

    if not target_path.exists():
        print(f"❌ Error: Target project path does not exist: {target_path}", file=sys.stderr)
        sys.exit(1)

    if not target_path.is_dir():
        print(f"❌ Error: Target project path is not a directory: {target_path}", file=sys.stderr)
        sys.exit(1)

    # Get knowledge base directory
    kb_dir = target_path / ".fellow-data" / "semantic"

    if not kb_dir.exists():
        print(f"❌ Error: Knowledge base directory does not exist: {kb_dir}", file=sys.stderr)
        print("   Run /fellow:build-kb first to create the knowledge base.", file=sys.stderr)
        sys.exit(1)

    # Load metadata to get changed files
    metadata_path = kb_dir / "extraction_metadata.json"
    metadata = load_json(metadata_path)

    if not metadata:
        print(f"❌ Error: Could not load extraction metadata: {metadata_path}", file=sys.stderr)
        sys.exit(1)

    # Get changed files from metadata
    changed_files = get_changed_files_from_metadata(metadata)

    if not changed_files:
        print("⚠️  Warning: No changed files found in metadata", file=sys.stderr)
        print("   Proceeding with merge anyway...", file=sys.stderr)

    # Perform merge
    try:
        stats = merge_knowledge_bases(kb_dir, changed_files)
        print_merge_statistics(stats)
        print(f"📁 Knowledge base location: {kb_dir}")
        print()
    except Exception as e:
        print(f"❌ Error during knowledge base merge: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
