# -*- coding: UTF-8 -*-
import requests
import json
from flask import request
import os

from os import environ

# url do grafana
#url = "http://localhost:3000/api/"
# TODO get value from os.environ("URL_GRAFANA")

# usuário do grafana
#username = "admin"
#password = "@a12345z_"
url = environ.get("GRAFANA_URL")
username = environ.get("GRAFANA_USERNAME")
password = environ.get("GRAFANA_PASSWORD")
verify_ssl = environ.get("VERIFY_SSL", "true") == "true"
# path pasta MODELO
path_modelo = "MODELO/"

"""
# Padrão JSON enviado à API (Não precisa deixar os comentários após '//' ou entre '/* */'):
#-----------------------------------------------------------------------------
{
    "cliente": "CLIENTE",
    "criar_pasta": "S", //S ou N. Se for N, os dashboards são inseridos na pasta existe ou atualizados caso já existam
    "dashboards": [
        {
            "ARLD00000": [ // Administração de Rede Longa Distância
                ["ARLD00100", "MapaVisaoGeralPortalMODELO"], // Gerência Rede
                ["ARLD00200", "TopologiaWANPortalMODELO"], //Topologia
                ["ARLD00300", /*Informações Circuitos e Roteadores*/ ["InformacoesCircuitosRoteadoresMODELO" /*Diário*/, "IndicadoresDesempenhoWANNacionalMODELO" /*Mensal*/]],
                ["ARLD00400", "OcupacaoBandaTrimestralMODELO"] //Alta Utilização Persistente
            ]
        },
        {
            "ARL00000": [ // Administração de Rede Local
                ["ARL00100", "TopologiaLANPortalMODELO"], //Topologia
                ["ARL00200", "GerenciaWIFIPortalMODELO"] //Wifi
            ]
        },
        {
            "INF00000": [ // Infovia
                ["INF00100", "DisponibilidadeInfoviaMODELO"] //Monitoração
            ]
        },
        {
            "ING00000": [ // Informações Gerenciais
                {
                    "ING00100": [ //Ambiente
                        ["ING00106", "CertificadoDigitalPlanilhaXLSMODELO"], // Certificado Digital Planilha
                        ["ING00101", "RelatorioPDFMODELO"], // Datacenter
                        ["ING00102", "RelatorioPDFMODELO"], //Infovia
                        ["ING00103", "RelatorioPDFLANMODELOJURIS"], //Lan
                        ["ING00104", "RelatorioPDFMODELO"], //Lan
                        ["ING00105", "RelatorioPDFMODELO"] //Wan
                    ]
                },
                {
                    "ING00300": [ //Documentos
                        ["ING00300", "InformativoPDFMODELO"], //Informativo
                        ["ING00301", "DocumentosPDFMODELO"], // Manuais
                        ["ING00302", "DocumentosPDFMODELO"] // Modelos Tecnológicos
                    ]
                },
                {
                    "ING00400": "PlantaInstaladaMODELO" //Planta Instalada
                },
                {
                    "ING00500": [ //Segurança
                        ["ING00501", "RelatorioPDFMODELO"], // AntiDDOS
                        ["ING00502", "RelatorioPDFMODELO"], // FIREWALL
                        ["ING00503", "RelatorioPDFMODELO"] // IPS
                    ]
                }
            ]
        },
        {
            "MDP00000": [ // Monitoração por Demanda
                ["MPD00100", "MonitoracaoDemandaMODELO"] // Painel 1
            ]
        }
    ]
}
"""


# chama a API do grafana para criar uma nova pasta
def criar_nova_pasta(cliente):
    dict_nova_pasta = {
        "description": cliente,
        "parentUid": "0",
        "title": cliente,
        "uid": cliente,
    }
    # convertendo dic em JSON
    dados_nova_pasta = json.loads(json.dumps(dict_nova_pasta))

    # chama a API do grafana para criar a pasta do cliente
    response = requests.post(
        url=url + "folders",
        json=dados_nova_pasta,
        auth=(username, password),
        verify=verify_ssl,
    )
    resp_nova_pasta = json.loads(response.content)
    # em resp_nova_pasta tem o JSON dos dados da pasta criada
    return resp_nova_pasta


# ----------------------------------------------------------------------------------------


