from pawpal_system import Owner, Pet, Task, Scheduler


def print_schedule(tasks):
    print("Daily Schedule")
    print("-" * 40)

    for task in tasks:
        status = "Done" if task.completed else "Pending"
        print(
            f"{task.time} | {task.description} | "
            f"{task.priority} priority | {task.duration} mins | "
            f"{task.frequency} | {status}"
        )


def print_conflicts(conflicts):
    print("\nConflict Warnings")
    print("-" * 40)

    if not conflicts:
        print("No scheduling conflicts found.")
        return

    for time, tasks in conflicts.items():
        print(f"Conflict at {time}:")
        for task in tasks:
            print(f" - {task.description} ({task.priority} priority)")


def main():
    owner = Owner(name="Alex")

    dog = Pet(name="Buddy", species="Dog")
    cat = Pet(name="Whiskers", species="Cat")

    walk = Task(
        description="Morning walk",
        duration=30,
        priority="High",
        time="08:00",
        frequency="daily"
    )

    breakfast = Task(
        description="Feed breakfast",
        duration=10,
        priority="High",
        time="08:30",
        frequency="daily"
    )

    medicine = Task(
        description="Give medicine",
        duration=5,
        priority="Medium",
        time="08:30",
        frequency="daily"
    )

    dog.add_task(walk)
    dog.add_task(breakfast)
    cat.add_task(medicine)

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)

    daily_tasks = scheduler.sort_by_time()
    conflicts = scheduler.detect_conflicts()

    print(f"Owner: {owner.name}")
    print(f"Number of pets: {len(owner.pets)}\n")

    print_schedule(daily_tasks)
    print_conflicts(conflicts)


if __name__ == "__main__":
    main()