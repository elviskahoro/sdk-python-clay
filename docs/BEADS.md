# Beads workflow

This repository uses Beads with a local Dolt database and the shared DoltHub
remote `elviskahoro/sdk-python-clay`. Each Conductor workspace keeps its local
database in `.beads-local/`; credentials remain in the developer's existing
Dolt configuration.

## Setup

Conductor runs `scripts/setup-beads.sh` when creating a workspace. To set up a
workspace manually, run:

```bash
./scripts/setup-beads.sh
```

## Synchronization

Pull shared issues before starting work and push committed Dolt history when
you want to publish changes:

```bash
bd dolt pull
bd dolt push
```

Automatic push is disabled so concurrent workspaces do not race while writing
the remote. Do not commit `.beads-local/`, Dolt database files, or credentials.
