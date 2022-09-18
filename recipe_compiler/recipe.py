from enum import Enum
from dataclasses import dataclass

import frontmatter


class RecipeCategory(Enum):
    APPETIZER = "appetizer"
    ENTREE = "entree"
    ASIAN = "asian"
    ITALIAN = "italian"
    DESSERT = "dessert"
    OTHER = "other"

@dataclass
class Recipe:
    name: str
    residence: str
    category: RecipeCategory
    recipe_name: str
    cover_img: str
    quote: str
    ingredients: str
    instructions: str

    @property
    def slug(self) -> str:
        """Returns the recipe name formatted as kebab-case

        Returns:
            str: The recipe_name in kebab-case format
        """

        return self.recipe_name.lower()\
            .replace("č", "c")\
            .replace("ć", "c")\
            .replace("đ", "d")\
            .replace("š", "s")\
            .replace(" ", "-")\
            .replace("'", "")\
            .replace('"', "")
