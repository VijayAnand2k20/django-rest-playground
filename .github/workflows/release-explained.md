# How the Release Workflow Works

This document explains the `release.yml` GitHub Actions workflow — what it does and how it works.

## Overview

When a Git tag containing `VJAI` (e.g. `Something_VJAI`) is pushed, the workflow automatically:

1. Checks out the repository on a single runner.
2. Reads the `version` field from `info.yml` inside each project folder.
3. Zips each project folder with the name `foldername_version_VJAI.zip`.
4. Creates a new **GitHub Release** and attaches the zips directly.

---

## Single Job, Single Runner

The entire workflow runs in one job (`release`) on one Ubuntu runner. No artifact upload/download is needed because everything happens in the same workspace.

```
Runner
├── checkout code
├── read version from backend/info.yml   → e.g. 2026.04.01
├── read version from py_client/info.yml → e.g. 2026.04.03
├── zip backend/   → backend_2026.04.01_VJAI.zip
├── zip py_client/ → py_client_2026.04.03_VJAI.zip
└── gh release create Something_VJAI backend_2026.04.01_VJAI.zip py_client_2026.04.03_VJAI.zip
     └── attaches zips to GitHub Release page
```

---

## Step-by-Step Breakdown

| Step | What happens | Where |
|------|-------------|-------|
| `Checkout code` | Clones the repo onto the runner | Runner's local disk |
| `Zip folders` | Reads version from `info.yml`, runs `zip -r` for each folder with `foldername_version_VJAI.zip` naming | Runner's local disk |
| `Create GitHub Release` | Calls `gh release create` with the `.zip` files | GitHub API — creates the release page and attaches the files |

---

## Zip Naming Convention

Each zip file is named using the pattern: **`foldername_version_VJAI.zip`**

The `version` value is read from the `info.yml` file inside each folder:

```yaml
# backend/info.yml (example)
version: 2026.04.01
```

This produces: `backend_2026.04.01_VJAI.zip`

---

## Adding a New Folder

To include a new folder (e.g. `frontend`) in every release, ensure it has an `info.yml` with a `version` field, then add the corresponding lines in the `Zip folders` step and append the resulting file to the `gh release create` command:

```yaml
- name: Zip folders
  run: |
    BACKEND_VERSION=$(grep '^version:' backend/info.yml | awk '{print $2}')
    PY_CLIENT_VERSION=$(grep '^version:' py_client/info.yml | awk '{print $2}')
    FRONTEND_VERSION=$(grep '^version:' frontend/info.yml | awk '{print $2}')   # ← add this
    if [ -z "$BACKEND_VERSION" ]; then echo "Error: version not found in backend/info.yml" && exit 1; fi
    if [ -z "$PY_CLIENT_VERSION" ]; then echo "Error: version not found in py_client/info.yml" && exit 1; fi
    if [ -z "$FRONTEND_VERSION" ]; then echo "Error: version not found in frontend/info.yml" && exit 1; fi    # ← add this
    echo "BACKEND_ZIP=backend_${BACKEND_VERSION}_VJAI.zip" >> $GITHUB_ENV
    echo "PY_CLIENT_ZIP=py_client_${PY_CLIENT_VERSION}_VJAI.zip" >> $GITHUB_ENV
    echo "FRONTEND_ZIP=frontend_${FRONTEND_VERSION}_VJAI.zip" >> $GITHUB_ENV    # ← add this
    zip -r "backend_${BACKEND_VERSION}_VJAI.zip" backend/
    zip -r "py_client_${PY_CLIENT_VERSION}_VJAI.zip" py_client/
    zip -r "frontend_${FRONTEND_VERSION}_VJAI.zip" frontend/                    # ← add this

- name: Create GitHub Release
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    gh release create "${{ github.ref_name }}" \
      --repo "${{ github.repository }}" \
      --title "Release ${{ github.ref_name }}" \
      --generate-notes \
      "${{ env.BACKEND_ZIP }}" "${{ env.PY_CLIENT_ZIP }}" "${{ env.FRONTEND_ZIP }}"   # ← add this
```

