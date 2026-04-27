# How the Release Workflow Works

This document explains the `release.yml` GitHub Actions workflow — what it does and how it works.

## Overview

When a Git tag matching `v*` (e.g. `v1.0.0`) is pushed, the workflow automatically:

1. Checks out the repository on a single runner.
2. Zips each project folder sequentially.
3. Creates a new **GitHub Release** and attaches the zips directly.

---

## Single Job, Single Runner

The entire workflow runs in one job (`release`) on one Ubuntu runner. No artifact upload/download is needed because everything happens in the same workspace.

```
Runner
├── checkout code
├── zip backend/   → backend.zip
├── zip py_client/ → py_client.zip
└── gh release create v1.0.0 backend.zip py_client.zip
     └── attaches zips to GitHub Release page
```

---

## Step-by-Step Breakdown

| Step | What happens | Where |
|------|-------------|-------|
| `Checkout code` | Clones the repo onto the runner | Runner's local disk |
| `Zip folders` | Runs `zip -r` for each folder | Runner's local disk |
| `Create GitHub Release` | Calls `gh release create` with the `.zip` files | GitHub API — creates the release page and attaches the files |

---

## Adding a New Folder

To include a new folder (e.g. `frontend`) in every release, add a new `zip` line in the `Zip folders` step and append the resulting file to the `gh release create` command:

```yaml
- name: Zip folders
  run: |
    zip -r backend.zip backend/
    zip -r py_client.zip py_client/
    zip -r frontend.zip frontend/   # ← add this

- name: Create GitHub Release
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    gh release create "${{ github.ref_name }}" \
      --repo "${{ github.repository }}" \
      --title "Release ${{ github.ref_name }}" \
      --generate-notes \
      backend.zip py_client.zip frontend.zip   # ← add this
```

