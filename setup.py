from setuptools import setup, find_packages

setup(name="phylonetwork",
    version="1.1",
    author=(u"Gabriel Cardona"
            u", David Sánchez"
            u", Pau Ruŀlan Ferragut"),
    author_email=(u"bielcardona@gmail.com"
                  u", dscharles@gmail.com"
                  u", pau@rullan.cat"),
    license="BSD",
    keywords="phylogenetic trees networks",
    packages=['phylonetwork'],
    package_dir = {'phylonetwork': 'src/phylonetwork'},
    install_requires = [
        'networkx',
        'pyparsing',
        'numpy'
    ]
)
