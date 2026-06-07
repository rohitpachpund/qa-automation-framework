from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class CareersPage(BasePage):
    """Page object for the Polaris Careers form."""

    URL = "https://dev.polarismarketresearch.com/careers"
    NAME_INPUT = "#name"
    EMAIL_INPUT = "#email"
    COUNTRY_DROPDOWN = "#country"
    PHONE_INPUT = "#phone"
    POSITION_INPUT = "#position"
    RESUME_UPLOAD_LABEL = (
        "xpath=/html/body/div[2]/main/section[4]/div/div/div/form/div[2]/div[5]/div/label[1]"
    )
    SUBMIT_BUTTON = "button[type='submit']:has-text('Submit')"
    SUCCESS_MESSAGE = ".toast-success, .success-message, [role='alert']"
    ERROR_MESSAGE = ".error, .invalid-feedback, .field-error"

    COMMON_FIELD_LOCATORS = {
        "name": NAME_INPUT,
        "email": EMAIL_INPUT,
        "country": COUNTRY_DROPDOWN,
        "phone": PHONE_INPUT,
        "position": POSITION_INPUT,
    }
    REQUIRED_FIELDS = ("name", "email", "country", "phone", "position")

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def load(self) -> None:
        self.navigate(self.URL)

    def submit_careers_form(self, data: dict[str, str]) -> None:
        self.fill_common_fields(self.COMMON_FIELD_LOCATORS, data, self.REQUIRED_FIELDS)
        self.upload_file(self.RESUME_UPLOAD_LABEL, data["resume_path"])
        self.click_submit(self.SUBMIT_BUTTON)

    def submit_form(self, data: dict[str, str]) -> None:
        self.submit_careers_form(data)

    def validate_successful_submission(self) -> None:
        self.wait_for_success_message(self.SUCCESS_MESSAGE)
        self.assert_no_error_state(self.ERROR_MESSAGE)
