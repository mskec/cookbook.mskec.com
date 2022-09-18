from marko.block import Document, Heading, List, Quote
from recipe_compiler.recipe import Recipe, RecipeCategory

import marko
import frontmatter
from marko.inline import RawText


def get_recipe_name(document: Document) -> str:
    """Returns the content of the first h1 (#) tag in a markdown document

    Args:
        document (Document): A Marko Markdown Document object

    Returns:
        str: The content of the first h1 tag in the document
    """

    for node in document.children:
        if type(node) is Heading and node.level == 1:
            return node.children[0].children


def get_quote(document: Document) -> str:
    """Returns the content of the first quote (>) tag in a markdown document

    Args:
        document (Document): A Marko Markdown Document object

    Returns:
        str: The content of the first quote tag in the document
    """

    for node in document.children:
        if type(node) is Quote:
            return "\n".join(
                text.children
                for text in node.children[0].children
                if type(text) is RawText
            )


def get_list_within_section(document: Document, header: str) -> list[str]:
    """Returns a list nested within a section defined by the header string

    Args:
        document (Document): A Marko Markdown Document object
        section (str): The string of a header defining a given section

    Returns:
        list[str]: A list of items within the given section
    """

    is_within_section = False

    for node in document.children:
        if type(node) is Heading:
            if node.children[0].children == header:
                is_within_section = True
            else:
                is_within_section = False
        if type(node) is List and is_within_section:
            return [item.children[0].children[0].children for item in node.children]


def get_ingredients(document: Document) -> list[str]:
    """Returns the list of ingredients from the recipe document

    Args:
        document (Document): A Marko Markdown Document object

    Returns:
        list[str]: A list of ingredients from the document
    """

    return get_list_within_section(document, "Ingredients")


def get_instructions(document: Document) -> list[str]:
    """Returns the list of instructions from the recipe document

    Args:
        document (Document): A Marko Markdown Document object

    Returns:
        list[str]: A list of instructions from the document
    """

    return get_list_within_section(document, "Directions")


def parse_to_recipe(content: str) -> Recipe:
    """Parse a Markdown formatted string to a Recipe object

    Args:
        content (str): A Markdown formatted string

    Returns:
        Recipe: A Recipe object representing the given content
    """

    recipe_metadata = frontmatter.loads(content)

    document = marko.parse(content)
    recipe_name = get_recipe_name(document)

    ingredients = list()
    instructions = list()
    in_ingredients = False
    in_instructions = False
    for line in content.splitlines():
        if line.strip().lower() == "## Ingredients".lower():
            in_ingredients = True
            in_instructions = False
        elif line.strip().lower() == "## Instructions".lower():
            in_ingredients = False
            in_instructions = True
        elif in_ingredients:
            ingredients.append(line)
        elif in_instructions:
            instructions.append(line)

    # quote = get_quote(document)
    # ingredients = get_ingredients(document)
    # instructions = get_instructions(document)

    category = RecipeCategory(recipe_metadata["category"].lower())
    cover_img = recipe_metadata["cover_img"] if "cover_img" in recipe_metadata else (category.value.lower() + ".png")
    # print(recipe_name, cover_img)

    return Recipe(
        name=recipe_metadata["name"],
        residence=recipe_metadata["residence"],
        category=category,
        recipe_name=recipe_name,
        cover_img=cover_img,
        quote=recipe_metadata["quote"] if "quote" in recipe_metadata else "",
        ingredients="\n".join(ingredients),
        instructions="\n".join(instructions),
    )
