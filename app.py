import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler


def get_pet(owner: Owner, pet_name: str, pet_species: str) -> Pet | None:
    for pet in owner.pets:
        if pet.name.lower() == pet_name.lower() and pet.species == pet_species:
            return pet
    return None

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner

owner_name = st.text_input("Owner name", value=owner.name)
owner.name = owner_name

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    task_time = st.text_input("Time (HH:MM)", value="08:00")
with col5:
    frequency = st.selectbox("Frequency", ["daily", "weekly", "once"], index=0)

if st.button("Add task"):
    clean_pet_name = pet_name.strip()
    clean_task_title = task_title.strip()
    clean_time = task_time.strip()

    if not clean_pet_name:
        st.error("Please enter a pet name before adding a task.")
    elif not clean_task_title:
        st.error("Please enter a task title before adding a task.")
    elif not clean_time:
        st.error("Please enter a task time in HH:MM format.")
    else:
        pet = get_pet(owner, clean_pet_name, species)
        if pet is None:
            pet = Pet(name=clean_pet_name, species=species)
            owner.add_pet(pet)

        new_task = Task(
            description=clean_task_title,
            duration=int(duration),
            priority=priority,
            time=clean_time,
            frequency=frequency,
        )
        pet.add_task(new_task)
        st.success(f"Added '{clean_task_title}' for {pet.name}.")

task_rows = []
for pet in owner.pets:
    for task in pet.get_tasks():
        task_rows.append(
            {
                "pet": pet.name,
                "species": pet.species,
                "task": task.description,
                "duration_minutes": task.duration,
                "priority": task.priority,
                "time": task.time,
                "frequency": task.frequency,
                "completed": task.completed,
            }
        )

if task_rows:
    st.write("Current tasks:")
    st.table(task_rows)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    scheduler = Scheduler(st.session_state.owner)
    sorted_tasks = scheduler.sort_by_time()
    conflicts = scheduler.detect_conflicts()

    if sorted_tasks:
        schedule_rows = []
        for task in sorted_tasks:
            schedule_rows.append(
                {
                    "time": task.time,
                    "task": task.description,
                    "priority": task.priority,
                    "duration_minutes": task.duration,
                    "frequency": task.frequency,
                    "completed": task.completed,
                }
            )

        st.success("Schedule generated.")
        st.write("Sorted daily schedule:")
        st.table(schedule_rows)
    else:
        st.info("No tasks available to schedule yet.")

    if conflicts:
        st.warning("Conflict warnings:")
        for time, conflict_tasks in conflicts.items():
            st.write(f"{time}: {len(conflict_tasks)} tasks overlap")
            for task in conflict_tasks:
                st.write(f"- {task.description} ({task.priority})")
    else:
        st.success("No scheduling conflicts found.")

