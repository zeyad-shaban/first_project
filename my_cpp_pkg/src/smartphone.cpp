#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"


class Smartphone : public rclcpp::Node  {
    public:
    Smartphone() : Node("smartphone") {
        subscription_ = this->create_subscription<std_msgs::msg::String>("robot_news", 10, std::bind(&Smartphone::onRobotNews, this, std::placeholders::_1));

        RCLCPP_INFO(this->get_logger(), "Smartphone has started");
    }

    void onRobotNews(const std_msgs::msg::String::SharedPtr msg) {
        RCLCPP_INFO(this->get_logger(), "I heard: %s", msg->data.c_str());
    }

    private:
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<Smartphone>());
    rclcpp::shutdown();
    
    return 0;
}