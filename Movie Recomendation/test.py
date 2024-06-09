import time

def loading_percentage(total_time):
    for i in range(101):
        print(f'\rLoading... {i}%', end='')
        time.sleep(total_time / 100)
    print()  # For new line after completion

loading_percentage(5)


