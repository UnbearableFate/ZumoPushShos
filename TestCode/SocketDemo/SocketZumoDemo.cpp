#include <kernel.h>
#include "kernel_cfg.h"
#include "app.h"
#include "mbed.h"
#include "app_config.h"
#include "GR_PEACH_WlanBP3595.h"
#include "Zumo.h"


GR_PEACH_WlanBP3595 wlan;
Serial pc(USBTX, USBRX);


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

void task_main(intptr_t exinf) {

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

	char data2[128];
	socket.receive_all(data2,128);

	ledStatus(1,0,1);

	pc.printf("ret2:%s\r\n",data2);

	int l,r;

	l = 0;
	r = 0;

	int i = 0;

	while(1){
		i++;
		if(*(data2 + i) != 'l') r = r*10 + (*(data2 + i));
		else break;
	}
	sscanf((data2 + i),"%d",&l);


	zumo.driveTank(l,r);

	ledStatus(1,1,0);

	socket.close();
	wlan.disconnect();
}
