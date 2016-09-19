# configuration file for Jupyter Hub
import os

c = get_config()
# ==================================================
#          configure docker spawner
# =================================================
# spawn with Docker
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.network_name = os.environ['SPAWNER_NETWORK']
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.remove_containers = True
c.DockerSpawner.container_image =  os.environ['SPAWNER_IMAGE']
c.DockerSpawner.volumes = {os.environ['SPAWNER_HOST_VOLUME']: {'bind': '/jupyter': 'mode': 'rw'}}
c.DockerSpawner.hub_ip_connect = os.environ['JUPYTERHUB_IP']

# The docker instances need access to the Hub, so the default loopback port doesn't work:
c.JupyterHub.hub_ip = os.environ['JUPYTERHUB_IP']

# OAuth with GitHub
c.JupyterHub.authenticator_class = 'oauthenticator.GitHubOAuthenticator'

c.Authenticator.whitelist = whitelist = set()
c.Authenticator.admin_users = admin = set()

join = os.path.join
here = os.path.dirname(__file__)

with open(join(here, 'userlist')) as f:
    for line in f:
        if not line:
            continue
        parts = line.split()
        name = parts[0]
        whitelist.add(name)
        if len(parts) > 1 and parts[1] == 'admin':
            admin.add(name)


c.GitHubOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']
c.GitHubOAuthenticator.client_id = os.environ['GITHUB_CLIENT_ID']
c.GitHubOAuthenticator.client_secret = os.environ['GITHUB_CLIENT_SECRET']


# ssl config
ssl = join(here, 'ssl')
keyfile = join(ssl, 'ssl.key')
certfile = join(ssl, 'ssl.cert')
if os.path.exists(keyfile):
    c.JupyterHub.ssl_key = keyfile
if os.path.exists(certfile):
    c.JupyterHub.ssl_cert = certfile

# Set the log level by value or name.
c.JupyterHub.log_level = 'DEBUG'
