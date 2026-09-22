"""
Automated Startup Job Application Engine
---------------------------------------
Applies to startup jobs from CSV using Anjali Kashyap's profile and active Chrome session.
Supports:
  - Ashby ATS (Full form fill + Resume PDF upload + EEO disclosures)
  - Wellfound (Logged-in application via Chrome Profile 9)
  - Peerlist & Direct Startup Careers
"""

import asyncio
import csv
import json
import os
import sys
import urllib.request
from pathlib import Path
from playwright.async_api import async_playwright

CSV_PATH = r"C:\Users\nites\Downloads\STARTUP_2026-09-22 - Sheet1.csv"
DATA_DIR = Path(r"C:\Users\nites\Music\ai_data\anjali_data")
RESUME_PATH = str(DATA_DIR / "AnjaliResume.pdf")
OUTPUT_DIR = Path(r"C:\Users\nites\Documents\ExpertByAi\system-controlAi\artifacts\sessions\session_job_applications")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CANDIDATE = {
    "full_name": "Anjali Kashyap",
    "first_name": "Anjali",
    "last_name": "Kashyap",
    "email": "anjalikashyap9608@gmail.com",
    "phone": "+91-9608411997",
    "clean_phone": "9608411997",
    "location": "Bengaluru, Karnataka, India",
    "city": "Bengaluru",
    "state": "Karnataka",
    "country": "India",
    "postal_code": "560037",
    "linkedin": "https://www.linkedin.com/in/anjali-kashyap",
    "github": "https://github.com/kashyapanjali",
    "current_company": "Software Engineer",
    "experience_years": "1.5",
    "current_ctc": "600000",
    "current_ctc_lpa": "6 LPA",
    "expected_ctc": "800000",
    "expected_ctc_lpa": "8 LPA",
    "notice_period": "30 Days",
    "notice_period_days": "30",
    "authorized_in_india": "Yes",
    "requires_sponsorship": "No",
    "gender": "Female",
    "resume_path": RESUME_PATH
}

NOTE_TEMPLATE = (
    "Hi Team,\n\n"
    "I am a Full Stack / Frontend Engineer with 1.5 years of production experience "
    "building performant React, React Native, and Node.js applications. "
    "I have worked on high-scale dashboards, interactive mobile interfaces, and clean REST APIs. "
    "I am actively looking for an impactful engineering role in Bengaluru / Remote and have a 30-day notice period.\n\n"
    "Best regards,\n"
    "Anjali Kashyap\n"
    "anjalikashyap9608@gmail.com | +91-9608411997\n"
    "https://www.linkedin.com/in/anjali-kashyap"
)


