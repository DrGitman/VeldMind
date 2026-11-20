# Contributing to VeldMind

Thanks for helping build VeldMind. Please keep to these simple rules so the code stays clean and easy to follow.

## 1. Branches

| Branch | What it is for |
|---|---|
| `main` | The final product only. Nobody pushes here directly. |
| `dev` | Where all finished work comes together. |
| `feature/...`, `fix/...`, `docs/...`, `chore/...` | Short-lived work branches. Always start from `dev` and merge back into `dev`. |

**Name your branch after the issue:**

```
feature/VM-41-fence-editor
fix/VM-63-sync-retry
docs/VM-70-setup-guide
```

Keep branches short-lived: aim to merge within 1 to 3 days. Delete the branch after it is merged.

## 2. Day to day steps

```bash
# get the latest dev
git checkout dev
git pull

# start your task
git checkout -b feature/VM-41-fence-editor

# work, then save your changes
git add .
git commit -m "feat(app): add undo to fence editor"

# push and open a pull request into dev
git push -u origin feature/VM-41-fence-editor
```

When the whole product is ready, the team lead opens one pull request from `dev` into `main`.

## 3. Commit messages

Start with a type, then say what changed:

| Type | Use it for |
|---|---|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation only |
| `chore` | Setup, tooling, CI |
| `test` | Adding or fixing tests |
| `refactor` | Code changes that do not change behaviour |

Examples:

```
feat(app): show grazing days left per camp
fix(gateway): drop duplicate GPS fixes
docs(readme): add setup steps
```

## 4. Pull requests

Before you ask for a review, check that:

- [ ] The PR links to an issue (VM-xx)
- [ ] UI changes include a screenshot or a short clip
- [ ] Tests are added or updated
- [ ] App changes work with no internet
- [ ] No secrets, keys or `.env` files are included
- [ ] It matches the design in Figma

Pull requests into `dev` need **1 review**. The final pull request from `dev` into `main` needs **2 reviews**.

## 5. Secrets

- Never commit `.env`, keys, passwords or tokens.
- Put new settings in `env.example` with an empty or fake value, so others know they exist.
- Store real values in GitHub Actions secrets.

## 6. Who reviews what

See [CODEOWNERS](CODEOWNERS). GitHub asks the right people to review automatically.

## 7. Need help?

Open an issue or ask in the team chat. No question is too small.
