from recipe_compiler.recipe import Recipe, RecipeCategory


def test_recipe_slug():
    # Given
    name = "Thomas Eckert"
    residence = "Seattle, WA"
    category = RecipeCategory("dessert")
    recipe_name = '"Pie" Shell Script'
    quote = "Hello, World"
    ingredients = [""]
    instructions = [""]

    expected = "pie-shell-script"

    # When
    recipe = Recipe(
        name=name,
        residence=residence,
        category=category,
        recipe_name=recipe_name,
        cover_img="dessert.png",
        style_block=None,
        quote=quote,
        ingredients="\n".join(ingredients),
        instructions="\n".join(instructions)
    )

    # Then
    assert expected == recipe.slug
