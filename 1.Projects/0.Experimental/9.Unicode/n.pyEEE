# -*- coding: utf-8 -*-
from colorama import Fore
from colorama import init as initcolor
from ipaddress import ip_address, ip_network
import pyperclip

def main():    
    print(f'{Fore.GREEN}Уведомление о присвоении IP Адреса{Fore.RESET}\r\n')
    clr = ''
    clrreset = ''
    
    ip = input('IP: ')

    suggestGW = ''
    if ip_address(ip) in ip_network('10.0.0.0/8'):
        suggestGW = '.'.join(ip.split('.')[:3] +['1'])        
    gw = input(f'GW [{suggestGW}]: ')
    if gw == '':
        gw = suggestGW

    mask = input(f'mask [255.255.255.0]: ')
    if mask ==  '':
        mask = '255.255.255.0'
    
    ticket = input(f'Номер заявки: ')
    address = input(f'Адрес подключения: ')
    service_number = input(f'Номер услуги: ')

    public = ', c публичным IP адресом' if ip_address(ip).is_global else ''
    
    print('\r\n\r\n\r\n\r\n\r\n\r\n')

    resultdict = {}
    for c in ['pure', 'colored']:    
        if c == 'colored':
        	clr = Fore.YELLOW
        	clrreset = Fore.RESET
        result = ( f'Здравствуйте, по Вашей заявке предоставляем параметры подключения к сети Бизнес-Связь{public}.\r\n'
                    '\r\n' +
                   f'Заявка №: {clr}{ticket}{clrreset}\r\n' * bool(ticket) +
                   f'Услуга №: {clr}{service_number}{clrreset}\r\n' * bool(service_number) +
                   f'Адрес подключения: {clr}{address}{clrreset}\r\n\r\n' * bool(address) +                   
                   f'IP адрес: {clr}{ip}{clrreset}\r\n' +
                   f'Маска подсети: {clr}{mask}{clrreset}\r\n' +
                   f'Основной шлюз: {clr}{gw}{clrreset}\r\n\r\n' +
                   f'Основной DNS сервер: where_was_ip\r\n' +
                   f'Альтернативный DNS сервер: where_was_ip\r\n\r\n\r\n' +
                   f'С Уважением, \r\n' +
                   f'Артеменко Евгений\r\n' +
                   f'специалист тех.отдела\r\n' +
                   f'ООО Бизнес-связь\r\n' +
                   f'тел. 8(862)5555-911\r\n' +
                   f'mail: support@bisv.ru\r\n'   )
        resultdict[c] = result

    pyperclip.copy(resultdict['pure'])
    print(resultdict['colored']) 

if __name__ == '__main__':
    initcolor()
    main()
