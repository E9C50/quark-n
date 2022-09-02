import calendar
import os
from datetime import datetime

import psutil
import pygame

NET_STATS = []
NET_INTERFACE = 'wlan0'


def set_env():
    display_no = os.getenv("DISPLAY")
    if display_no:
        print("I'm running under X display = " + str(display_no))

    if not os.getenv('SDL_FBDEV'):
        os.putenv('SDL_FBDEV', '/dev/fb1')


def speed_rx():
    try:
        if_stat = open('/proc/net/dev').readlines()
        for interface in if_stat:
            if NET_INTERFACE in interface:
                stat = float(interface.split()[1])
                NET_STATS[0:] = [stat]
    except:
        pass


def speed_tx():
    try:
        if_stat = open('/proc/net/dev').readlines()
        for interface in if_stat:
            if NET_INTERFACE in interface:
                stat = float(interface.split()[9])
                NET_STATS[1:] = [stat]
    except:
        pass


def refresh_speed():
    last_stats = list(NET_STATS)
    speed_rx()
    speed_tx()
    return last_stats


def get_date_info():
    try:
        return datetime.now().strftime('%Y-%m-%d') + ' ' + calendar.day_name[datetime.now().weekday()][:3]
    except:
        return '2999-13-32 Mon'


def get_ip_address():
    try:
        return psutil.net_if_addrs()[NET_INTERFACE][0].address
    except:
        return '10.1.1.44'


def get_cpu_usage():
    try:
        return 'CPU: ' + str(round(psutil.cpu_percent(None), 2)) + '%'
    except:
        return 'CPU: 999.99%'


def get_ram_usage():
    try:
        return 'RAM: ' + str(round(psutil.virtual_memory().percent, 2)) + '%'
    except:
        return 'RAM: 999.99%'


def get_net_speed(last_stat):
    try:
        rx = 'R ' + str(round((float(NET_STATS[0]) - last_stat[0]) / 1024, 2))
        tx = 'T ' + str(round((float(NET_STATS[1]) - last_stat[1]) / 1024, 2))
        return rx, tx
    except:
        return 'R 99.99', 'T 99.99'


if __name__ == '__main__':
    set_env()
    screen_clock = ''
    screen_cpu_ram = ''

    refresh_speed()

    pygame.init()
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((240, 135))

    F_DIGIB_74 = pygame.font.Font('font/DS-DIGIB.TTF', 74)
    F_msyhbd_18 = pygame.font.Font('font/msyhbd.ttc', 18)

    sync_time = datetime.now().timestamp()
    get_net_speed(NET_STATS)

    while True:
        if datetime.now().timestamp() - sync_time < 1:
            continue

        sync_time = datetime.now().timestamp()
        stat_o = refresh_speed()

        screen.fill((0, 0, 0))

        cpu_text = F_msyhbd_18.render(get_cpu_usage(), True, (0, 255, 0))
        screen.blit(cpu_text, (0, 0))

        ram_text = F_msyhbd_18.render(get_ram_usage(), True, (0, 255, 0))
        screen.blit(ram_text, (120, 0))

        clock_text = F_DIGIB_74.render(datetime.now().strftime('%H:%M:%S'), True, (0, 255, 0))
        screen.blit(clock_text, (0, 18))

        weekday_info = calendar.day_name[datetime.now().weekday()][:3]
        date_text = F_msyhbd_18.render(datetime.now().strftime('%Y-%m-%d') + ' ' + weekday_info, True, (0, 255, 0))
        screen.blit(date_text, (0, 88))

        ip_text = F_msyhbd_18.render(get_ip_address(), True, (0, 255, 0))
        screen.blit(ip_text, (0, 112))

        rx_text = F_msyhbd_18.render(get_net_speed(stat_o)[0], True, (0, 255, 0))
        screen.blit(rx_text, (170, 88))

        tx_text = F_msyhbd_18.render(get_net_speed(stat_o)[1], True, (0, 255, 0))
        screen.blit(tx_text, (170, 112))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