def buscar_dados_pasta(cliente):
    # chama a API do grafana para obter os dados da pasta do cliente
    response = requests.get(
        url=url + "folders/" + cliente, auth=(username, password), verify=verify_ssl
    )
    resp_pasta_grafana = json.loads(response.content)
    # em resp_pasta_grafa tem o JSON dos dados da pastas
    return resp_pasta_grafana


# ----------------------------------------------------------------------------------------


# busca codigo em lista_codigos_menu
def buscar_codigo_lista(linha, lista_codigos_menu):
    i = 0
    while i < len(lista_codigos_menu) and linha.find(lista_codigos_menu[i]) == -1:
        i = i + 1
    if i < len(lista_codigos_menu):
        return True
    return False


# ----------------------------------------------------------------------------------------


# modifica o html do menuportal para habilitar os itens de menu referentes aos dashboards importados
def modificar_html_menuportal(html_data, lista_codigos_menu):
    html_data_novo = ""
    vet_html_data = html_data.split("\\n")
    for indice, dado in enumerate(vet_html_data):
        if not buscar_codigo_lista(dado, lista_codigos_menu):
            html_data_novo += dado
            if indice < len(vet_html_data) - 1:
                html_data_novo += "\\n"
    return html_data_novo


# ----------------------------------------------------------------------------------------


# chama a API do grafana para importar o dashboard
def importar_dashboard(
    nome_arq_json, cliente, folderId, folderUid, path, flag_menuportal, lista_itens_menu
):
    erro_html_data = ""

    # verificando se o nome do arquivo de modelo 'xxxxxxxxxMODELO' tem algo a mais. Exemplo: 'xxxxxxxxxMODELO-0123456789.json'
    lista_arquivos_modelo = os.listdir(path_modelo)
    for nome_arq in lista_arquivos_modelo:
        if os.path.isfile(path_modelo + nome_arq) and nome_arq.find(nome_arq_json) >= 0:
            nome_arq_json = nome_arq

    # verifica se o arquivo .json exite
    if os.path.isfile(path_modelo + nome_arq_json):
        # abre o arquivo do dashboard MODELO .json
        with open(path_modelo + nome_arq_json, "r", encoding="utf-8") as f:
            json_dashboard = json.load(f)
        f.close()

        # altera "MODELO" p/ "CLIENTE" e "modelo" p/ "cliente"
        str_aux = json.dumps(json_dashboard)
        str_json_dashboard = str_aux.replace("MODELO", str(cliente).upper()).replace(
            "modelo", str(cliente).lower()
        )
        json_dashboard = json.loads(str_json_dashboard)

        # alterando o 'id' do dashboarda para 0
        json_dashboard["id"] = 0

        # se for o menu: 'menuportalmodelo.json' modificar o hmtl
        if flag_menuportal == True:
            # extraindo a chave 'html_data' do JSON
            panels = json_dashboard.get("panels")
            html_data = json.dumps(panels[0].get("html_data"))
            if html_data != "null":
                json_dashboard.get("panels")[0]["html_data"] = json.loads(
                    modificar_html_menuportal(html_data, lista_itens_menu).encode(
                        "utf-8"
                    )
                )
            else:
                erro_html_data = (
                    " Erro: 'html_data' do 'meuportalmodelo' está em branco."
                )

        # monta o JSON para enviar à chamada da API do grafana para importar o dashboard
        dict_dashboard = {
            "dashboard": json_dashboard,
            "folderId": folderId,
            "folderUid": folderUid,
            "overwrite": True,
            "path": path,
        }

        # convertendo dic em JSON
        dados_dashboard = json.loads(json.dumps(dict_dashboard))

        # chamada da API do grafana para importar o dashboard
        response = requests.post(
            url=url + "dashboards/import",
            json=dados_dashboard,
            auth=(username, password),
            verify=verify_ssl,
        )
        # resposta da API do grafana
        resp_novo_dashboard = json.loads(response.content)
        # verificando se a importação do dashboard deu certo
        if not (
            json.dumps(resp_novo_dashboard.get("title")).find(cliente) >= 0
            or json.dumps(resp_novo_dashboard.get("uid")).find(cliente) >= 0
        ):
            return (
                "Erro: Importação dashboard '"
                + nome_arq_json
                + "': "
                + json.dumps(resp_novo_dashboard)
                + erro_html_data
            )
        return (
            "Ok: Dashboard '"
            + nome_arq_json
            + "' importado corretamente!"
            + erro_html_data
        )
    return "Erro: Arquivo dashboard '" + nome_arq_json + "' não encontrado."


