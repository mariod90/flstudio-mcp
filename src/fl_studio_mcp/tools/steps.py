"""Step sequencer tools: read/write the channel-rack grid of the current pattern."""

from __future__ import annotations

from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

from .transport import _safe_call


def register(mcp: FastMCP) -> None:
    @mcp.tool(
        annotations={
            "title": "Get step sequencer row",
            "readOnlyHint": True,
            "idempotentHint": True,
            "openWorldHint": True,
        },
    )
    def fl_get_steps(
        channel: Annotated[int, Field(ge=0, description="Channel-rack index (0-based).")],
        length: Annotated[int, Field(ge=1, le=512)] = 16,
    ) -> dict:
        """Read one channel's step grid in the current pattern as a string: 'x' = on, '.' = off."""
        return _safe_call("channel_get_steps", {"channel": channel, "length": length})

    @mcp.tool(
        annotations={
            "title": "Set step sequencer row",
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": True,
        },
    )
    def fl_set_steps(
        channel: Annotated[int, Field(ge=0, description="Channel-rack index (0-based).")],
        steps: Annotated[str, Field(
            min_length=1, max_length=512,
            description="One char per 16th-note step: 'x' = on, '.' = off. "
                        "E.g. kick four-on-the-floor: 'x...x...x...x...'.",
        )],
    ) -> dict:
        """Write one channel's step grid in the current pattern. Steps beyond the string are untouched.
        Returns the grid read back from FL."""
        return _safe_call("channel_set_steps", {"channel": channel, "steps": steps})
