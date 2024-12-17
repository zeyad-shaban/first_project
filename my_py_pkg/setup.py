from setuptools import find_packages, setup

package_name = 'my_py_pkg'

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
            'py_node = my_py_pkg.my_first_node:main',
            'robot_news_publisher = my_py_pkg.robot_news_publisher:main',
            'mobile_phone = my_py_pkg.mobile_phone:main',
            'add_two_ints_server = my_py_pkg.add_two_ints_server:main',
            'add_two_ints_client = my_py_pkg.add_two_ints_client:main',
            'number_publisher = my_py_pkg.number_publisher:main',
            'number_counter = my_py_pkg.number_counter:main',
            'hardware_status_publisher = my_py_pkg.hardware_status_publisher:main',
            'battery_control = my_py_pkg.battery_control:main',
            'led_control = my_py_pkg.led_control:main',
        ],
    },
)