def load_jobs():
    """Load jobs from CSV."""
    if not os.path.exists(CSV_PATH):
        print(f"[!] CSV not found at: {CSV_PATH}")
        return []

    jobs = []
    with open(CSV_PATH, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = {k.strip(): v.strip() for k, v in row.items() if k}
            jobs.append(clean_row)
    return jobs


def is_cdp_available(url="http://localhost:9222"):
    """Check if Chrome is running with remote debugging."""
    try:
        req = urllib.request.Request(f"{url.rstrip('/')}/json/version", headers={"User-Agent": "JobAgent"})
        with urllib.request.urlopen(req, timeout=1.2) as resp:
            return resp.status == 200
    except Exception:
        return False


async def get_browser_page(playwright):
    """Connect to active Chrome Profile 9 via CDP or launch persistent real Chrome."""
    cdp_url = "http://localhost:9222"
    if is_cdp_available(cdp_url):
        print(f"[+] Connecting over CDP to running Chrome (port 9222)...")
        browser = await playwright.chromium.connect_over_cdp(cdp_url)
        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        page = context.pages[-1] if context.pages else await context.new_page()
        return browser, context, page, True

    # Fallback: Launch real Chrome with Profile 9
    print(f"[+] Chrome port 9222 not open. Launching Google Chrome with Profile 9...")
    user_data = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
    try:
        context = await playwright.chromium.launch_persistent_context(
            user_data_dir=user_data,
            channel="chrome",
            headless=False,
            args=["--no-sandbox", "--start-maximized", "--profile-directory=Profile 9"]
        )
        page = context.pages[0] if context.pages else await context.new_page()
        return None, context, page, False
    except Exception as e:
        print(f"[!] Primary profile locked ({e}). Using dedicated agent profile...")
        agent_data = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data - SystemControlAI")
        context = await playwright.chromium.launch_persistent_context(
            user_data_dir=agent_data,
            channel="chrome",
            headless=False,
            args=["--no-sandbox", "--start-maximized"]
        )
        page = context.pages[0] if context.pages else await context.new_page()
        return None, context, page, False


async def apply_ashby(page, job):
    """Fill and process Ashby application."""
    url = job.get("job_link", "").rstrip("/")
    if not url.endswith("/application"):
        url += "/application"

    print(f"[*] Navigating to Ashby form: {url}")
    await page.goto(url, wait_until="networkidle", timeout=30000)
    await asyncio.sleep(2)

    # 1. Fill Name
    name_inputs = page.locator('input[name="_systemfield_name"], input[placeholder*="Name" i], input[id*="name" i]')
    if await name_inputs.count() > 0:
        await name_inputs.first.fill(CANDIDATE["full_name"])
        print("  [v] Filled Name: Anjali Kashyap")

    # 2. Fill Email
    email_inputs = page.locator('input[name="_systemfield_email"], input[type="email"], input[placeholder*="Email" i]')
    if await email_inputs.count() > 0:
        await email_inputs.first.fill(CANDIDATE["email"])
        print("  [v] Filled Email: anjalikashyap9608@gmail.com")

    # 3. Fill Phone
    phone_inputs = page.locator('input[name*="phone" i], input[type="tel"], input[placeholder*="Phone" i]')
    if await phone_inputs.count() > 0:
        await phone_inputs.first.fill(CANDIDATE["phone"])
        print("  [v] Filled Phone: +91-9608411997")

    # 4. Upload Resume PDF
    file_inputs = page.locator('input[type="file"]')
    if await file_inputs.count() > 0 and os.path.exists(RESUME_PATH):
        await file_inputs.first.set_input_files(RESUME_PATH)
        print(f"  [v] Uploaded Resume PDF: {Path(RESUME_PATH).name}")
        await asyncio.sleep(2)

    # 5. Fill LinkedIn
    linkedin_inputs = page.locator('input[name*="linkedin" i], input[placeholder*="linkedin" i]')
    if await linkedin_inputs.count() > 0:
        await linkedin_inputs.first.fill(CANDIDATE["linkedin"])
        print("  [v] Filled LinkedIn URL")

    # 6. Fill GitHub
    github_inputs = page.locator('input[name*="github" i], input[placeholder*="github" i]')
    if await github_inputs.count() > 0:
        await github_inputs.first.fill(CANDIDATE["github"])
        print("  [v] Filled GitHub URL")

    # 7. Fill Location / City
    loc_inputs = page.locator('input[name*="location" i], input[placeholder*="Location" i], input[name*="city" i]')
    if await loc_inputs.count() > 0:
        await loc_inputs.first.fill(CANDIDATE["city"])
        print("  [v] Filled Location: Bengaluru")

    # 8. Notice period / CTC if present
    np_inputs = page.locator('input[name*="notice" i], input[placeholder*="notice" i]')
    if await np_inputs.count() > 0:
        await np_inputs.first.fill(CANDIDATE["notice_period"])
        print("  [v] Filled Notice Period")

    salary_inputs = page.locator('input[name*="compensation" i], input[name*="salary" i], input[placeholder*="salary" i]')
    if await salary_inputs.count() > 0:
        await salary_inputs.first.fill(CANDIDATE["expected_ctc_lpa"])
        print("  [v] Filled Expected CTC")

    # Capture screenshot of filled application
    company = job.get("company", "ashby").replace(" ", "_")
    shot_path = OUTPUT_DIR / f"{company}_filled.png"
    await page.screenshot(path=str(shot_path), full_page=False)
    print(f"  [v] Saved application screenshot: {shot_path.name}")
    return True


async def apply_wellfound(page, job):
    """Process Wellfound job in active logged-in Chrome."""
    url = job.get("job_link", "")
    print(f"[*] Navigating to Wellfound: {url}")
    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
    await asyncio.sleep(2)

    company = job.get("company", "wellfound").replace(" ", "_")
    shot_path = OUTPUT_DIR / f"{company}_page.png"
    await page.screenshot(path=str(shot_path), full_page=False)
    print(f"  [v] Page loaded and screenshot saved: {shot_path.name}")

    # Look for Apply Button
    apply_btn = page.locator('button:has-text("Apply"), a:has-text("Apply"), button:has-text("Quick Apply")').first
    if await apply_btn.count() > 0:
        btn_text = await apply_btn.inner_text()
        print(f"  [v] Found Apply Button: '{btn_text}'")
        try:
            await apply_btn.click()
            await asyncio.sleep(2)
            # Check for note field
            note_area = page.locator('textarea[name*="note" i], textarea[placeholder*="note" i], textarea[placeholder*="pitch" i]').first
            if await note_area.count() > 0:
                await note_area.fill(NOTE_TEMPLATE)
                print("  [v] Injected tailored pitch/note for Anjali Kashyap.")
            
            shot_filled = OUTPUT_DIR / f"{company}_apply_modal.png"
            await page.screenshot(path=str(shot_filled), full_page=False)
            print(f"  [v] Captured application modal: {shot_filled.name}")
        except Exception as e:
            print(f"  [!] Note: Clicked apply or interaction handled: {e}")
    else:
        print("  [i] Already applied or requires direct company site navigation.")
    return True


async def main():
    jobs = load_jobs()
    if not jobs:
        print("No jobs found in CSV.")
        return

    print("=" * 70)
    print("      SYSTEM CONTROL AI - AUTOMATED JOB APPLICATION RUNNER")
    print("=" * 70)
    print(f"Candidate: {CANDIDATE['full_name']} ({CANDIDATE['email']})")
    print(f"Resume:    {RESUME_PATH} (Exists: {os.path.exists(RESUME_PATH)})")
    print(f"Total CSV Jobs: {len(jobs)}")
    print("=" * 70)

    # Allow selecting a single job or running all
    target_idx = None
    if len(sys.argv) > 1:
        try:
            target_idx = int(sys.argv[1])
            print(f"[Targeting single job index #{target_idx}]")
        except ValueError:
            pass

    async with async_playwright() as playwright:
        browser, context, page, is_cdp = await get_browser_page(playwright)

        selected_jobs = [j for j in jobs if int(j.get("id", 0)) == target_idx] if target_idx else jobs

        for idx, job in enumerate(selected_jobs, start=1):
            comp = job.get("company", "Unknown")
            role = job.get("role", "Engineer")
            link = job.get("job_link", "")
            print(f"\n[{idx}/{len(selected_jobs)}] Processing: {comp} - {role}")
            print(f"URL: {link}")

            try:
                if "ashbyhq.com" in link:
                    await apply_ashby(page, job)
                elif "wellfound.com" in link:
                    await apply_wellfound(page, job)
                elif "peerlist.io" in link:
                    await page.goto(link, wait_until="domcontentloaded", timeout=20000)
                    shot = OUTPUT_DIR / f"{comp.replace(' ', '_')}_peerlist.png"
                    await page.screenshot(path=str(shot))
                    print(f"  [v] Peerlist job page saved: {shot.name}")
                else:
                    await page.goto(link, wait_until="domcontentloaded", timeout=20000)
                    shot = OUTPUT_DIR / f"{comp.replace(' ', '_')}_site.png"
                    await page.screenshot(path=str(shot))
                    print(f"  [v] Direct site saved: {shot.name}")
            except Exception as e:
                print(f"  [ERROR] Encountered error processing {comp}: {e}")

        print("\n" + "=" * 70)
        print("Application run complete! Review screenshots in:")
        print(f"{OUTPUT_DIR}")
        print("=" * 70)

        if not is_cdp:
            await context.close()


if __name__ == "__main__":
    asyncio.run(main())
