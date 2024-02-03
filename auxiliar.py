import sqlite3, math, os.path, sys
from decimal import Decimal as dc
from decimal import getcontext

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def coord_grau_decimal(coordenada):
    """
    Converte a coordenada de graus, minutos e segundos para graus em decimal.

    Args:
        coordenada (string): Coordenada em grau, minutos e segundos.

    Returns:
        float: Coordenada em decimal.
    """
    if 'º' in coordenada: 
        coordenada = coordenada.replace('º','°')
        
    if '\"' in coordenada and '\'\'' not in coordenada: 
        coordenada = coordenada.replace('\"','\'\'')
    if ',' in coordenada:
        coordenada = coordenada.replace(',','.')
        
    getcontext().prec = 15
    
    grau = int(coordenada[:coordenada.find('°')]) if '°' in coordenada else 0
    
    minuto = int(coordenada[coordenada.find('°')+1:coordenada.find('\'')]) / 60 if '\'' in coordenada else 0
    
    segundo = int(coordenada[coordenada.find('\'')+1:coordenada.find('\'\'')]) / 3600 if '\'\'' in coordenada else 0
    
    return dc(f'{grau}') + dc(f'{minuto}') + dc(f'{segundo}')

def dist(lat_1=0, lat_2=0, lon_1=0, lon_2=0):
    """
    Calcula a distância entre os pontos.

    Args:
        lat_1 (int, optional): Latitude de projeto. Defaults to 0.
        lat_2 (int, optional): Latitude tabelada. Defaults to 0.
        lon_1 (int, optional): Longitude de projeto. Defaults to 0.
        lon_2 (int, optional): Longitude tabelada. Defaults to 0.

    Returns:
        float: Distância entre o projeto e a cidade tabelada.
    """ 
    getcontext().prec = 15
       
    dif_lat = dc(f'{lat_1}')-dc(f'{lat_2}')
    dif_lon = dc(f'{lon_1}')-dc(f'{lon_2}')
    d = math.sqrt(dc(f'{dif_lat**2}') + dc(f'{dif_lon**2}'))
    
    return d

def distancia_rad(lat):
    """
    Calcula as distâncias entre a latitude de projeto e as latitudes tabeladas.

    Args:
        lat (float): Latitude de projeto.

    Returns:
        str: Início da string das tabelas de radiação relacionadas à latitude mais próxima.
    """    
    rads = {
        '30S': dist(lat_1=lat, lat_2=30),
        '25S': dist(lat_1=lat, lat_2=25),
        '23.30S': dist(lat_1=lat, lat_2=coord_grau_decimal('23°30\'')),
        '20S': dist(lat_1=lat, lat_2=20),
        '17S': dist(lat_1=lat, lat_2=17),
        '13S': dist(lat_1=lat, lat_2=13),
        '08S': dist(lat_1=lat, lat_2=8),
        '04S': dist(lat_1=lat, lat_2=4),
        '00S': dist(lat_1=lat, lat_2=0)
        }
    
    return min(rads, key=rads.get)

def distancia_cid(lat, lon):
    """
    Calcula a distância entre a cidade de projeto e as cidades tabeladas.

    Args:
        lat (str): Latitude de projeto.
        lon (str): Longitude de projeto.

    Returns:
        str: Nome da cidade com menor distância.
    """
    conn = sqlite3.connect(resource_path('data/dados_externos.db'))
    cursor = conn.cursor()
    
    cursor.execute('SELECT cidade, lat, lon FROM dez')
    
    cidades = {}

    for row in cursor.fetchall():
        k = row[0]
        v = (
            coord_grau_decimal(row[1].replace('\"',' ').strip()),
            coord_grau_decimal(row[2].replace('\"',' ').strip())
            )
        cidades[k] = v

    conn.close()
    
    dist_cid = {}
    
    for k, v in cidades.items(): 
        dist_cid[k] = dist(lat, v[0], lon, v[1])
        
    return min(dist_cid, key=dist_cid.get)

def externo(cidade, estacao, mes):
    """
    Busca os dados externos para a cidade indicda.

    Args:
        cidade (str): Cidade dos dados.
        estacao (str): Estação de projeto (inverno ou verao).
        mes (str): Mês do projeto de verão (mar ou dez).

    Returns:
        tuple: Tupla com valor da temperatura externa e umidade relativa.
    """ 
    getcontext().prec = 15
       
    if 'inverno' in estacao:
        conn = sqlite3.connect(resource_path('data/dados_externos.db'))
        cursor = conn.cursor()
    
        cursor.execute('SELECT td_min, tm_min, ur FROM jun WHERE cidade = ?', (cidade,))
        
        dados = cursor.fetchall()

        te = (dc(f'{dados[0][0]}') + dc(f'{dados[0][1]}')) / 2 + 4
        ur = dados[0][2]
        
        conn.close()
                
        return (te, ur)
    else:
        conn = sqlite3.connect(resource_path('data/dados_externos.db'))
        cursor = conn.cursor()
    
        cursor.execute(f'SELECT td_max, tm_max, ur FROM {mes} WHERE cidade = ?', (cidade,))
        
        dados = cursor.fetchall()

        te = (dc(f'{dados[0][0]}') + dc(f'{dados[0][1]}')) / 2
        ur = dados[0][2]
        
        conn.close()
        
        return (te, ur)
    
