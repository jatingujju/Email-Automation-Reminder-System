import sqlite3

from datetime import datetime
from dateutil.rrule import rrulestr

from renderer import EmailRenderer
from mailer import send_email


# Absolute database path
DB_PATH = r"D:\Projects\Aipreneur\Python\Email-Automation-Reminder-System\email-automation\db\email_automation.db"

print("Using Database:", DB_PATH)

# Initialize renderer
renderer = EmailRenderer()


def get_due_reminders():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    query = """
        SELECT
            reminders.id,
            contacts.full_name,
            contacts.email,
            reminders.reminder_title,
            reminders.reminder_message,
            reminders.rrule,
            reminders.scheduled_time

        FROM reminders

        INNER JOIN contacts
        ON reminders.contact_id = contacts.id
    """

    cursor.execute(query)

    reminders = cursor.fetchall()

    print("Fetched reminders:", reminders)

    conn.close()

    return reminders


def process_reminders():

    print("\nChecking reminders...\n")

    now = datetime.now()

    reminders = get_due_reminders()

    if not reminders:
        print("No reminders found.")
        return

    for reminder in reminders:

        (
            reminder_id,
            full_name,
            email,
            title,
            message,
            rrule_string,
            scheduled_time
        ) = reminder

        print(f"\nProcessing reminder for: {email}")

        # RRULE parsing
        rule = rrulestr(
            rrule_string,
            dtstart=datetime.fromisoformat(scheduled_time)
        )

        next_occurrence = rule.after(now, inc=True)

        print("Next occurrence:", next_occurrence)

        print("\nReminder is due. Sending email...\n")

        # Email template context
        context = {
            "name": full_name,
            "event_name": title,
            "event_date": now.strftime("%d %B %Y"),
            "event_time": now.strftime("%I:%M %p")
        }

        # Generate HTML email
        html_content = renderer.render_markdown_template(
            "reminder.md",
            context
        )

        # Send email
        send_email(
            email,
            title,
            html_content
        )

        print(f"\nReminder dispatched to {email}\n")


if __name__ == "__main__":

    process_reminders()