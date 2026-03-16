from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Task:
	description: str
	duration: int
	priority: str
	time: str
	completed: bool = False
	frequency: str = "daily"

	def mark_complete(self) -> None:
		self.completed = True


@dataclass
class Pet:
	name: str
	species: str
	tasks: List[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		self.tasks.append(task)

	def get_tasks(self) -> List[Task]:
		return self.tasks


@dataclass
class Owner:
	name: str
	pets: List[Pet] = field(default_factory=list)

	def add_pet(self, pet: Pet) -> None:
		self.pets.append(pet)

	def get_all_tasks(self) -> List[Task]:
		all_tasks: List[Task] = []
		for pet in self.pets:
			all_tasks.extend(pet.get_tasks())
		return all_tasks


class Scheduler:
	def __init__(self, owner: Owner) -> None:
		self.owner = owner

	def get_all_tasks(self) -> List[Task]:
		return self.owner.get_all_tasks()

	def sort_by_time(self) -> List[Task]:
		return sorted(self.get_all_tasks(), key=lambda task: task.time)

	def get_incomplete_tasks(self) -> List[Task]:
		return [task for task in self.get_all_tasks() if not task.completed]

	def detect_conflicts(self) -> Dict[str, List[Task]]:
		conflicts: Dict[str, List[Task]] = {}
		for task in self.sort_by_time():
			conflicts.setdefault(task.time, []).append(task)

		return {
			time: tasks
			for time, tasks in conflicts.items()
			if len(tasks) > 1
		}
