"""Shared steps of the configuration tours (menu «+» → list → record)."""

ADMIN = 'Solo para el **responsable**: el personal de mostrador normalmente no ve estos menús.'


def open_list(g, menu, text):
    g.open_app()
    item = g.menu(menu)
    g.step(text, marks=[item], crop='top')
    item.click()
    g.page.wait_for_selector('.o_list_view .o_data_row', timeout=30000)
    g.wait(900)


def search(g, value):
    box = g.page.locator('.o_searchview input').first
    box.fill(value)
    g.wait(600)
    box.press('Enter')
    g.page.locator('.o_searchview .o_facet_values', has_text=value).first.wait_for(timeout=10000)
    if g.page.locator('.o_searchview_autocomplete:visible').count():
        box.press('Escape')
    g.wait(1500)


def open_record(g, row):
    cells = row.locator('td.o_data_cell:not(.o_handle_cell)')
    cells.first.click()
    g.page.wait_for_selector('.o_form_view .o_form_sheet', timeout=30000)
    g.wait(900)
