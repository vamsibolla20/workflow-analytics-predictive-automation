from __future__ import annotations

import os
import logging
from dataclasses import dataclass

# This module intentionally does NOT contain client endpoints, credentials,
# flow IDs, user IDs, or production scheduling details.


@dataclass
class WorkflowTriggerConfig:
    api_base_url: str
    api_key: str


class WorkflowClient:
    """
    Portfolio-safe API integration interface.

    Replace `trigger_workflow` with your own organisation's documented API call.
    Do not hard-code credentials or production identifiers.
    """

    def __init__(self, config: WorkflowTriggerConfig):
        self.config = config

    def trigger_workflow(self, workflow_id: str) -> dict:
        logging.info("Demo trigger requested for workflow_id=%s", workflow_id)

        # In a real implementation:
        # 1. Authenticate using environment variables / secret manager
        # 2. Call the documented workflow start endpoint
        # 3. Check status codes and response payloads
        # 4. Log safely without exposing tokens
        #
        # This repository intentionally performs no external request.
        return {
            "workflow_id": workflow_id,
            "status": "demo_only",
            "message": "No external API call was made.",
        }


def load_config_from_env() -> WorkflowTriggerConfig:
    base_url = os.getenv("WORKFLOW_API_BASE_URL", "https://example.invalid")
    api_key = os.getenv("WORKFLOW_API_KEY", "demo-placeholder")
    return WorkflowTriggerConfig(api_base_url=base_url, api_key=api_key)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    client = WorkflowClient(load_config_from_env())
    print(client.trigger_workflow("demo_workflow_001"))
