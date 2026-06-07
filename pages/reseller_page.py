from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class ResellerPage(BasePage):
    """Page object for the Polaris Reseller form."""

    URL = "https://dev.polarismarketresearch.com/reseller"
    NAME_INPUT = "#name"
    COMPANY_INPUT = "#company"
    EMAIL_INPUT = "#email"
    COUNTRY_DROPDOWN = "#country"
    PHONE_INPUT = "#phone"
    MESSAGE_TEXTAREA = "#message"
    SUBMIT_BUTTON = "button[type='submit']:has-text('Submit')"
    SUCCESS_MESSAGE = ".toast-success, .success-message, [role='alert']"
    ERROR_MESSAGE = ".error, .invalid-feedback, .field-error"

    COMMON_FIELD_LOCATORS = {
        "name": NAME_INPUT,
        "company": COMPANY_INPUT,
        "email": EMAIL_INPUT,
        "country": COUNTRY_DROPDOWN,
        "phone": PHONE_INPUT,
        "message": MESSAGE_TEXTAREA,
    }
    REQUIRED_FIELDS = ("name", "company", "email", "country", "phone", "message")

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def load(self) -> None:
        self.navigate(self.URL)

    def submit_reseller_form(self, data: dict[str, str]) -> None:
        self.fill_common_fields(self.COMMON_FIELD_LOCATORS, data, self.REQUIRED_FIELDS)
        self.click_submit(self.SUBMIT_BUTTON)

    def submit_form(self, data: dict[str, str]) -> None:
        self.submit_reseller_form(data)

    def validate_successful_submission(self) -> None:
        self.wait_for_success_message(self.SUCCESS_MESSAGE)
        self.assert_no_error_state(self.ERROR_MESSAGE)
