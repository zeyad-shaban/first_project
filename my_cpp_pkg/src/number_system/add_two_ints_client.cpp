#include <rclcpp/rclcpp.hpp>
#include <example_interfaces/srv/add_two_ints.hpp>

using namespace std::chrono_literals;
using example_interfaces::srv::AddTwoInts;

class AddTwoIntsClient : public rclcpp::Node {
   private:
    rclcpp::Client<AddTwoInts>::SharedPtr client_;
    std::thread thread1_;

    void callAddTwoIntsServer(int a, int b) {
        while(!client_->wait_for_service(1s))
            RCLCPP_WARN(this->get_logger(), "Waiting for 'add_two_ints' server...");

        auto req = std::make_shared<AddTwoInts::Request>();
        req->a = a;
        req->b = b;

        auto future = client_->async_send_request(req);
        
        if (future.wait_for(5s) == std::future_status::ready) {
            try{
                auto res = future.get();
                RCLCPP_INFO(this->get_logger(), "%ld + %ld = %ld", req->a, req->b, res->sum);
            } catch (const std::exception &err) {
                RCLCPP_ERROR(this->get_logger(), "Service call 'add_two_ints' failed, %s", err.what());
            }
        } else {
            RCLCPP_ERROR(this->get_logger(), "Service call 'add_two_ints' timed out.");
        }
    }

   public:
    AddTwoIntsClient() : Node("add_two_ints_client")
    {
        client_ = this->create_client<AddTwoInts>("add_two_ints");
        thread1_ = std::thread(std::bind(&AddTwoIntsClient::callAddTwoIntsServer, this, 1,  4));
    }
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<AddTwoIntsClient>());
    rclcpp::shutdown();
    return 0;
}