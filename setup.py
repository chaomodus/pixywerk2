"""Package configuration."""
from setuptools import find_packages, setup

LONG_DESCRIPTION = """Pixywerk 2 is a filesystem based static site generator."""

INSTALL_REQUIRES = ["yaml-1.3", "markdown", "jstyleson", "jinja2"]

# Extra dependencies
EXTRAS_REQUIRE = {
    # Test dependencies
    "tests": [
        "black",
        "bandit>=1.1.0",
        "flake8>=3.2.1",
        "mypy>=0.470",
        "prospector[with_everything]>=0.12.4",
        "pytest-cov>=1.8.0",
        "pytest-xdist>=1.15.0",
        "pytest>=3.0.3",
        "sphinx_rtd_theme>=0.1.6",
        "sphinx-argparse>=0.1.15",
        "Sphinx>=1.4.9",
    ]
}

SETUP_REQUIRES = ["pytest-runner>=2.7.1", "setuptools_scm>=1.15.0"]
setup(
    author="Cassowary Rusnov",
    author_email="rusnovn@gmail.com",
    classifiers=[
        "Development Status :: 1 - Pre-alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    description="A filesystem-based website generator / CMS",
    # entry_points={
    #    'console_scripts': [
    #        'cookbook = spicerack.cookbook:main',
    #    ],
    # },
    include_package_data=True,
    extras_require=EXTRAS_REQUIRE,
    install_requires=INSTALL_REQUIRES,
    keywords=["cms", "website", "compiler"],
    license="MIT",
    long_description=LONG_DESCRIPTION,
    name="pixywerk2",
    packages=find_packages(exclude=["*.tests", "*.tests.*"]),
    platforms=["GNU/Linux"],
    setup_requires=SETUP_REQUIRES,
    use_scm_version=True,
    url="https://git.antpanethon.com/cas/pixywerk2",
    zip_safe=False,
)
