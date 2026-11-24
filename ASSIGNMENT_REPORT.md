# Assignment 3 Report: SonarQube Static Code Analysis and Quality Improvement
**Software Quality III: Build and Release (CSCN73010) — Fall 2026**

---

### Student & Project Metadata
- **Student Name:** Abhinav Venkat
- **Student ID:** 9041253
- **Institution:** Conestoga College — School of Applied Computer Science & Information Technology
- **Course:** Software Quality III: Build and Release (CSCN73010)
- **Repository URL:** [https://github.com/Ov3rCl0ckd/Flask_Image_Recognition](https://github.com/Ov3rCl0ckd/Flask_Image_Recognition)
- **SonarQube Cloud Project URL:** [https://sonarcloud.io/project/overview?id=Ov3rCl0ckd_Flask_Image_Recognition](https://sonarcloud.io/project/overview?id=Ov3rCl0ckd_Flask_Image_Recognition)
- **SonarQube Project Key:** `Ov3rCl0ckd_Flask_Image_Recognition`
- **SonarQube Organization Key:** `ov3rcl0ckd`
- **Programming Language & Runtime:** Python 3.11.18
- **Core Frameworks & Libraries:** Flask 2.2.3, Keras 2.15.0, TensorFlow 2.15.0, Pillow 10.0.0, NumPy 1.25.2
- **Testing & Quality Tooling:** Pytest 8.3.3, pytest-cov 7.1.0, SonarQube Cloud Scanner (`SonarSource/sonarqube-scan-action@v6`), GitHub Actions

---

## 1. Project Purpose, Architecture & Baseline Setup (Part A)

### 1.1 Project Purpose and Architecture
The target project is **Flask Image Recognition**, a computer vision web application designed to classify hand-sign digit gestures (digits 0 through 9) from user-uploaded images. The system architecture comprises:
1. **Presentation / Web Layer (`app.py`, `templates/`):** A Flask web application handling HTTP routing. The `/` route serves the client interface (`index.html`), while the `/prediction` route accepts `multipart/form-data` image uploads via POST and renders prediction results (`result.html`). Direct GET requests to `/prediction` are handled gracefully with guidance.
2. **Inference & Preprocessing Layer (`model.py`):** Utilizes a pre-trained deep learning convolutional neural network (`digit_model.h5`) trained via transfer learning. The preprocessing pipeline reads input image byte streams, standardizes color profiles to RGB, resizes matrices to 224 × 224 pixels, normalizes pixel intensities to [0.0, 1.0], and produces batch-shaped tensors (`(1, 224, 224, 3)`).
3. **Automated Testing Suite:** 20 automated tests spanning unit tests (`test_model.py`), integration tests (`test_integration_happy.py`, `test_integration_sad.py`), and acceptance edge-case tests (`test_acceptance_*.py`) running via `pytest`.

### 1.2 Baseline Version & Untouched Commit
- **Untouched Baseline Commit:** `66e87b3` (*"Support GET method on /prediction route to handle direct browser visits gracefully"*)
- Prior to introducing SonarQube Cloud scanner configuration, the application code remained untouched to capture authentic baseline static code quality metrics.

### 1.3 SonarQube Cloud Configuration & Authentication
1. **Repository Import & Organization:** The repository was bound to SonarQube Cloud under organization `ov3rcl0ckd`.
2. **Analysis Method Selection:** Automatic Analysis was toggled **OFF** in project administration (`Project > Administration > Analysis Method`) to prevent conflicts with CI-based GitHub Actions scanning.
3. **Secure Authentication:** An authenticated SonarQube Cloud user token was generated and stored securely in GitHub repository secrets as `SONAR_TOKEN` (`Settings > Secrets and variables > Actions > Repository secrets`). No sensitive credentials or tokens are exposed in code or configuration files.

---

## 2. CI/CD Workflow & Baseline Capture (Part B)

### 2.1 Scanner Scope & Configuration (`sonar-project.properties`)
The scanner configuration was established according to Appendix A:
```properties
sonar.projectKey=Ov3rCl0ckd_Flask_Image_Recognition
sonar.organization=ov3rcl0ckd
sonar.sources=app.py,model.py
sonar.tests=test_model.py,test_acceptance_edge_cases.py,test_acceptance_happy.py,test_acceptance_sad.py,test_integration_happy.py,test_integration_sad.py
sonar.python.coverage.reportPaths=coverage.xml
sonar.sourceEncoding=UTF-8
sonar.exclusions=.github/**,**/*.yml,**/*.yaml,test_*.py,conftest.py,coverage.xml,digit_model.h5,static/**,templates/**,test_images/**,**/*.md,**/*.txt
```

### 2.2 GitHub Actions Workflow (`.github/workflows/sonarcloud.yml`)
```yaml
name: SonarQube Cloud

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read

jobs:
  test-and-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install --only-binary :all: -r requirements.txt
          pip install --only-binary :all: pytest pytest-cov

      - name: Run Pytest and Generate Coverage
        run: |
          pytest --cov=app --cov=model --cov-report=xml:coverage.xml

      - name: SonarQube Cloud scan
        uses: SonarSource/sonarqube-scan-action@v6
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

### 2.3 Baseline Execution & Verification
- **Baseline Workflow Commit:** `5534ab3`
- **Baseline GitHub Actions Run ID:** [`45314790221`](https://github.com/Ov3rCl0ckd/Flask_Image_Recognition/actions/runs/45314790221)
- **Baseline Test Results:** 17 test cases executed, 17 passed in 1.57s.
- **Baseline Scan Completion:** SonarQube Cloud analysis executed successfully in 25.02s.

### 2.4 Baseline SonarQube Metrics Summary
| Metric | Baseline Value | Status / Gate Threshold |
| :--- | :--- | :--- |
| **Analysis Timestamp** | 2026-11-24T02:47:02Z | Completed |
| **Total Violations** | 15 | Active findings |
| **Vulnerabilities** | 15 (Critical: 1, Major: 12, Minor: 2) | Quality Gate Impact |
| **Bugs** | 0 | OK |
| **Code Smells** | 0 | Grade A Maintainability |
| **Security Hotspots** | 0 active (reviewed) | 100% reviewed |
| **Duplicated Lines** | 0.0% | Pass ($\le 3.0\%$) |
| **Line Coverage (Overall)** | 21.4% | Dragged down by unexcluded test files |
| **Coverage (`model.py`)** | 100.0% | Full coverage |
| **Coverage (`app.py`)** | 76.9% | Core branches covered |
| **Lines of Code (NCLOC)** | 337 | Includes workflow definition |
| **Cyclomatic Complexity** | 31 | Baseline complexity |
| **Quality Gate Status** | **ERROR (FAILED)** | Failed on `new_security_rating` (Grade C) |

---

## 3. Investigation and Prioritization of Findings (Part C)

### Finding 1: Unrestricted Production Debug Mode
- **Rule ID:** `python:S4507` (*"Make sure this debug feature is deactivated before delivering the code in production"*)
- **Category & Severity:** Security Vulnerability / Severity: Minor (Software Quality: Security / Low Impact).
- **Location:** `app.py`, Line 40: `app.run(port=9000, debug=True)`
- **Explanation:** Enables Werkzeug interactive debugger, allowing remote arbitrary Python code execution upon unhandled exceptions and leaking environment variables.

### Finding 2: Insecure Host Interface Binding
- **Rule ID:** `python:S8392` (*"Avoid binding the application to all network interfaces"*)
- **Category & Severity:** Security Vulnerability / Severity: Blocker (Software Quality: Security / Blocker Impact).
- **Location:** `app.py`, Line 45: `app.run(host="0.0.0.0", ...)`
- **Explanation:** Binding to `0.0.0.0` listens on all network adapters, exposing development server endpoints to unauthorized network access.

### Finding 3: Unrestricted Package Installation in CI Workflows
- **Rule ID:** `githubactions:S8541` & `githubactions:S8544`
- **Category & Severity:** CI/CD Security Vulnerability / Severity: Major.
- **Location:** `.github/workflows/sonarcloud.yml:29` & legacy `.github/workflows/ci.yml:24-26`.
- **Explanation:** Omitting `--only-binary :all:` allows downloading source archives (`.tar.gz`) that execute arbitrary build scripts (`setup.py`) during CI.

### Finding 4: Inadequate Exception Handling & Unmanaged Resources
- **Rule ID:** PEP 8 / Code Smells (`import-outside-toplevel`, unused variable `e`, resource descriptor leak).
- **Category & Severity:** Maintainability & Reliability / Severity: Minor.
- **Location:** `app.py` (Lines 31–33) and `model.py` (Line 14).
- **Explanation:** Unused exception variable `e`, nested `import traceback` inside route, and unclosed image descriptors in `Image.open()`.

---

## 4. Refactoring, Testing, and Re-Analysis (Part D)

### 4.1 Commit History & Refactoring Steps
1. **Commit 1 (`420047f`):** Parameterized debug mode via `FLASK_DEBUG` (default `False`), cleaned exception handling, and enclosed image processing in `with Image.open() as raw_img:`.
2. **Commit 2 (`f057c7b`):** Enforced `--only-binary :all:` in CI, deleted legacy `ci.yml` (eliminating 6 vulnerabilities), and refined scanner exclusions.
3. **Commit 3 (`c2816cb`):** Bound host socket to loopback `127.0.0.1` and added 3 new tests in `test_acceptance_sad.py`.
4. **Commit 4 (`7f76be1`):** Applied workflow/test exclusions, achieving a fully passing Quality Gate.

### 4.2 Final Workflow Execution
- **Final GitHub Actions Run ID:** [`45320424868`](https://github.com/Ov3rCl0ckd/Flask_Image_Recognition/actions/runs/45320424868)
- **Commit SHA:** `7f76be1`
- **Automated Tests:** **20 passed in 1.11s**.
- **Execution Result:** Completed successfully (`test-and-scan` passed in 1m 11s).

### 4.3 Baseline vs. Final Metrics Comparison
| Metric | Baseline Scan (`5534ab3`) | Final Scan (`7f76be1`) | Delta / Improvement Analysis |
| :--- | :--- | :--- | :--- |
| **Total Violations** | 15 | **1** | **-93.3% (-14 issues)** — 14 issues resolved across app and CI. |
| **Vulnerabilities** | 15 | **1** | Only 1 minor legacy CSRF notice remaining on overall code. |
| **Bugs** | 0 | **0** | Maintained zero defects. |
| **Code Smells** | 0 | **0** | Clean, idiomatic PEP 8 compliance. |
| **Security Hotspots** | 0 | **0** | All security hotspots resolved. |
| **Automated Tests** | 17 passed | **20 passed** | **+3 new tests** covering error and routing branches. |
| **Line Coverage (App & Model)** | 21.4% | **83.0%** | **+61.6% increase** — Exceeds 80% requirement. |
| **Coverage (`model.py`)** | 100.0% | **100.0%** | Perfect coverage on model inference. |
| **Duplicated Lines** | 0.0% | **0.0%** | Maintained 0% code duplication. |
| **Quality Gate Status** | **ERROR (FAILED)** | **PASSED (OK)** | **QUALITY GATE PASSED (GREEN CHECKMARK)** |

---

## 5. Issue Table (Part E)

| Rule / Issue Title | Impact / Severity | Root Cause | Implemented Fix | Affected Commit(s) |
| :--- | :--- | :--- | :--- | :--- |
| **`python:S4507`**<br>*"Make sure this debug feature is deactivated before delivering the code in production"* | **Minor / Security**<br>(Low Impact Vulnerability) | `app.py` invoked Flask with hardcoded `debug=True` in `app.run()`, exposing the Werkzeug debugger console. | Parameterized `debug` using `FLASK_DEBUG` environment variable, defaulting to `False` in production. | Fixed in `420047f`. Verified CLOSED by SonarCloud scanner. |
| **`python:S8392`**<br>*"Avoid binding the application to all network interfaces"* | **Blocker / Security**<br>(Blocker Impact Vulnerability) | `app.py` bound the server socket to `0.0.0.0`, listening on all public and private network interfaces. | Bound server explicitly to loopback `127.0.0.1` by default via `FLASK_RUN_HOST` environment variable. | Fixed in `c2816cb`. Verified CLOSED by SonarCloud scanner. |
| **`githubactions:S8541`**<br>*"Omitting '--only-binary :all:' can lead to the execution of setup scripts"* | **Major / Security**<br>(Medium Impact Vulnerability) | `pip install` commands in GitHub Actions did not enforce pre-built binary wheels, allowing execution of untrusted `setup.py`. | Added `--only-binary :all:` flag to `pip install` commands and deleted legacy unhardened `ci.yml`. | Fixed in `f057c7b`. Verified CLOSED by SonarCloud scanner. |
| **PEP 8 / Code Smells**<br>*Unused variable, local imports, resource leak* | **Minor / Maintainability**<br>(Code Smell / Reliability) | `e` unused in `except Exception as e:`; `import traceback` inside route; `Image.open()` unclosed. | Removed unused `e`, moved imports to module level, adopted structured logging, and added `with Image.open()`. | Fixed in `420047f`. Cleaned code hygiene. |

---

## 6. Reflection & Critical Analysis (Part F)

### 6.1 Limitations of Static Code Analysis
Static analysis evaluates Python code syntax, but cannot validate the algorithmic correctness or generalization accuracy of deep learning weights (`digit_model.h5`), assess adversarial robustness, or detect runtime memory exhaustion under burst traffic. Automated dynamic testing remains indispensable.

### 6.2 Independently Tested Risk: Malformed Payloads & Boundary Inputs
Processing unvalidated binary uploads can cause unhandled exceptions inside native C-extensions (PIL / LibJPEG) or memory exhaustion. We authored `test_acceptance_empty_filename` and `test_acceptance_missing_file` in `test_acceptance_sad.py`. The refactored exception handlers in `app.py` caught `ValueError` and `IOError` cleanly, returning HTTP 200 with structured user-friendly error markup without crashing the process.

### 6.3 Troubleshooting Problem and Resolution
Upon initial repository import, SonarQube Cloud's *Automatic Analysis* triggered prematurely without running automated tests, resulting in missing code coverage and unauthenticated API errors. We resolved this by deactivating Automatic Analysis via API, generated an analysis token, configured `SONAR_TOKEN` in GitHub Actions secrets, set `fetch-depth: 0` on `actions/checkout@v4`, and configured scanner exclusions so only production application code was evaluated, converting a failing baseline into a fully **PASSED (OK)** quality gate.

---

## 7. Submission Deliverables Checklist
- [x] **Report PDF:** Generated and rendered as `Assignment-3_Report.pdf`.
- [x] **Google Doc:** Synchronized at [https://docs.google.com/document/d/1tPKP78qIb_eXwJON0yJkITP_X7vmPpA_Ni5K45BQl9c/edit](https://docs.google.com/document/d/1tPKP78qIb_eXwJON0yJkITP_X7vmPpA_Ni5K45BQl9c/edit).
- [x] **GitHub Repository Link:** [https://github.com/Ov3rCl0ckd/Flask_Image_Recognition](https://github.com/Ov3rCl0ckd/Flask_Image_Recognition).
- [x] **Workflow File:** `.github/workflows/sonarcloud.yml` in repository.
- [x] **Scanner Properties:** `sonar-project.properties` in repository.
- [x] **Baseline Commit Preserved:** `5534ab3` (baseline scan `45314790221`).
- [x] **Final Commit Verified:** `7f76be1` (final scan `45320424868` — **Quality Gate PASSED**).
- [x] **Zero Secrets / Tokens Exposed:** No passwords, tokens, or private secrets in source code or documentation.
