# Polaris Form Automation

Python Playwright automation framework for Polaris Market Research forms using Pytest and the Page Object Model pattern.

## Project Structure

```text
Polaris Form Automation/
├── pages/
│   ├── base_page.py
│   ├── contact_page.py
│   ├── careers_page.py
│   └── reseller_page.py
├── tests/
│   ├── conftest.py
│   ├── test_contact_form.py
│   ├── test_careers_form.py
│   └── test_reseller_form.py
├── utils/
│   ├── sample_resume.txt
│   └── test_data.py
├── config.py
├── playwright.config.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## Setup

```bash
cd "/home/rohit/Desktop/Polaris Form Automation"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install
```

## Run Tests

```bash
cd "/home/rohit/Desktop/Polaris Form Automation"
python -m pytest
```

Run a specific form test:

```bash
python -m pytest tests/test_contact_form.py
python -m pytest tests/test_careers_form.py
python -m pytest tests/test_reseller_form.py
```

Generate an HTML report:

```bash
python -m pytest --html=reports/report.html --self-contained-html
```

Do not run test files directly with `python tests/test_contact_form.py`.
Pytest must collect the tests so fixtures, package imports, and reporting work correctly.

## Current Locators

Form locators are stored in their page objects:

- `pages/contact_page.py`
- `pages/careers_page.py`
- `pages/reseller_page.py`

Reusable actions live in `pages/base_page.py`, including:

- `fill_input()`
- `select_dropdown()`
- `upload_file()`
- `fill_common_fields()`

Common IDs currently used across the form page objects:

- `#name`
- `#company`
- `#email`
- `#phone`
- `#designation`
- `#country`
- `#message`
- `button[type='submit']:has-text('Submit')`

Careers resume upload uses the provided label XPath and resolves the associated file input for Playwright upload.

## Common Errors

If you see `ModuleNotFoundError: No module named 'pytest'`, activate the virtual environment and install requirements:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

If you see `ModuleNotFoundError: No module named 'pages'`, run tests with Pytest from the project root:

```bash
cd "/home/rohit/Desktop/Polaris Form Automation"
python -m pytest
```
