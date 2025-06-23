# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a static recipe website generator that converts Markdown recipe files into a beautiful HTML cookbook. The project is forked from Microsoft/DevCookbook and creates a personal cookbook website.

## Setup Commands

### Environment Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment (run this before other commands)
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### Build/Compile
```bash
# Development build
python3 compile.py --target dev

# Production build (with HTML minification)
python3 compile.py --target prod
```

### Testing
```bash
# Run tests (ensure virtual environment is activated)
python3 -m pytest tests/
```

## Architecture

The codebase follows a modular pipeline architecture:

1. **Recipe Files**: Markdown files in `recipes/` with YAML frontmatter containing metadata (name, residence, category) and structured content (ingredients, instructions)
2. **Compiler Pipeline**: The `recipe_compiler/` module processes recipes through distinct phases:
   - `read.py`: Reads recipe files from disk
   - `parse.py`: Parses Markdown + frontmatter into Recipe objects using marko and python-frontmatter
   - `recipe.py`: Defines the Recipe dataclass and RecipeCategory enum
   - `render.py`: Converts Recipe objects to HTML using Jinja2 templates
   - `write.py`: Writes generated HTML files to the output directory
3. **Templates**: Jinja2 HTML templates in `recipe_compiler/templates/` for homepage and individual recipe pages
4. **Static Assets**: CSS and images in `public/` directory, copied to output
5. **Output**: Generated static site in `out/` directory

## Recipe Structure

Recipe files use this format:
```markdown
---
name: Author Name
residence: Location
category: italian|asian|appetizer|entree|dessert|other
css_html_background: optional-hex-color
cover_img: optional-custom-image.png
quote: optional-quote-text
---

# Recipe Name

## Ingredients
* ingredient 1
* ingredient 2

## Instructions
* step 1
* step 2
```

Categories determine the default cover image and affect homepage grouping. The slug generation handles special characters (Croatian diacritics: č→c, ć→c, đ→d, š→s).

## Development Notes

- Always activate the virtual environment before running commands
- HTML minification only applies to production builds (`--target prod`)
- Templates use `path_base` global for production vs local path handling
- Static assets are copied from `public/` to `out/` after HTML generation
- Recipe parsing handles both frontmatter metadata and markdown content sections