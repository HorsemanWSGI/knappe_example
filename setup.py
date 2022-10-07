from setuptools import setup


setup(
    name='knappe_example',
    install_requires = [
        'horseman >= 1.0a1',
        'knappe',
        'colander',
        'deform',
        'chameleon',
    ],
    extras_require={
        'test': [
            'WebTest',
            'pytest',
            'pyhamcrest',
        ]
    }
)
