# Clipping by Points

Este código tem como objetivo criar uma trilha (linha) entre pontos geográficos e realizar o recorte de um shapefile com base nessa trilha. Além disso, é possível gerar um buffer em torno da trilha e salvar os resultados em shapefiles separados.

## Requisitos

- Python 3.x
- Bibliotecas: geopandas, shapely

## Utilização

1. Faça o download e instale o Python em sua máquina, caso ainda não tenha: https://www.python.org/downloads/

2. Instale as bibliotecas necessárias. Abra o prompt de comando e execute o seguinte comando:

   ```
   pip install geopandas shapely
   ```

3. Baixe o código "poit_to_line.py" do repositório do GitHub: [[link do repositório](https://github.com/psiques/clipping_by_points)]

4. Execute o código no Python. Você será solicitado a inserir algumas informações:

   - Insira o caminho para o arquivo de pontos: [caminho completo para o arquivo de pontos]
   - Digite a metragem do buffer em metros: [valor numérico da metragem do buffer]
   - Insira o caminho para o shapefile a ser recortado: [caminho completo para o shapefile a ser recortado]
   - Digite o diretório de saída: [caminho completo para o diretório de saída]

5. Aguarde o processamento do código. Os resultados serão salvos como shapefiles no diretório de saída especificado.

## Descrição

O código é dividido em diferentes etapas:

1. Carregamento do arquivo de pontos: O usuário insere o caminho para o arquivo de pontos geográficos. O código carrega o shapefile usando a biblioteca geopandas e realiza a projeção dos dados no sistema de coordenadas UTM (zona 23S) para cálculos mais precisos, editável pelo usuário.

2. Criação das linhas entre os pontos: Com base nos pontos carregados, o código cria segmentos de linha (trilha) conectando cada ponto ao próximo.

3. Criação do buffer: O usuário insere a metragem desejada para o buffer em metros. O código cria um buffer em torno da trilha usando a função `buffer` da biblioteca shapely.

4. Dissolução das áreas: As áreas dos buffers são dissolvidas em uma única área, removendo as arestas internas e considerando apenas a geometria da trilha como um todo.

5. Recorte do shapefile: O usuário insere o caminho para o shapefile que será recortado com base na área do buffer. O código carrega o shapefile e utiliza a função `clip` da biblioteca geopandas para realizar o recorte.

6. Salvamento dos shapefiles de saída: Os shapefiles resultantes da trilha, buffer e recorte são salvos no diretório de saída especificado pelo usuário.

## Contribuição

Este código foi desenvolvido por Thais Sousa em colaboração com ChatGPT. Sinta-se à vontade para contribuir com melhorias ou correções através de pull requests.
