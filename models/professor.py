from models.person import Person
from exceptions.custom_exceptions import ProfessorAlreadyAssignedException


class Professor(Person):

    def __init__(self, id: int, first_name: str, last_name: str, personal_code: str, department: str):
        super().__init__(id, first_name, last_name)
        self.personal_code = personal_code
        self.department = department
        self.courses = []

    def assign_courses(self, courses):
        if courses in self.courses:
            raise ProfessorAlreadyAssignedException(
                "این درس قبلا به استاد اختصاص داده شده است.")
        self.courses.append(courses)

    def get_courses(self) -> list:
        return self.courses

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "personal code": self.personal_code,
            "department": self.department,
            "courses": [
                {
                    "id": course.id,
                    "title": course.title,
                    "unit": course.unit,
                    "code": course.code,
                } for course in self.courses
            ],
        })
        return data
