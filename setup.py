import setuptools

with open('C:/Users/158333/OneDrive - Arrow Electronics, Inc/Documents/Mentor project/Packages/requirements.txt') as r:
    install_requires = r.read().splitlines()

setuptools.setup(
    name='autofw',
    version='2.0.2',
    author='Krunal Prajapati, Rohan Bangoriya',
    author_email='krunalprajapati1904@gmail.com, rohanbangoriya008@gmail.com',
    description="this is trial run autofw packages...",
    packages=setuptools.find_packages(),
    entry_points={"pytest11": ["plugin1 = autofw.pytest_plugins.pytest_hooks",
                               "plugin2 = autofw.pytest_plugins.session_fixtures",
                               "plugin3 = autofw.pytest_plugins.function_fixtures"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires
)
