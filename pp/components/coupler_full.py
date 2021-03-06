import numpy as np

import picwriter.components as pc

from pp.components.waveguide_template import wg_strip
from pp.picwriter2component import picwriter2component
import pp


@pp.autoname
def coupler_full(
    length=40.0,
    gap=0.5,
    dw=0.1,
    angle=np.pi / 6,
    parity=1,
    waveguide_template=wg_strip,
    port=(0, 0),
    direction="EAST",
    **kwargs
):
    """ Adiabatic Full Coupler.  Design based on asymmetric adiabatic full coupler designs, such as the one reported in 'Integrated Optic Adiabatic Devices on Silicon' by Y. Shani, et al (IEEE Journal of Quantum Electronics, Vol. 27, No. 3 March 1991).

    In this design, Region I is the first half of the input S-bend waveguide where the input waveguides widths taper by +dw and -dw, Region II is the second half of the S-bend waveguide with constant, unbalanced widths, Region III is the coupling region where the waveguides from unbalanced widths to balanced widths to reverse polarity unbalanced widths, Region IV is the fixed width waveguide that curves away from the coupling region, and Region V is the final curve where the waveguides taper back to the regular width specified in the waveguide template.

    Args:
       wgt (WaveguideTemplate):  WaveguideTemplate object
       length (float): Length of the coupling region.
       gap (float): Distance between the two waveguides.
       dw (float): Change in waveguide width.  Top arm tapers to the waveguide width - dw, bottom taper to width - dw.
       angle (float): Angle in radians (between 0 and pi/2) at which the waveguide bends towards the coupling region.  Default=pi/6.
       parity (integer -1 or 1): If -1, mirror-flips the structure so that the input port is actually the *bottom* port.  Default = 1.
       port (tuple): Cartesian coordinate of the input port (AT TOP if parity=1, AT BOTTOM if parity=-1).  Defaults to (0,0).
       direction (string): Direction that the component will point *towards*, can be of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, OR an angle (float, in radians).  Defaults to 'EAST'.

    """

    c = pc.FullCoupler(
        pp.call_if_func(wg_strip, **kwargs),
        length=length,
        gap=gap,
        dw=dw,
        angle=angle,
        parity=parity,
        port=port,
        direction=direction,
    )

    return picwriter2component(c)


if __name__ == "__main__":
    import pp

    c = coupler_full()
    pp.show(c)
