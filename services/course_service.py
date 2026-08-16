from schemas.course_schema import CourseCreate, CourseUpdate
from models.course import Course
from data.storage import courses, get_next_course_id, save_all
from exceptions.custom_exceptions import CourseNotFoundException, InvalidDataException


def create_course(course_data: CourseCreate) -> Course:
    if any(
        course.code == course_data.code 
        for course in courses.values()):
        raise InvalidDataException("کد درس تکراری است")

    course = Course(
        id=get_next_course_id(),
        title=course_data.title,
        unit=course_data.unit,
        capacity=course_data.capacity,
        code=course_data.code,
    )
    courses[course.id] = course
    save_all()

    return course


def get_all_courses() -> list[Course]:
    return list(courses.values())


def get_course_by_id(course_id: int) -> Course:
    course = courses.get(course_id)
    if course is None:
        raise CourseNotFoundException("درس پیدا نشد")
    return course


def update_course(course_id: int, course_data: CourseUpdate) -> Course:
    course = get_course_by_id(course_id)

    if course_data.code is not None:
        duplicate = any(
            c.id != course_id and c.code == course_data.code 
            for c in courses.values())

        if duplicate:
            raise InvalidDataException("کد درس تکراری است")
        course.code= course_data.code

    if course_data.title is not None:
        course.title= course_data.title

    if course_data.unit is not None:
        course.unit = course_data.unit

    if course_data.capacity is not None:
        if course_data.capacity < len(course.students):
            raise InvalidDataException("ظرفیت جدید نمی تواند کمتر از دانشجویان ثبت نام شده باشد")
        course.capacity = course_data.capacity

    save_all()
    return course


def delete_course(course_id: int) -> None:
    course = get_course_by_id(course_id)

    for student in list(course.students):
        if course in student.selected_courses:
            student.selected_courses.remove(course)

    if course.professor is not None and course in course.professor.courses:
        course.professor.courses.remove(course)


    del courses[course_id]
    save_all()
