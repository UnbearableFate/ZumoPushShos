#include <kernel.h>
#include "kernel_cfg.h"
#include "app.h"
#include "mbed.h"
#include "app_config.h"
#include "GR_PEACH_WlanBP3595.h"
#include "Zumo.h"
#include <queue>
#include <vector>
#include <string>

GR_PEACH_WlanBP3595 wlan;
Serial pc(USBTX, USBRX);
std::queue< vector<int> > speedQueue;

//LED
DigitalOut led_r(LED1);
DigitalOut led_g(LED2);
DigitalOut led_b(LED3);

void ledStatus(int r,int g,int b){
	led_r = r;
	led_g = g;
	led_b = b;
}

Zumo zumo;
/*
void dataHandle(char data[])
{
	string
	if (cmdstr[cmdstr.size() - 1] != ' ')
		cmdstr += " ";
	while (cmdstr.size() != 0)
	{
		for (auto i = cmdstr.begin(); i != cmdstr.end(); ++i) {
			cout << *i;
			if (*i == ' ') {
				cmdline.push_back(string(cmdstr.begin(), i));
				cmdstr.erase(cmdstr.begin(), i + 1);
				break;
			}
		}
	}
}
*/
void dataHandle(char data2[])
{
	for (int i = 0; i !=256 ;i += 8)
		{
		int sign = 0;

		if(data2[i+0] == '+')
		    sign = 1;
		if (data2[i+0] == '-')
		    sign = -1;
		if (sign == 0)
			break;
		int l = (static_cast<int>(data2[i+1]) - 48) *100 + (static_cast<int>(data2[i+2]) - 48) *10 + (static_cast<int>(data2[i+3]) - 48) *1;
		l *= sign;

		sign = 0;
		if(data2[i+4] == '+')
		    sign = 1;
		if (data2[i+4] == '-')
		    sign = -1;
		int r = (static_cast<int>(data2[i+5]) - 48) *100 + (static_cast<int>(data2[i+6]) - 48) *10 + (static_cast<int>(data2[i+7]) - 48) *1;
		r *= sign;

		vector<int> spe;
		spe.push_back(l);
		spe.push_back(r);
		speedQueue.push(spe);
		}
}

void dataHandleSimple(char data2[])
{
	for (int i = 0; i <256 ;i += 12)
		{
		int sign = 0;

		if(data2[i+0] == '+')
		    sign = 1;
		if (data2[i+0] == '-')
		    sign = -1;
		if (sign == 0)
			break;
		int l = (static_cast<int>(data2[i+1]) - 48) *100 + (static_cast<int>(data2[i+2]) - 48) *10 + (static_cast<int>(data2[i+3]) - 48) *1;
		l *= sign;

		sign = 0;
		if(data2[i+4] == '+')
		    sign = 1;
		if (data2[i+4] == '-')
		    sign = -1;
		int r = (static_cast<int>(data2[i+5]) - 48) *100 + (static_cast<int>(data2[i+6]) - 48) *10 + (static_cast<int>(data2[i+7]) - 48) *1;
		r *= sign;

		int time = (static_cast<int>(data2[i+8]) - 48) *1000 + (static_cast<int>(data2[i+9]) - 48) *100 + (static_cast<int>(data2[i+10]) - 48) *10
				+ (static_cast<int>(data2[i+11]) - 48) *1;

		vector<int> spe;
		spe.push_back(l);
		spe.push_back(r);
		spe.push_back(time);
		speedQueue.push(spe);

		}
}

void task_main(intptr_t exinf) {
/*
	dly_tsk(3000);
	zumo.driveTank(100,100);
	dly_tsk(5000);
	zumo.driveTank(0,0);
	*/
	ledStatus(1,1,1);

	pc.baud(9600);

	int ret = wlan.init(IP_ADDRESS, SUBNET_MASK, DEFAULT_GATEWAY);
	if(ret!=0){
		pc.printf("wifi initialize error\r\n");
		return;
	}

	ledStatus(0,1,0);

	pc.printf("wlan connecting\r\n");
	pc.printf("%s %s\r\n",WLAN_SSID,WLAN_PSK);

	ret = wlan.connect(WLAN_SSID, WLAN_PSK);
	if(ret!=0){
		pc.printf("wifi connect error\r\n");
		return;
	}


	ledStatus(0,0,1);

	TCPSocketConnection socket;
	pc.printf("socket connecting\r\n");
	ret = socket.connect(SERVER_ADDRESS, SERVER_PORT);
	if(ret!=0){
		pc.printf("socket connect error\r\n");
		return;
	}
	ledStatus(0,1,1);

	char *data1 = strdup("aaaa");

	ret = socket.send_all(data1, strlen(data1));

	if(ret == -1){
		pc.printf("socket send error\r\n");
		return;
		}

	ledStatus(1,0,0);

	while(true)
	{
	char data2[256];
	socket.receive_all(data2,256);

	ledStatus(1,0,1);

	pc.printf("ret2:%s\r\n",data2);

	dataHandle(data2);

	while(!speedQueue.empty())
	{
		int left = speedQueue.front()[0];
		int right = speedQueue.front()[1];
		//int timeT = speedQueue.front()[2];
		speedQueue.pop();
		zumo.driveTank(left,right);
		//dly_tsk(timeT);
		dly_tsk(50);
		ledStatus(1,1,0);
	}
	zumo.driveTank(0,0);

	//zumo.driveTank(l,r);
	//dly_tsk(50);
	//zumo.driveTank(0,0);
	//ledStatus(1,1,0);
	}
	socket.close();
	wlan.disconnect();
}
/*
void task_gogo(intptr_t exinf)
{
	while(true)
	{
		if(!speedQueue.empty())
		{
			int l = speedQueue.front()[i+0];
			int r = speedQueue.front()[i+1];
			speedQueue.pop();
			zumo.driveTank(l,r);
			dly_tsk(50);
			zumo.driveTank(0,0);
			//ledStatus(1,1,0);
		}
	}
}
*/
