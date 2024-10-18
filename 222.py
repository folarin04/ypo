import pexpect
import logging

# Set up logging
logging.basicConfig(filename='network_device_config.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
credentials = {
    "ip": '192.168.56.101',
    "username": 'prne',
    "password": 'cisco123!',
    "enable_password": 'class123!'
}

def configure_device(session, protocol): 
    """Configure the device by setting the hostname."""
    try:
        session.sendline('configure terminal')
        session.expect(r'\(config\)#')
        logging.info('Entered configuration mode')
        
        session.sendline('hostname R1')
        session.expect(r'R1\(config\)#')
        logging.info('Hostname set to R1')
        
        session.sendline('exit')
        session.sendline('exit')
        logging.info('Exited configuration mode and closed session')
    except Exception as e:
        logging.error(f"Error during device configuration: {e}")
        
    session.close()
    print_success(protocol)

def print_success(protocol):
    """Print a success message."""
    print('---------------------------------------------')
    print(f'--- Success! {protocol.upper()} connection established to {credentials["ip"]}')
    print(f'    Username: {credentials["username"]}')
    print('---------------------------------------------')
    logging.info(f'Successfully connected to {credentials["ip"]} using {protocol.upper()}')

def handle_ssh(session):
    """Handle SSH connection."""
    try:
        if session.expect(['Password:', 'continue connecting (yes/no)?', pexpect.TIMEOUT, pexpect.EOF]) == 1:
            session.sendline('yes')
            session.expect('Password:') 
        
        session.sendline(credentials["password"])
        if session.expect(['>', '#', pexpect.TIMEOUT, pexpect.EOF]) == 0:
            session.sendline('enable')
            if session.expect(['Password:', '#', pexpect.TIMEOUT, pexpect.EOF]) == 0:
                session.sendline(credentials["enable_password"])
                session.expect('#')
        
        logging.info('SSH connection successful')
        configure_device(session, 'ssh')  # Passing 'ssh' protocol to configure_device
    except Exception as e:
        logging.error(f"SSH connection failed: {e}")

def handle_telnet(session):
    """Handle Telnet connection."""
    try:
        session.expect('Username:')
        session.sendline(credentials["username"])
        session.expect('Password:')
        session.sendline(credentials["password"])
        
        if session.expect(['>', '#', pexpect.TIMEOUT, pexpect
