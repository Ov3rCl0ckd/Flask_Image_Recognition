# Assignment 2 Report: Software Quality III - Build and Release (CSCN73010)

**Student Name / ID:** [Your Name / ID]  
**Course:** Software Quality III: Build and Release (CSCN73010)  
**Repository Link:** [https://github.com/Sachin-crypto/Flask_Image_Recognition](https://github.com/Sachin-crypto/Flask_Image_Recognition)  

---

## 1. Project Setup and Local Execution Summary
To set up and run the legacy Flask Image Recognition application locally:
1. **Clone the Repository:** 
   ```bash
   git clone https://github.com/Sachin-crypto/Flask_Image_Recognition.git
   cd Flask_Image_Recognition
   ```
2. **Create and Activate Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\Activate.ps1
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Application:**
   ```bash
   flask --app app.py run --debug
   ```
5. **Usage:** Open `http://127.0.0.1:5000` (or port 9000 as configured in `app.py`), upload an image from the `test_images/` directory, and view the predicted hand sign digit.

---

## 2. Legacy Code & Architecture Exploration
- **`app.py`**: The core Flask web server handling routing (`/` for home page and `/prediction` for processing image uploads via POST).
- **`model.py`**: Handles loading the Keras deep learning model (`digit_model.h5`), image resizing, normalization, array conversion, and prediction inference.
- **`conftest.py`**: Defines pytest fixtures (such as `client`) for testing Flask routes.
- **Test Files (`test_model.py`, `test_acceptance_*.py`, `test_integration_*.py`)**: Comprehensive test suite covering unit tests, integration tests, and acceptance tests for happy paths and edge cases.

### Architecture Flow
1. **Client / Browser**: User interacts with the HTML web interface (`templates/index.html`) and uploads an image file.
2. **Flask Route (`/prediction`)**: Receives the file stream and passes it to `preprocess_img`.
3. **Preprocessing (`model.py`)**: Opens the image using Pillow, resizes it to `(224, 224)`, normalizes pixel values (`/ 255.0`), and reshapes into `(1, 224, 224, 3)`.
4. **Model Inference**: The preprocessed tensor is passed to the Keras model (`digit_model.h5`), returning class probabilities via `np.argmax`.
5. **Response**: The prediction result is rendered and displayed to the user via `templates/result.html`.

---

## 3. Pylint and Pre-commit Configuration
- **Pylint (`.pylintrc`)**: Configured to enforce PEP 8 style guidelines, detect code smells, and ensure code cleanliness. Initial analysis identified missing module/function docstrings and a bare `except:` block.
- **Code Quality Improvements**:
  - Added descriptive docstrings to `app.py` and `model.py`.
  - Replaced bare ` except:` with specific exception handling (` except Exception:`).
  - Ensured consistent return paths across functions.
  - Achieved a Pylint score of **9.68/10**.
- **Pre-commit (`.pre-commit-config.yaml`)**: Configured hooks for automatic checks (trailing whitespace removal, end-of-file fixer, YAML syntax check) before commits are finalized.

---

## 4. Pytest Automated Test Suite
The test suite consists of **17 tests** covering:
- **Acceptance Tests**: Successful image upload (`test_acceptance_happy.py`), missing file handling (`test_acceptance_sad.py`), and edge cases (`test_acceptance_edge_cases.py`).
- **Integration Tests**: End-to-end route testing (`test_integration_happy.py` and `test_integration_sad.py`).
- **Model Tests**: Preprocessing shape validation, normalization range check (`0` to `1`), prediction class integer type verification, and consistency checks (`test_model.py`).

**Local Execution Result:**
```bash
$ python -m pytest
============================= test session starts =============================
platform win32 -- Python 3.11.0, pytest-8.3.3
collected 17 items

test_acceptance_edge_cases.py ......                                     [ 35%]
test_acceptance_happy.py ...                                             [ 52%]
test_acceptance_sad.py .                                                 [ 58%]
test_integration_happy.py .                                              [ 64%]
test_integration_sad.py .                                                [ 70%]
test_model.py .....                                                      [100%]

============================= 17 passed in 5.33s ==============================
```

---

## 5. GitHub Actions CI/CD Pipeline
A GitHub Actions workflow (`.github/workflows/ci.yml`) was established to automate quality control on every push and pull request:
- **Steps executed**:
  1. Checks out repository code.
  2. Sets up Python 3.11 environment.
  3. Installs dependencies (`requirements.txt`, `pylint`).
  4. Runs Pylint code quality checks (`pylint app.py model.py`).
  5. Executes pytest test suite (`pytest`).
- **CI Progression**: Initial workflow runs identified linter warnings and missing dependencies, which were iteratively corrected through local linting and dependency pinning, resulting in a robust, passing CI pipeline.
