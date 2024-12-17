from setuptools import find_packages, setup

package_name = 'turtle_eater'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='zeyadcode',
    maintainer_email='zeyadcode@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'turtle_spawner = turtle_eater.turtle_spawner:main',
            'turtle_hunter = turtle_eater.turtle_hunter:main',
        ],
    },
)
