# eve-packages-linux

First-party **eve** packages for Linux instances — everything that runs **after**
SSH is reachable (VNC, desktops, Steam, dev tools, and the Linux side of
rustdesk/nomachine/splashtop/sunshine).

> **Status: scaffold.** Packages are extracted here in v4.0 Phase 3, scaffolded
> from `eve-plugin-template`. See the v4.0 roadmap.

"Linux" is an organizational grouping, **not** a compatibility claim: each package
declares its precise distribution/version support (e.g. Ubuntu 26.04) via its
manifest `supports`, and eve never offers a package to an incompatible instance.

MIT licensed.
