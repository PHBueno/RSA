import os
from base64 import b64decode

from rsa.utils.logging.config import log

pem_rsa_key_identifier = {
    'private': [
        '-----BEGIN RSA PRIVATE KEY-----',
        '-----END RSA PRIVATE KEY-----',
    ],
    'public': [
        '-----BEGIN RSA PUBLIC KEY-----',
        '-----END RSA PUBLIC KEY-----',
    ],
}


def _remove_pem_identifier(content: list, key_type: str):
    """
    Função privada utilizada para remover o identificador PEM das chaves Públicas e Privadas.

    Arguments:
        content (list): Uma lista com o conteúdo da chave.
        key_type (str): O tipo de chave que será tratada.

    Returns:
        Uma lista com a chave sem os identificadores.
    """
    _content = content

    for key_indentifier in pem_rsa_key_identifier[key_type]:
        if key_indentifier in _content:
            index = _content.index(key_indentifier)
            del _content[index]
        # TODO: Escrever exception
    return _content


def read_key_file(key_file_path: str, key_type: str):
    """
    Função utilizada para fazer a leitura dos arquivos com as chaves do RSA.

    Se o arquivo estiver no formado `.pem` é feito o decode do base64, caso contrário é feito somente a leitura do arquivo

    Arguments:
        key_file_path (str): O caminho absoluto para a chave
        key_type (str): O tipo de chave que será tratada

    Returns:
        O hexadecimal da chave

    """
    path, extension = os.path.splitext(key_file_path)
    try:
        with open(key_file_path, 'r') as file:
            # Se estiver no formato .pem, faz uncode do base64
            if extension == '.pem':
                _content = [item.rstrip() for item in file.readlines()]
                content_without_identifier = _remove_pem_identifier(
                    content=_content,
                    key_type=key_type,
                )
                content = ''.join(content_without_identifier)
                return b64decode(content)
            else:
                return file.read().encode()
    except FileNotFoundError:
        log.error(f'O arquivo {key_file_path} não foi encontrado!')
        raise FileNotFoundError(
            f'O arquivo {key_file_path} não foi encontrado!'
        )
    except PermissionError:
        log.error(f'Permissão negada para leitura do arquivo {key_file_path}')
        raise PermissionError(
            f'Permissão negada para leitura do arquivo {key_file_path}'
        )


def read_file(file_path: str) -> str:
    """
    Função utilizada para realizar a leitura do conteúdo de arquivos

    Arguments:
        file_path (str): O caminho absoluto para o arquivo que será lido

    Returns:
        O conteúdo do arquivo
    """

    try:
        log.info(f'Lendo arquivo em {file_path}')
        with open(file_path, 'r') as file:
            message = (
                file.read()
            )  # TODO: Alterar quando utilizar processamento por bloco
            log.info('Arquivo lido com sucesso!')
        return message
    except FileNotFoundError:
        log.error(f'O arquivo {file_path} não foi encontrado!')
        raise FileNotFoundError(f'O arquivo {file_path} não foi encontrado!')
    except PermissionError:
        log.error(f'Permissão negada para leitura do arquivo {file_path}')
        raise PermissionError(
            f'Permissão negada para leitura do arquivo {file_path}'
        )
