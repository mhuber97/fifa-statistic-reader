from configparser import ConfigParser

def save_config():
    #Write configuration data to file
    config = ConfigParser()

    config.read('config.ini')
    config.add_section('main')
    config.set('main', 'driver', 'fill')
    config.set('main', 'username', 'fill')
    config.set('main', 'dbname', 'fill')
    config.set('main', 'password', 'fill')
    config.set('main', 'server', 'fill')
    config.set('main', 'port', 'fill')

    with open('config.ini', 'w') as f:
        config.write(f)

if __name__ == "__main__":
    save_config()