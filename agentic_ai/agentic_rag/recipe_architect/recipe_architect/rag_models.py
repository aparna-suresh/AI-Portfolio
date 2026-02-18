from pydantic import BaseModel
from pydantic import Field
from typing import Optional, Literal, List


class Route(BaseModel):
    datasource: Literal["vectorstore", "generic_search"] = Field(
        description="Given a user question choose to route it to generic search or a vectorstore.",
    )


class RecipeSearch(BaseModel):
    # content_search: Optional[str] = Field(
    #     None,
    #     description="Similarity search query.",
    # )
    # title_search: Optional[str] = Field(
    #     None,
    #     description=(
    #         "Alternate version of the content search query to apply to recipe titles. "
    #         "Should be succinct and only include key words that could be in a recipe "
    #         "title. Use only if user asks explicitly for a specific recipe."
    #     ),
    # )

    category: Optional[Literal[
        "Baking", "Breads", "Condiments and sides", "Drinks", "Grains and Pasta",
        "Mains", "Other", "Salads", "Soup", "Sweet", "Vegan"
    ]] = Field(
        None,
        description=(
            "Indicates the category of the recipe to search for. "
            "Should be one of the provided values."
            "MANDATORY: Select the best category from the list if mentioned. If not mentioned, return none."
            "Example: 'sourdough' -> Breads, 'cupcake' -> Baking, 'lentil soup' -> Soup. etc"
        )
    )
    is_nut_free: Optional[int] = Field(
        None,
        description="Nut free filter. Only use if explicitly specified.",
    )
    is_gluten_free: Optional[int] = Field(
        None,
        description="Gluten free filter. Only use if explicitly specified.",
    )
    is_dairy_free: Optional[int] = Field(
        None,
        description="Dairy free filter. Only use if explicitly specified.",
    )
    is_spicy_food: Optional[int] = Field(
        None,
        description="Spicy food filter. Only use if explicitly specified.",
    )

    is_comfort_food: Optional[int] = Field(
        None,
        description="Comfort food filter. Only use if explicitly specified.",
    )
    is_light_food: Optional[int] = Field(
        None,
        description="Light food filter. Only use if explicitly specified.",
    )
    is_hearty_food: Optional[int] = Field(
        None,
        description="Hearty food filter. Only use if explicitly specified.",
    )
    is_healthy: Optional[int] = Field(
        None,
        description="Healthy food filter. Only use if explicitly specified.",
    )

    is_breakfast: Optional[int] = Field(
        None,
        description="Breakfast filter. Only use if explicitly specified.",
    )
    is_lunch: Optional[int] = Field(
        None,
        description="Lunch filter. Only use if explicitly specified.",
    )
    is_dinner: Optional[int] = Field(
        None,
        description="Dinner filter. Only use if explicitly specified.",
    )
    is_quick: Optional[int] = Field(
        None,
        description="Quick filter. Only use if explicitly specified.",
    )

    is_no_oven: Optional[int] = Field(
        None,
        description="No oven filter. Only use if explicitly specified.",
    )

    is_slow_cooker: Optional[int] = Field(
        None,
        description="Slow cooker filter. Only use if explicitly specified.",
    )
    is_air_fryer: Optional[int] = Field(
        None,
        description="Air fryer filter. Only use if explicitly specified.",
    )
    is_one_pot: Optional[int] = Field(
        None,
        description="One pot filter. Only use if explicitly specified.",
    )

class Grade(BaseModel):
    title: str = Field(description="Title of the document being scored.")
    analysis: str = Field(description="A brief sentence explaining the relevance score given.")
    score: int = Field(
        description="Relevance score ranging from 0 to 5, with 0 being completely irrelevant and 5 being highly relevant.")


class GradeList(BaseModel):
    scores: List[Grade] = Field(description="List of relevance scores with analysis.")

class RedefinedQuery(BaseModel):
    reasoning: str = Field(description="Why the original query failed and what is being changed.")
    relaxed_filters: dict = Field(description="The new metadata filters (e.g., removing 'is_quick').")