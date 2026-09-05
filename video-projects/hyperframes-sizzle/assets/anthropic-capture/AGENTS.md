# AGENTS.md

## Shared Claude guidance for Codex

Before working in this directory or its descendants, read and follow [CLAUDE.md](./CLAUDE.md) in this same directory. It contains the shared folder-specific instructions; read referenced instructions explicitly rather than relying on Claude's `@` import syntax. Read applicable ancestor guidance as well, with more specific folder rules applying within their scope.

Use available Codex tools for Claude-specific tool names and skill invocations. Do not assume Claude hooks, named agents, plugins, or MCP services are installed in Codex. Preserve the source's workflow gates and verification requirements, subject to current user instructions and higher-priority runtime rules. If a required capability is unavailable, report it instead of claiming it ran.
