from setuptools import setup

setup(
    name='farmbot-py',
    version='0.1',
    packages=['farmbot', '', 'farmbot'],
    package_dir={'': 'src'},
    url='https://github.com/xebia/farmbot-py',
    license='',
    author='Serge Beaumont',
    author_email='',
    description='Client for FarmBot via MQTT', install_requires=['paho-mqtt', 'requests']
)
