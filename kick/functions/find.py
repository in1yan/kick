from pydantic_ai import RunContext
from pathlib import Path


def find(ctx: RunContext[str], pattern: str, limit: int = 100) -> str:
    """
    Search for files matching a glob pattern under the current working directory.

    The search is performed recursively from the directory. Matching file paths are returned relative to the search
    directory, one per line.

    Args:
        pattern: Glob pattern used to match files (e.g. "*.py",
            "**/*.json", "src/**/*.ts").
        limit: Maximum number of matching paths to return. If the limit is
            reached, the output is truncated and a notice is appended.

    Returns:
        A newline-separated string containing the relative paths of all
        matching files. If the number of matches exceeds `limit`, the final
        line indicates that the result set was truncated.

    Notes:
        - Searches recursively using `pathlib.Path.rglob()`.
        - `.git` and `node_modules` directories are ignored.
    """
    results = []
    for res in Path(ctx.deps).rglob(pattern):
        if ".git" in res.parts or "node_modules" in res.parts:
            continue

        results.append(str(res.relative_to(ctx.deps)))
        if len(results) > limit:
            results.append("Limit exceeded ...")
            break
    return "\n".join(results)
