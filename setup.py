from setuptools import setup, find_packages


# Used for installing test dependencies directly
tests_require = [
    'nose',
    'flake8'
]

setup(
    name='meter-events',
    version='1.0.0',
    description="Telemetry Processing service for meter event detection",
    author="Robbie Eaton",
    author_email="john.robert.eaton@gmail.com",
    python_requires=">=3.7",    # Uses f-strings extensively
    packages=find_packages(exclude=['test', 'fixtures']),
    install_requires=[],
    test_suite='nose.collector',
    tests_require=tests_require,
    # For installing test dependencies directly
    extras_require={'test': tests_require},
    entry_points={
        'console_scripts': [
            'process_meter_events=meter_events.__main__:main'
            ],
        },
)
