"""Main Controller"""

from mediaplex.lib.base import BaseController
from mediaplex.lib import helpers
from mediaplex.controllers.error import ErrorController
from mediaplex.controllers.admin import AdminController

from tg import expose, flash, require, url, request, redirect
from pylons.i18n import ugettext as _
#from tg import redirect, validate

#from catwalk.tg2 import Catwalk
from repoze.what import predicates
from mediaplex.controllers.secure import SecureController

class RootController(BaseController):
    @expose('mediaplex.templates.login')
    def login(self, came_from=url('/')):
        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(
            login_counter = str(login_counter),
            came_from = came_from,
        )

    @expose()
    def post_login(self, came_from=helpers.url_for(controller='/admin')):
        if not request.identity:
            login_counter = request.environ['repoze.who.logins'] + 1
            redirect(came_from)
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=url('/')):
        flash(_('We hope to see you soon!'))
        redirect(came_from)
