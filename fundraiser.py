import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# ----------------------------
# CONFIG
# ----------------------------

TEAMS = [
    "Team 1",
    "Team 2",
    "Team 3",
    "Team 4",
    "Team 5",
    "Team 6",
    "Team 7",
    "Team 8",
    "Team 9",
    "Team 10",
    "Team 11",
    "Team 12",
]

TOTAL_CREDITS = 100
DATA_FILE = "votes.csv"

STUDENT_EMAILS = [
    "guelluehan.bakir1@tha.de",
    "leon.balliet@tha.de",
    "tuba.baslik@tha.de",
    "chris.bauer@tha.de",
    "lucy.beck1@tha.de",
    "kevin.behner@tha.de",
    "berke.bozdogan@tha.de",
    "yunus.emre.cevik1@tha.de",
    "helgi.eggerz@tha.de",
    "florian.fischer2@tha.de",
    "jan.hartisch@tha.de",
    "mario.hartl@tha.de",
    "lenny.heinrich@tha.de",
    "elias.hektor@tha.de",
    "philipp.meyer2@tha.de",
    "fabio.reinkensmeier@tha.de",
    "maximilian.sager@tha.de",
    "laura.slusalek1@tha.de",
    "elena-camelia.spiridon@tha.de",
    "derya.suetcue@tha.de",
    "ken.truong@tha.de",
    "robin.winterhalder@tha.de",
    "mehdi.yesiltas@hs-augsburg.de",
    "ferit.yesiltas@tha.de",
    "ahmet.yetisir@tha.de",
]

# ----------------------------
# LOAD / INIT DATA
# ----------------------------

data_path = Path(DATA_FILE)
if data_path.exists():
    votes_df = pd.read_csv(data_path)
else:
    votes_df = pd.DataFrame(columns=["name"] + TEAMS)

# ----------------------------
# APP LAYOUT
# ----------------------------

st.title("Fundraiser Game – Invest in the Teams 💰")
st.write(
    f"You have a total of **{TOTAL_CREDITS} credits**. "
    "Distribute them among the 12 teams."
)

# Student dropdown
name = st.selectbox("Select your email", ["-- Please select --"] + STUDENT_EMAILS)

st.markdown("### Allocate your credits")

credits = {}
remaining_placeholder = st.empty()

for team in TEAMS:
    credits[team] = st.number_input(
        f"Credits for {team}",
        min_value=0,
        max_value=TOTAL_CREDITS,
        step=1,
        key=team,
    )

total_given = sum(credits.values())
remaining = TOTAL_CREDITS - total_given

remaining_placeholder.markdown(
    f"**Total allocated:** {total_given} / {TOTAL_CREDITS}  "
    f"(**Remaining:** {remaining})"
)

# ----------------------------
# SUBMIT (ONE VOTE PER STUDENT)
# ----------------------------

if st.button("Submit my investment"):
    if name == "-- Please select --":
        st.error("Please select your email.")
    elif total_given != TOTAL_CREDITS:
        st.error(f"Your credits must sum to exactly {TOTAL_CREDITS}. Currently: {total_given}.")
    else:
        clean_name = name.strip()
        new_row = {"name": clean_name, **credits}

        # Remove any existing vote from this student (enforce one row per email)
        votes_df = votes_df[votes_df["name"] != clean_name]

        # Append the updated/new vote
        votes_df = pd.concat([votes_df, pd.DataFrame([new_row])], ignore_index=True)

        votes_df.to_csv(DATA_FILE, index=False)

        st.success("Your vote has been recorded (or updated if you voted before). ✅")

# ----------------------------
# TEACHER VIEW
# ----------------------------

st.markdown("---")
st.header("Teacher View")

# Clear all data button
if st.button("🗑️ Clear ALL data (Teacher Only)"):
    votes_df = pd.DataFrame(columns=["name"] + TEAMS)
    votes_df.to_csv(DATA_FILE, index=False)
    st.success("All data has been cleared successfully!")

if st.checkbox("Show aggregated results"):
    if votes_df.empty:
        st.info("No votes yet.")
    else:
        totals = votes_df[TEAMS].sum().sort_values(ascending=False)
        st.subheader("Total credits per team")
        st.bar_chart(totals)
        st.write(totals.to_frame("Total Credits"))

# streamlit run fundraiser.py