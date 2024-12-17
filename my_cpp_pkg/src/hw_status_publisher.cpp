#include "rclcpp/rclcpp.hpp"
#include "dummy_interfaces/msg/hardware_status.hpp"


using namespace std::chrono_literals;

class HWStatusPublisher : public rclcpp::Node
{
public:
    HWStatusPublisher() : Node("hw_status_publisher")
    {
        publisher_ = this->create_publisher<dummy_interfaces::msg::HardwareStatus>("hw_status", 10);
        timer_ = this->create_wall_timer(1s, std::bind(&HWStatusPublisher::callback_publish_hw_status, this));

        RCLCPP_INFO(this->get_logger(), "hw_status_publisher/hw_status topic Started...");
    }

    void callback_publish_hw_status()
    {
        auto msg = dummy_interfaces::msg::HardwareStatus();
        msg.are_motors_ready = true;
        msg.burning = true;
        msg.debug_msg = "python is better still...";

        publisher_->publish(msg);
    }

private:
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<dummy_interfaces::msg::HardwareStatus>::SharedPtr publisher_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);

    rclcpp::spin(std::make_shared<HWStatusPublisher>());
    rclcpp::shutdown();

    return 0;
}