# RSA CLI
[![Documentation Status](https://readthedocs.org/projects/rsa-cli/badge/?version=latest)](https://rsa-cli.readthedocs.io/pt-br/latest/?badge=latest)

## Instalação

```bash
pip install rsa-cli
```

## Informações básicas

RSA é uma CLI utilizada para criar chaves RSA públicas e privadas, realizar a cifração e decifração de informações.

```bash
rsa --help
```

```bash
Usage: rsa [OPTIONS] COMMAND [ARGS]...                                                                                                                   
                                                                                                                                                          
 RSA cli para criação de chaves, cifração e decifração de informações                                                                                     
                                                                                                                                                          
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version                                                                                                                                              │
│ --help             Show this message and exit.                                                                                                         │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ cript           Realiza cifração da mensagem                                                                                                           │
│ dcript          Realiza a decifração de um criptograma                                                                                                 │
│ decode-keys     Realiza o decode de chaves criptográficas OpenSSL                                                                                      │
│ generate-keys   Cria chaves pública e privada para o RSA                                                                                               │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Como usar?
### Gerando chaves RSA
O RSA é um algoritmo que utiliza chaves públicas e privadas para cifração e decifração de informações. Normalmente a chave pública é utilizada para a cifração de informações e a chave privada é utilizada na decifração. 
A chave pública pode ser compartilhada livremente com os envolvidos na comunicação e a chave privada deve ser mantida em segurança.

```bash
rsa generate-keys --help
```
```bash
Usage: rsa generate-keys [OPTIONS]                                                                                                                       
                                                                                                                                                          
 Cria chaves pública e privada para o RSA                                                                                                                 
                                                                                                                                                          
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --file-prefix        TEXT     O prefixo para a criação dos arquivos de chaves. [default: None] [required]                                           │
│    --public-exp         INTEGER  O expoente público para a criação das chaves [default: 65537]                                                         │
│    --output-type        TEXT     O formato de saída das chaves ["hex", "pem"] [default: hex]                                                           │
│    --output-path        TEXT     O path onde as chaves serão salvas [default: /home/pedro]                                                             │
│    --help                        Show this message and exit.                                                                                           │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
#### Gerando chaves com opções básicas

```bash
rsa generate-keys --file-prefix=new-keys --output-type=pem
```
As chaves pública e privada serão escritas em arquivos com os nomes `new-keys_public_key.pem` e `new-keys_private_key.pem`, dentro do diretório definido utilizando a opção `--output-path`, se a opção não for definida o padrão de diretório será a home do usuário.

É possível gerar chaves no formato Hexadecimal:

```bash
rsa generate-keys --file-prefix=new-keys-hex --output-type=hex
```

### Cifrando informações
```bash
rsa cript --help
```
```bash
Usage: rsa cript [OPTIONS] [MESSAGE]                                                                                                                     
                                                                                                                                                          
 Realiza cifração da mensagem                                                                                                                             
                                                                                                                                                          
╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   message      [MESSAGE]  A mensagem que se deseja cifrar [default: None]                                                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --output-filename        TEXT  O arquivo onde o criptograma será salvo [default: None] [required]                                                  │
│    --public-key              TEXT  A chave pública para a cifração [default: None]                                                                     │
│    --message-file            TEXT  O caminho absoluto do arquivo com a mensagem que se deseja cifrar [default: None]                                   │
│    --key-file                TEXT  O caminho absoluto com a chave pública [default: None]                                                              │
│    --output-path             TEXT  O path onde o criptograma será salvo [default: /home/pedro]                                                         │
│    --help                          Show this message and exit.                                                                                         │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### Cifrando informações com opções básicas

```bash
rsa cript 'Minha mensagem para cifrar' --output-file-name=criptograma.txt --key-file=/home/teste/cript/new-keys_public_key.pem
```
Este comando irá cifrar a informação passada via linha de comando, utilizando a chave pública informada na opção `--key-file`. O criptograma será escrito no arquivo `criptograma.txt`, dentro do diretório definido na opção `--output-path`, se esta opção não for definida o diretório padrão será utilizado (home do usuário).

#### Cifrando informações em arquivos
Com o CLI é possível cifrar informações que estejam dentro de arquivos.

- Criando o arquivo que será cifrado:
```bash
echo 'Minha mensagem para cifrar' > minha-mensagem.txt
```

- Cifrando o arquivo:
```bash
rsa --message-file=minha-mensagem.txt --key-file=/home/teste/cript/new-keys_public_key.pem --output-file-name=criptograma.txt
```

### Decifrando informações
```bash
rsa dcript --help
```
```bash
Usage: rsa dcript [OPTIONS] [CRIPTOGRAM]                                                                                                                 
                                                                                                                                                          
 Realiza a decifração de um criptograma                                                                                                                   
                                                                                                                                                          
╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   criptogram      [CRIPTOGRAM]  O Criptograma que se deseja decifrar [default: None]                                                                   │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --output-filename        TEXT  O arquivo onde a mensagem será salva [default: None] [required]                                                      │
│    --private-key            TEXT  A chave privada para a decifração [default: None]                                                                    │
│    --criptogram-file        TEXT  O caminho absoluto do arquivo com o criptograma que se deseja decifrar [default: None]                               │
│    --key-file               TEXT  O caminho absoluto com a chave privada [default: None]                                                               │
│    --output-path            TEXT  O path onde a mensagem será salva [default: /home/pedro]                                                             │
│    --help                         Show this message and exit.                                                                                          │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### Decifrando informações com opções básicas
```bash
rsa dcript --criptogram-file=/home/teste/cript/files/criptograma.txt --key-file=/home/teste/cript/new-keys_private_key.pem --output-filename=message.txt
```

Este comando irá decifrar o critograma escrito em `/home/teste/cript/files/criptograma.txt`, utilizando a chave privada informada com a opção `--key-file`. A mensagem decifrada será escrita no arquivo `message.txt`, dentro do diretório definido na opção `--output-path`, se esta opção não for definida o diretório padrão será utilizado (home do usuário).