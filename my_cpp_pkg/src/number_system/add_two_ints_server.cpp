#include <rclcpp/rclcpp.hpp>
#include <example_interfaces/srv/add_two_ints.hpp>


using namespace example_interfaces::srv;

class AddTwoIntsServer : public rclcpp::Node{
   private:
    rclcpp::Service<AddTwoInts>::SharedPtr server_;

    void callbackAddTwoInts(const AddTwoInts::Request::SharedPtr req, AddTwoInts::Response::SharedPtr res) {
        res->sum = req->a + req->b;
        RCLCPP_INFO(this->get_logger(), "%ld + %ld = %ld", req->a, req->b, res->sum);
    }

   public:
    AddTwoIntsServer() : Node("add_two_ints_server") {
        server_ = this->create_service<AddTwoInts>("add_two_ints", std::bind(&AddTwoIntsServer::callbackAddTwoInts, this, std::placeholders::_1, std::placeholders::_2));

        RCLCPP_INFO(this->get_logger(), "add_two_ints_server Started...");
    }
};


int main(int argc, char** argv) {
    rclcpp::init(argc, argv);

    auto node = std::make_shared<AddTwoIntsServer>();
    rclcpp::spin(node);

    rclcpp::shutdown();
    
    return 0;
}