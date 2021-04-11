# telegramBotDriver
Telegram group driving robo car

## Project description
Telegram groups drives 2 cars via group chat. Cars are connected via Bluetooth to machine that is connected to internet. 
Machine runs pyhton telegram bot programe that controls communication between robot (bluetooth) and Telegram chat (internet), it is an intermediate.

For robo car [ELLEGO UNO R3 Project Smart Robot Car Kit V 3.0 Plus]https://www.elegoo.com/products/elegoo-smart-robot-car-kit-v-3-0-plus is used, and for machine Raspberry Pi 4 is deployed. 

## Setup 

### 1. Clone and setup python env
```
git clone https://github.com/marcelicmateo/telegramBotDriver.git;
cd telegramBotDriver; cd telegramBot; python3 -m venv telegramBot; 
telegramBot/bin/pip3 install -r requirements.txt; cd ..;
```

### 2. Upload firmaware to arduino uno
Run platformio from vscode or something

### 3. Create telegram chat and get tokens for python bot
Follow instruction [BotFather]https://core.telegram.org/bots#6-botfather for obtaining chat tokens. 
I place my token in seperate *secrets.py* file and include in main program (*robo.py*).
Run **robo.py**
```
telegramBot/bin/python robo.py
```
## Usefull links 
[Telegram bot documentation]https://core.telegram.org/bots




