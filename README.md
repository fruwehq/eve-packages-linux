# eve-packages-linux

First-party **eve** packages for Linux instances — everything that runs **after**
SSH is reachable: remote desktops (VNC, ThinLinc, Waypipe), full desktop
environments (GNOME / KDE / XFCE, plus headless variants), dev toolchains
(`dev-toolchain`, `docker`, `vscode`), and AI coding tools (`claude`, `codex-cli`,
`goose`, `hermes`, `opencode`).

These 18 packages are the **ubuntu-only** set extracted out of the eve core repo
in v4.0 Phase 3. Each declares `supports: {os_families: [ubuntu]}` (several also
constrain `arches`), and eve never offers a package to an incompatible instance.
"Linux" is an organizational grouping, **not** a compatibility claim: the precise
distribution/version support lives in each manifest's `supports` + `install`
block. (The dual-OS packages — discord, nomachine, rdp, rustdesk, splashtop,
steam, sunshine, xpra — are split linux/windows separately and live elsewhere.)

## Consumption

Pull this catalog into an eve checkout alongside the core:

```
eve pull github.com/fruwehq/eve-packages-linux
```

`eve pull` drops each `<id>/` package under `plugins/packages/` so eve discovers
it like any built-in. You do **not** clone this repo manually or vendor anything.

## How packages run

Every package is self-contained CONTENT — a manifest (`eve-plugin.yaml`) plus a
`commands/` and `provision/` tree. None of them ship their own entrypoint:
every command's `exec: scripts/package-plugin` resolves to the **core generic
dispatcher** at the consuming eve checkout's repo root
(`scripts/package-plugin`, which stays in eve). So a package is pure data — it
extracts verbatim and runs against whatever eve version you've checked out.

## Layout

```
<id>/
  eve-plugin.yaml        # manifest: supports, install steps, command execs
  commands/ubuntu/       # per-OS command shims (status, down)
  provision/ubuntu/      # per-OS provisioning scripts run by the dispatcher
```

## Conformance

`.github/workflows/conformance.yml` checks out this repo plus `fruwehq/eve` (for
the harness, schema, and the `scripts/package-plugin` dispatcher) and runs
`eve/scripts/plugin-test` against every `*/eve-plugin.yaml`.

MIT licensed.
