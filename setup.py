import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="emtvlc_api",
	version="0.1.1",
	author="Ed0",
	author_email="ed0@ed0.com",
	description="Python module to retrieve bus times and stops for EMT valencia",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/ElEd0/EMTValencia-API",
	packages=setuptools.find_packages(),
	install_requires=[
		'requests'
	],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)