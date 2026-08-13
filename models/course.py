from exceptions.custom_exceptions import (
    CourseFullException,
    CourseNotSelectedException,
    CourseAlreadySelectedException,
    ProfessorAlreadyAssignedException,
    )


class Course:

    def __init__(self, id: int, title: str, code: str, unit: int, capacity: int):
        self.id = id
        self.title = title
        self.code = code
        self.unit = unit
        self.capacity = capacity
        self.professor = None
        self.student = []

    def is_full(self) -> bool:
        return len(self.student) >= self.capacity

    def add_student(self, student):
        if student in self.student:
            raise CourseAlreadySelectedException(
                " دانشجو قبلا در این درس ثبت شده است ")
        if self.is_full():
            raise CourseFullException("ظرفیت این درس نکمیل شده است")
        self.student.append(student)

    def remove_student(self, student):
        if student in self.student:
            raise CourseNotSelectedException(
                " دانشجو در این درس ثبت نام نشده است ")
        self.student.remove(student)

    def assign_professor(self, professor):
        if self.professor is not None and self.professor.id == professor.id:
            raise ProfessorAlreadyAssignedException(
                "درس قبلا به این استاد اختصاص داده شده است ")
        if self.professor is not None and professor.id != self.professor.id:
            raise ProfessorAlreadyAssignedException("این درس استاد دارد")
        self.professor = professor
        professor.assign_courses(self)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "unit": self.unit,
            "code": self.code,
            "capacity": self.capacity,
            "remaining capacity": self.capacity - len(self.student),
            "professor": None if self.professor is None else {
                "id": self.professor.id,
                "first name": self.professor.first_name,
                "last name": self.professor.last_name,
                "personal code": self.professor.personal_code,
            },
            "students": [
                {
                    "id": student.id,
                    "first name": student.first_name,
                    "last name": student.last_name,
                    "student number": student.student_number,
                }
                for student in self.student
            ],
        }