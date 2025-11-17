from sqlmodel import SQLModel, Field, JSON


class TaskResults(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    task_id: str = Field(default=None, unique=True)
    status: str = Field(default=None)
    result: dict | None = Field(default=None, sa_type=JSON)
    error: str = Field(default=None)
