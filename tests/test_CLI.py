import os

from typer.testing import CliRunner

from rsa.core.cli import cli
from rsa.utils.cli.read_files import read_file

runner = CliRunner()

default_files_path = os.path.expanduser('~')

cript_filespath = os.path.join(default_files_path, 'rsa', 'pytest')

mensagem = 'teste testando'

public_key_pem_file = 'pytest-key-pem_public_key.pem'
private_key_pem_file = 'pytest-key-pem_private_key.pem'

public_key_hex_file = 'pytest-key-hex_public_key.txt'
private_key_hex_file = 'pytest-key-hex_private_key.txt'


def test_rsa_cli_deve_retornar_0_ao_stdout():
    result = runner.invoke(cli)
    assert result.exit_code == 0


def test_rsa_cli_deve_criar_os_arquivos_de_chaves_pem():
    from shutil import rmtree

    filepath = os.path.join(cript_filespath, 'cript')
    key_file_prefix = 'pytest-key-pem'

    if os.path.exists(cript_filespath):
        rmtree(cript_filespath)

    runner.invoke(
        cli,
        [
            'generate-keys',
            '--file-prefix',
            f'{key_file_prefix}',
            '--output-path',
            f'{cript_filespath}',
            '--output-type',
            'pem',
        ],
    )

    assert os.path.isfile(f'{filepath}/{public_key_pem_file}')
    assert os.path.isfile(f'{filepath}/{private_key_pem_file}')


def test_rsa_cli_deve_criar_os_arquivos_de_chaves_hex():
    filepath = os.path.join(cript_filespath, 'cript')
    key_file_prefix = 'pytest-key-hex'

    runner.invoke(
        cli,
        [
            'generate-keys',
            '--file-prefix',
            f'{key_file_prefix}',
            '--output-path',
            f'{cript_filespath}',
            '--output-type',
            'hex',
        ],
    )

    assert os.path.isfile(f'{filepath}/{public_key_hex_file}')
    assert os.path.isfile(f'{filepath}/{private_key_hex_file}')


def test_rsa_cli_cript_deve_retornar_erro_ao_setar_mais_de_um_parametro_para_mensagem():
    key_filepath = os.path.join(
        cript_filespath, 'cript', f'{public_key_pem_file}'
    )  # O path com o arquivo de chave

    message_error = 'É necessário informar somente um dos parâmetros "message", ou "--message-file"'

    result = runner.invoke(
        cli,
        [
            'cript',
            f'{mensagem}',
            '--message-file',
            'fake-message-file.txt',
            '--output-file-name',
            'pytest-criptogram.txt',
            '--key-file',
            f'{key_filepath}',
        ],
    )

    assert result.exit_code == 2
    assert message_error in result.output


def test_rsa_cli_deve_retornar_erro_se_nenhum_parametro_de_mensagem_for_informado():
    key_filepath = os.path.join(
        default_files_path, 'cript', f'{public_key_pem_file}'
    )  # O path com o arquivo de chave

    message_error = (
        'É necessário fornecer o arquivo, ou a mensagem que será cifrada'
    )

    result = runner.invoke(
        cli,
        [
            'cript',
            '--output-file-name',
            'pytest-criptogram.txt',
            '--key-file',
            f'{key_filepath}',
        ],
    )

    assert result.exit_code == 2
    assert message_error in result.output


def test_rsa_cli_cript_deve_retornar_erro_se_nenhum_parametro_para_public_key_for_setado():
    message_error = 'É necessário fornecer o arquivo, ou a chave pública que será utilizada para a cifração'

    result = runner.invoke(
        cli,
        [
            'cript',
            f'{mensagem}',
            '--output-file-name',
            'pytest-criptogram.txt',
        ],
    )

    assert result.exit_code == 2
    assert message_error in result.output


def test_rsa_cli_cript_deve_retornar_erro_ao_setar_mais_de_um_parametro_para_public_key():
    key_filepath = os.path.join(
        default_files_path, 'cript', f'{public_key_pem_file}'
    )  # O path com o arquivo de chave

    message_error = 'É necessário informar somente um dos parâmetros "--key-file", ou "--public-key"'

    result = runner.invoke(
        cli,
        [
            'cript',
            f'{mensagem}',
            '--key-file',
            f'{key_filepath}',
            '--public-key',
            '12345',
            '--output-file-name',
            'pytest-criptogram.txt',
        ],
    )

    assert result.exit_code == 2
    assert message_error in result.output


def test_rsa_cli_dcript_deve_retornar_erro_se_nenhum_parametro_para_criptogram_for_setado():
    key_filepath = os.path.join(
        default_files_path, 'cript', f'{private_key_pem_file}'
    )  # O path com o arquivo de chave

    message_error = (
        'É necessário fornecer o arquivo, ou o criptograma que será decifrada'
    )

    result = runner.invoke(
        cli,
        [
            'dcript',
            '--key-file',
            f'{key_filepath}',
            '--output-filename',
            'pytest-message.txt',
        ],
    )

    assert result.exit_code == 2
    assert message_error in result.output


