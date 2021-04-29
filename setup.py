from setuptools import setup

setup(
    name='nebulento',
    version='0.1.0',
    packages=['nebulento'],
    url='https://github.com/OpenJarbas/nebulento',
    license='apache-2.0',
    author='jarbasai',
    author_email='jarbasai@mailfence.com',
    install_requires=["quebra_frases", "rapidfuzz"],
    description='dead simple fuzzy matching intent parser'
)
