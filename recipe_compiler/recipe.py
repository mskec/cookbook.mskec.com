from dataclasses import dataclass
from recipe_compiler.recipe_category import RecipeCategory

import frontmatter


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
