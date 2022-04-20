import setuptools

setuptools.setup(
    name="ldz_tools", 
    version="1.0.0",
    author="Derry Liu",
    author_email="liudz@chinaexpressair.com",
    description="misc tools of ldz",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
    '': ['*.yaml', '*.csv'],
    },
)
