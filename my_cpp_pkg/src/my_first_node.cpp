#include "rclcpp/rclcpp.hpp"

class MyNode: public rclcpp::Node {
    public:

    MyNode(): rclcpp::Node("cpp_test"), counter(0) {
        RCLCPP_INFO(this->get_logger(), "bruh2");

        timer_ = this->create_wall_timer(std::chrono::seconds(2), std::bind(&MyNode::timerCallback, this));
    }

    private:
    
    void timerCallback() {
        RCLCPP_INFO(this->get_logger(), "Hello %d",++counter);
    }

    int counter = 0;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);

        auto node = std::make_shared<MyNode>();
    
    rclcpp::spin(node);
    rclcpp::shutdown();

    return 0;
}