# ----------------------------------------------------------------------------------------

from app import app


# ***** API criar cliente ***************************************************************
@app.route("/criar_cliente", methods=["POST"])
def criar_cliente():
    # pegando os dados enviados à API
    dados_req = request.get_json()
    return process_client(dados_req)


# service
def process_client(dados_req):
    lista_msg_resposta = []
    cliente = dados_req.get("cliente")
    criar_pasta = dados_req.get("criar_pasta")
    dicts_dashboards = dados_req.get("dashboards")

    if criar_pasta == "S":
        # criando a pasta no grafana
        resp_pasta_grafana = criar_nova_pasta(cliente)
    else:
        # obtendo os dados da pasta já existente no grafana
        resp_pasta_grafana = buscar_dados_pasta(cliente)

    if resp_pasta_grafana.get("title") == cliente:  # pasta criada corretamente ou já existente
        if criar_pasta == "S":
            lista_msg_resposta.append("Ok: Pasta '" + cliente + "' criada com sucesso!")
        else:
            lista_msg_resposta.append("Ok: Pasta '" + cliente + "' encontrada!")

        # === importando os dashboards ===
        # pegando dados da pasta criada para incluir no JSON dos dashboards a serem importados
        folderId = resp_pasta_grafana.get("id")
        folderUid = resp_pasta_grafana.get("uid")
        path = resp_pasta_grafana.get("url")

        lista_codigos_menu = []
        lista_nomes_dashboards = []

        print("dicts_dashboards")
        print(json.dumps(dicts_dashboards))

        # pegandos as chaves dos dics do JSON
        for level0 in dicts_dashboards.keys():
            # pegado os códigos dos itens de menu principal
            lista_codigos_menu.append(level0)
            dado0 = dicts_dashboards.get(level0)
            # percorre os dics do primeiro nível
            if type(dado0) is str:
                lista_nomes_dashboards.append(dado0)
            else: 
                for level1 in dado0.keys():
                    lista_codigos_menu.append(level1)
                    dado1 = dado0.get(level1)
                    # percorre os dics do primeiro nível
                    if type(dado1) is str:
                        lista_nomes_dashboards.append(dado1)
                    else: 
                        for level2 in dado1.keys():
                            lista_codigos_menu.append(level2)
                            dado2 = dado1.get(level2)
                            # percorre os dics do primeiro nível
                            if type(dado2) is str:
                                lista_nomes_dashboards.append(dado2)
                            else: 
                                for level3 in dado2.keys():
                                    lista_codigos_menu.append(level3)
                                    dado3 = dado2.get(level3)

        # removendo os codigos de menu duplicados
        lista_codigos_menu_final = []
        for codigo in lista_codigos_menu:
            if codigo not in lista_codigos_menu_final:
                lista_codigos_menu_final.append(codigo)

        # removendo os nomes de dashboards duplicados
        lista_nomes_dashboards_final = []
        for nome in lista_nomes_dashboards:
            if nome not in lista_nomes_dashboards_final:
                lista_nomes_dashboards_final.append(nome)

        # importando todos dashboards
        for nome_dash in lista_nomes_dashboards_final:
            lista_msg_resposta.append(
                importar_dashboard(
                    nome_dash, cliente, folderId, folderUid, path, False, []
                )
            )

        # importando o menu 'menuportalmodelo'. Sempre ele é importado
        lista_msg_resposta.append(
            importar_dashboard(
                "menuportalmodelo",
                cliente,
                folderId,
                folderUid,
                path,
                True,
                lista_codigos_menu_final,
            )
        )

        return lista_msg_resposta

    if criar_pasta == "S":
        return (
            "Erro: Criação da pasta '"
            + cliente
            + "': "
            + json.dumps(resp_pasta_grafana)
        )
    else:
        return (
            "Erro: Pasta '"
            + cliente
            + "' não encontrada: "
            + json.dumps(resp_pasta_grafana)
        )


# ***************************************************************************************
