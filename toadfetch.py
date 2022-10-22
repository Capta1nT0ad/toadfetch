#!/usr/bin/env /usr/bin/python3

# Start the clock!
from time import monotonic
from datetime import timedelta
start_time = monotonic()

# Import modules
from command import run
from json import loads
from os import environ, path
from colorama import Fore, Style

# Get distro
try:
    distro_json = run(["hostnamectl", "--json=short"]).output.decode()
    distro_json_parse = loads(distro_json)
    distro = distro_json_parse["OperatingSystemPrettyName"]
except:
    distro = "Unknown"
if distro == "null":
    distro = "Unknown"

# Get CPU info
cpu_info_full = run(["lscpu"]).output.decode().splitlines()
cpu_architecture = cpu_info_full[0].removeprefix("Architecture:                    ")
cpu_number = cpu_info_full[3].removeprefix("CPU(s):                         ")
cpu_vendor = cpu_info_full[5].removeprefix("Vendor ID:                      ")
cpu_freq = str(float(run(["cat", "/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq"]).output.decode()) / 1000000)
cpu = cpu_number + "-core " + cpu_architecture + cpu_vendor + " CPU at " + cpu_freq + " GHz"

# Get image output from catimg
if "Arch Linux" in distro:
    if cpu_vendor == " Apple":
        image = run(["catimg", "/usr/share/toadfetch/images/asahilinux.png", "-H", "32", "-r", "2"]).output.decode()
    else:
        image = run(["catimg", "/usr/share/toadfetch/images/archlinux.png", "-H", "32", "-r", "2"]).output.decode()
elif "Mint" in distro:
    image = run(["catimg", "/usr/share/toadfetch/images/linuxmint.png", "-H", "32", "-r", "2"]).output.decode()
elif "Debian" in distro:
    image = run(["catimg", "/usr/share/toadfetch/images/debian.png", "-H", "32", "-r", "2"]).output.decode()
elif "Fedora" in distro:
    image = run(["catimg", "/usr/share/toadfetch/images/fedora.png", "-H", "32", "-r", "2"]).output.decode()
elif "Ubuntu" in distro:
    image = run(["catimg", "/usr/share/toadfetch/images/ubuntu.png", "-H", "32", "-r", "2"]).output.decode()
else:
    image = run(["catimg", "/usr/share/toadfetch/images/linux.png", "-H", "32", "-r", "2"]).output.decode()
if path.exists("images/custom.png"):
    image = run(["catimg", "/usr/share/toadfetch/images/custom.png", "-H", "32", "-r", "2"]).output.decode()

# Split each line of the image into a list
split_image = image.splitlines()

# Get hostname
hostname = run(["cat", "/etc/hostname"]).output.decode()

# Get username and full name
try:
    username = run(["whoami"]).output.decode()
except:
    username = "Unknown"
if username == "":
    username = "Unknown"

# Get model, search all the available locations otherwise return "Unknown". Only /sys/firmware/devicetree/base/model is tested.
try:
    model = run(["cat", "/sys/firmware/devicetree/base/model"]).output.decode()
except:
    try:
        model = run(["getprop", "ro.product.brand"]).output.decode() + run(["getprop", "ro.product.model"]).output.decode()
    except:
        try:
            model = run(["cat", "/sys/devices/virtual/dmi/id/product_name"]).output.decode()
        except:
            try:
                model = run(["cat", "/tmp/sysinfo/model"]).output.decode()
            except:
                model = "Unknown"

# Get kernel release
kernel = run(["uname", "-r"]).output.decode()

# Get uptime
uptime = run(["uptime", "-p"]).output.decode().removeprefix("up ")

# Get memory info

# Get and split meminfo
memory_pretty_split = run(["cat", "/proc/meminfo"]).output.decode().splitlines()

# Total memory
memory_total_pretty = memory_pretty_split[0]
memory_total = int(memory_total_pretty.removeprefix("MemTotal:        ").removesuffix(" kB")) / 1000

# Used memory
memory_used_pretty = memory_pretty_split[2]

memory_used_str = memory_used_pretty.removeprefix("MemAvailable:    ").removesuffix(" kB")

memory_used_int_kb = int(memory_used_str)
memory_used_int_mb = memory_used_int_kb / 1000


