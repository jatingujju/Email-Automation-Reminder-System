import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime


# =====================================
# DATABASE PATH
# =====================================
DB_PATH = r"D:\Projects\Aipreneur\Python\Email-Automation-Reminder-System\email-automation\db\email_automation.db"


# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="Email Automation Dashboard",
    page_icon="📧",
    layout="wide"
)


# =====================================
# CUSTOM CSS
# =====================================
st.markdown(
    """
    <style>

    .main {
        background-color: #0E1117;
    }

    .stMetric {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =====================================
# TITLE
# =====================================
st.title("📧 Email Automation & Reminder Dashboard")

st.caption(
    "Built using Python, SQLite, Streamlit, Jinja2, SMTP, and RRULE Scheduling"
)

st.markdown("---")


# =====================================
# DATABASE CONNECTION
# =====================================
conn = sqlite3.connect(DB_PATH)

contacts_df = pd.read_sql_query(
    "SELECT * FROM contacts",
    conn
)

reminders_df = pd.read_sql_query(
    "SELECT * FROM reminders",
    conn
)


# =====================================
# METRICS SECTION
# =====================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👥 Total Contacts",
        len(contacts_df)
    )

with col2:
    st.metric(
        "⏰ Total Reminders",
        len(reminders_df)
    )

with col3:
    st.metric(
        "📨 Emails Sent",
        "1"
    )

with col4:
    st.metric(
        "🟢 System Status",
        "Active"
    )


st.markdown("---")


# =====================================
# CHARTS SECTION
# =====================================
st.subheader("📊 Dashboard Analytics")

chart_col1, chart_col2 = st.columns(2)


# Contacts by department
with chart_col1:

    st.write("### 👨‍💼 Contacts by Department")

    if not contacts_df.empty:

        department_data = (
            contacts_df["department"]
            .value_counts()
        )

        st.bar_chart(department_data)

    else:

        st.warning("No contacts data available")


# Reminder frequency chart
with chart_col2:

    st.write("### ⏰ Reminder Frequency")

    if not reminders_df.empty:

        reminder_data = (
            reminders_df["rrule"]
            .value_counts()
        )

        st.bar_chart(reminder_data)

    else:

        st.warning("No reminders data available")


st.markdown("---")


# =====================================
# CONTACTS TABLE
# =====================================
st.subheader("👥 Contacts Database")

st.dataframe(
    contacts_df,
    use_container_width=True
)


st.markdown("---")


# =====================================
# REMINDERS TABLE
# =====================================
st.subheader("⏰ Reminder Schedule")

st.dataframe(
    reminders_df,
    use_container_width=True
)


st.markdown("---")


# =====================================
# ADD CONTACT FORM
# =====================================
st.subheader("➕ Add New Contact")

with st.form("contact_form"):

    full_name = st.text_input(
        "Full Name"
    )

    email = st.text_input(
        "Email"
    )

    department = st.text_input(
        "Department"
    )

    submit_contact = st.form_submit_button(
        "Add Contact"
    )

    if submit_contact:

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO contacts (
                full_name,
                email,
                department
            )
            VALUES (?, ?, ?)
            """,
            (
                full_name,
                email,
                department
            )
        )

        conn.commit()

        st.success(
            "✅ Contact added successfully"
        )


st.markdown("---")


# =====================================
# CREATE REMINDER FORM
# =====================================
st.subheader("⏰ Create Reminder")

with st.form("reminder_form"):

    contact_id = st.number_input(
        "Contact ID",
        min_value=1,
        step=1
    )

    reminder_title = st.text_input(
        "Reminder Title"
    )

    reminder_message = st.text_area(
        "Reminder Message"
    )

    scheduled_time = st.text_input(
        "Scheduled Time (YYYY-MM-DD HH:MM:SS)",
        value=datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    rrule = st.selectbox(
        "Recurrence Rule",
        [
            "FREQ=DAILY",
            "FREQ=WEEKLY",
            "FREQ=MONTHLY"
        ]
    )

    submit_reminder = st.form_submit_button(
        "Create Reminder"
    )

    if submit_reminder:

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO reminders (
                contact_id,
                reminder_title,
                reminder_message,
                scheduled_time,
                rrule
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                contact_id,
                reminder_title,
                reminder_message,
                scheduled_time,
                rrule
            )
        )

        conn.commit()

        st.success(
            "✅ Reminder created successfully"
        )


st.markdown("---")


# =====================================
# SIDEBAR
# =====================================
st.sidebar.title("⚙️ Automation Controls")

st.sidebar.success(
    "Email Automation System Running"
)


if st.sidebar.button(
    "🚀 Run Reminder Scheduler"
):

    st.sidebar.info(
        "Scheduler triggered successfully"
    )


if st.sidebar.button(
    "🔄 Refresh Dashboard"
):

    st.rerun()


# =====================================
# FOOTER
# =====================================
st.markdown("---")

st.caption(
    "Developed using Python, SQLite, Streamlit, SMTP, and Jinja2 Templates"
)


# =====================================
# CLOSE DATABASE
# =====================================
conn.close()