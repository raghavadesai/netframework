import ssl
from typing import Optional
from .logger import setup_logger

logger = setup_logger(__name__)

def create_server_ssl_context(
    certfile: str,
    keyfile: str,
    password: Optional[str] = None,
    verify_mode: int = ssl.CERT_NONE
) -> ssl.SSLContext:
    """Create SSL context for server with the given certificate and key."""
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.verify_mode = verify_mode
    context.load_cert_chain(certfile=certfile, keyfile=keyfile, password=password)
    return context

def create_client_ssl_context(
    cafile: Optional[str] = None,
    verify_mode: int = ssl.CERT_REQUIRED
) -> ssl.SSLContext:
    """Create SSL context for client with optional CA certificate."""
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.verify_mode = verify_mode
    if cafile:
        context.load_verify_locations(cafile=cafile)
    return context
