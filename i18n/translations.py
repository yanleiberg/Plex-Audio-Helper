import gettext
import os

def setup_i18n(language='zh_CN'):
    localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'i18n')
    translate = gettext.translation('messages', localedir, languages=[language], fallback=True)
    translate.install()
    return translate.gettext

_ = setup_i18n()