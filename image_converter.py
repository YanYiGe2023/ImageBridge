import os
import sys
import argparse
from PIL import Image
from pathlib import Path

version = "1.0"


def convert_image(input_path, output_path, format, quality=85):
    """
    执行图片格式转换

    参数:
    input_path: 输入文件路径
    output_path: 输出文件路径
    format: 目标格式 ('webp', 'jpg', 'png')
    quality: 输出质量 (1-100)
    """
    try:
        with Image.open(input_path) as img:
            # 创建输出目录
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # 处理透明背景转换
            if format in ('jpg', 'jpeg') and img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')

            # 保存为指定格式
            if format == 'webp':
                img.save(output_path, 'WEBP', quality=quality, method=6)
            elif format == 'jpg':
                img.save(output_path, 'JPEG', quality=quality, optimize=True)
            else:  # PNG
                img.save(output_path, 'PNG', optimize=True)

            return True, ""

    except Exception as e:
        return False, str(e)


def batch_convert(input_folder, output_folder, operation, format, quality=85):
    """
    批量转换文件夹中的图片

    参数:
    input_folder: 输入文件夹
    output_folder: 输出文件夹
    operation: 转换类型 ('to_webp', 'from_webp')
    format: 目标格式 (当 operation 为 'from_webp' 时使用)
    quality: 输出质量
    """
    # 支持的输入格式
    if operation == 'to_webp':
        input_extensions = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')
        output_extension = '.webp'
    else:  # from_webp
        input_extensions = ('.webp', '.WEBP')
        output_extension = f'.{format.lower()}'

    # 统计变量
    converted = 0
    skipped = 0
    errors = []

    print(f"\n{'=' * 50}")
    print(f"开始转换: {input_folder} → {output_folder}")
    print(f"操作类型: {'转 WebP' if operation == 'to_webp' else '转 ' + format.upper()}")
    print(f"质量设置: {quality}")
    print(f"{'=' * 50}\n")

    # 遍历输入文件夹
    for file in Path(input_folder).iterdir():
        if not file.is_file():
            continue

        # 检查文件扩展名
        if file.suffix.lower() not in input_extensions:
            skipped += 1
            continue

        # 构建输出路径
        output_file = Path(output_folder) / (file.stem + output_extension)

        # 执行转换
        success, error_msg = convert_image(
            str(file),
            str(output_file),
            'webp' if operation == 'to_webp' else format.lower(),
            quality
        )

        if success:
            print(f"✓ {file.name} → {output_file.name}")
            converted += 1
        else:
            print(f"× {file.name} 失败: {error_msg}")
            errors.append(f"{file.name}: {error_msg}")

    # 打印结果
    print(f"\n{'=' * 50}")
    print(f"转换完成!")
    print(f"- 成功转换: {converted} 个文件")
    print(f"- 跳过文件: {skipped} 个")

    if errors:
        print(f"\n错误信息 ({len(errors)} 个错误):")
        for error in errors:
            print(f"  {error}")

    print(f"\n输出位置: {os.path.abspath(output_folder)}")
    return converted, len(errors)


def main():
    # 创建命令行解析器
    parser = argparse.ArgumentParser(
        description="全能图像转换工具 v" + version,
        formatter_class=argparse.RawTextHelpFormatter
    )

    # 添加命令参数
    parser.add_argument(
        'operation',
        choices=['to_webp', 'from_webp'],
        help="转换方向:\n"
             "  to_webp   - 将普通图片转为 WebP\n"
             "  from_webp - 将 WebP 转为其他格式"
    )

    parser.add_argument(
        '-i', '--input',
        default='./input',
        help="输入文件夹路径 (默认: ./input)"
    )

    parser.add_argument(
        '-o', '--output',
        default='./output',
        help="输出文件夹路径 (默认: ./output)"
    )

    parser.add_argument(
        '-f', '--format',
        choices=['jpg', 'jpeg', 'png'],
        default='png',
        help="当使用 from_webp 操作时的输出格式 (默认: png)"
    )

    parser.add_argument(
        '-q', '--quality',
        type=int,
        choices=range(1, 101),
        default=85,
        metavar="1-100",
        help="输出图像质量 (默认: 85)"
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='全能图像转换工具 v' + version
    )

    # 解析参数
    args = parser.parse_args()

    # 执行转换
    try:
        batch_convert(
            args.input,
            args.output,
            args.operation,
            args.format,
            args.quality
        )
    except KeyboardInterrupt:
        print("\n操作已取消")
        sys.exit(0)
    except Exception as e:
        print(f"发生错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()