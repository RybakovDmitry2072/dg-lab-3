from sqlmodel import Session, select

from app.models import TaskResults


def create_task_result(session: Session, task_result: TaskResults):
    """
    Create a new TaskResult in the database.

    :param session: The session to use for the database operations
    :param task_result: The TaskResult to create in the database
    """
    session.add(task_result)
    session.commit()


def get_task_result_by_taskid(session: Session, task_id: str):
    """
    Get a TaskResult from the database by its task ID.

    :param session: The session to use for the database operations
    :param task_id: The task ID of the TaskResult to retrieve

    :return: The TaskResult with the given task ID, or None if not found
    """
    statement = select(TaskResults).where(TaskResults.task_id == task_id)
    task_result = session.exec(statement).one_or_none()
    return task_result
