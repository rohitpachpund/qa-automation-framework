if __name__ == "__main__":
    raise SystemExit("Run this test with Pytest from the project root: python -m pytest tests/test_careers_form.py")

from pages.careers_page import CareersPage
from utils.test_data import CAREERS_FORM_DATA


def test_careers_form_submission(page):
    careers_page = CareersPage(page)

    careers_page.load()
    careers_page.submit_form(CAREERS_FORM_DATA)
    careers_page.validate_successful_submission()
