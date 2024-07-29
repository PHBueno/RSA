import os
from importlib.metadata import version

from typing import Optional

from rich.console import Console
from typer import Argument, Context, Exit, Option, Typer
from typing_extensions import Annotated

from rsa.core.RSA import RSA
from rsa.utils.cli.read_files import read_file, read_key_file
from rsa.utils.cli.validate_arguments import (
    validate_criptogram_param,
    validate_message,
    validate_public_key,
)
from rsa.utils.cli.write_files import write_file, write_key_file
from rsa.utils.decode_rsa_key import decode_private_key as decoder_priv_key
from rsa.utils.logging.config import log

cli = Typer(
    add_completion=False,
    no_args_is_help=True,
    help='RSA cli para criação de chaves, cifração e decifração de informações',
    pretty_exceptions_show_locals=False,
)

decode_keys = Typer(
    add_completion=False,
    no_args_is_help=True,
    help='Realiza o decode de chaves criptográficas OpenSSL',
    pretty_exceptions_show_locals=False,
)

cli.add_typer(decode_keys, name='decode-keys')

__version__ = version('rsa-cli')
console = Console()
rsa = RSA()

def version_callback(value: bool):
    if value:
        print(f"RSA CLI Version: {__version__}")
        raise Exit()

@cli.callback()
def common(
    ctx: Context,
    version: Annotated[
        Optional[bool],
        Option("--version", is_eager=True, callback=version_callback),
    ] = None
):
    pass


@cli.command(help='Cria chaves pública e privada para o RSA')
def generate_keys(
    file_prefix: Annotated[
        Optional[str],
        Option(help='O prefixo para a criação dos arquivos de chaves.'),
    ],
    public_exp: Annotated[
        int, Option(help='O expoente público para a criação das chaves')
    ] = 65537,
    output_type: Annotated[
        Optional[str],
        Option(help='O formato de saída das chaves ["hex", "pem"]'),
    ] = 'hex',
    output_path: Annotated[
        str,
        Option(help='O path onde as chaves serão salvas'),
    ] = os.path.expanduser('~'),
):
    from base64 import b64encode

    log.info('Gerando Chaves RSA')
    private_key, public_key = rsa.generate_keys(public_exp=public_exp)

    # Se o tipo de output for `pem`, realiza o encode em base64
    if output_type == 'pem':
        private_key = b64encode(bytes(private_key, 'utf-8')).decode('utf-8')
        public_key = b64encode(bytes(public_key, 'utf-8')).decode('utf-8')

    keys_path = os.path.join(output_path, 'cript')

    # Define a extensão que será utilizada para o arquivo da chave
    extension = 'pem' if output_type == 'pem' else 'txt'

    # Dicionário com relação arquivo: conteúdo
    keys_files = {
        f'{file_prefix}_private_key.{extension}': str(private_key),
        f'{file_prefix}_public_key.{extension}': str(public_key),
    }

    # Realiza a escrita das chaves
    for file, content in keys_files.items():
        write_key_file(
            key_file_path=keys_path,
            key_filename=file,
            content=content,
            key_type='private' if 'private' in file else 'public',
        )


@decode_keys.command(help='Realiza o decode de chaves Privadas do OpenSSL')
def private(
    key_file: Annotated[
        Optional[str], Option(help='O arquivo com a chave privada OpenSSL')
    ],
):
    log.info('... Decodificando Chave Privada ...')

    priv_key_bytes = read_key_file(
        key_file_path=str(key_file),
        key_type='private',
    )
    priv_key_decoded = decoder_priv_key(private_key_bytes=priv_key_bytes)

    for k, v in priv_key_decoded.items():
        console.print(f'{k} = {v}')


@cli.command(help='Realiza cifração da mensagem')
def cript(
    output_file_name: Annotated[
        Optional[str],
        Option(help='O arquivo onde o criptograma será salvo'),
    ],
    message: Annotated[
        Optional[str],
        Argument(
            help='A mensagem que se deseja cifrar', callback=validate_message
        ),
    ] = None,
    public_key: Annotated[
        Optional[str],
        Option(
            help='A chave pública para a cifração',
            callback=validate_public_key,
        ),
    ] = None,
    message_file: Annotated[
        Optional[str],
        Option(
            help='O caminho absoluto do arquivo com a mensagem que se deseja cifrar'
        ),
    ] = None,
    key_file: Annotated[
        Optional[str],
        Option(help='O caminho absoluto com a chave pública'),
    ] = None,
    output_path: Annotated[
        str,
        Option(help='O path onde o criptograma será salvo'),
    ] = os.path.expanduser('~'),
):
    log.info('...Cifrando mensagem...')

    pub_key = (
        read_key_file(key_file_path=str(key_file), key_type='public').decode()
        if key_file
        else str(public_key)
    )

    absolute_path = os.path.join(
        output_path, 'cript', 'files'
    )  # Concatenação dos paths $output_path/cript/files

    _message = (
        read_file(file_path=message_file) if message_file else str(message)
    )
    cif = rsa.cript(public_key=pub_key, msg=str(_message))

    write_file(
        path=absolute_path, filename=str(output_file_name), content=str(cif)
    )  # Escreve a cifra no arquivo


@cli.command(help='Realiza a decifração de um criptograma')
def dcript(
    output_filename: Annotated[
        Optional[str],
        Option(help='O arquivo onde a mensagem será salva'),
    ],
    criptogram: Annotated[
        Optional[str],
        Argument(
            help='O Criptograma que se deseja decifrar',
            callback=validate_criptogram_param,
        ),
    ] = None,
    private_key: Annotated[
        Optional[str], Option(help='A chave privada para a decifração')
    ] = None,
    criptogram_file: Annotated[
        Optional[str],
        Option(
            help='O caminho absoluto do arquivo com o criptograma que se deseja decifrar'
        ),
    ] = None,
    key_file: Annotated[
        Optional[str],
        Option(help='O caminho absoluto com a chave privada'),
    ] = None,
    output_path: Annotated[
        str,
        Option(help='O path onde a mensagem será salva'),
    ] = os.path.expanduser('~'),
):
    log.info('...Decifrando Criptograma...')

    priv_key = (
        read_key_file(
            key_file_path=str(key_file),
            key_type='private',
        ).decode()
        if key_file
        else str(private_key)
    )

    absolute_path = os.path.join(output_path, 'cript', 'files')

    _criptogram = (
        read_file(file_path=criptogram_file)
        if criptogram_file
        else str(criptogram)
    )

    dcif = rsa.dcript(private_key=priv_key, criptogram=int(_criptogram))

    write_file(
        path=absolute_path, filename=str(output_filename), content=str(dcif)
    )
