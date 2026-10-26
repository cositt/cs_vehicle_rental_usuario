TASK = dict(
    id='nuevo-cliente',
    title='Dar de alta un cliente nuevo',
    short='Cliente nuevo',
    cat='clientes',
    summary='Antes de reservar, el cliente tiene que existir. Para particulares se rellenan también los datos de conducción (DNI y carnet).',
    when='Llega un cliente que no ha alquilado nunca.',
    before=['Tienes su DNI (o CIF si es empresa), dirección, teléfono y correo.',
            'Si va a conducir él: su carnet de conducir.'],
    tags=['cliente nuevo', 'alta cliente', 'crear cliente', 'contacto', 'dni', 'nif', 'cif', 'carnet', 'conductor', 'empresa', 'particular'],
    result='El cliente ya sale al escribir su nombre en el asistente de reserva.',
    notes=[['tip', '¿Es una **empresa** con varios conductores? Crea la empresa y añade cada conductor como contacto suyo: [[conductor-empresa]].']],
    next=['reservar', 'conductor-empresa'],
)


def run(g):
    g.open_app()
    g.step('Pulsa **Clientes** en el menú.', marks=[g.menu('Clientes')], crop='top')
    g.go('Clientes')
    new = g.page.locator('.o_control_panel button.o-kanban-button-new, .o_control_panel button.o_list_button_add, .o_control_panel button', has_text='Nuevo').first
    g.step('Antes de crear, **busca** si ya existe (por nombre, teléfono o DNI). Si no sale, pulsa **Nuevo**.',
           marks=[g.page.locator('.o_searchview').first, new], crop='top')
    new.click()
    g.wait(1500)
    g.radio('company_type', 'Individuo')
    g.fill('name', 'Juan Ejemplo Ruiz')
    g.fill('street', 'C/ Inventada, 7')
    g.fill('zip', '29004')
    g.fill('city', 'Málaga')
    g.fill('phone', '600 000 004')
    g.fill('email', 'juan.ejemplo@ejemplo.es')
    g.fill('vat', '22222222J')
    g.step('Rellena los datos básicos:',
           labels=['**Individuo** (particular) o **Compañía** (empresa). Sale marcado **Individuo**: cámbialo solo si es una empresa.', '**Nombre** completo (o razón social).', '**Dirección**.',
                   '**Teléfono** y **correo**: el correo es donde le llegan contrato y facturas.', '**NIF** (DNI o CIF).'],
           marks=[g.field('company_type'), g.field('name'), [g.field('street'), g.field('city'), g.field('zip')],
                  [g.field('phone'), g.field('email')], g.field('vat')],
           crop=g.page.locator('.o_form_sheet').first)
    tab = g.tab('Conducción')
    tab.click()
    g.wait(600)
    g.fill('driver_identity_number', '22222222J')
    g.fill('birth_date', '15/03/1988')
    g.fill('driver_license_number', '22222222J')
    g.fill('driver_license_issue_date', '20/04/2008')
    g.fill('driver_license_expiry_date', '20/04/2033')
    g.step('Si va a conducir, abre la pestaña **Conducción** y rellena DNI, fecha de nacimiento y **carnet**.',
           labels=['Pestaña **Conducción**.', 'DNI y fecha de nacimiento (para saber si es menor de 25 o mayor de 60).', 'Número de carnet, expedición y caducidad.'],
           marks=[tab, [g.field('driver_identity_number'), g.field('birth_date')],
                  [g.field('driver_license_number'), g.field('driver_license_issue_date'), g.field('driver_license_expiry_date')]],
           crop=g.band(tab, g.field('driver_license_number')),
           warn='La **caducidad** del carnet no puede ser anterior a la **expedición**. Revisa que no esté caducado.')
    g.save()
    g.step('Guarda (la nube de arriba). Ya puedes reservarle una furgoneta.', marks=[g.page.locator('.o_breadcrumb').first], crop='top')
