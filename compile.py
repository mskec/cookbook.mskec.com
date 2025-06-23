from jinja2 import Environment, PackageLoader, select_autoescape
from recipe_compiler.read import read_recipe_file
from recipe_compiler.parse import parse_to_recipe
from recipe_compiler.render import (
    render_home_page,
    render_recipe_page,
)
from recipe_compiler.write import write_home_page, write_page

import shutil
import argparse
import glob
import minify_html

OUT_DIR = "./out"

parser = argparse.ArgumentParser()
parser.add_argument(
    "-t", "--target", help="The target for compilation ['dev','prod']", default="dev"
)

if __name__ == "__main__":
    target = parser.parse_args().target

    # Read
    recipe_files = glob.glob("./recipes/*.md")
    recipe_contents = [read_recipe_file(recipe_file) for recipe_file in recipe_files]

    # Parse
    recipes = [parse_to_recipe(recipe_content) for recipe_content in recipe_contents]

    # Render
    env = Environment(
        loader=PackageLoader("recipe_compiler", "templates"),
        autoescape=select_autoescape(["html"]),
    )

    # Handles the path setting for production versus local
    # (Production has /cookbook/ prepended to the path)
    env.globals = {"path_base": "/"}

    home_page = render_home_page(recipes, env)
    # contribute_page = render_contribute_page(env)
    recipe_pages = zip(
        [recipe.slug for recipe in recipes],
        [render_recipe_page(recipe, env) for recipe in recipes],
    )

    # Minify html
    if target == 'prod':
        home_page = minify_html.minify(home_page)
        recipe_pages = map(
            lambda page: [page[0], minify_html.minify(page[1])],
            recipe_pages
        )

    # Write
    write_home_page(home_page)
    # write_page("contribute", contribute_page)
    for recipe_slug, recipe_page in recipe_pages:
        write_page(recipe_slug, recipe_page)

    # Copy resources
    shutil.copytree("./public", OUT_DIR, dirs_exist_ok=True)
