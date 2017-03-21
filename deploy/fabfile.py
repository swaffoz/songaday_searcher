import os
from fabric.contrib.files import sed
from fabric.api import env, local, sudo, reboot, settings

# initialize the base directory
abs_dir_path = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))


# declare environment global variables

# FreeBSD does not have bash, so we'll use tcsh instead
env.shell = '/bin/tcsh -c'

# user that will log into the box
env.user = 'freebsd'

# list of remote IP addresses
env.hosts = ['159.203.165.95']

# ssh key path
env.ssh_keys_dir = os.path.join(abs_dir_path, 'deploy', 'ssh-keys')


def start_provision():
    """
    Start server provisioning
    """
    # Prevent root SSHing into the remote server
    sed('/etc/ssh/sshd_config', '^UsePAM yes', 'UsePAM no', use_sudo=True)
    sed('/etc/ssh/sshd_config', '^PermitRootLogin yes',
        'PermitRootLogin no', use_sudo=True)
    sed('/etc/ssh/sshd_config', '^#PasswordAuthentication yes',
        'PasswordAuthentication no', use_sudo=True)

    upload_keys()
    sudo('service sshd reload')
    upgrade_server()


def upload_keys():
    """
    Upload the SSH public/private keys to the remote server via scp
    """
    authorized_keys = os.path.join(env.ssh_keys_dir, 'authorized_keys')
    make_authorized_keys_file = 'cat {} > {}'.format(
        os.path.join(env.ssh_keys_dir, '*'),
        authorized_keys
    )
    scp_command = 'scp -r {} {}@{}:~/.ssh'.format(
        authorized_keys,
        env.user,
        env.host_string
    )
    remove_authorized_keys_file = 'rm {}'.format(
        authorized_keys
    )

    local(make_authorized_keys_file)
    local(scp_command)
    local(remove_authorized_keys_file)


def upgrade_server():
    """
    Upgrade the server as a root user
    """
    sudo('pkg upgrade -y')
    sudo('pkg install -y python27 py27-pip')
    print('Rebooting...')
    sudo('reboot', warn_only=True, quiet=True)
