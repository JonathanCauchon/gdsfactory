""" this example shows how to add_grating couplers without fiber array
"""

import pp

from pp.routing.connect_component import get_route2individual_gratings
from pp.ports.add_port_markers import get_optical_text


def add_grating_couplers(
    component,
    get_route_factory=get_route2individual_gratings,
    optical_io_spacing=50,
    min_input2output_spacing=200,
    optical_routing_type=2,
    bend_factory=pp.c.bend_circular,
    grating_coupler=pp.c.grating_coupler_te,
    straight_factory=pp.c.waveguide,
    with_align_ports=True,
    layer_label=pp.LAYER.LABEL,
):
    """ returns component with grating ports and labels on each port
    can add align_ports reference structure
    """
    component = pp.call_if_func(component)
    grating_coupler = pp.call_if_func(grating_coupler)

    c = pp.routing.add_io_optical(
        component,
        optical_io_spacing=optical_io_spacing,
        bend_factory=bend_factory,
        straight_factory=straight_factory,
        grating_coupler=grating_coupler,
        get_route_factory=get_route_factory,
        optical_routing_type=optical_routing_type,
        min_input2output_spacing=min_input2output_spacing,
    )

    if with_align_ports:
        gc_port_name = list(grating_coupler.ports.keys())[0]
        gci = c << grating_coupler
        gco = c << grating_coupler
        length = c.ysize - 2 * grating_coupler.xsize
        wg = c << straight_factory(length=length)
        wg.rotate(90)
        wg.xmin = c.xmax + optical_io_spacing - grating_coupler.ysize / 2
        wg.ymin = c.ymin + grating_coupler.xsize

        gci.connect(gc_port_name, wg.ports["W0"])
        gco.connect(gc_port_name, wg.ports["E0"])

        port = wg.ports["E0"]
        label = get_optical_text(
            port, grating_coupler, 0, component_name=f"loopback_{component.name}"
        )
        c.label(label, position=port.midpoint, layer=layer_label)

        port = wg.ports["W0"]
        label = get_optical_text(
            port, grating_coupler, 1, component_name=f"loopback_{component.name}"
        )
        c.label(label, position=port.midpoint, layer=layer_label)

    return c


if __name__ == "__main__":
    c = pp.c.ring_single_bus(gap=0.3, bend_radius=5, wg_width=0.45)
    cc = add_grating_couplers(c)
    pp.show(cc)
