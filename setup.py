from distutils.command.build_py import build_py
import glob
import os
from subprocess import check_call
import tempfile

import setuptools

here = os.path.dirname(os.path.abspath(__file__))
name = "nbstencilaproxy"
pkg = os.path.join(here, name)


def npm_install():
    """Install nbstencilaproxy js package"""
    with tempfile.TemporaryDirectory() as td:
        check_call(["npm", "pack", here], cwd=td)
        tgz = glob.glob(os.path.join(td, "*.tgz"))[0]
        check_call(["npm", "install", "--no-save", tgz], cwd=pkg)


class build_npm_py(build_py):
    """install with npm packages"""

    def run(self):
        # when installing, install npm package
        npm_install()
        return super().run()


setuptools.setup(
    name=name,
    version="0.1.0.dev",
    url="https://github.com/minrk/" + name,
    author="Min RK, Daniel Nüst, Ryan Lovett",
    description="Jupyter extension to proxy Stencila",
    packages=setuptools.find_packages(),
    cmdclass={"build_py": build_npm_py},
    keywords=["Jupyter"],
    classifiers=["Framework :: Jupyter"],
    install_requires=["notebook", "nbserverproxy >= 0.8.3"],
    package_data={"nbstencilaproxy": ["static/**", "node_modules/**"]},
)
