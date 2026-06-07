if __name__ == "__main__":
    raise SystemExit("Run this test with Pytest from the project root: python -m pytest tests/test_reseller_form.py")

from pages.reseller_page import ResellerPage
from utils.test_data import RESELLER_FORM_DATA


def test_reseller_form_submission(page):
    reseller_page = ResellerPage(page)

    reseller_page.load()
    reseller_page.submit_form(RESELLER_FORM_DATA)
    reseller_page.validate_successful_submission()
