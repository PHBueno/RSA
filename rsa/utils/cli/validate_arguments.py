from typing import Optional

from typer import BadParameter, Context


def validate_message(context: Context, value: str):
    # Se nenhum dos valores forem setados
    if not context.params.get('message_file') and not value:
        raise BadParameter(
            'É necessário fornecer o arquivo, ou a mensagem que será cifrada'
        )

    # Se ambos os valores forem setados
    if context.params.get('message_file') and value:
        raise BadParameter(
            'É necessário informar somente um dos parâmetros "message", ou "--message-file"'
        )

    return value


def validate_public_key(context: Context, value: str):
    # Se nenhum dos valores forem setados
    if not context.params.get('key_file') and not value:
        raise BadParameter(
            'É necessário fornecer o arquivo, ou a chave pública que será utilizada para a cifração'
        )

    # Se ambos os valores forem setados
    if context.params.get('key_file') and value:
        raise BadParameter(
            'É necessário informar somente um dos parâmetros "--key-file", ou "--public-key"'
        )

    return value


def validate_criptogram_param(context: Context, value: Optional[str]):
    # Se nenhum dos valores forem setados
    if not context.params.get('criptogram_file') and not value:
        raise BadParameter(
            'É necessário fornecer o arquivo, ou o criptograma que será decifrada'
        )

    # Se ambos os valores forem setados
    if context.params.get('criptogram_file') and value:
        raise BadParameter(
            'É necessário informar somente um dos parâmetros "criptogram", ou "--criptogram-file"'
        )

    return value
