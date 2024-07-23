# Chrome Memory Reducer
Chrome Memory Reducer é uma aplicação Python que minimiza o uso de memória do Google Chrome automaticamente, utilizando uma aplicação em segundo plano com ícone na bandeja do sistema.

## Funcionalidades
+ Ativar/Desativar a redução de memória do Google Chrome.
+ Minimize para a bandeja do sistema com um ícone personalizado.
+ Interface simples com opções de menu na bandeja do sistema.

## Pré-requisitos
+ Python 3.6 ou superior
+ Bibliotecas Python: psutil, pystray, Pillow

## Instalação
1. Clone este repositório:
```
git clone https://github.com/danielmamaimagem/chrome_memory_reducer.git
cd chrome_memory_reducer
```
2. Instale as dependências necessárias:
```
pip install -r requirements.txt
```
3. Execute o script Python:
```
python memory_reducer.py
```
A aplicação será iniciada e minimizada na bandeja do sistema.

## Como Funciona a Limpeza de Memória
O script utiliza a função SetProcessWorkingSetSize da biblioteca kernel32.dll do Windows para realizar a limpeza de memória. Esta função é chamada para cada processo do Google Chrome em execução, ajustando o conjunto de trabalho do processo para liberar memória não utilizada de volta para o sistema. Isso ajuda a reduzir o consumo de memória RAM do Google Chrome sem fechar os processos.

### Explicação Técnica:
+ Identificação dos Processos: O script utiliza a biblioteca psutil para iterar sobre todos os processos em execução e identificar aqueles cujo nome contém 'chrome'.
+ Ajuste do Conjunto de Trabalho: Para cada processo identificado, o script abre um handle para o processo com permissões totais (PROCESS_ALL_ACCESS) e chama a função SetProcessWorkingSetSize com parâmetros -1 para ajustar o conjunto de trabalho mínimo e máximo, efetivamente solicitando ao sistema operacional que libere a memória não utilizada.
+ Execução Contínua: Este processo é repetido a cada 5 segundos enquanto a funcionalidade estiver ativada, garantindo uma limpeza contínua da memória.
Contribuição

> Sinta-se à vontade para abrir issues e pull requests. Toda contribuição é bem-vinda!

