import operator
from pydantic import BaseModel
from typing import Annotated, Optional
from pydantic import Field
from lang_graph.assistant.custom_operators import operator_replace_string, operator_replace_int


# %%
class Analyst(BaseModel):
    name: str = Field(description='Name of analyst')
    organization: str = Field(description='Organization of then analyst')
    role: str = Field(description='Role of the analyst')
    description: str = Field(description='Description of the analyst')

class Analysts(BaseModel):
    analysts: list[Analyst] = Field(
        default_factory=list,
        description="Comprehensive list of analysts with their name, role, "
                    "organization and description")

# %%
class InterviewState(BaseModel):
    topic: str
    analyst: Analyst
    conversations: Annotated[list[str], operator.add] = []
    questions: Annotated[list[str], operator.add] = []
    num_questions: int = 2
    search_results: Annotated[list[str], operator.add] = []
    answer: Annotated[list[str], operator.add] = []
    max_turns: int = 2
    section: str = None


class Questions(BaseModel):
    questions: list[str]


class SearchQueryState(BaseModel):
    query: str


# %%
class ResearchGraphState(BaseModel):
    max_analysts: int = 3
    topic: Annotated[str, operator_replace_string]
    human_feedback: Optional[str] = None
    analysts: list[Analyst] = []
    num_questions: Annotated[int, operator_replace_int] = 2
    section: Annotated[list[str], operator.add] = []
    report: str = None