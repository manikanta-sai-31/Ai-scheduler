import streamlit as st
import requests
import json

st.title("🧠 Smart AI Daily Scheduler")

time_slots = [
    "12:00 - 1:00",
    "1:00 - 2:00",
    "2:00 - 3:00",
    "3:00 - 4:00",
    "4:00 - 5:00",
    "5:00 - 6:00",
    "6:00 - 7:00",
    "7:00 - 8:00",
    "8:00 - 9:00",
    "9:00 - 10:00",
]

for time in time_slots:
    if time not in st.session_state:
        st.session_state[time] = ""

st.subheader("Enter Your Tasks")

tasks_input = st.text_area("Enter tasks (comma separated)", "")
priority = st.selectbox("Select Priority", ["High", "Medium", "Low"])
energy = st.selectbox("Select Energy Level", ["Morning", "Afternoon", "Night"])

def generate_ai_schedule():
    prompt = f"""
You are an intelligent daily scheduler.

User input:
- Tasks: {tasks_input}
- Priority level: {priority}
- Energy level: {energy}

Available time slots:
{', '.join(time_slots)}

Your job:
Create a realistic daily schedule for the user.

Important instructions:
1. Use the user's actual tasks as much as possible.
2. Do not use vague words like "work", "learn", "fun", or "task" unless absolutely necessary.
3. Make task names specific and meaningful based on the user's input.
4. Schedule important tasks in the best slots based on the user's energy level.
5. Add breaks naturally, but do not overuse them.
6. Fill every time slot with exactly one activity.
7. Keep activity names short and clear.
8. Return only valid JSON.
9. Do not include explanations, headings, or extra text.

Example of good task names:
- Python Practice
- Gym Workout
- Resume Building
- AI Project Work
- Lunch Break
- Revision
- Mock Interview Practice

Use this exact JSON format:
{{
  "12:00 - 1:00": "Task name",
  "1:00 - 2:00": "Task name",
  "2:00 - 3:00": "Task name"
}}
"""

    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        result = response.json()

        ai_text = result["response"].strip()

        start = ai_text.find("{")
        end = ai_text.rfind("}") + 1
        ai_text = ai_text[start:end]

        schedule = json.loads(ai_text)

        for time in time_slots:
            st.session_state[time] = schedule.get(time, "Free Time")

        st.success("AI Schedule Generated Successfully ✅")

    except Exception as e:
        st.error(f"Error: {e}")

def clear_schedule():
    for time in time_slots:
        st.session_state[time] = ""

col1, col2 = st.columns(2)

with col1:
    if st.button("Generate AI Schedule"):
        generate_ai_schedule()

with col2:
    if st.button("Clear Schedule"):
        clear_schedule()

st.subheader("Today's Schedule")

for time in time_slots:
    st.text_input(time, key=time)