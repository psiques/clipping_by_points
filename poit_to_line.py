import geopandas as gpd
from shapely.geometry import LineString

# Função para recortar o shapefile de entrada pelo buffer
def recortar_shape(buffer, shape):
    recorte = gpd.clip(shape, buffer)
    return recorte

# Função para salvar o GeoDataFrame como shapefile
def salvar_shape(gdf, caminho):
    gdf.to_file(caminho)

# Caminho para o arquivo de pontos
cam = input("Insira o caminho para o arquivo de pontos: ")

# Substituindo as barras invertidas por barras normais
cam = cam.replace("\\", "/")

# Carregando o shapefile de pontos
pontos = gpd.read_file(cam)

# Calculando a média da distância entre os pontos
dists = []
for i in range(len(pontos)-1):
    atual = pontos.iloc[i]
    prox = pontos.iloc[i+1]
    dist = atual.geometry.distance(prox.geometry)
    dists.append(dist)

media_dist = sum(dists) / len(dists)
limite_dist = 3 * media_dist

# Removendo os segmentos de linha que ultrapassem o limite de distância
segmentos = []
for i in range(len(pontos)-1):
    atual = pontos.iloc[i]
    prox = pontos.iloc[i+1]
    dist = atual.geometry.distance(prox.geometry)
    if dist <= limite_dist:
        segmento = LineString([atual.geometry, prox.geometry])
        segmentos.append(segmento)

# Criando um GeoDataFrame com os segmentos de linha
linhas = gpd.GeoDataFrame(geometry=segmentos, crs='EPSG:32723')

# Solicitando a metragem do buffer em metros
buffer_size = float(input("Digite a metragem do buffer em metros: "))

# Criando o buffer ao redor das linhas
areas_buffer = linhas.buffer(buffer_size)

# Dissolvendo as áreas
area_dissolv = areas_buffer.unary_union

# Criando um GeoDataFrame com a área dissolvida
area_dissolv_gdf = gpd.GeoDataFrame(geometry=[area_dissolv], crs='EPSG:32723')

# Caminho para o shapefile de entrada para recortar
caminho_shape = input("Insira o caminho para o shapefile a ser recortado: ")

# Substituindo as barras invertidas por barras normais
caminho_shape = caminho_shape.replace("\\", "/")

# Carregando o shapefile a ser recortado
shape_recort = gpd.read_file(caminho_shape)

# Recortando o shapefile pelo buffer
shape_recortado = recortar_shape(area_dissolv_gdf.geometry[0], shape_recort)

# Salvando os shapefiles de saída
saida = input("Digite o diretório de saída: ")

# Perguntar ao usuário se deseja salvar a trilha
salvar_trilha = input("Deseja salvar a trilha? (S/N): ")
if salvar_trilha.upper() == "S":
    trilha_saida = saida + "/trilha_" + cam.split("/")[-1]
    salvar_shape(linhas, trilha_saida)

# Perguntar ao usuário se deseja salvar o buffer
salvar_buffer = input("Deseja salvar o buffer? (S/N): ")
if salvar_buffer.upper() == "S":
    buffer_saida = saida + "/buffer_" + str(buffer_size) + "m"
    salvar_shape(area_dissolv_gdf, buffer_saida)

# Salvando o shapefile recortado
recorte_saida = saida + "/recorte_" + caminho_shape.split("/")[-1]
salvar_shape(shape_recortado, recorte_saida)
