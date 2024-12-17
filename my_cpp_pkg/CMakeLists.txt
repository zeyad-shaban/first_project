cmake_minimum_required(VERSION 3.8)
project(my_cpp_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in further dependencies manually.
# find_package(<dependency> REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(example_interfaces REQUIRED)
find_package(dummy_interfaces REQUIRED)

add_executable(cpp_node src/my_first_node.cpp)
add_executable(robot_news_publisher src/robot_news_publisher.cpp)
add_executable(smartphone src/smartphone.cpp)
add_executable(hw_status_publisher src/hw_status_publisher.cpp)
add_executable(number_counter src/number_system/number_counter.cpp)
add_executable(add_two_ints_server src/number_system/add_two_ints_server.cpp)
add_executable(add_two_ints_client src/number_system/add_two_ints_client.cpp)

ament_target_dependencies(
  cpp_node
  rclcpp
  std_msgs
)

ament_target_dependencies(
  robot_news_publisher
  rclcpp
  std_msgs
)

ament_target_dependencies(
  smartphone
  rclcpp
  std_msgs
)

ament_target_dependencies(
  number_counter
  rclcpp
  std_msgs
  example_interfaces
)

ament_target_dependencies(
  add_two_ints_server
  rclcpp
  example_interfaces
)

ament_target_dependencies(
  add_two_ints_client
  rclcpp
  example_interfaces
)

ament_target_dependencies(
  hw_status_publisher
  rclcpp
  dummy_interfaces
)

install(
  TARGETS
  cpp_node
  robot_news_publisher
  smartphone
  number_counter
  add_two_ints_server
  add_two_ints_client
  hw_status_publisher
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
