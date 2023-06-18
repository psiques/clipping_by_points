import geopandas as gpd
from shapely.geometry import LineString

# Função para recortar o shapefile de entrada pelo buffer
def recortar_shapefile(buffer, shapefile):
    recorte = shapefile.geometry.clip(buffer)
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

# Projetando os dados para um sistema de coordenadas planas
pontos = pontos.to_crs('EPSG:31983')

# Obtendo o CRS do shapefile de pontos
crs_pontos = pontos.crs

# Criando todas as linhas entre os pontos
segmentos_linha = []
for i in range(len(pontos)-1):
    ponto_atual = pontos.iloc[i]
    proximo_ponto = pontos.iloc[i+1]
    segmento_linha = LineString([ponto_atual.geometry, proximo_ponto.geometry])
    segmentos_linha.append(segmento_linha)

# Calculando a distância média
distancia_media = sum(segmento.length for segmento in segmentos_linha) / len(segmentos_linha)

# Removendo linhas com comprimento superior a 3 vezes a distância média
segmentos_filtrados = [segmento for segmento in segmentos_linha if segmento.length <= 3 * distancia_media]

# Criando um novo GeoDataFrame com os segmentos de linha filtrados
multilinhas = gpd.GeoDataFrame(geometry=segmentos_filtrados, crs=crs_pontos)

# Solicitando a metragem do buffer em metros
buffer_size = float(input("Digite a metragem do buffer em metros: "))

# Criando o buffer ao redor das linhas
areas_buffer = multilinhas.buffer(buffer_size)

# Carregando o shapefile a ser recortado
caminho_shapefile = input("Insira o caminho para o shapefile a ser recortado: ")
caminho_shapefile = caminho_shapefile.replace("\\", "/")
shapefile_recortar = gpd.read_file(caminho_shapefile)

# Obtendo o CRS do shapefile a ser recortado
crs_shapefile = shapefile_recortar.crs

# Transformando o CRS do buffer
areas_buffer = areas_buffer.to_crs(crs_shapefile)

# Dissolvendo as áreas
area_dissolvida = areas_buffer.unary_union

# Criando um GeoDataFrame com a área dissolvida
area_dissolvida_gdf = gpd.GeoDataFrame(geometry=[area_dissolvida], crs=crs_shapefile)

# Recortando o shapefile pelo buffer
shapefile_recortado = recortar_shapefile(area_dissolvida_gdf.geometry[0], shapefile_recortar)

# Salvando os shapefiles de saída
caminho_saida = input("Digite o caminho para salvar o shapefile recortado: ")
caminho_saida = caminho_saida.replace("\\", "/")
salvar_shapefile(shapefile_recortado, caminho_saida)
