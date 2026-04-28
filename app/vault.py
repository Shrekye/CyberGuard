import hvac
import os
import logging


def get_vault_client():
    client = hvac.Client(
        url=os.environ.get('VAULT_ADDR', 'http://openbao:8200'),
        token=os.environ.get('VAULT_TOKEN')
    )
    if not client.is_authenticated():
        logging.error("Authentificed is impossible")
        return None
    return client


def get_secret(path, key, mount_point='secret'):
    """
    Récupère un secret spécifique.
    Exemple : get_secret('database', 'password')
    """
    client = get_vault_client()
    if not client:
        return None
    try:
        read_ressourse = client.secrets.kv.v2.read_secret_version(
            path=path,
            mount_point=mount_point
        )
        return read_ressourse['data']['data'].get(key)
    except Exception as e:
        logging.error(f"Erreur lors de la lecture du secret {path}/{key} : {e}")
        return None