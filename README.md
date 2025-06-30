# ImageBridge
Universal Image Format Converter

## 使用说明
```
全能图像转换工具 v1.0

positional arguments:
  {to_webp,from_webp}   转换方向:
                          to_webp   - 将普通图片转为 WebP
                          from_webp - 将 WebP 转为其他格式

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        输入文件夹路径 (默认: ./input)
  -o OUTPUT, --output OUTPUT
                        输出文件夹路径 (默认: ./output)
  -f {jpg,jpeg,png}, --format {jpg,jpeg,png}
                        当使用 from_webp 操作时的输出格式 (默认: png)
  -q 1-100, --quality 1-100
                        输出图像质量 (默认: 85)
  -v, --version         show program's version number and exit
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.