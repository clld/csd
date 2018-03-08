"""script to create the default set of map marker icons distributed with clld."""
import os
import sys

import pyx
from pyx import bbox, unit, style, path, color, canvas, deco
# set the scale to 1/20th of an inch
unit.set(uscale=0.05, wscale=0.02, defaultunit="inch")

linewidth = style.linewidth(1.2)


ICONS = [
'tD2B48C',
'tFFE4C4',
't87CEEB',
'cADD8E6',
't2E8B57',
'c3CB371',
'tBA55D3',
'tDA70D6',
'cEE82EE',
'tFF4500',
'cFF7F50',
'tFFA500',
'cFFD700',
't008080',
't008B8B',
'c00FFFF',
't008B8B',
'c00FFFF',
't778899',
'cB0C4DE',
]


def polygon(*points):  # pragma: no cover
    args = []
    for i, point in enumerate(points):
        args.append(path.moveto(*point) if i == 0 else path.lineto(*point))
    args.append(path.closepath())
    return path.path(*args)


shapes = {
    "c": path.circle(20, 20, 13.6),  # circle
    "s": path.rect(8, 8, 24, 24),  # square
    "t": polygon((2, 4), (38, 4), (20, 35)),  # triangle (pyramid)
    "f": polygon((2, 36), (38, 36), (20, 5)),  # inverted pyramid
    "d": polygon((20, 2), (38, 20), (20, 38), (2, 20)),  # diamond
}


def pyxColor(string):
    """Return a pyxColor instance.

    :param string: RGB color name like 'ffffff'
    :return: pyx color.

    >>> assert pyxColor('ffffff')
    """
    assert len(string) == 6
    colorTuple = tuple(
        int('0x' + c, 16) for c in [string[i:i + 2] for i in range(0, 6, 2)])
    return color.rgb(*[i / 255.0 for i in colorTuple])


if __name__ == '__main__':  # pragma: no cover
    out = sys.argv[1]
    if not pyx:
        sys.exit(1)
    for icon in ICONS:
        icon = icon.lower()
        c = canvas.canvas()
        c.draw(
            shapes[icon[0]],
            [deco.stroked([linewidth]), deco.filled([pyxColor(icon[1:])])])
        stream = c.pipeGS("pngalpha", resolution=20, bbox=bbox.bbox(0, 0, 40, 40))
        with open(os.path.join(out, icon + '.png'), 'wb') as fp:
            fp.write(stream.read())
    sys.exit(0)

