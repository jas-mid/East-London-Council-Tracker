"""Headless tests of the Streamlit pages, using Streamlit's own test harness."""
import pytest
from streamlit.testing.v1 import AppTest

from council_tracker.paths import PROJECT_ROOT
from council_tracker.repository import get_repository


def open_contacts_page():
    app = AppTest.from_file(str(PROJECT_ROOT / "app.py"))
    app.switch_page("pages/contacts_page.py")
    return app.run()


def rendered_urls(app):
    return {element.proto.page for element in app.get("page_link")}


def test_contacts_page_prompts_for_a_council_first():
    app = open_contacts_page()
    assert not app.exception
    assert "Select your council" in app.info[0].value


@pytest.mark.parametrize("council", get_repository().members("east_london"), ids=lambda c: c.name)
def test_selecting_a_council_renders_each_of_its_links(council):
    app = open_contacts_page()
    app = app.sidebar.radio[0].set_value(council).run()

    assert not app.exception
    assert app.subheader[0].value == f"{council.name} Council"
    assert {link.url for link in council.links} <= rendered_urls(app)


@pytest.mark.parametrize("page", [None, "pages/statistics_page.py"], ids=["home", "statistics"])
def test_page_renders_without_errors(page):
    app = AppTest.from_file(str(PROJECT_ROOT / "app.py"))
    if page:
        app.switch_page(page)
    assert not app.run().exception
