from setuptools import setup
setup(
    name='caPaloAlto',
    py_modules=['base', 'devices'],
    install_requires=['requests', 'ElementTree']
)