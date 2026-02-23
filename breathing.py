import time
import streamlit as st

def breathing_exercise():
    st.subheader("🧘 Guided Breathing Exercise (4-4-4 Technique)")

    if st.button("Start Breathing"):
        progress = st.progress(0)
        timer_display = st.empty()

        total_steps = 12  # 3 cycles × 4 sec each
        step = 0

        for cycle in range(3):

            # Inhale
            for i in range(4):
                timer_display.markdown(f"### Inhale... 🌬️ ({4-i}s)")
                progress.progress(step / total_steps)
                time.sleep(1)
                step += 1

            # Hold
            for i in range(4):
                timer_display.markdown(f"### Hold... 😌 ({4-i}s)")
                progress.progress(step / total_steps)
                time.sleep(1)
                step += 1

            # Exhale
            for i in range(4):
                timer_display.markdown(f"### Exhale... 💨 ({4-i}s)")
                progress.progress(step / total_steps)
                time.sleep(1)
                step += 1

        progress.progress(1.0)
        st.success("✨ You completed the breathing session!")