import setuptools

setuptools.setup(
    name="nbstencilaproxy",
    version='0.1.0',
    url="https://github.com/nuest/nbstencilaproxy",
    author="Min RK, Daniel Nüst, Ryan Lovett",
    description="Jupyter extension to proxy Stencila",
    packages=setuptools.find_packages(),
	keywords=['Jupyter'],
	classifiers=['Framework :: Jupyter'],
    install_requires=[
        'notebook',
        'nbserverproxy >= 0.8.2'
    ],
    package_data={'nbstencilaproxy': ['static/*']},
)
