// 2021-8-17 by YH PARK
/***************************************************************************
	Simple DB 예제
****************************************************************************/
#include <iostream>
#include <mysql.h>

int main()
{
	MYSQL conn;
	mysql_init(&conn);
	MYSQL* connection = mysql_real_connect(&conn, "127.0.0.1", "root", "1234", "testdb", 3306, NULL, 0);
	
	if (!connection)
		std::cout << "mysql_real_connect() error" << std::endl;
	else
		std::cout << "mysql connection success" << std::endl;


	if (mysql_query(connection, "SELECT * FROM testtable where test_id = 1") != 0)
	{
		std::cout << "mysql_query() error" << std::endl;
	}

	MYSQL_RES* sql_results = mysql_store_result(connection);

	MYSQL_ROW sql_row;

	for (int rdx = 0; rdx < sql_results->row_count; rdx++)
	{
		sql_row = mysql_fetch_row(sql_results);
		for (int cdx = 0; cdx < sql_results->field_count; cdx++) 
		{
			std::cout << sql_row[cdx];
			if (cdx < sql_results->field_count - 1)std::cout << ", ";
		}
		std::cout << std::endl;
	}

	mysql_close(connection);
	return 0;
}