from models.student import Student
from services.student_service import get_student_by_id
from services.professor_service import get_professor_by_id
from services.course_service import get_course_by_id
from data.storage import save_all

def select_course_for_student(student_id: int, course_id: int) -> Student:
    student = get_student_by_id(student_id)
    course = get_course_by_id(course_id)
    student.select_course(course)
    course.add_student(student)
    save_all()
    return student


def drop_course_for_student(student_id: int, course_id: int):
    student = get_student_by_id(student_id)
    course = get_course_by_id(course_id)
    student.drop_course(course)
    course.remove_student(student)
    save_all()
    return student


def get_student_courses(student_id: int):
    student = get_student_by_id(student_id)
    return student.get_courses()


def assign_professor_to_course(course_id: int, professor_id: int):
    course = get_course_by_id(course_id)
    professor = get_professor_by_id(professor_id)
    course.assign_professor(professor)
    save_all()
    return course