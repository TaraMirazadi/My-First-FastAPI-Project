from models.person import Person
from exceptions.custom_exceptions import (
    CourseAlreadySelectedException, CourseNotSelectedException)


class Student(Person):
    def __init__(self, id: int, first_name: str, last_name: str, student_number: str, major: str):
        super().__init__(id, first_name, last_name)
        self.student_number = student_number
        self.major = major
        self.selected_courses = []

    def select_course(self, course):
        if course in self.selected_courses:
            raise CourseAlreadySelectedException(
                "این درس قبلا توسط دانشجو انتخاب شده است")
        self.selected_courses.append(course)

    def drop_course(self, course):
        if course not in self.selected_courses:
            raise CourseNotSelectedException(
                "این درس قبلا توسط دانشجو انتخاب نشده است")
        self.selected_courses.remove(course)

    def get_courses(self) -> list:
        return self.selected_courses

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "student number": self.student_number,
            "major": self.major,
            "selected courses": [
                {
                    "id": course.id,
                    "title": course.title,
                    "unit": course.unit,
                    "code": course.code,
                } for course in self.selected_courses
            ],
        })
        return data