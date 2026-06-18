# eve-packages-linux

First-party **eve** packages for Linux (Ubuntu) instances — content that runs
**after** the instance is manageable over SSH: remote desktops & access
(`vnc`, `rdp`, `rustdesk`, `nomachine`, `splashtop`, `thinlinc`, `waypipe`,
`xpra`, `sunshine`), full desktop environments (GNOME / KDE / XFCE, plus headless
variants), and `docker`, `steam`, `discord`, `macos-desktop-theme`.

Each package declares `supports: {os_families: [ubuntu]}` (several also constrain
`arches`); eve never offers a package to an incompatible instance. "Linux" is an
organizational grouping, **not** a compatibility claim — the precise support
lives in each manifest's `supports` + `install` block. The Windows halves of the
dual-OS tools (discord, nomachine, rdp, rustdesk, splashtop, steam, sunshine,
xpra) live in
[eve-packages-windows](https://github.com/fruwehq/eve-packages-windows).

> **AI agents and developer tooling** (`claude`, `codex-cli`, `goose`, `hermes`,
> `opencode`, `dev-toolchain`, `vscode`) moved to
> **[eve-plugins-ai](https://github.com/fruwehq/eve-plugins-ai)** (v4.2).

## Use it

This is an external plugin source — nothing is bundled in eve core:

```sh
eve plugin source add --recommended eve-packages-linux
eve pull
```

(or add it from the eve TUI's plugin screen — press `g`). It's in eve's
recommended-source catalog. Pair it with
[eve-providers](https://github.com/fruwehq/eve-providers) (providers + OS
identity), and optionally eve-plugins-ai.

## How packages run

Every package is self-contained CONTENT — a manifest (`eve-plugin.yaml`) plus a
`commands/` and `provision/` tree. None ship their own entrypoint: each command's
`exec: scripts/package-plugin` resolves to the **core generic dispatcher** at the
consuming eve checkout (`scripts/package-plugin`, which stays in eve). A package
is pure data — it materializes verbatim and runs against whatever eve version you
have. See [package-anatomy](https://github.com/fruwehq/eve/blob/main/docs/package-anatomy.md).

## Layout

```
<id>/
  eve-plugin.yaml        # manifest: supports, install steps, command execs
  commands/ubuntu/       # host-side command shims (status, down)
  provision/ubuntu/      # guest-side provisioning scripts run by the dispatcher
```

## Conformance

`.github/workflows/conformance.yml` checks out this repo plus `fruwehq/eve` (for
the harness, schema, and the `scripts/package-plugin` dispatcher) and runs
`eve/scripts/plugin-test` against every `*/eve-plugin.yaml`.

MIT licensed.
