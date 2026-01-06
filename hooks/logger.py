#!/usr/bin/env python3
"""
Fellow Logging Utility

Logs enrichment events for debugging and analysis.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class FellowLogger:
    """Logger for Fellow enrichment events."""

    def __init__(self, log_dir: Optional[Path] = None):
        """
        Initialize logger.

        Args:
            log_dir: Directory to store logs. If None, searches for .fellow-data/logs/
        """
        if log_dir is None:
            log_dir = self._find_log_dir()

        self.log_dir = log_dir
        self.enabled = self._check_if_enabled()

        if self.enabled and self.log_dir:
            self.log_dir.mkdir(parents=True, exist_ok=True)

    def _find_log_dir(self) -> Optional[Path]:
        """Find or create log directory."""
        # Search upward for .fellow-data/
        current = Path.cwd()
        for _ in range(10):
            fellow_data = current / '.fellow-data'
            if fellow_data.exists() and fellow_data.is_dir():
                return fellow_data / 'logs'
            if current.parent == current:  # Reached root
                break
            current = current.parent

        # Fallback: Use Fellow plugin directory
        try:
            script_dir = Path(__file__).parent.parent
            return script_dir / '.fellow-data' / 'logs'
        except:
            return None

    def _check_if_enabled(self) -> bool:
        """Check if logging is enabled via environment variable or config."""
        # Check environment variable
        if os.environ.get('FELLOW_LOGGING', '').lower() in ('1', 'true', 'yes'):
            return True

        # Check hooks.json config
        try:
            hooks_config = Path(__file__).parent.parent / '.claude-plugin' / 'hooks.json'
            if hooks_config.exists():
                with open(hooks_config, 'r') as f:
                    config = json.load(f)
                    for hook in config.get('hooks', []):
                        if hook.get('name') == 'fellow-context-enrichment':
                            return hook.get('config', {}).get('logging_enabled', False)
        except:
            pass

        return False

    def log_enrichment_event(
        self,
        original_prompt: str,
        is_coding_request: bool,
        intent: str,
        confidence: float,
        kb_found: bool,
        kb_path: Optional[str],
        entities_found: int,
        workflows_found: int,
        constraints_found: int,
        enriched_prompt: str,
        source: str = "hook"
    ):
        """
        Log an enrichment event.

        Args:
            original_prompt: User's original prompt
            is_coding_request: Whether detected as coding request
            intent: Intent category (create, modify, fix, etc.)
            confidence: Detection confidence score
            kb_found: Whether knowledge base was found
            kb_path: Path to knowledge base (if found)
            entities_found: Number of relevant entities
            workflows_found: Number of relevant workflows
            constraints_found: Number of applicable constraints
            enriched_prompt: Final enriched prompt (or original if pass-through)
            source: Source of enrichment ("hook" or "command")
        """
        if not self.enabled or not self.log_dir:
            return

        try:
            timestamp = datetime.now()
            log_entry = {
                "timestamp": timestamp.isoformat(),
                "source": source,
                "original_prompt": original_prompt,
                "detection": {
                    "is_coding_request": is_coding_request,
                    "intent": intent,
                    "confidence": confidence
                },
                "knowledge_base": {
                    "found": kb_found,
                    "path": kb_path
                },
                "enrichment": {
                    "entities_count": entities_found,
                    "workflows_count": workflows_found,
                    "constraints_count": constraints_found,
                    "was_enriched": kb_found and is_coding_request
                },
                "enriched_prompt": enriched_prompt if kb_found and is_coding_request else None,
                "prompt_length": {
                    "original": len(original_prompt),
                    "enriched": len(enriched_prompt)
                }
            }

            # Write to daily log file
            log_file = self.log_dir / f"enrichment_{timestamp.strftime('%Y-%m-%d')}.jsonl"
            with open(log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')

            # Also write human-readable summary
            summary_file = self.log_dir / f"enrichment_{timestamp.strftime('%Y-%m-%d')}.log"
            with open(summary_file, 'a') as f:
                f.write(f"\n{'='*80}\n")
                f.write(f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {source.upper()}\n")
                f.write(f"{'='*80}\n")
                f.write(f"Original Prompt ({len(original_prompt)} chars):\n")
                f.write(f"{original_prompt}\n")
                f.write(f"\n")
                f.write(f"Detection:\n")
                f.write(f"  - Coding Request: {is_coding_request}\n")
                f.write(f"  - Intent: {intent}\n")
                f.write(f"  - Confidence: {confidence:.2f}\n")
                f.write(f"\n")
                f.write(f"Knowledge Base:\n")
                f.write(f"  - Found: {kb_found}\n")
                if kb_path:
                    f.write(f"  - Path: {kb_path}\n")
                f.write(f"\n")
                if kb_found and is_coding_request:
                    f.write(f"Enrichment:\n")
                    f.write(f"  - Entities: {entities_found}\n")
                    f.write(f"  - Workflows: {workflows_found}\n")
                    f.write(f"  - Constraints: {constraints_found}\n")
                    f.write(f"  - Enriched Length: {len(enriched_prompt)} chars\n")
                    f.write(f"\n")
                    f.write(f"Enriched Prompt:\n")
                    f.write(f"{enriched_prompt}\n")
                else:
                    f.write(f"Result: Pass-through (no enrichment)\n")
                f.write(f"\n")

        except Exception as e:
            # Silently fail - don't break the enrichment process
            print(f"Warning: Failed to write log: {e}", file=sys.stderr)

    def log_error(self, error: str, context: Dict[str, Any]):
        """Log an error event."""
        if not self.enabled or not self.log_dir:
            return

        try:
            timestamp = datetime.now()
            log_entry = {
                "timestamp": timestamp.isoformat(),
                "type": "error",
                "error": error,
                "context": context
            }

            error_file = self.log_dir / f"errors_{timestamp.strftime('%Y-%m-%d')}.jsonl"
            with open(error_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')

        except Exception as e:
            print(f"Warning: Failed to write error log: {e}", file=sys.stderr)


def get_logger() -> FellowLogger:
    """Get a logger instance."""
    return FellowLogger()
