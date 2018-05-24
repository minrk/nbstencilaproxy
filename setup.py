import setuptools

setuptools.setup(
    name="nbstencilaproxy",
    version='0.1.0.dev',
    url="https://github.com/minrk/nbstencilaproxy",
    author="Min RK, Daniel Nüst, Ryan Lovett",
    description="Jupyter extension to proxy Stencila",
    packages=setuptools.find_packages(),
	keywords=['Jupyter'],
	classifiers=['Framework :: Jupyter'],
    install_requires=[
        'notebook',
        'nbserverproxy >= 0.8.3',
    ],
    package_data={'nbstencilaproxy': ['static/*']},
)
