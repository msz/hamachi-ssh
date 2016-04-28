from setuptools import setup, find_packages
setup(
    name="hamachi-ssh",
    version="1.0",
    packages=find_packages(),
    scripts=["hamachi_ssh.py"],
    entry_points={
        "console_scripts": ["hamachi-ssh-update = hamachi_ssh:main"]
    },

    # metadata for upload to PyPI
    author="Michał Szewczak",
    description="A helper utility for easy SSH connection to machines on Hamachi",
    license="MIT",
    keywords="hamachi ssh config hostname update ip",
    url="https://github.com/iroq/hamachi-ssh",
    download_url="https://github.com/iroq/hamachi-ssh/archive/v1.0.tar.gz"
)