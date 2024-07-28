import os

from rsa.utils.logging.config import log


def _create_dir(path: str) -> dict[str, str]:
    """
    Realiza a criação dos paths necessários caso não existam

    Arguments:
        path (str): O path que será criado

    Returns:
        Um dicionário com mensagem de falha ou sucesso
    """
    log.info(f'Criando diretório "{path}"')
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            log.info(f'Diretório {path} criado com sucesso')
            return {'ok': 'success'}
        except PermissionError:
            log.error(f'Permissão negada para a criação do diretório: {path}')
            return {'nok': 'permission error'}
    else:
        log.info(f'O diretório {path} já existe')
        return {'ok': 'dir exists'}


def write_key_file(
    key_file_path: str, key_filename: str, content: str, key_type: str
) -> dict[str, str]:
    """
    Realiza a escrita das chaves RSA.

    Arguments:
        path (str): O diretório onde o arquivo será criado
        filename (str): O nome do arquivo
        content (str): O conteúdo que será escrito no arquivo.

    Returns:
        Um dicionário com mensagem de falha ou sucesso
    """
    pem_key = {
        'public_header': '-----BEGIN RSA PUBLIC KEY-----',
        'public_footer': '-----END RSA PUBLIC KEY-----',
        'private_header': '-----BEGIN RSA PRIVATE KEY-----',
        'private_footer': '-----END RSA PRIVATE KEY-----',
    }

    _create_dir(path=key_file_path)

    _, extension = os.path.splitext(key_filename)

    absolute_path = os.path.join(key_file_path, key_filename)

    pem_header = pem_key[f'{key_type}_header']
    pem_footer = pem_key[f'{key_type}_footer']

    try:
        with open(absolute_path, 'w') as file:
            if extension == '.pem':
                file.write(f'{pem_header}\n')
                file.write(f'{content}\n')
                file.write(f'{pem_footer}')
            else:
                file.write(f'{content}')
        log.info('Conteúdo escrito com sucesso!')
        return {'ok': 'success'}
    except Exception as e:
        log.error(f'Erro para escrever no arquivo {key_filename}: {e}')
        return {'nok': str(e)}


def write_file(path: str, filename: str, content: str) -> dict[str, str]:
    """
    Realiza a escrita de arquivos para a saída do CLI

    Arguments:
        path (str): O diretório onde o arquivo será criado
        filename (str): O nome do arquivo
        content (str): O conteúdo que será escrito no arquivo.

    Returns:
        Um dicionário com mensagem de falha ou sucesso
    """
    _create_dir(path=path)

    absolute_path = os.path.join(path, filename)

    log.info(f'Escrevendo conteúdo em {absolute_path}')
    try:
        with open(absolute_path, 'w') as file:
            file.write(content)
        log.info('Conteúdo escrito com sucesso!')
        return {'ok': 'success'}
    except Exception as e:
        log.error(f'Erro para escrever no arquivo {filename}: {e}')
        return {'nok': str(e)}
