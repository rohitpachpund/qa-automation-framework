from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


COMMON_USER = {
    "name": "Automation Tester",
    "company": "Automation QA Labs",
    "email": "automation.tester@example.com",
    "phone": "9876543210",
    "designation": "QA Automation Engineer",
    "country": "India",
}


CONTACT_FORM_DATA = {
    **COMMON_USER,
    "message": "This is a test enquiry submitted by Playwright automation.",
}


CAREERS_FORM_DATA = {
    "name": COMMON_USER["name"],
    "email": COMMON_USER["email"],
    "country": COMMON_USER["country"],
    "phone": COMMON_USER["phone"],
    "position": "QA Automation Engineer",
    "resume_path": str(Path("/home/rohit/Downloads") / "sample.pdf"),
}


RESELLER_FORM_DATA = {
    **COMMON_USER,
    "message": "This is a test reseller enquiry submitted by Playwright automation.",
}