def hora_rad(hora):
    """
    Monta um lista com as horas de operação, para extrair os dados de radiação tabelados.

    Args:
        hora (tuple): Tupla com hora de início e fim. ('h1:m1', 'h2:m2')

    Returns:
        list: Lista com as horas para cálculo de carga térmica através da radiação.
    """    
    
    hora_arred = []
    
    for i, v in enumerate(hora):
        if i == 0:
            hora_arred.append(math.floor(int(v[:v.find(':')]) + float(dc(f'{int(v[v.find(":")+1:]) / 60}'))))
        else:
            hora_arred.append(math.ceil(int(v[:v.find(':')]) + float(dc(f'{int(v[v.find(":")+1:]) / 60}'))))
        
        if hora_arred[i] == 24:
            hora_arred[i] = 0
            
    if hora_arred[0] == hora_arred[1]:
        hora_arred[1] -= 1
        
    hora_calc = []
    stop = hora_arred[1]
    
    if hora_arred[1] < hora_arred[0]:
        stop += 24

    for i in range(hora_arred[0]-1, stop):
        hr = i % 24 + 1

        hora_calc.append(hr)
    
    return hora_calc

def rad(estacao, mes, lat, hora, orientacao, zero=0):
    """
    Busca nas tabelas o valor da radição para hora e orientação indicadas.

    Args:
        estacao (str): Estação de projeto (inverno ou verao).
        mes (str): Mês do projeto de verão (mar ou dez).
        lat (str): Latitude da tabela de radiação.
        hora (list): Lista das horas de cálculo.
        orientacao (str): Orientação da superfície.
        zero(int): Opção para zerar todos os valores (0 - mantém o padrão, 1 - substitui tudo por zero)

    Returns:
        dict: Dicionário com os valores de radiação para cada hora e orientação.
    """
    horas_disp = {
        6: '"06h"',
        7: '"07h"',
        8: '"08h"',
        9: '"09h"',
        10: '"10h"',
        11: '"11h"',
        12: '"12h"',
        13: '"13h"',
        14: '"14h"',
        15: '"15h"',
        16: '"16h"',
        17: '"17h"',
        18: '"18h"'
        }
    
    rads = {}
    
    conn = sqlite3.connect(resource_path('data/radiacao.db'))
    cursor = conn.cursor()
        
    if 'inverno' in estacao:
        tab = f'"{lat}jun"'
        for i, v in enumerate(hora):
            if v not in horas_disp.keys():
                rads[v] = 0
            else:
                if zero == 1:
                   rads[v] = 0
                else: 
                    cursor.execute(f'Select {horas_disp[v]} FROM {tab} WHERE orientacao =?', (orientacao,))
                    dados = cursor.fetchone()
                    rads[v] = dados[0]
    else:
        tab = f'"{lat}{mes}"'
        for i, v in enumerate(hora):
            if v not in horas_disp.keys():
                rads[v] = 0
            else:
                if zero == 1:
                    rads[v] = 0
                else:
                    cursor.execute(f'Select {horas_disp[v]} FROM {tab} WHERE orientacao =?', (orientacao,))
                    dados = cursor.fetchone()
                    rads[v] = dados[0]

    conn.close()    
        
    return rads

def converter_potencia(valor, pot1, pot2):
    getcontext().prec = 13
    
    if pot1 == 'w':  
        if pot2 == 'tr':
            return dc(f'{valor}') * dc('0.0002843451361')
        else:
            return dc(f'{valor}') * dc('3.4121416331279')
    
    elif pot1 == 'btuh':
        if pot2 == 'tr':
            return dc(f'{valor}') / 12000
        else:
            return dc(f'{valor}') * 1 / dc('3.4121416331279')

    else:
        if pot2 == 'btuh':
            return dc(f'{valor}') * 12000
        else:
            return dc(f'{valor}') * 1 / dc('0.0002843451361')

def Q_rad(area=0, absortancia=0, u=0, rad=0, fs=0, tipo='op'):
    """
    Calcula a carga térmica por radiação da parede, por hora.
    Args:
        area (decimal): Área da parede.
        absortancia (decimal): Absortância da parede.
        u (decimal): Coeficiente global de transferência de calor da parede.
        rad (dict): Dicionário de radiações.
        fs (decimal): Fator solar.
        tipo (str): Tipo da superfície (op - opaca ou tr - translúcida)

    Returns:
        dict: Dicionário com as cargas térmicas por radiação.
    """
    getcontext().prec = 6    
    Q = {}
    
    if tipo == 'op':
        for k, v in rad.items():
            Q[k] = area * absortancia * u * int(v) / dc('22.5')
    
    else:
        for k, v in rad.items():
            Q[k] = area * fs * int(v)
        
        
    return Q

def Q_conv(area=0, u=0, t_int=0, t_ext=0):
    """
    Calcula a carga térmica por trocas entre ambientes da parede.
    Args:
        area (decimal): Área da parede.
        u (decimal): Coeficiente global de transferência de calor da parede.
        t_int(decimal): Temperatura interna.
        t_ext (decimal): Temperatura externa.

    Returns:
        dict: Dicionário com as cargas térmicas por troca entre ambientes.
    """
    getcontext().prec = 6
    Q = area * u * (dc(f'{t_ext}') - dc(f'{t_int}'))
    
    return Q