def test_rsa_cli_dcript_deve_retornar_erro_ao_setar_mais_de_um_parametro_para_criptogram():
    key_filepath = os.path.join(
        default_files_path, 'cript', f'{private_key_pem_file}'
    )  # O path com o arquivo de chave

    message_error = 'É necessário informar somente um dos parâmetros "criptogram", ou "--criptogram-file"'

    result = runner.invoke(
        cli,
        [
            'dcript',
            'fake-criptogram',
            '--key-file',
            f'{key_filepath}',
            '--criptogram-file',
            '/teste/fake-criptogram.txt',
            '--output-filename',
            'pytest-message.txt',
        ],
    )

    assert result.exit_code == 2
    assert message_error in result.output


def test_deve_retornar_erro_quando_informar_um_arquivo_de_chave_publica_inexistente():
    fake_public_key_file = '/teste/fake-key_public_key.pem'
    message_error = f'O arquivo {fake_public_key_file} não foi encontrado!'

    result = runner.invoke(
        cli,
        [
            'cript',
            f'{mensagem}',
            '--output-file-name',
            'pytest-criptogram.txt',
            '--key-file',
            f'{fake_public_key_file}',
        ],
    )

    assert isinstance(result.exception, FileNotFoundError)
    assert message_error in str(result.exception)


def test_deve_retornar_erro_quando_informar_um_arquivo_de_mensagem_inexistente():
    key_filepath = os.path.join(
        cript_filespath, 'cript', f'{public_key_pem_file}'
    )  # O path com o arquivo de chave pública "~/rsa/pytest/cript/f'{public_key_pem_file}'"

    fake_message_file = '/teste/fake-message.txt'
    message_error = f'O arquivo {fake_message_file} não foi encontrado!'

    result = runner.invoke(
        cli,
        [
            'cript',
            '--message-file',
            f'{fake_message_file}',
            '--output-file-name',
            'pytest-criptogram.txt',
            '--key-file',
            f'{key_filepath}',
        ],
    )

    assert isinstance(result.exception, FileNotFoundError)
    assert message_error in str(result.exception)


def test_rsa_cli_deve_criar_arquivo_com_a_cifra_a_partir_de_uma_chave_pem():
    key_filepath = os.path.join(
        cript_filespath, 'cript', f'{public_key_pem_file}'
    )  # O path com o arquivo de chave

    criptogram_path = os.path.join(cript_filespath, 'cript', 'files')

    runner.invoke(
        cli,
        [
            'cript',
            f'{mensagem}',
            '--output-file-name',
            'pytest-criptogram.txt',
            '--output-path',
            f'{cript_filespath}',
            '--key-file',
            f'{key_filepath}',
        ],
    )

    assert os.path.isfile(f'{criptogram_path}/pytest-criptogram.txt')


def test_rsa_cli_deve_criar_arquivo_com_a_cifra_a_partir_de_uma_chave_hex():
    key_filepath = os.path.join(
        cript_filespath, 'cript', f'{public_key_hex_file}'
    )  # O path com o arquivo de chave

    criptogram_path = os.path.join(cript_filespath, 'cript', 'files')

    runner.invoke(
        cli,
        [
            'cript',
            f'{mensagem}',
            '--output-file-name',
            'pytest-criptogram-publickey-hex.txt',
            '--output-path',
            f'{cript_filespath}',
            '--key-file',
            f'{key_filepath}',
        ],
    )

    assert os.path.isfile(
        f'{criptogram_path}/pytest-criptogram-publickey-hex.txt'
    )


def test_rsa_cli_o_conteudo_do_criptograma_deve_ser_diferente_da_mensagem():
    criptogram_path = os.path.join(
        cript_filespath, 'cript', 'files', 'pytest-criptogram.txt'
    )

    content = read_file(file_path=criptogram_path)

    assert content.isdigit
    assert content != mensagem


def test_rsa_cli_deve_criar_arquivo_com_a_mensagem():
    key_filepath = os.path.join(
        cript_filespath, 'cript', f'{private_key_pem_file}'
    )  # O path com o arquivo de chave

    criptogram_path = os.path.join(
        cript_filespath, 'cript', 'files', 'pytest-criptogram.txt'
    )  # `default_files_path`/cript/files/pytest-criptogram.txt

    message_path = os.path.join(
        cript_filespath, 'cript', 'files', 'pytest-message.txt'
    )  # `default_files_path`/cript/files/pytest-message.txt

    runner.invoke(
        cli,
        [
            'dcript',
            '--key-file',
            f'{key_filepath}',
            '--criptogram-file',
            f'{criptogram_path}',
            '--output-filename',
            'pytest-message.txt',
            '--output-path',
            f'{cript_filespath}',
        ],
    )

    assert os.path.isfile(f'{message_path}')


def test_rsa_cli_o_conteudo_do_arquivo_decifrado_deve_ser_igual_a_mensagem():
    message_path = os.path.join(
        cript_filespath, 'cript', 'files', 'pytest-message.txt'
    )  # `default_files_path`/cript/files/pytest-message.txt

    content = read_file(file_path=message_path)

    assert mensagem == content
