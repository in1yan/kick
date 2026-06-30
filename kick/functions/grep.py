import os
from pydantic_ai import RunContext
import shutil
import asyncio


async def grep(
    ctx: RunContext[str],
    pattern: str,
    glob: str | None = None,
    ignore_case: bool = True,
):
    """
    Search for a text pattern in files under the current working directory using
    ripgrep (`rg`).

    Args:
        pattern: The text or regular expression to search for.
        glob: Optional glob pattern to limit searched files (e.g. "*.py",
            "*.ts", "src/**"). If omitted, all files are searched.
        ignore_case: If True, perform a case-insensitive search.

    Returns:
        A string containing the ripgrep exit code and any matching lines.
        If ripgrep is not installed, returns an error message indicating that
        the tool is unavailable.

    Notes:
        - Uses ripgrep (`rg`) as the search backend.
        - Matching lines include file paths and line numbers.
    """

    if not shutil.which("rg"):
        return "Grep Tool is not Available , Because Rip Grep is not installed"
    cmd = ["rg", "--line-number"]
    if ignore_case:
        cmd.append("--ignore-case")
    if glob:
        cmd.extend(["--glob", glob])
    cmd.extend([pattern, "."])
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=ctx.deps,
    )
    output = []

    while True:
        line = await process.stdout.readline()
        if not line:
            break
        print(line.decode(), end="", flush=True)
        output.append(line.decode())
    await process.wait()
    return f"Exit Code: \n {process.returncode}\n STDOUT: {'\n'.join(output)}"
