import os
from base64 import b64decode

from rsa.utils.logging.config import log


def read_key_file(key_file_path: str) -> str:
    """
    Função utilizada para fazer a leitura dos arquivos com as chaves do RSA.

    Se o arquivo estiver no formado `.pem` é feito o decode do base64, caso contrário é feito somente a leitura do arquivo

    Arguments:
        key_file_path (str): O caminho absoluto para a chave

    Returns:
        O hexadecimal da chave

    """
    path, extension = os.path.splitext(key_file_path)
    try:
        with open(key_file_path, 'r') as file:
            # Se estiver no formato .pem, faz uncode do base64
            if extension == '.pem':
                file.readline()
                content = file.readline()
                return b64decode(content).decode()
            else:
                return file.read()
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
