from setuptools import setup

PLUGIN_ENTRY_POINT = 'ovos-intent-plugin-nebulento=nebulento.opm:NebulentoPipelinePlugin'


setup(
    name='nebulento',
    version='0.1.0',
    packages=['nebulento'],
    url='https://github.com/OpenJarbas/nebulento',
    license='apache-2.0',
    author='jarbasai',
    author_email='jarbasai@mailfence.com',
    install_requires=["quebra_frases", "rapidfuzz"],
    description='dead simple fuzzy matching intent parser',
    entry_points={'ovos.pipeline': PLUGIN_ENTRY_POINT}
)
