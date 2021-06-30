/*
 * Copyright (c) 2016, Peter Thorson. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in the
 *       documentation and/or other materials provided with the distribution.
 *     * Neither the name of the WebSocket++ Project nor the
 *       names of its contributors may be used to endorse or promote products
 *       derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL PETER THORSON BE LIABLE FOR ANY
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 */
#include <cstdlib>

#include <websocketpp/config/asio_no_tls_client.hpp>
#include <websocketpp/client.hpp>
#include <rapidjson/document.h>
#include <rapidjson/writer.h>
#include <rapidjson/stringbuffer.h>
#include <rapidjson/rapidjson.h>
#include <sstream>
#include <chrono>
#include <iostream>
#include <string>

using namespace std;
using namespace chrono;
using namespace rapidjson;

typedef websocketpp::client<websocketpp::config::asio_client> client;

using websocketpp::lib::placeholders::_1;
using websocketpp::lib::placeholders::_2;
using websocketpp::lib::bind;

// pull out the type of messages sent by our config
typedef websocketpp::config::asio_client::message_type::ptr message_ptr;

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

// This message handler will be invoked once for each incoming message. It
// prints the message and then sends a copy of the message back to the server.
void on_message(client* c, websocketpp::connection_hdl hdl, message_ptr msg) {
	/*std::cout << "on_message called with hdl: " << hdl.lock().get()
		<< " and message: " << msg->get_payload()
		<< std::endl;*/

	std::string payload = msg->get_payload();
	cout << "msg=[" << payload << "]" << endl;

	Document d;
	d.Parse(payload.c_str());

	string optype = d["optype"].GetString();
	std::cout << optype << std::endl;

	websocketpp::lib::error_code ec;

	int count = d["count"].GetInt();
	count -= 1;

	stringstream ss;
	ss << "{" << endl;
	ss << "\"optype\" : \"" << "client_msg" << "\"," << endl;
	ss << "\"wsid\" : \""	<< "c++wsid" << "\"," << endl;
	ss << "\"wstype\" : \"" << "c++ws" << "\"," << endl;
	ss << "\"count\" : \""	<< count << "\"," << endl;
	ss << "\"timestamp\" : \"" << get_time_stamp() << "\"" << endl;
	ss << "}" << endl;
	string output_buf = ss.str();

	c->send(hdl, output_buf, msg->get_opcode(), ec);
	if (ec) {
		std::cout << "Echo failed because: " << ec.message() << std::endl;
	}
}

int main(int argc, char* argv[]) {
	// Create a client endpoint
	client c;

	std::string uri = "ws://localhost:8000";

	if (argc == 2) {
		uri = argv[1];
	}

	try {
		// Set logging to be pretty verbose (everything except message payloads)
		c.set_access_channels(websocketpp::log::alevel::all);
		c.clear_access_channels(websocketpp::log::alevel::frame_payload);

		// Initialize ASIO
		c.init_asio();

		// Register our message handler
		c.set_message_handler(bind(&on_message, &c, ::_1, ::_2));

		websocketpp::lib::error_code ec;
		client::connection_ptr con = c.get_connection(uri, ec);
		if (ec) {
			std::cout << "could not create connection because: " << ec.message() << std::endl;
			return 0;
		}

		// Note that connect here only requests a connection. No network messages are
		// exchanged until the event loop starts running in the next line.
		c.connect(con);

		// Start the ASIO io_service run loop
		// this will cause a single connection to be made to the server. c.run()
		// will exit when this connection is closed.
		c.run();
	}
	catch (websocketpp::exception const & e) {
		std::cout << e.what() << std::endl;
	}
}
