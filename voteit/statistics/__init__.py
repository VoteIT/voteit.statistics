from pyramid.i18n import TranslationStringFactory

PROJECTNAME = 'voteit.statistics'
StatisticsMF = TranslationStringFactory(PROJECTNAME)


def includeme(config):
    config.scan(PROJECTNAME)
    config.add_translation_dirs('%s:locale/' % PROJECTNAME)
