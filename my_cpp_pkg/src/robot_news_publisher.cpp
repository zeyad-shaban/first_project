#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"


using namespace std::chrono_literals;

class RobotNewsPublisher : public rclcpp::Node {
    public:
    RobotNewsPublisher() : Node("robot_news_publisher") {
        publisher_ = this->create_publisher<std_msgs::msg::String>("robot_news", 10);
        timer_ = this->create_wall_timer(500ms, std::bind(&RobotNewsPublisher::publishNews, this));

        RCLCPP_INFO(this->get_logger(), "Robot News Publisher CPP has started");
    }

    private:
    void publishNews() {
        auto msg = std_msgs::msg::String();
        msg.data = "Hello world " + robot_name;

        publisher_->publish(msg);
    }
    std::string robot_name = "X001_CPP";
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);

    auto node = std::make_shared<RobotNewsPublisher>();
    rclcpp::spin(node);
    rclcpp::shutdown();

    return 0;
}