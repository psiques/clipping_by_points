import geopandas as gpd
from shapely.geometry import LineString

# Função para recortar o shapefile de entrada pelo buffer
def recortar_shapefile(buffer, shapefile):
    recorte = gpd.clip(shapefile, buffer)
    return recorte

# Função para salvar o GeoDataFrame como shapefile
def salvar_shapefile(gdf, caminho):
    gdf.to_file(caminho)

# Caminho para o arquivo de pontos
cam_pontos = input("Insira o caminho para o arquivo de pontos: ")

# Substituindo as barras invertidas por barras normais
cam_pontos = cam_pontos.replace("\\", "/")

# Carregando o shapefile de pontos
pontos = gpd.read_file(cam_pontos)

# Calculando a média da distância entre os pontos
distancias = []
for i in range(len(pontos)-1):
    ponto_atual = pontos.iloc[i]
    proximo_ponto = pontos.iloc[i+1]
    distancia = ponto_atual.geometry.distance(proximo_ponto.geometry)
    distancias.append(distancia)

media_distancia = sum(distancias) / len(distancias)
limite_distancia = 3 * media_distancia

# Removendo os segmentos de linha que ultrapassem o limite de distância
segmentos_linha = []
for i in range(len(pontos)-1):
    ponto_atual = pontos.iloc[i]
    proximo_ponto = pontos.iloc[i+1]
    distancia = ponto_atual.geometry.distance(proximo_ponto.geometry)
    if distancia <= limite_distancia:
        segmento_linha = LineString([ponto_atual.geometry, proximo_ponto.geometry])
        segmentos_linha.append(segmento_linha)

# Criando um GeoDataFrame com os segmentos de linha
linhas = gpd.GeoDataFrame(geometry=segmentos_linha, crs='EPSG:32723')

# Solicitando a metragem do buffer em metros
buffer_size = float(input("Digite a metragem do buffer em metros: "))

# Criando o buffer ao redor das linhas
areas_buffer = linhas.buffer(buffer_size)

# Dissolvendo as áreas
area_dissolvida = areas_buffer.unary_union

# Criando um GeoDataFrame com a área dissolvida
area_dissolvida_gdf = gpd.GeoDataFrame(geometry=[area_dissolvida], crs='EPSG:32723')

# Caminho para o shapefile de entrada para recortar
caminho_shapefile = input("Insira o caminho para o shapefile a ser recortado: ")

# Substituindo as barras invertidas por barras normais
caminho_shapefile = caminho_shapefile.replace("\\", "/")

# Carregando o shapefile a ser recortado
shapefile_recortar = gpd.read_file(caminho_shapefile)

# Recortando o shapefile pelo buffer
shapefile_recortado = recortar_shapefile(area_dissolvida_gdf.geometry[0], shapefile_recortar)

# Salvando os shapefiles de saída
caminho_saida = input("Digite o diretório de saída: ")

# Perguntar ao usuário se deseja salvar a trilha
salvar_trilha = input("Deseja salvar a trilha? (S/N): ")
if salvar_trilha.upper() == "S":
    trilha_saida = caminho_saida + "/trilha_" + cam_pontos.split("/")[-1]
    salvar_shapefile(linhas, trilha_saida)

# Perguntar ao usuário se deseja salvar o buffer
salvar_buffer = input("Deseja salvar o buffer? (S/N): ")
if salvar_buffer.upper() == "S":
    buffer_saida = caminho_saida + "/buffer_" + str(buffer_size) + "m"
    salvar_shapefile(area_dissolvida_gdf, buffer_saida)

# Salvando o shapefile recortado
recorte_saida = caminho_saida + "/recorte_" + caminho_shapefile.split("/")[-1]
salvar_shapefile(shapefile_recortado, recorte_saida)
