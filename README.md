# Hiding information in images using the LSB technique

## Requirements
- [Python 3](https://www.python.org/)
- [Pillow 7.1.1](https://pypi.org/project/Pillow/)
- [NumPy 1.18.2](https://pypi.org/project/numpy/)
- [OpenCV 4.2.0.34](https://pypi.org/project/opencv-python/)

## Usage 

    usage: main.py [-h] [-e] [-m MESSAGE] [-b CODING] -s FILE [-r FILE] [-f FILE]

```
optional arguments:
  -h, --help  show this help message and exit
  -e          extracting the secret message, embedding by default
  -m MESSAGE  the secret message to embed
  -b CODING   the number of bits for a symbol, 8 bits by default
  -s FILE     the name of the source file
  -r FILE     the name of the result file
  -f FILE     the text file containing the secret message
```

## Examples
- Embedding
```
➜  python main.py -s resources/src.bmp -r resources/res.bmp -f resources/chars10000.txt
```
- Extracting
```
➜  python main.py -e -s resources/res.bmp
```

## License & copyright
Licensed under the [MIT-License](LICENSE.md).