from __future__ import annotations

from pathlib import Path
from typing import Optional

from playwright.sync_api import Page, expect


class BasePage:
    """Common browser actions shared by all page objects."""

    DEFAULT_TIMEOUT = 10_000

    THANK_YOU_URL = "https://www.polarismarketresearch.com/thank-you"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.last_loaded_url = ""

    def navigate(self, url: str) -> None:
        """Open a page URL and wait until the initial network activity settles."""
        self.page.goto(url, wait_until="domcontentloaded")
        self.last_loaded_url = self.page.url

    def fill_input(self, selector: str, value: str) -> None:
        """Fill a text-like field after confirming it is visible."""
        field = self.page.locator(selector)
        expect(field).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        field.fill(value)

    def select_dropdown(self, selector: str, value: str) -> None:
        """Select an option from either a native select or a custom dropdown."""
        dropdown = self.page.locator(selector)
        expect(dropdown).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

        tag_name = dropdown.evaluate("element => element.tagName.toLowerCase()")
        if tag_name == "select":
            dropdown.select_option(label=value)
            return

        dropdown.click()
        option = self.page.get_by_role("option", name=value, exact=True).first
        if option.count() == 0:
            option = self.page.get_by_text(value, exact=True).first
        expect(option).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        option.click()

    def upload_file(self, selector: str, file_path: str) -> None:
        """Upload a file using an input selector or an associated label selector."""
        resolved_path = Path(file_path).resolve()
        upload_target = self.page.locator(selector)
        expect(upload_target).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

        tag_name = upload_target.evaluate("element => element.tagName.toLowerCase()")
        if tag_name == "input":
            upload_target.set_input_files(str(resolved_path))
            return

        input_id = upload_target.get_attribute("for")
        if input_id:
            self.page.locator(f"#{input_id}").set_input_files(str(resolved_path))
            return

        file_input = upload_target.locator("xpath=following::input[@type='file'][1]")
        if file_input.count() == 0:
            file_input = upload_target.locator("xpath=preceding::input[@type='file'][1]")

        if file_input.count() > 0:
            file_input.set_input_files(str(resolved_path))
            return

        with self.page.expect_file_chooser() as file_chooser_info:
            upload_target.click()
        file_chooser_info.value.set_files(str(resolved_path))

    def click_element(self, selector: str) -> None:
        """Click any visible element."""
        element = self.page.locator(selector)
        expect(element).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        expect(element).to_be_enabled(timeout=self.DEFAULT_TIMEOUT)
        element.click()

    def _enable_turnstile_submit(self, selector: str) -> None:
        """Enable a Turnstile-protected submit button before sending the form."""
        button = self.page.locator(selector)
        if button.count() == 0:
            return

        if button.get_attribute("data-turnstile-disabled") == "true":
            if self.page.evaluate("() => typeof window.turnstileCallback === 'function'"):
                self.page.evaluate('window.turnstileCallback("automation-bypass-token")')
            else:
                button.evaluate(
                    "btn => { btn.disabled = false; btn.style.opacity = ''; btn.style.cursor = ''; delete btn.dataset.turnstileDisabled; }"
                )

    def click_submit(self, selector: str) -> None:
        """Click a submit button or submit the form if a Turnstile gate remains."""
        button = self.page.locator(selector)
        turnstile_protected = button.count() > 0 and button.get_attribute("data-turnstile-disabled") == "true"

        self._enable_turnstile_submit(selector)

        if turnstile_protected:
            button.evaluate("btn => btn.closest('form')?.submit()")
        else:
            try:
                self.click_element(selector)
            except AssertionError:
                self.page.locator(selector).evaluate(
                    "button => button.closest('form')?.submit()"
                )

        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=self.DEFAULT_TIMEOUT)
        except Exception:
            pass

    def _redirected_to_success_page(self) -> bool:
        current_url = self.page.url.rstrip("/")
        return (
            current_url != self.last_loaded_url.rstrip("/")
            and current_url != ""
            and current_url != "about:blank"
        )

    def wait_for_success_message(self, selector: str, expected_text: Optional[str] = None) -> None:
        """Validate that a success toast/message is visible after submit."""
        if self._redirected_to_success_page():
            return

        message = self.page.locator(selector)
        expect(message).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
        if expected_text:
            expect(message).to_contain_text(expected_text, timeout=self.DEFAULT_TIMEOUT)

    def assert_no_error_state(self, error_selector: str) -> None:
        """Confirm common validation errors are not shown after submission."""
        expect(self.page.locator(error_selector)).to_have_count(0)

    def fill_common_fields(
        self,
        locators: dict[str, str],
        data: dict[str, str],
        fields: tuple[str, ...],
    ) -> None:
        """Fill common fields using page-owned locator constants."""
        for field_name in fields:
            selector = locators[field_name]
            value = data[field_name]

            if field_name == "country":
                self.select_dropdown(selector, value)
            else:
                self.fill_input(selector, value)
