import os

OUT_DIR = "./out"

def write_home_page(home_page: str):
    """Writes the home_page HTML to file

    Args:
        home_page (str): A string of HTML to be written to file
    """

    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)
    
    with open(f"{OUT_DIR}/index.html", "w+") as f:
        f.write(home_page)


def write_page(slug: str, page: str):
    """Writes the page HTML to `/{slug}/index.html`

    Args:
        slug (str):
        page (str): A string of HTML to be written to file
    """

    assert slug != "index"

    if not os.path.exists(f"{OUT_DIR}/{slug}"):
        os.makedirs(f"{OUT_DIR}/{slug}")

    with open(f"{OUT_DIR}/{slug}/index.html", "w+") as f:
        f.write(page)
