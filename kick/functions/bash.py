from pydantic_ai import RunContext
import asyncio


async def bash(ctx: RunContext[str], command: str, timeout: int = 30) -> str:
    """
    Execute a shell command in the workspace and return its output.

    Args:
        command: The shell command to execute.
        timeout: Maximum execution time in seconds(Optional).

    Returns:
        The command's exit code, standard output, standard error, or an error message if execution fails.
    """
    print(f"-- calling bash({ctx.deps}, {command}, timeout = {timeout})")

    process = await asyncio.create_subprocess_shell(
        command,
        cwd=ctx.deps,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )

    output = []

    async def readoutput():
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            print(line.decode(), end="", flush=True)
            output.append(line.decode())

    reader = asyncio.create_task(readoutput())

    try:
        await asyncio.wait_for(process.wait(), timeout=timeout)
    except asyncio.TimeoutError:
        process.kill()
        await process.wait()
        await reader
        return f"Command timed out after : {timeout} seconds"
    except asyncio.CancelledError:
        process.kill()
        await process.wait()
        raise
    await reader
    if len(output) > 100:
        output = output[-100:]
    return f"Exit Code:\n{process.returncode}\n" + "STDOUT: " + "\n".join(output)
