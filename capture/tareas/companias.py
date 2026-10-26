TASK = dict(
    id='companias',
    title='Trabajar con las dos compañías (Sunset y Pinveco)',
    short='Las dos compañías',
    cat='empezar',
    summary='Cada furgoneta es de Sunset o de Pinveco, y cada compañía factura lo suyo. Para que todo funcione, ten **siempre marcadas las dos** arriba a la derecha.',
    when='Lo primero al entrar cada día, y siempre que te salga un error de compañía o de «Acceso denegado».',
    before=['Has entrado en Odoo con tu usuario.'],
    tags=['compania', 'empresa', 'sunset', 'pinveco', 'selector', 'acceso denegado', 'marcar companias', 'multiempresa'],
    result='Ves las furgonetas, contratos y facturas de las dos compañías. Los contratos se pasan solos a la compañía dueña de la furgoneta.',
    notes=[['warn', 'Con **solo una** compañía marcada, al elegir una furgoneta de la otra te saldrá: «Marque también … en el selector de compañías». No es un fallo: marca las dos.']],
    next=['menu', 'reservar'],
)


def run(g):
    g.open_app()
    sw = g.page.locator('.o_switch_company_menu').first
    g.step('Arriba a la derecha está el **selector de compañías**. Púlsalo.', marks=[sw], crop='top')
    sw.click()
    g.wait(800)
    menu = g.page.locator('.o-dropdown--menu').last
    g.step('Marca las casillas de **Sunset** y **Pinveco**: las dos tienen que tener el ✓.',
           labels=['Casilla de **Sunset**.', 'Casilla de **Pinveco**.'],
           marks=[menu.locator('.dropdown-item, .o_switch_company_item', has_text='Sunset').first,
                  menu.locator('.dropdown-item, .o_switch_company_item', has_text='Pinveco').first],
           crop=menu,
           detail='El nombre que sale en **negrita** es la compañía «principal» del momento. Da igual cuál sea mientras las **dos** estén marcadas.')
    g.page.keyboard.press('Escape')