memory = str(memory_used_int_mb) + " MB / " + str(memory_total) + " MB"

# Get desktop Environment
de = environ.get('XDG_CURRENT_DESKTOP')

# Get window manager
wm_pretty_full = run(["wmctrl", "-m"]).output.decode().splitlines()
wm = wm_pretty_full[0].removeprefix("Name: ")

# Get GTK theme
theme_pretty = run(["gsettings", "get", "org.gnome.desktop.interface", "icon-theme"]).output.decode()
theme = theme_pretty.removeprefix("'").removesuffix("'")


# Start output
print("\n     ", split_image[0])
print("     ", split_image[1])
print("     ", split_image[2], " ", Style.BRIGHT + Fore.BLUE + username + Style.RESET_ALL + " on " + Style.BRIGHT + Fore.BLUE + hostname)
print("     ", split_image[3], Fore.LIGHTBLACK_EX + "  ⎯⎯⎯⎯" + Fore.RED + "⎯⎯⎯⎯" + Fore.GREEN + "⎯⎯⎯⎯" + Fore.YELLOW + "⎯⎯⎯⎯" + Fore.BLUE + "⎯⎯⎯⎯" + Fore.MAGENTA + "⎯⎯⎯⎯" + Fore.CYAN + "⎯⎯⎯⎯" + Fore.WHITE + "⎯⎯⎯⎯")
print("     ", split_image[4], Fore.GREEN + "\033[3m  distro:  " + Style.RESET_ALL + Style.BRIGHT + Fore.CYAN + distro + Style.RESET_ALL)
print("     ", split_image[5], Fore.GREEN + "\033[3m  model:   " + Style.RESET_ALL + Style.BRIGHT + Fore.CYAN + model + Style.RESET_ALL)
print("     ", split_image[6], Fore.GREEN + "\033[3m  cpu:    " + Style.RESET_ALL + Style.BRIGHT + Fore.CYAN + cpu + Style.RESET_ALL)
print("     ", split_image[7], Fore.GREEN + "\033[3m  memory:  " + Style.RESET_ALL + Style.BRIGHT + Fore.CYAN +  memory + Style.RESET_ALL)
print("     ", split_image[8], Fore.GREEN + "\033[3m  kernel:  " + Style.RESET_ALL + Style.BRIGHT + Fore.CYAN + kernel + Style.RESET_ALL)
if wm == de:
    print("     ", split_image[9], Fore.GREEN + "\033[3m  de:      " + Style.RESET_ALL + Style.BRIGHT + Fore.CYAN + de + Style.RESET_ALL)
else:
    print("     ", split_image[9], Fore.GREEN + "\033[3m  de:      " + Style.RESET_ALL + Style.BRIGHT + Fore.CYAN + de + " on " + wm + Style.RESET_ALL)
print("     ", split_image[10], Fore.GREEN + "\033[3m  theme:   " + Style.RESET_ALL + Style.BRIGHT + Fore.CYAN + theme + Style.RESET_ALL)
print("     ", split_image[11], Fore.GREEN + "\033[3m  uptime:  " + Style.RESET_ALL + Style.BRIGHT + Fore.CYAN + uptime + Style.RESET_ALL)
print("     ", split_image[12])
end_time = monotonic()
total_time_full = str(timedelta(seconds=end_time - start_time))
total_time_short = total_time_full.removeprefix("0:00:")
total_time_short_int = float(total_time_short)
if total_time_short_int <= 00.079999:
    total_time_desc = Fore.GREEN + "normal" + Fore.RESET
elif total_time_short_int >= 00.080000 and total_time_short_int <= 00.299999:
    total_time_desc = Fore.BLUE + "unusual" + Fore.RESET
elif total_time_short_int >= 00.300000 and total_time_short_int <= 00.999999:
    total_time_desc = Fore.YELLOW + "sluggish" + Fore.RESET
else:
    total_time_desk = Fore.RED + "too slow" + Fore.RESET

print("     ", split_image[13], Fore.YELLOW + "\033[3m  speed:   "  + Style.RESET_ALL + Style.BRIGHT + Fore.LIGHTYELLOW_EX + total_time_short + " seconds" + " (" + total_time_desc + Fore.YELLOW + ")" + Style.RESET_ALL)
print("     ", split_image[14])
print("     ", split_image[15], "\n")


