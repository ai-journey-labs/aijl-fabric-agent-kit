#!/usr/bin/env python3
"""Set up and check an operator workstation for the AIJL Agent Kit for Microsoft Fabric.

Run it from the repository root, in your own terminal (not through the agent):

    python scripts/kit_setup.py                         set up, then check
    python scripts/kit_setup.py --check                 check only, change nothing
    python scripts/kit_setup.py --copilot               also check the GitHub Copilot setup
    python scripts/kit_setup.py --apply-copilot-rules   also add the Copilot terminal rules
                                                        to your VS Code User settings

On macOS and Linux, use python3. Standard library only; Python 3.11 or later.

What it does:
- Checks the tools the kit needs.
- Generates .mcp.json for this platform from scripts/mcp_servers.json. A previous
  .mcp.json that differs is kept as .mcp.json.bak.
- Creates .claude/settings.local.json from the example if it does not exist. It never
  overwrites that file and never prints its values.
- Reads the lead operator's decision on Microsoft's EULA for the powerbi-modeling server
  (FABRIC_AGENT_PBI_EULA: accepted or declined). It never accepts the EULA itself: the
  server is added to .mcp.json, with the acceptance variable, only when the setting is
  accepted.
- Reads the identity mode (FABRIC_AGENT_IDENTITY: certificate, user or managed-identity)
  and pins each MCP server to that mode's credential in .mcp.json. Checks the credential
  settings the mode needs, and which kind of identity the project Azure CLI profile is
  signed in as.
- Checks that local files are git-ignored and that the Copilot copy of the skills is current.
- With --copilot, checks the Copilot terminal rules and credential variables. With
  --apply-copilot-rules, adds missing rules to your VS Code User settings, after saving a
  backup, if the file is plain JSON.

The output contains no credential values, so it is safe to paste to the agent.
Exit code 0 means ready; 1 means something needs attention.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERVERS_FILE = ROOT / "scripts" / "mcp_servers.json"
RULES_FILE = ROOT / "scripts" / "copilot_terminal_rules.json"
MCP_FILE = ROOT / ".mcp.json"
MCP_BACKUP = ROOT / ".mcp.json.bak"
LOCAL_SETTINGS = ROOT / ".claude" / "settings.local.json"
LOCAL_EXAMPLE = ROOT / ".claude" / "settings.local.json.example"
SYNC_SCRIPT = ROOT / "scripts" / "sync_skills.py"
KIT_VERSION_FILE = ROOT / "KIT_VERSION"

PLACEHOLDER = "<set locally>"
MODE_KEY = "FABRIC_AGENT_IDENTITY"
DEFAULT_MODE = "certificate"
CREDENTIAL_KEYS = (
    "AZURE_TENANT_ID",
    "AZURE_CLIENT_ID",
    "AZURE_CLIENT_CERTIFICATE_PATH",
    "AZURE_CONFIG_DIR",
)
# Never allowed: the kit uses no client secrets.
FORBIDDEN_KEYS = ("AZURE_CLIENT_SECRET",)
# Set by the kit in .mcp.json; an operator value would override it, or accept a licence
# the lead operator has not accepted.
KIT_MANAGED_KEYS = ("AZURE_TOKEN_CREDENTIALS", "PBI_MODELING_MCP_ACCEPT_EULA")
# The lead operator's decision on Microsoft's EULA for the powerbi-modeling server.
EULA_KEY = "FABRIC_AGENT_PBI_EULA"
EULA_VALUES = ("accepted", "declined")

# Identity modes, keyed by FABRIC_AGENT_IDENTITY. Options are those in the Identity
# section of docs/security_and_access.md. Keys not listed as required or optional must
# be absent, so that no tool signs in as a different identity than the mode intends.
MODES = {
    "certificate": {
        "options": "A or B (service principal with your own certificate)",
        "required": ("AZURE_TENANT_ID", "AZURE_CLIENT_ID", "AZURE_CLIENT_CERTIFICATE_PATH", "AZURE_CONFIG_DIR"),
        "optional": (),
        "cli_identity": "service principal",
    },
    "user": {
        "options": "D (dedicated agent user account)",
        "required": ("AZURE_TENANT_ID", "AZURE_CONFIG_DIR"),
        "optional": (),
        "cli_identity": "user",
    },
    "managed-identity": {
        "options": "E (managed identity on an Azure virtual machine)",
        "required": ("AZURE_CONFIG_DIR",),
        "optional": ("AZURE_TENANT_ID", "AZURE_CLIENT_ID"),
        "cli_identity": "managed identity",
    },
}
RULES_SETTING = "chat.tools.terminal.autoApprove"
MIN_PYTHON = (3, 11)
MIN_NODE = 18

# (command, purpose, required)
TOOLS = (
    ("git", "version control", True),
    ("uv", "Python tool runner", True),
    ("uvx", "starts the fabric MCP server", True),
    ("node", "starts the powerbi-modeling MCP server", True),
    ("npx", "starts the powerbi-modeling MCP server", True),
    ("az", "Azure CLI, for the az rest fallback", True),
    ("openssl", "creates your certificate (SETUP.md step 5); on Windows it is in Git Bash", False),
    ("code", "VS Code command line", False),
    ("claude", "Claude Code command line, for Claude Code users", False),
)


class Report:
    """Prints check results and counts what still needs attention."""

    def __init__(self) -> None:
        self.failures = 0
        self.todos = 0

    def section(self, title: str) -> None:
        print(f"\n{title}")

    def line(self, status: str, text: str) -> None:
        if status == "FAIL":
            self.failures += 1
        elif status == "TODO":
            self.todos += 1
        print(f"  {status:<5} {text}")


def platform_key() -> str:
    """Return the platform as <os>-<arch>, for example win32-x64 or darwin-arm64."""
    if sys.platform == "win32":
        system = "win32"
    elif sys.platform == "darwin":
        system = "darwin"
    elif sys.platform.startswith("linux"):
        system = "linux"
    else:
        system = sys.platform
    machine = platform.machine().lower()
    arch = {"amd64": "x64", "x86_64": "x64", "arm64": "arm64", "aarch64": "arm64"}.get(machine, machine)
    return f"{system}-{arch}"


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def check_tools(report: Report) -> None:
    report.section("Tools")
    if sys.version_info >= MIN_PYTHON:
        report.line("OK", f"python {platform.python_version()}")
    else:
        report.line("FAIL", f"python {platform.python_version()}: version 3.11 or later is needed")
    for command, purpose, required in TOOLS:
        path = shutil.which(command)
        if path is None:
            report.line("FAIL" if required else "INFO", f"{command} not found ({purpose})")
            continue
        if command == "node":
            check_node_version(report, path)
        else:
            report.line("OK", command)


def check_node_version(report: Report, path: str) -> None:
    try:
        result = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=30)
        version = result.stdout.strip().lstrip("v")
        major = int(version.split(".")[0])
    except (OSError, ValueError, subprocess.SubprocessError):
        report.line("FAIL", "node found, but its version could not be read")
        return
    if major >= MIN_NODE:
        report.line("OK", f"node {version}")
    else:
        report.line("FAIL", f"node {version}: version {MIN_NODE} or later is needed")


def build_mcp_config(key: str, mode: str, eula_accepted: bool) -> tuple[dict, list[tuple[str, str]]]:
    """Build the .mcp.json content for this platform, identity mode and EULA decision.

    Also return the servers left out, each with the reason: "platform" or "eula".
    """
    spec = read_json(SERVERS_FILE)
    overrides = spec.get("identity_modes", {}).get(mode, {})
    servers: dict = {}
    left_out: list[tuple[str, str]] = []
    for name, server in spec["servers"].items():
        supported = server.get("platforms")
        if supported and key not in supported:
            left_out.append((name, "platform"))
            continue
        eula = server.get("eula")
        if eula and not eula_accepted:
            left_out.append((name, "eula"))
            continue
        command, args = server["command"], list(server["args"])
        override = overrides.get(name, {})
        args += override.get("args", [])
        env = {**server.get("env", {}), **(eula or {}).get("env", {}), **override.get("env", {})}
        if key.startswith("win32"):
            # Claude Code on Windows needs cmd /c to start npx and similar launchers.
            command, args = "cmd", ["/c", command, *args]
        entry: dict = {"type": "stdio", "command": command, "args": args}
        if env:
            entry["env"] = env
        servers[name] = entry
    return {"mcpServers": servers}, left_out


def setup_mcp(report: Report, key: str, mode: str | None, eula_accepted: bool, write: bool) -> None:
    report.section("MCP servers (.mcp.json)")
    if mode is None:
        report.line("FAIL", f".mcp.json not checked: set {MODE_KEY} to a valid identity mode first")
        return
    config, left_out = build_mcp_config(key, mode, eula_accepted)
    for name, reason in left_out:
        if reason == "platform":
            report.line("WARN", f"{name}: the pinned version has no release for {key}, so it is left out")
        else:
            report.line("INFO", f"{name}: left out, because {EULA_KEY} is not accepted")

    existing = None
    if MCP_FILE.exists():
        try:
            existing = read_json(MCP_FILE)
        except (json.JSONDecodeError, OSError):
            existing = None
    if existing == config:
        report.line("OK", f".mcp.json matches the kit for {key}, identity mode {mode}")
        return
    if not write:
        state = "differs from the kit" if MCP_FILE.exists() else "does not exist"
        report.line("FAIL", f".mcp.json {state}; run the script without --check to generate it")
        return
    if MCP_FILE.exists():
        shutil.copyfile(MCP_FILE, MCP_BACKUP)
        report.line("INFO", "the previous .mcp.json was saved as .mcp.json.bak")
    MCP_FILE.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    report.line("OK", f".mcp.json generated for {key}, identity mode {mode}; restart VS Code to load it")


def read_local_env() -> dict | None:
    """Return the env block of .claude/settings.local.json, {} if absent, None if invalid."""
    if not LOCAL_SETTINGS.exists():
        return {}
    try:
        data = read_json(LOCAL_SETTINGS)
    except (json.JSONDecodeError, OSError):
        return None
    env = data.get("env") if isinstance(data, dict) else None
    return env if isinstance(env, dict) else {}


def identity_mode(report: Report, values: dict, where: str) -> str | None:
    """Report the identity mode set in values, and return it (None if invalid)."""
    value = values.get(MODE_KEY)
    if not value or value == PLACEHOLDER:
        report.line("INFO", f"{MODE_KEY} is not set ({where}); using {DEFAULT_MODE}, options A or B")
        return DEFAULT_MODE
    if value not in MODES:
        report.line("FAIL", f"{MODE_KEY} is {value!r}; use one of: {', '.join(MODES)} (SETUP.md step 7)")
        return None
    report.line("OK", f"identity mode {value}: option {MODES[value]['options']}")
    return value


def eula_decision(report: Report, values: dict, where: str) -> bool:
    """Report the EULA decision for the powerbi-modeling server; return True only if accepted."""
    value = values.get(EULA_KEY)
    if not value or value == PLACEHOLDER:
        report.line("TODO", f"{EULA_KEY} is not set ({where}); set it to accepted or declined, as the lead operator recorded under Tooling in 01_environment_overview.md")
        return False
    if value not in EULA_VALUES:
        report.line("FAIL", f"{EULA_KEY} is {value!r}; use accepted or declined ({where})")
        return False
    if value == "accepted":
        report.line("OK", "Microsoft's EULA for the powerbi-modeling server: accepted by the lead operator")
        return True
    report.line("INFO", "Microsoft's EULA for the powerbi-modeling server: declined, so the server is not used")
    return False


def setup_local_settings(report: Report, write: bool) -> tuple[dict | None, str | None]:
    """Create the local settings file if needed; return its env block and identity mode."""
    report.section("Local settings (.claude/settings.local.json)")
    if not LOCAL_SETTINGS.exists():
        if not write:
            report.line("TODO", "the file does not exist; run the script without --check to create it")
            return None, DEFAULT_MODE
        shutil.copyfile(LOCAL_EXAMPLE, LOCAL_SETTINGS)
        report.line("OK", "created from .claude/settings.local.json.example")
    env = read_local_env()
    if env is None:
        report.line("FAIL", "the file is not valid JSON")
        return None, None
    return env, identity_mode(report, env, "SETUP.md step 7")


def check_credentials(report: Report, values: dict, mode: str, where: str) -> None:
    """Report whether each credential variable the mode needs is set, never its value."""
    spec = MODES[mode]
    for name in FORBIDDEN_KEYS:
        if values.get(name):
            report.line("FAIL", f"{name} is set; the kit never uses client secrets. Remove it and treat the secret as exposed")
    for name in KIT_MANAGED_KEYS:
        if values.get(name):
            report.line("TODO", f"{name} is set ({where}); remove it, because the kit sets it in .mcp.json")
    for name in CREDENTIAL_KEYS:
        value = values.get(name)
        unset = not value or value == PLACEHOLDER
        if name in spec["required"]:
            if unset:
                report.line("TODO", f"{name} is not set ({where})")
            elif name == "AZURE_CLIENT_CERTIFICATE_PATH" and not Path(value).expanduser().is_file():
                report.line("TODO", f"{name} is set, but no file exists at that path")
            elif name == "AZURE_CONFIG_DIR" and not Path(value).expanduser().is_dir():
                report.line("TODO", f"{name} is set, but the folder does not exist yet (SETUP.md step 8)")
            else:
                report.line("OK", f"{name} is set")
        elif name in spec["optional"]:
            if value == PLACEHOLDER:
                report.line("TODO", f"{name} still holds the placeholder ({where}); set it or remove the line")
            elif value:
                report.line("OK", f"{name} is set (optional in identity mode {mode})")
        elif value is not None:
            report.line("TODO", f"{name} is not used in identity mode {mode}; remove it ({where}), so no tool signs in as another identity")


def same_id(first: object, second: object) -> bool:
    """Compare two client IDs. GUIDs are not case-sensitive, and a pasted one may carry spaces."""
    return str(first or "").strip().lower() == str(second or "").strip().lower()


def check_cli_profile(report: Report, values: dict, mode: str) -> None:
    """Report which kind of identity the project Azure CLI profile is signed in as, never its name."""
    report.section("Project Azure CLI profile")
    config_dir = values.get("AZURE_CONFIG_DIR")
    if not config_dir or config_dir == PLACEHOLDER or not Path(config_dir).expanduser().is_dir():
        report.line("TODO", "not checked until AZURE_CONFIG_DIR points to an existing folder (SETUP.md step 8)")
        return
    az = shutil.which("az")
    if az is None:
        report.line("INFO", "az not found, so the profile was not checked")
        return
    env = {**os.environ, "AZURE_CONFIG_DIR": str(Path(config_dir).expanduser())}
    try:
        result = subprocess.run(
            [az, "account", "show", "--query", "user", "--output", "json"],
            capture_output=True, text=True, timeout=120, env=env,
        )
        user = json.loads(result.stdout) if result.returncode == 0 else None
    except (OSError, ValueError, subprocess.SubprocessError):
        user = None
    if not isinstance(user, dict):
        report.line("TODO", "the project profile is not signed in (SETUP.md step 8)")
        return
    kind, name = user.get("type"), str(user.get("name", ""))
    if kind == "servicePrincipal" and name in ("systemAssignedIdentity", "userAssignedIdentity"):
        actual = "managed identity"
    elif kind == "servicePrincipal":
        actual = "service principal"
    elif kind == "user":
        actual = "user"
    else:
        actual = "unknown"
    expected = MODES[mode]["cli_identity"]
    if actual != expected:
        report.line("FAIL", f"the project profile is signed in as a {actual}, but identity mode {mode} needs a {expected}; sign in again (SETUP.md step 8)")
    elif mode == "certificate" and not same_id(name, values.get("AZURE_CLIENT_ID")):
        report.line("FAIL", "the project profile is signed in as a different service principal from AZURE_CLIENT_ID; sign in again (SETUP.md step 8)")
    else:
        report.line("OK", f"the project profile is signed in as a {actual}, as identity mode {mode} needs")


def check_git(report: Report) -> None:
    report.section("Repository")
    if shutil.which("git") is None:
        report.line("INFO", "git not found, so git checks were skipped")
        return
    for rel in (".mcp.json", ".claude/settings.local.json"):
        tracked = subprocess.run(
            ["git", "ls-files", "--error-unmatch", rel], cwd=ROOT, capture_output=True
        )
        if tracked.returncode == 0:
            report.line("FAIL", f"{rel} is tracked by git; run: git rm --cached {rel}")
            continue
        ignored = subprocess.run(["git", "check-ignore", "-q", rel], cwd=ROOT, capture_output=True)
        if ignored.returncode == 0:
            report.line("OK", f"{rel} is git-ignored")
        elif ignored.returncode == 1:
            report.line("FAIL", f"{rel} is not git-ignored; fix .gitignore before you commit")
        else:
            report.line("INFO", f"could not check {rel}; is this folder a git repository?")

    result = subprocess.run(
        [sys.executable, str(SYNC_SCRIPT), "--check"], cwd=ROOT, capture_output=True, text=True
    )
    if result.returncode == 0:
        report.line("OK", "the Copilot copy of the skills is up to date")
    else:
        report.line("WARN", "the Copilot copy of the skills is out of date; tell the lead operator")


def vscode_user_settings() -> Path:
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    return base / "Code" / "User" / "settings.json"


def check_copilot(report: Report, settings_path: Path, apply: bool, local_mode: str | None) -> None:
    report.section("GitHub Copilot")
    where = "in the environment VS Code starts from; SETUP.md step 9.1"
    names = (MODE_KEY, *CREDENTIAL_KEYS, *FORBIDDEN_KEYS, *KIT_MANAGED_KEYS)
    values = {name: os.environ[name] for name in names if name in os.environ}
    mode = identity_mode(report, values, where)
    if mode is not None and local_mode is not None and mode != local_mode:
        report.line("FAIL", f"{MODE_KEY} is {mode} in the environment but {local_mode} in .claude/settings.local.json; make them match, then run this script again")
    if mode is not None:
        check_credentials(report, values, mode, where)

    rules: dict = read_json(RULES_FILE)["rules"]
    if not settings_path.exists():
        report.line("TODO", f"VS Code User settings not found at {settings_path}; open VS Code once, or pass --vscode-settings")
        return
    text = settings_path.read_text(encoding="utf-8-sig")
    try:
        data = json.loads(text) if text.strip() else {}
    except json.JSONDecodeError:
        data = None  # Comments or trailing commas: VS Code accepts them, json does not.

    if isinstance(data, dict):
        current = data.get(RULES_SETTING)
        current = current if isinstance(current, dict) else {}
        missing = [rule for rule, value in rules.items() if current.get(rule) != value]
    else:
        missing = [rule for rule in rules if json.dumps(rule) not in text]

    if not missing:
        report.line("OK", "terminal rules are in your VS Code User settings")
        return
    if not apply:
        report.line("TODO", f"{len(missing)} terminal rule(s) missing from your VS Code User settings; run with --apply-copilot-rules")
        return
    if not isinstance(data, dict):
        report.line("TODO", "your User settings contain comments or trailing commas, so they were not changed; add the rules from scripts/copilot_terminal_rules.json by hand")
        return
    block = data.get(RULES_SETTING)
    if block is None:
        block = data[RULES_SETTING] = {}
    if not isinstance(block, dict):
        report.line("FAIL", f"{RULES_SETTING} in your User settings is not an object; fix it by hand")
        return
    backup = settings_path.with_name(settings_path.name + ".aijl-backup")
    shutil.copyfile(settings_path, backup)
    for rule in missing:
        block[rule] = rules[rule]
    settings_path.write_text(json.dumps(data, indent=4) + "\n", encoding="utf-8")
    report.line("OK", f"added {len(missing)} terminal rule(s); your previous settings are in {backup.name}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Set up and check a workstation for the AIJL Agent Kit for Microsoft Fabric.")
    parser.add_argument("--check", action="store_true", help="check only; change nothing")
    parser.add_argument("--copilot", action="store_true", help="also check the GitHub Copilot setup")
    parser.add_argument("--apply-copilot-rules", action="store_true", help="add missing Copilot terminal rules to your VS Code User settings (implies --copilot)")
    parser.add_argument("--vscode-settings", type=Path, help="path to your VS Code User settings.json, if not in the default place")
    args = parser.parse_args()
    if args.check and args.apply_copilot_rules:
        parser.error("--check changes nothing, so it cannot be combined with --apply-copilot-rules")

    key = platform_key()
    version = KIT_VERSION_FILE.read_text(encoding="utf-8").strip() if KIT_VERSION_FILE.exists() else "unknown"
    mode = "check" if args.check else "setup"
    print(f"AIJL Agent Kit for Microsoft Fabric, kit {version}: workstation {mode} on {key}")

    report = Report()
    check_tools(report)
    env, mode = setup_local_settings(report, write=not args.check)
    eula_accepted = eula_decision(report, env, "SETUP.md step 7") if env is not None else False
    if env is not None and mode is not None:
        check_credentials(report, env, mode, "SETUP.md step 7")
    setup_mcp(report, key, mode, eula_accepted, write=not args.check)
    if env is not None and mode is not None:
        check_cli_profile(report, env, mode)
    check_git(report)
    if args.copilot or args.apply_copilot_rules:
        check_copilot(report, args.vscode_settings or vscode_user_settings(), args.apply_copilot_rules, mode)
    else:
        print("\nGitHub Copilot\n  INFO  skipped; add --copilot if you use GitHub Copilot")

    print()
    if report.failures == 0 and report.todos == 0:
        print("Result: ready.")
    else:
        print(f"Result: not ready. {report.failures} problem(s) and {report.todos} item(s) to do.")
    print("This output contains no credential values. You can paste it to the agent.")
    return 0 if report.failures == 0 and report.todos == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
