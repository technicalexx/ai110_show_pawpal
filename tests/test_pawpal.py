from pawpal_system import Pet, Task


def test_mark_complete_changes_task_to_completed() -> None:
	task = Task(
		description="Feed breakfast",
		duration=10,
		priority="High",
		time="08:00",
	)

	assert task.completed is False

	task.mark_complete()

	assert task.completed is True


def test_add_task_increases_pet_task_count() -> None:
	pet = Pet(name="Buddy", species="Dog")
	task = Task(
		description="Morning walk",
		duration=30,
		priority="Medium",
		time="09:00",
	)

	starting_count = len(pet.get_tasks())

	pet.add_task(task)

	assert len(pet.get_tasks()) == starting_count + 1
