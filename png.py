
# Copyright (C) 2011 by Stefano Palazzo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import zlib
import struct


def make(image: '[[[r, g, b, a, ], ], ]') -> bytes:
    '''
    Create PNG image from RGBA data

    Expects a list of lines of pixels of R, G, B, and Alpha values.
    I.e: [
         [ [0, 0, 0, 0], [0, 0, 0, 0], ],
         [ [0, 0, 0, 0], [0, 0, 0, 0], ],
                                       ]

    '''
    def cr_png(buf, width, height):
        def png_pack(png_tag, data):
            chunk_head = png_tag + data
            return (struct.pack("!I", len(data)) + chunk_head +
                struct.pack("!I", 0xFFFFFFFF & zlib.crc32(chunk_head)))
        raw_data = (b"".join(b'\x00' + buf[span:span + (width * 4)]
            for span in range((height - 1) * (width * 4), -1, - (width * 4))))
        return b"".join([
            b'\x89PNG\r\n\x1a\n',
            png_pack(b'IHDR', struct.pack("!2I5B", width, height,
                8, 6, 0, 0, 0)),
            png_pack(b'IDAT', zlib.compress(raw_data, 9)),
            png_pack(b'IEND', b'')])
    def make_buffer(image):
        def bufgen(nested):
            for i in nested[::-1]:
                for j in i:
                    for k in j if len(j) == 4 else list(j) + [255]:
                        yield k
        height, width = len(image), len(image[0])
        return bytes(bufgen(image)), width, height
    return cr_png(*make_buffer(image))

def show(png):
    open("/tmp/test.png", "wb").write(png)
    subprocess.getoutput("xdg-open /tmp/test.png")
    subprocess.getoutput("rm /tmp/test.png")
