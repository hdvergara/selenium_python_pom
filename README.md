# Selenium Page Object Model (Python)

<div align="center">

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-4.41.0-43B02A.svg)](https://www.selenium.dev/)
[![pytest](https://img.shields.io/badge/pytest-latest-0A9EDC.svg)](https://pytest.org/)
[![Pipenv](https://img.shields.io/badge/pipenv-managed-608880.svg)](https://pipenv.pypa.io/)
[![Allure](https://img.shields.io/badge/allure-reports-FF6C37.svg)](https://docs.qameta.io/allure/)
[![Pydantic](https://img.shields.io/badge/pydantic-2.x-E92063.svg)](https://docs.pydantic.dev/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/YOUR_GITHUB_USER/YOUR_REPO_NAME/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_GITHUB_USER/YOUR_REPO_NAME/actions/workflows/ci.yml)

</div>

> **Replace `YOUR_GITHUB_USER/YOUR_REPO_NAME` in the CI badge URL** with your GitHub username and repository name after you push this workflow.

Browser UI automation with **Python**, **Selenium WebDriver**, and the **Page Object Model (POM)**. Tests target the public [Sauce Demo (Swag Labs)](https://www.saucedemo.com/) sandbox—suitable for learning, demos, and portfolio samples.

---

## Table of contents

- [Features](#features)
- [Tech stack](#tech-stack)
- [Project structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Test markers & parallel runs](#test-markers--parallel-runs)
- [CI/CD & GitHub Actions](#cicd--github-actions)
- [Security & best practices](#security--best-practices)
- [License](#license)

---

## Features

- Page Object pattern for maintainable locators and page actions
- Shared `Actions` helper with explicit waits (`visibility`, `element_to_be_clickable`)
- Multi-browser support (Chrome, Firefox, Edge) via **Selenium Manager** (no manual driver binaries)
- Settings from environment variables using **Pydantic Settings v2**
- **pytest** + **Allure** for reporting
- **Markers** (`smoke`, `regression`) registered in `pytest.ini`
- Optional **parallel** test runs via `pytest-xdist` (dev dependency)
- **GitHub Actions** workflow: tests on push/PR, scheduled runs, **Allure** published to **GitHub Pages** (default branch) and as downloadable artifacts (including PRs)
- Structured logging with **Loguru**

---

## Tech stack

| Area | Choice |
|------|--------|
| Language | Python 3.12 |
| Automation | Selenium 4.41 |
| Test runner | pytest (+ pytest-xdist for parallel runs) |
| Dependency / env | Pipenv, python-dotenv |
| Config validation | Pydantic v2, pydantic-settings |
| Reporting | Allure Framework |
| Logging | Loguru |
| CI/CD | GitHub Actions + GitHub Pages (Allure HTML) |

---

## Project structure

```text
selenium_python_pom/
├── .github/
│   └── workflows/
│       └── ci.yml              # Tests, Allure HTML, optional GitHub Pages deploy
├── core/
│   ├── actions/
│   │   └── actions.py          # Reusable waits and interactions (click, send_text, etc.)
│   ├── browser/
│   │   ├── browser.py          # WebDriver factory (Chrome / Firefox / Edge)
│   │   └── browser_type.py     # Browser enum
│   └── config/
│       └── browser_config.py   # Pydantic settings (browser, headless, .env)
├── pages/
│   ├── login_page.py           # Login page object
│   └── inventory_page.py       # Post-login inventory (product listing)
├── tests/
│   ├── conftest.py             # Fixtures: browser, sauce_demo_env, Allure screenshot on failure
│   ├── sauce_demo_env.py       # Typed env bundle for tests
│   └── test_sauce_demo_login.py  # Login + negative scenarios (markers: smoke / regression)
├── pytest.ini                  # Pytest defaults and marker registration
├── .env.example                # Template for environment variables (copy to `.env`)
├── Pipfile
├── Pipfile.lock
└── README.md
```

---

## Prerequisites

- **Python** 3.12 (see `Pipfile`; 3.10+ may work if you adjust `[requires]`)
- **Pipenv** for virtualenv and dependency locking

Install Pipenv globally if needed:

```bash
pip install pipenv
```

**Optional:** [Allure Commandline](https://github.com/allure-framework/allure2/releases) on your `PATH` to open HTML reports (`allure serve`).

---

## Installation

Clone the repository and install dependencies:

```bash
git clone <your-repo-url>
cd selenium_python_pom
pipenv install
```

Activate the project virtual environment:

```bash
pipenv shell
```

Optional — install **dev** packages (e.g. **pytest-xdist** for parallel runs):

```bash
pipenv install --dev
```

---

## Configuration

1. Copy the example file and adjust values:

   ```bash
   copy .env.example .env
   ```

   On Linux or macOS:

   ```bash
   cp .env.example .env
   ```

2. Edit `.env`. Supported keys include:

   | Variable | Description |
   |----------|-------------|
   | `URL` | Base URL (default: Sauce Demo) |
   | `USER` / `PASS` | Demo credentials (see Sauce Demo login page for accepted users) |
   | `browser` | `chrome`, `firefox`, or `edge` |
   | `headless` | `true` or `false` |

The application reads `.env` via **pydantic-settings** (`core/config/browser_config.py`). Tests load the same file through **`load_dotenv()`** in `tests/conftest.py` before reading `URL`, `USER`, and `PASS`.

---

## Usage

### Run all tests (console output)

```bash
pytest
```

Verbose output:

```bash
pytest -s -v
```

### Run a specific test file

```bash
pytest tests/test_sauce_demo_login.py -v
```

### Allure report (generate results)

```bash
pytest --alluredir=reports/allure-results
```

### View the Allure report

With Allure CLI installed:

```bash
allure serve reports/allure-results
```

### IDE (PyCharm / VS Code)

Open the test class or method and use the built-in **Run** action. Console output only unless you configure Allure as above.

---

## Test markers & parallel runs

Markers are defined in `pytest.ini` to avoid typos and `PytestUnknownMarkWarning`:

| Marker | Purpose |
|--------|---------|
| `smoke` | Fast critical path (e.g. successful login). |
| `regression` | Broader coverage, including invalid login and locked-out user. |

Examples:

```bash
# Smoke tests only (typical quick CI gate)
pytest -m smoke

# Full regression suite
pytest -m regression

# Everything except smoke (if you add more markers later)
pytest -m "not smoke"
```

### Parallel execution (`pytest-xdist`)

Install dev dependencies (includes **pytest-xdist**):

```bash
pipenv install --dev
```

Run tests in parallel (one worker process per CPU is a good default; tune for your machine):

```bash
pytest -n auto
```

Each test gets its own **function-scoped** `browser` fixture, so workers do not share a WebDriver session. If you add **session-scoped** drivers later, avoid `-n` unless you isolate per worker (e.g. separate profiles).

---

## CI/CD & GitHub Actions

The workflow [`.github/workflows/ci.yml`](.github/workflows/ci.yml) runs **pytest** with **Allure** on **Ubuntu**, installs **Google Chrome** (for Selenium), and builds `.env` from **repository variables** and **secrets** (with **defaults** so forks and first runs work without configuration).

### CI variables and secrets (optional)

Configure under **Settings → Secrets and variables → Actions**:

| Name | Type | Purpose | Default if unset |
|------|------|---------|------------------|
| `SAUCE_DEMO_URL` | Variable | Application base URL | `https://www.saucedemo.com` |
| `SAUCE_DEMO_USER` | Variable | Login username | `standard_user` |
| `SAUCE_DEMO_PASS` | **Secret** (recommended) or Variable | Login password | `secret_sauce` |
| `SAUCE_DEMO_BROWSER` | Variable | `chrome`, `firefox`, or `edge` | `chrome` |
| `SAUCE_DEMO_HEADLESS` | Variable | `true` or `false` | `true` |

**Password resolution order:** `SAUCE_DEMO_PASS` **secret** → `SAUCE_DEMO_PASS` **variable** → built-in default. Prefer a **secret** so the value is masked in logs and not shown in the Variables UI.

For the public Swag Labs demo, the defaults are the same values documented on the login page; override when you point CI at another environment.

### When it runs

| Trigger | Behavior |
|---------|----------|
| **Push** to `main` or `master` | Full test run; Allure HTML deployed to **GitHub Pages** (if configured). |
| **Pull request** into `main` or `master` | Full test run; Allure HTML uploaded as a **workflow artifact** (download from the Actions run). Pages is **not** updated from PRs (avoids overwriting the live report with unmerged code). |
| **Schedule** | Twice per month (`06:00 UTC` on the **1st and 15th**) — approximate “every ~14 days”. Adjust the cron expression in the workflow if you need a different cadence. |
| **workflow_dispatch** | Manual run from the **Actions** tab. |

The workflow is designed so **Allure is generated whether tests pass or fail** (with a fallback HTML page if report generation itself fails).

### One-time repository setup (GitHub UI)

1. **Actions permissions**  
   **Settings → Actions → General → Workflow permissions** → select **Read and write permissions** (required for uploading the Pages artifact and for default `GITHUB_TOKEN` behavior in some setups).

2. **GitHub Pages**  
   **Settings → Pages → Build and deployment** → **Source**: **GitHub Actions** (not “Deploy from a branch” for this workflow).

3. After the first successful deployment job, the Pages URL appears in the **deploy** job log and under **Settings → Pages**. It usually looks like:

   `https://<user>.github.io/<repository>/`

4. Update the **CI badge** at the top of this README: replace `YOUR_GITHUB_USER/YOUR_REPO_NAME` with your real `owner/repo` path.

### Where to open the Allure report (GitHub Pages URL)

The CI workflow publishes the **static Allure HTML** to your repo’s **GitHub Pages** site. The report is served at the **root** of that site (same as `index.html` generated by Allure).

| Your repository | Typical URL for the live Allure report |
|-------------------|----------------------------------------|
| `https://github.com/<owner>/<repo>` | `https://<owner>.github.io/<repo>/` |

**Example for this project:** if the repository is `github.com/YOUR_GITHUB_USER/selenium_python_pom`, open:

```text
https://YOUR_GITHUB_USER.github.io/selenium_python_pom/
```

Replace `YOUR_GITHUB_USER` with your GitHub username (or organization name). The **repository name** in the path must match the repo slug exactly (e.g. `selenium_python_pom`).

**How to confirm the exact URL after a run**

1. **Actions** → open the **CI** workflow run → job **Deploy Allure to GitHub Pages** → check the **`github-pages` environment** link or the step output (often labeled **page_url**).
2. **Settings → Pages** → **Visit site** (shown once Pages has been deployed at least once).

**Note:** Pull requests do not update this URL; only runs on the **default branch** (push / schedule / manual dispatch) refresh the published report.

### Artifacts vs Pages

- **Pull requests:** Download the **`allure-report`** zip from the workflow run summary (**Artifacts** section).
- **Default branch:** Same artifact is available, and the report is also deployed to **GitHub Pages** when the deploy job completes (only on **push** / **schedule** / **workflow_dispatch** to the repository **default branch**, not from PR workflows).

### Troubleshooting: “Deploy” / Allure on Pages did not run

1. **Pull request** — By design, **deploy** is skipped on `pull_request` events. Merge to the default branch or use **workflow_dispatch** on that branch to publish Pages.
2. **Wrong branch** — Deploy runs only when `github.ref` is the **default branch** (e.g. `Settings → General → Default branch`). Pushes to feature branches run **build** + artifact, but **not** Pages upload/deploy.
3. **Build job failed** — If **install**, **Chrome**, **pipenv**, or **Upload Pages artifact** fails, `needs.build.result` is not `success` and **deploy** is skipped. Open the **build** job log.
4. **Environment protection** — If **github-pages** has **required reviewers**, the **deploy** job waits until approved (**Actions** → waiting job).
5. **Pages source** — **Settings → Pages** must use **GitHub Actions** as the build source.

### MCP / API

No extra MCP configuration is required in the repository for CI: everything is standard **GitHub Actions** YAML. If you use the **GitHub MCP** in Cursor for other tasks, it does not need new files here—ensure the token can read Actions if you automate status checks.

---

## Security & best practices

For this **educational demo**, a local `.env` may hold credentials that work against the public Swag Labs test site. In **production** or **shared CI**, do **not** commit real secrets or store them in plain text in the repository.

- In **GitHub Actions**, use **Actions secrets** (e.g. `SAUCE_DEMO_PASS`) and **repository variables** as documented in [CI variables and secrets](#ci-variables-and-secrets-optional).
- Prefer **secret stores** (cloud provider, vault) or **CI/CD environment variables** injected at runtime with least privilege.
- The `.env` file is listed in `.gitignore` to reduce accidental commits. Use `.env.example` as the only tracked template.
- If a secret was ever committed, rotate it and consider history cleanup (`git filter-repo` or similar).

---

## License

This project is released under the [MIT License](LICENSE).
