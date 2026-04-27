# How the Release Workflow Works

This document explains the `release.yml` GitHub Actions workflow — what it does, why it uploads/downloads artifacts, and where each operation happens.

## Overview

When a Git tag matching `v*` (e.g. `v1.0.0`) is pushed, the workflow automatically:

1. Zips each project folder in parallel.
2. Uploads those zips to **GitHub's temporary artifact storage**.
3. Downloads them in a separate job and attaches them to a new **GitHub Release**.

---

## Why Two Jobs?

### Job 1 — `zip-artifacts` (matrix)

```
zip-artifacts (backend)  ──┐
                            ├──► artifacts stored in GitHub's artifact store
zip-artifacts (py_client) ─┘
```

Each matrix job runs on **its own runner** (a fresh Ubuntu VM). That means:

- `backend` is zipped on runner A.
- `py_client` is zipped on runner B.
- They run **in parallel**, saving time.

Because each runner is isolated, the `.zip` files created on runner A are not visible to runner B, and neither is visible to the `release` job running on runner C. This is why **upload** is needed.

### Job 2 — `release`

```
release ──► downloads all .zip files ──► creates GitHub Release with them attached
```

This job runs on a **new, clean runner** that starts with no files at all. It uses `actions/download-artifact` to pull all the zips that were uploaded by the matrix jobs, then uses `gh release create` to publish them.

---

## Step-by-Step Breakdown

### `zip-artifacts` job

| Step | What happens | Where |
|------|-------------|-------|
| `Checkout code` | Clones the repo onto the runner | Runner (e.g. runner A for `backend`) |
| `Create <folder>.zip` | Runs `zip -r backend.zip backend/` | Runner's local disk |
| `Upload <folder>.zip` | Sends the `.zip` to GitHub's artifact store | GitHub's servers (temporary storage tied to this workflow run) |

### `release` job

| Step | What happens | Where |
|------|-------------|-------|
| `Download all artifacts` | Fetches all uploaded `.zip` files into `artifacts/` | Downloads from GitHub's artifact store → runner's local disk |
| `Create GitHub Release` | Calls `gh release create` with the `.zip` files | GitHub API — creates the release page and attaches the files |

---

## Where Are Uploads and Downloads Happening?

```
┌─────────────────────────────────────────────────────────────────┐
│                    GitHub Actions Run                           │
│                                                                 │
│  Runner A (zip-artifacts / backend)                             │
│  ├── checkout code                                              │
│  ├── zip backend/ → backend.zip                                 │
│  └── upload backend.zip ──────────────────────────────────┐    │
│                                                            │    │
│  Runner B (zip-artifacts / py_client)                      ▼    │
│  ├── checkout code                               GitHub Artifact│
│  ├── zip py_client/ → py_client.zip              Store         │
│  └── upload py_client.zip ────────────────────────────────┤    │
│                                                            │    │
│  Runner C (release)                                        │    │
│  ├── download all artifacts ◄──────────────────────────────┘    │
│  │   (lands in artifacts/ folder on Runner C)                   │
│  └── gh release create v1.0.0 artifacts/*.zip                  │
│       └── attaches zips to GitHub Release page                 │
└─────────────────────────────────────────────────────────────────┘
```

- **Upload** happens on runners A and B → files go to **GitHub's artifact store** (temporary, scoped to this workflow run).
- **Download** happens on runner C → files come from **GitHub's artifact store** onto runner C's disk.
- **Release** is created via the GitHub API — the `.zip` files become downloadable assets on the repository's **Releases page**.

---

## Adding a New Folder

To include a new folder (e.g. `frontend`) in every release, only one line needs to change in `release.yml`:

```yaml
matrix:
  folder:
    - backend
    - py_client
    - frontend   # ← add this
```

No other part of the workflow needs updating because the `release` job uses `artifacts/*.zip` — it picks up whatever was uploaded automatically.
