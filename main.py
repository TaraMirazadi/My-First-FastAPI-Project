from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from exceptions.custom_exceptions import (
    CourseAlreadySelectedException,
    CourseFullException,
    CourseNotFoundException,
    CourseNotSelectedException,
    CourseSelectionException,
    StudentNotFoundException,
    ProfessorAlreadyAssignedException,
    ProfessorNotFoundException,
    InvalidDataException,
)
from routers.students import router as student_router
from routers.professors import router as professor_router
from routers.courses import router as course_router

from data.storage import load_all, save_all, students, professors, courses

app = FastAPI(title="Simple Course Selection System",
              description="پروژه پایانی درس برنامه نویسی پیشرفته",
              version="1.0.0")

app.include_router(student_router)
app.include_router(professor_router)
app.include_router(course_router)


@app.on_event("startup")
def startup_load_data():
 load_all()


@app.on_event("shutdown")
def shutdown_save_data():
    save_all()


@app.get("/",tags=["Root"])
def root():
    return {
        "message": "به سیستم انتخاب واحد خوش آمدید"
    }


@app.get("/debug/storage", tags=["Debug"])
def debug_storage_summary():
    return {
        "student_count": len(students),
        "professor_count": len(professors),
        "course_count": len(courses),
        "storage_folder": "data/files"
    }


@app.get("/debug/storage/all", tags=["Debug"])
def debug_storage_all():
    return {
        "students": [student.to_dict() for student in students.values()],
        "professors": [professor.to_dict() for professor in professors.values()],
        "courses": [course.to_dict() for course in courses.values()],
    }


@app.exception_handler(StudentNotFoundException)
async def student_not_found_handler(request: Request, exc: StudentNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"Error": "Student Not Found", "message": str(exc)}
    )


@app.exception_handler(ProfessorNotFoundException)
async def professor_not_found_handler(request: Request, exc: ProfessorNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"Error": "Professor Not Found", "message": str(exc)}
    )


@app.exception_handler(CourseNotFoundException)
async def course_not_found_handler(request: Request, exc: CourseNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"Error": "Course Not Found", "message": str(exc)}
    )


@app.exception_handler(InvalidDataException)
async def invalid_data_handler(request: Request, exc: InvalidDataException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"Error": "Invalid Data", "message": str(exc)}
    )


@app.exception_handler(CourseFullException)
async def course_full_handler(request: Request, exc: CourseFullException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"Error": "Course Is Full", "message": str(exc)}
    )


@app.exception_handler(CourseAlreadySelectedException)
async def course_already_selected_handler(request: Request, exc: CourseAlreadySelectedException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"Error": "Course Already Selected", "message": str(exc)}
    )


@app.exception_handler(CourseNotSelectedException)
async def course_not_selected_handler(request: Request, exc: CourseNotSelectedException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"Error": "Course Not Selected", "message": str(exc)}
    )


@app.exception_handler(ProfessorAlreadyAssignedException)
async def professor_already_assigned_handler(request: Request, exc: ProfessorAlreadyAssignedException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"Error": "Professor Already Assigned", "message": str(exc)}
    )


@app.exception_handler(CourseSelectionException)
async def course_selection_exception_handler(request: Request, exc: CourseSelectionException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"Error": "Course Selection Exception", "message": str(exc)}
    )
