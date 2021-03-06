import pp

__version__ = "0.0.1"


@pp.autoname
def mmi2x2(
    wg_width=0.5,
    width_taper=0.95,
    length_taper=10,
    length_mmi=15.45,
    width_mmi=2.1,
    gap_mmi=0.2,
    layer=pp.LAYER.WG,
):
    """ mmi 1x2

    Args:
        wg_width: input waveguides width
        width_taper: interface between input waveguides and mmi region
        length_taper: into the mmi region
        length_mmi: in x direction
        width_mmi: in y direction
        gap_mmi: (width_taper + gap between tapered wg)/2
        layer: gds layer

    .. plot::
      :include-source:

      import pp
      c = pp.c.mmi2x2(length_mmi=15.45, width_mmi=2.1)
      pp.plotgds(c)

    """
    component = pp.Component()
    w_mmi = width_mmi
    w_taper = width_taper

    taper = pp.c.taper(length=length_taper, width1=wg_width, width2=w_taper)

    a = gap_mmi / 2 + width_taper / 2
    _mmi = pp.c.rectangle(
        size=(length_mmi, w_mmi),
        layer=layer,
        ports_parameters={
            "E": [(w_mmi / 2 - a, w_taper), (w_mmi / 2 + a, w_taper)],
            "W": [(w_mmi / 2 - a, w_taper), (w_mmi / 2 + a, w_taper)],
        },
    )

    mmi_section = component.add_ref(_mmi)

    # For each port on the MMI rectangle
    for port_name, port in _mmi.ports.items():

        # Create a taper
        _taper_ref = component.add_ref(taper)

        # Connect the taper to the mmi section
        _taper_ref.connect(port="2", destination=mmi_section.ports[port_name])

        # Add the taper port
        component.add_port(name=port_name, port=_taper_ref.ports["1"])

    return component


@pp.autoname
def mmi2x2_biased(
    wg_width=0.5,
    width_taper=0.95,
    length_taper=10,
    length_mmi=15.45,
    width_mmi=2.1,
    gap_mmi=0.2,
    layer=pp.LAYER.WG,
):
    return mmi2x2(
        wg_width=pp.bias.width(wg_width),
        width_taper=pp.bias.width(width_taper),
        length_taper=length_taper,
        length_mmi=length_mmi,
        width_mmi=pp.bias.width(width_mmi),
        gap_mmi=pp.bias.gap(gap_mmi),
        layer=layer,
    )


def test_mmi2x2():
    c = mmi2x2()
    pp.write_gds(c)


if __name__ == "__main__":
    # c = mmi2x2()
    c = mmi2x2_biased()
    # pp.write_to_libary("mmi1x2", width_mmi=10, overwrite=True)
    # print(c.get_optical_ports())
    pp.show(c)
