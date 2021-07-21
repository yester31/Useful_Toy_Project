#include <websocketpp/config/asio_no_tls.hpp>
#include <websocketpp/server.hpp>
#include <rapidjson/document.h>
#include <rapidjson/writer.h>
#include <rapidjson/stringbuffer.h>
#include <rapidjson/rapidjson.h>
#include <sstream>
#include <chrono>
#include <iostream>
#include <string>
#include <regex>

using namespace std;
using namespace chrono;
using namespace rapidjson;

typedef websocketpp::server<websocketpp::config::asio> server;

using websocketpp::lib::placeholders::_1;
using websocketpp::lib::placeholders::_2;
using websocketpp::lib::bind;

map<std::string, websocketpp::connection_hdl> ws_map;

string get_time_stamp()
{
	system_clock::time_point now = system_clock::now();
	system_clock::duration tp = now.time_since_epoch();

	tp -= duration_cast<seconds>(tp);

	time_t tt = system_clock::to_time_t(now);
	char time_str[1000];
	tm t = *localtime(&tt);
	sprintf(time_str, "%04u-%02u-%02u %02u:%02u:%02u.%03u", t.tm_year + 1900,
		t.tm_mon + 1, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec,
		static_cast<unsigned>(tp / milliseconds(1)));
	return time_str;
}

// pull out the type of messages sent by our config
typedef server::message_ptr message_ptr;

// Define a callback to handle incoming messages
void on_message(server* s, websocketpp::connection_hdl hdl, message_ptr msg) {
	//std::cout << "on_message called with hdl: " << hdl.lock().get()
	//	<< " and message: " << msg->get_payload()
	//	<< std::endl;

	// check for a special command to instruct the server to stop listening so
	// it can be cleanly exited.
	if (msg->get_payload() == "stop-listening") {
		s->stop_listening();
		return;
	}
	int count = 5;
	std::string payload = msg->get_payload();
	cout << "msg=[" << payload << "]" << endl;

	Document d;
	d.Parse(payload.c_str());

	string optype = d["optype"].GetString();
	std::cout << optype << std::endl;
	if (optype == "client_msg") {
		count = d["count"].GetInt();
		count -= 1;
	}

	try {
		stringstream ss;
		ss << "{" << endl;
		ss << "\"optype\" : \"" << "server_msg" << "\"," << endl;
		ss << "\"wsid\" : \"" << "c++ server" << "\"," << endl;
		ss << "\"wstype\" : \"" << "server" << "\"," << endl;
		ss << "\"count\" : \"" << count << "\"," << endl;
		ss << "\"timestamp\" : \"" << get_time_stamp() << "\"" << endl;
		ss << "}" << endl;
		string output_buf = ss.str();
		s->send(hdl, output_buf, msg->get_opcode());
		cout << "opcode??=[" << msg->get_opcode() << "]" << endl;
	}
	catch (websocketpp::exception const & e) {
		std::cout << "Echo failed because: "
			<< "(" << e.what() << ")" << std::endl;
	}
}

void on_open(server* s, websocketpp::connection_hdl hdl) {

	std::cout << "on_open" << std::endl;
	server::connection_ptr con = s->get_con_from_hdl(hdl);
	std::string ws_info = con->get_resource();
	string wsid;
	string wstype;
	std::regex re_wsid(".+wsid=([^&]+).*");
	std::regex re_wstype(".+wstype=([^&]+).*");
	std::smatch match_wsid;
	std::smatch match_wstype;
	if (std::regex_search(ws_info, match_wsid, re_wsid)) {
		std::cout << match_wsid[1].str() << std::endl;
		wsid = match_wsid[1].str();
	}
	if (std::regex_search(ws_info, match_wstype, re_wstype)) {
		std::cout << match_wstype[1].str() << std::endl;
		wstype = match_wstype[1].str();
	}
	string ws_key = wstype + wsid;
	ws_map.insert(pair<string, websocketpp::connection_hdl>(ws_key, hdl));
	std::cout << "the number of websocket connections :: "<<ws_map.size() << std::endl;

}

void on_close(server* s, websocketpp::connection_hdl hdl) {

	std::cout << "on_close" << std::endl;
	server::connection_ptr con = s->get_con_from_hdl(hdl);
	std::string ws_info = con->get_resource();
	string wsid;
	string wstype;
	std::regex re_wsid(".+wsid=([^&]+).*");
	std::regex re_wstype(".+wstype=([^&]+).*");
	std::smatch match_wsid;
	std::smatch match_wstype;
	if (std::regex_search(ws_info, match_wsid, re_wsid)) {
		std::cout << match_wsid[1].str() << std::endl;
		wsid = match_wsid[1].str();
	}
	if (std::regex_search(ws_info, match_wstype, re_wstype)) {
		std::cout << match_wstype[1].str() << std::endl;
		wstype = match_wstype[1].str();
	}
	string ws_key = wstype + wsid;
	ws_map.erase(ws_key);
	std::cout << "the number of websocket connections :: " << ws_map.size() << std::endl;

}

int main() {
	// Create a server endpoint
	server echo_server;

	try {
		// Set logging settings
		echo_server.set_access_channels(websocketpp::log::alevel::all);
		echo_server.clear_access_channels(websocketpp::log::alevel::frame_payload);

		// Initialize Asio
		echo_server.init_asio();

		// Register handler callbacks
		echo_server.set_open_handler(bind(&on_open, &echo_server, ::_1));
		echo_server.set_close_handler(bind(&on_close, &echo_server, ::_1));
		echo_server.set_message_handler(bind(&on_message, &echo_server, ::_1, ::_2));
		// Listen on port 9002
		echo_server.listen(9002);

		// Start the server accept loop
		echo_server.start_accept();

		// Start the ASIO io_service run loop
		echo_server.run();
	}
	catch (websocketpp::exception const & e) {
		std::cout << e.what() << std::endl;
	}
	catch (...) {
		std::cout << "other exception" << std::endl;
	}
}
