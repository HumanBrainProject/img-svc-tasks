from setuptools import setup, find_packages

with open('requirements.txt') as fp:
    install_requires = fp.read()

setup(
    name="hbp-image-tasks",
    description="Tasks executed by the HBP Image Service",
    author="Akos Hencz",
    author_email="akos.hencz@epfl.ch",
    packages=["hbp_image_tasks"],
    install_requires=install_requires,
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'ingest=hbp_image_tasks.ingest:main',
            'fetch_input=hbp_image_tasks.fetch_input:main',
            'send_results=hbp_image_tasks.send_results:main'
        ]
    },
    version='0.0.1'
)
