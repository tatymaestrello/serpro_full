import json
def readOption(dashboards, option):
    dict = option.split(":")
    if len(dict) >= 1:
        value = dict[0]
        level1 = {}
        try:
            level1 = dashboards[value]
        except Exception:
            dashboards[value] = {}
            level1 = dashboards[value]

        level2 = {}
        if len(dict) >= 2:
            value = value = dict[1]
            try:
                level2 = level1[value]
            except Exception:
                leaf = value.split("|")
                if len(leaf) == 1:
                    level2 = level1[value] = {}
                    level2 = level1[value]
                else:
                    level1[leaf[0]] = leaf[1]

            level3 = {}
            if len(dict) >= 3:
                value = value = dict[2]
                try:
                    level3 = level2[value]
                except Exception:
                    leaf = value.split("|")
                    if len(dict) > 1:
                        level2[leaf[0]] = leaf[1]
    return json.loads(json.dumps(dashboards))


def readOptions(options):
    dashs = {}
    for x in options:
        readOption(dashs, x)
    return dashs


def test():
    # options = [
    #     "ARLD00000",
    #     "ARLD00000:ARLD00200|InformacoesCircuitosRoteadoresMODELO",
    #     "ARLD00000:ARLD00300:ARLD00300|InformacoesCircuitosRoteadoresMODELO",
    #     "ARLD00000:ARLD00300:ARLD00301|IndicadoresDesempenhoWANNacionalMODELO",
    # ]
    options = [
        "ARLD00000",
        "ARLD00000:ARLD00300",
        "ARLD00000:ARLD00300:ARLD00300|InformacoesCircuitosRoteadoresMODELO",
        "INF00000",
        "ING00000",
        "ING00000:ING00100|Ambiente",
        "ING00000:ING00100|Ambiente:ING00101|RelatorioPDFMODELO",
        "ING00500|PlantaInstaladaMODELO",
        "ING00500|PlantaInstaladaMODELO:ING00501|RelatorioPDFMODELO",
    ]
    print(readOptions(options))


test()
