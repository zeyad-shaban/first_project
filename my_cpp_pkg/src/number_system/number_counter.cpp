#include <rclcpp/rclcpp.hpp>
#include <example_interfaces/srv/set_bool.hpp>
#include <example_interfaces/msg/int64.hpp>
#include <example_interfaces/msg/string.hpp>

using namespace std::chrono_literals;
using std::placeholders::_1;

class NumberCounter : public rclcpp::Node
{
private:
    rclcpp::Subscription<example_interfaces::msg::Int64>::SharedPtr subscriber;
    rclcpp::Publisher<example_interfaces::msg::Int64>::SharedPtr publisher;
    rclcpp::Service<example_interfaces::srv::SetBool>::SharedPtr service;
    int initial;
    int count;

    void numberCallback(const example_interfaces::msg::Int64::SharedPtr msg)
    {

        auto sender_msg = example_interfaces::msg::Int64();
        sender_msg.data = count += msg->data;
        publisher->publish(sender_msg);
    }

    void resetCounter(const std::shared_ptr<example_interfaces::srv::SetBool::Request> req, std::shared_ptr<example_interfaces::srv::SetBool::Response> res)
    {
        if (!req->data)
            return;

        res->success = true;
        count = initial;

        RCLCPP_INFO(this->get_logger(), "Reseted counter...");
    }

public:
    NumberCounter() : Node("number_count")
    {
        this->declare_parameter("initial_value", 5);
        initial = count = this->get_parameter("initial_value").as_int();

        subscriber = this->create_subscription<example_interfaces::msg::Int64>("number", 10, std::bind(&NumberCounter::numberCallback, this, _1));
        publisher = this->create_publisher<example_interfaces::msg::Int64>("number_count", 10);
        service = this->create_service<example_interfaces::srv::SetBool>("reset_counter", std::bind(&NumberCounter::resetCounter, this, std::placeholders::_1, std::placeholders::_2));

        this->declare_parameter("test123", 5);
        RCLCPP_INFO(this->get_logger(), "number_count Started...");
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);

    rclcpp::spin(std::make_shared<NumberCounter>());

    rclcpp::shutdown();
    return 0;
}