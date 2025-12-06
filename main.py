import routeros_api
import json
import ssl

# --- Reemplaza con los datos de tu router ---
ROUTER_HOST = '10.11.1.110' # IP por defecto en muchos modelos
ROUTER_USER = 'mda.skynet'
ROUTER_PASS = '*SkyN3t24*' # Deja vacío si no tiene contraseña por defecto

# Configura el contexto SSL si usas API-SSL (puerto 8729)
# context = ssl.create_default_context()
# context.check_hostname = False
# context.verify_mode = ssl.CERT_NONE # Deshabilita la verificación si no tienes un certificado válido

try:
    # Intenta la conexión
    connection = routeros_api.RouterOsApiPool(
        ROUTER_HOST,
        username=ROUTER_USER,
        password=ROUTER_PASS,
        port=5223, # Puerto API estándar. Usa 8729 si es API-SSL y configuras SSL.
        plaintext_login=True, # Necesario para RouterOS >= 6.43
        # use_ssl=False, # Cambia a True si usas API-SSL
        # ssl_context=context
    )
    api = connection.get_api()

    print(f"Conexión exitosa a {ROUTER_HOST}")

    # Ejecuta un comando: obtener direcciones IP
    # Los comandos API usan un formato de ruta, similar a la terminal de MikroTik
    ip_addresses = api.get_resource('/ip/address')
    print("\nDirecciones IP en el router:")
    for address in ip_addresses.get():
        print(f"  - Interfaz: {address['interface']}, Dirección: {address['address']}, Red: {address['network']}")

    # Cierra la conexión
    connection.disconnect()
    print("\nConexión cerrada.")

except routeros_api.exceptions.RouterOsApiError as e:
    print(f"Error de API de MikroTik: {e}")
except Exception as e:
    print(f"Error de conexión: {e}")

