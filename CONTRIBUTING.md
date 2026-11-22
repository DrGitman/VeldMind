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

`VM-41` means GitHub issue **#41**. Every branch needs an open issue first.

Keep branches short-lived: aim to merge within 1 to 2 days. GitHub deletes the branch for you after it is merged.

## 2. Work on your own, don't block anyone

We build in parallel and join everything at the end.

1. **Contracts first.** On Monday 23 Nov we agree and freeze the shared files in `/contracts` (API spec, database tables, LoRa message format, design tokens, seed data). After 13:00 they only change through a PR that everyone affected approves.
2. **Build against mocks.** Keep `USE_MOCKS=true` in your `.env`. Use the mock API, seed data, simulator recordings or sample files instead of waiting for someone else.
3. **Stay in your own folder.** See [CODEOWNERS](CODEOWNERS). Need a change in someone else's folder? Open an issue for them. Don't edit it yourself.
4. **Join at the end.** On 30 Nov and 1 Dec the team lead switches the mocks off, connects the real parts and we test the whole app together.

| Person | Own folders | Uses until integration |
|---|---|---|
| Frontend (Tuilika) | `/app` | Mock API from `contracts/openapi.yaml` + seed JSON |
| Backend 1 (Doomstorm-coder) | `/api` satellite & advisor, `/ml` | Local Supabase + seed data, saved Sentinel 2 scenes |
| Backend 2 (MiluSimau) | `/api` ingest, alerts, SMS | Gateway simulator recordings, Africa's Talking sandbox |
| Technical lead (Israel-Shingenge) | `/supabase`, `/gateway`, `/firmware`, `/contracts` | Postman collection, own simulator |
| QA (Avril-coder) | `/tests` | Mock app build, contract tests |
| Team lead (DrGitman) | `/docs` | Figma prototype |

## 3. Who merges

**Only the team lead (DrGitman) merges** pull requests into `dev`, runs the integration days and does the final merge from `dev` into `main` on 2 December. Everyone else opens pull requests and fixes review comments.

## 4. Day to day steps

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

Open your PR by 17:00. The team lead reviews and merges into `dev` the same day. When the whole product is ready, the team lead merges `dev` into `main`.

## 5. Commit messages

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

## 6. Pull requests

Before you ask for a review, check that:

- [ ] The description says `Closes #41` (your issue number). This closes the issue when the PR is merged. The PR checks fail without it.
- [ ] UI changes include a screenshot or a short clip
- [ ] Tests are added or updated
- [ ] App changes work with no internet
- [ ] No secrets, keys or `.env` files are included
- [ ] It matches the design in Figma

Pull requests into `dev` need **1 review**. The final pull request from `dev` into `main` needs **2 reviews**.

## 7. Secrets

- Never commit `.env`, keys, passwords or tokens.
- Put new settings in `env.example` with an empty or fake value, so others know they exist.
- Store real values in GitHub Actions secrets.

## 8. Who reviews what

See [CODEOWNERS](CODEOWNERS). GitHub asks the right people to review automatically.

## 9. Need help?

Open an issue or ask in the team chat. No question is too small.
