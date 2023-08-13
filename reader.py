def readOption(dashboards, option):
    dict = option.split(":")
    if len(dict) >= 1:
        value = dict[0]
        level0 = {}
        try:
            level0 = dashboards[value]
        except Exception:
            dashboards[value] = {}
            level0 = dashboards[value]

        if len(dict) >= 2:
            value = value = dict[1]
            try:
                level1 = level0[value]
            except Exception:
                leaf = value.split("|")
                if len(leaf) == 1:
                    level1 = level0[value] = {}
                    level1 = level0[value]
                else:
                    level0[leaf[0]] = leaf[1]

            if len(dict) >= 3:
                value = value = dict[2]
                try:
                    level2 = level1[value]
                except Exception:
                    leaf = value.split("|")
                    if len(dict) > 1:
                        level1[leaf[0]] = leaf[1]


def readOptions(options):
    dashs = {}
    for x in options:
        readOption(dashs, x)
    return dashs


def test():
    options = [
        "ARLD00000",
        "ARLD00000:ARLD00200|InformacoesCircuitosRoteadoresMODELO",
        "ARLD00000:ARLD00300:ARLD00300|InformacoesCircuitosRoteadoresMODELO",
        "ARLD00000:ARLD00300:ARLD00301|IndicadoresDesempenhoWANNacionalMODELO",
    ]

    print(readOptions(options))
# test()