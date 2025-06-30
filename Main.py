#!/usr/bin/env python3

import os
import sys
import image_converter
from pathlib import Path

version = "1.0"

# 原始转换脚本名称
CONVERTER_SCRIPT = "image_converter.py"


# 颜色定义 (ANSI 转义序列)
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def clear_screen():
    """清屏函数，跨平台支持"""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_banner():
    """显示程序横幅"""
    print(f"{Colors.BLUE}{'=' * 60}")
    print(f"{Colors.BOLD}ImageBridge v{version}{Colors.ENDC}")
    print(f"{Colors.BOLD}https://github.com/YanYiGe2023/ImageBridge{Colors.ENDC}")
    print(f"{Colors.BLUE}{'=' * 60}")

def run_converter(command):
    """运行转换器脚本
    try:
        clear_screen()
        print(f"{Colors.YELLOW}执行命令: python {CONVERTER_SCRIPT} {' '.join(command)}{Colors.ENDC}\n")
        result = subprocess.run(
            [sys.executable, CONVERTER_SCRIPT] + command,
            check=True
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}转换出错: {e}{Colors.ENDC}")
        return False
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}操作已取消{Colors.ENDC}")
        return False
    """


def get_input_folder():
    """获取用户输入文件夹路径"""
    default_input = "./input"
    print(f"\n{Colors.CYAN}请输入输入文件夹路径 (默认为 '{default_input}'):")
    path = input("> ").strip()
    return path if path else default_input


def get_output_folder():
    """获取用户输出文件夹路径"""
    default_output = "./output"
    print(f"\n{Colors.CYAN}请输入输出文件夹路径 (默认为 '{default_output}'):")
    path = input("> ").strip()
    return path if path else default_output


def get_quality():
    """获取质量设置"""
    while True:
        print(f"\n{Colors.CYAN}请输入图像质量 (1-100, 默认为 85):")
        q = input("> ").strip()
        if not q:
            return 85
        try:
            quality = int(q)
            if 1 <= quality <= 100:
                return quality
            print(f"{Colors.RED}错误: 质量值必须在 1-100 之间{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.RED}错误: 请输入有效数字{Colors.ENDC}")


def to_webp_menu():
    """转换为WebP菜单"""
    clear_screen()
    print(f"{Colors.GREEN}{'=' * 30}")
    print("转换为WebP格式")
    print(f"{'=' * 30}{Colors.ENDC}")

    input_folder = get_input_folder()
    output_folder = get_output_folder()
    quality = get_quality()

    if image_converter.batch_convert(input_folder, output_folder, "to_webp", format, quality):
        print(f"\n{Colors.GREEN}转换完成! 输出目录: {output_folder}{Colors.ENDC}")
    input("\n按回车键返回主菜单...")


def from_webp_menu():
    """从WebP转换菜单"""
    clear_screen()
    print(f"{Colors.GREEN}{'=' * 30}")
    print("从WebP转换格式")
    print(f"{'=' * 30}{Colors.ENDC}")

    input_folder = get_input_folder()
    output_folder = get_output_folder()

    # 格式选择
    print(f"\n{Colors.CYAN}请选择输出格式:")
    print("1) PNG (默认)")
    print("2) JPG/JPEG")
    choice = input("> ").strip()

    format = "png"
    if choice == "2":
        format = "jpg"

    quality = get_quality()
    if image_converter.batch_convert(input_folder, output_folder, "from_webp", format, quality):
        print(f"\n{Colors.GREEN}转换完成! 输出目录: {output_folder}{Colors.ENDC}")
    input("\n按回车键返回主菜单...")


def main_menu():
    """主菜单"""
    while True:
        clear_screen()
        display_banner()

        print(f"{Colors.YELLOW}请选择操作:{Colors.ENDC}")
        print(f"{Colors.CYAN}1) 将图像转换为WebP格式")
        print("2) 将WebP转换为其他格式")
        print("3) 退出程序")
        print(f"{Colors.YELLOW}{'-' * 30}{Colors.ENDC}")

        choice = input("> ").strip()

        if choice == "1":
            to_webp_menu()
        elif choice == "2":
            from_webp_menu()
        elif choice == "3":
            print(f"\n{Colors.BLUE}感谢使用ImageBridge{Colors.ENDC}")
            sys.exit(0)
        else:
            print(f"{Colors.RED}无效选择，请重新输入{Colors.ENDC}")
            input("按回车键继续...")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}程序已终止{Colors.ENDC}")
        sys.exit(0)