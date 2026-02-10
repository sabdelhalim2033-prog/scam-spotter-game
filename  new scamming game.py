import random
import time
import os
import shutil
import pyfiglet
from colorama import Fore, Style, init

init(autoreset=True)

# ================= GAME STATE =================
score = 0
lives = 3
boss_active = False
boss_hp = 0

# ================= MESSAGES =================
scam_texts = [
    "FREE PHONE", "VERIFY ACCOUNT", "BANK ALERT",
    "PASSWORD EXPIRED", "SUSPICIOUS LOGIN",
    "CLICK TO WIN", "ACCOUNT LOCKED",
    "GIFT CARD NEEDED", "URGENT ACTION",
    "RESET PASSWORD", "YOU WON CASH"
]

safe_texts = [
    "SCHOOL EMAIL", "GAME UPDATE", "FRIEND MESSAGE",
    "HOMEWORK DUE", "EVENT REMINDER",
    "PHOTO SHARED", "CLASS ANNOUNCE",
    "WEATHER UPDATE", "SYSTEM UPDATE"
]

boss_scam_texts = [
    "IT SUPPORT REQUIRED",
    "ACCOUNT SECURITY TEAM",
    "UNUSUAL PAYMENT",
    "SERVICE INTERRUPTION",
    "CONFIRM BILLING"
]

# ================= HELPERS =================
def clear():
    os.system("clear")

def term_width():
    return shutil.get_terminal_size().columns

def big_text(text, width):
    fig = pyfiglet.Figlet(font="small")
    return [line.center(width) for line in fig.renderText(text).splitlines()]

def draw_screen(message, color):
    width = term_width()
    box_w = min(70, width - 4)
    box_h = 15

    top = "+" + "-" * box_w + "+"
    empty = "|" + " " * box_w + "|"

    lines = big_text(message, box_w)
    pad = (box_h - len(lines)) // 2

    print(top.center(width))
    for _ in range(pad):
        print(empty.center(width))

    for l in lines:
        print(("|" + color + l[:box_w] + Style.RESET_ALL + "|").center(width))

    for _ in range(box_h - pad - len(lines)):
        print(empty.center(width))
    print(top.center(width))


def draw_hearts(lives):
    hearts = "♥ " * lives
    print(Fore.RED + hearts.center(term_width()) + Style.RESET_ALL)

def draw_skulls(hp):
    skulls = "☠️ " * hp
    print(Fore.WHITE + skulls.center(term_width()) + Style.RESET_ALL)

# ================= GAME START =================
clear()
draw_screen("SCAM SPOTTER", Fore.CYAN)
time.sleep(2)

# ================= MAIN LOOP =================
while lives > 0:
    clear()

    # Boss trigger
    if score >= 5 and not boss_active:
        boss_active = True
        boss_hp = 3
        draw_screen("BOSS SCAMMER", Fore.RED)
        time.sleep(2)

    # Status
    draw_hearts(lives)
    if boss_active:
        draw_skulls(boss_hp)
    draw_screen(f"SCORE {score}", Fore.YELLOW)

    # Message logic
    if boss_active:
        is_scam = True
        message = random.choice(boss_scam_texts)
        color = Fore.RED
    else:
        is_scam = random.choice([True, False])
        message = random.choice(scam_texts if is_scam else safe_texts)
        color = Fore.RED if is_scam else Fore.BLUE

    draw_screen(message, color)

    print("\nIs this a scam? (yes / no)\n".center(term_width()))
    answer = input("> ").strip().lower()

    correct = (answer == "yes" and is_scam) or (answer == "no" and not is_scam)

    if correct:
        if boss_active:
            boss_hp -= 1
            draw_screen("BOSS HIT", Fore.GREEN)
            time.sleep(1.2)
            if boss_hp <= 0:
                boss_active = False
                score += 3
                draw_screen("BOSS DEFEATED", Fore.GREEN)
                time.sleep(2)
        else:
            score += 1
            draw_screen("CORRECT", Fore.GREEN)
            time.sleep(1.2)
    else:
        lives -= 1
        draw_screen("WRONG", Fore.RED)
        time.sleep(1.2)

# ================= GAME OVER =================
clear()
draw_screen("GAME OVER", Fore.RED)
draw_screen(f"FINAL SCORE {score}", Fore.YELLOW)
