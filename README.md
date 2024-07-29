# Documentação para Executar o App FastAPI no Ambiente Linux (Ubuntu)
## Atualize e Faça o Upgrade do Ubuntu
`sudo apt update && sudo apt upgrade -y`
## Verifique a Versão do Python 3
`python3 --version`
## Instale a Virtualenv no Ubuntu 
`sudo apt install python3-venv -y`
## Crie uma Virtualenv chamada montseguro
`python3 -m venv montseguro`
## Entre na Virtualenv e Ative-a
`source montseguro/bin/activate`
## Dentro da Virtualenv, Crie uma Pasta chamada microservices e Entre nela
`mkdir microservices `
###### Next
`cd microservices`
## Clone o Repositório do GitHub
`git clone https://github.com/lucasmarrtt/montseguro .`
## Em Outro Terminal, Instale e Configure o Redis
`sudo apt install redis-server -y`
###### Next
`sudo systemctl enable redis-server`
###### Next
`sudo systemctl start redis-server`
## Verifique a Instalação do Redis
`redis-cli ping`
## Instale o Docker no Ubuntu
`sudo apt install docker.io -y`
###### Next
`sudo systemctl enable docker`
###### Next
`sudo systemctl start docker`
## Verifique a Instalação do Docker
`docker --version`
## Abra o Terminal na Pasta microservices (Certifique-se de que a Virtualenv esteja Ativada)
`cd path/to/microservices`
###### Next 
`source ../montseguro/bin/activate`
## Instale as Dependências do Projeto
`pip install -r requirements.txt`
## Crie a Imagem Docker
`docker build -t fastapi-app .`
## Execute o Container Docker
`docker run -d -p 8000:8000 fastapi-app`
## Acesse o Aplicativo no Navegador
Abra o navegador e acesse http://localhost:8000

### Observação Importante 
- Em databases.py, configure seu banco de dados conforme necessário.
- Você pode visitar o repositório de produção no link: [---coloque o link aqui---]

### Repita esses passos em sua instancia linux na AWS, Azure, Heroku etc 
- É importante esclarecer que cada servidor é unico. As configurações podem ser diferentes para outras distribuições linux, assim como windows e mac. 


# POR FAVOR LEIA AQUI 
Gostaria de informar que encontrei uma limitação inesperada ao tentar implementar a solução na AWS com Kubernetes. 
O nível gratuito da AWS oferece apenas uma CPU, enquanto a execução do Kubernetes 
requer pelo menos duas CPUs para garantir o funcionamento adequado do cluster. Executar kubernetes em uma instancia de nível gratuito tem 
muitas restrições de recursos, a instancia de (t2.micro) possui apenas 1 CPU e 1 GB/RAM o que é insuficiente para rodar um cluster kubernetes com junto com a aplicação nele, 
é recomendado no minimo 2 CPUs e 4 GB/RAM. Infelizmente, isso me impediu de seguir com a implementação conforme o plano inicial. 

Agradeço pela compreensão e peço desculpas por qualquer inconveniente.

