if __name__ == "__main__":
    raise SystemExit("Run this test with Pytest from the project root: python -m pytest tests/test_contact_form.py")

from pages.contact_page import ContactPage
from utils.test_data import CONTACT_FORM_DATA


def test_contact_form_submission(page):
    contact_page = ContactPage(page)

    contact_page.load()
    contact_page.submit_form(CONTACT_FORM_DATA)
    contact_page.validate_successful_submission()
