import os
import config


def init_database():
    # Create .gdc/ directory if it does not exist
    if not os.path.isdir(config.DB_DIR):
        os.mkdir(config.DB_DIR)

    # Check if minions.yaml exists
    if not os.path.isfile(config.MINIONS_FILE):
        raise Exception('Create `.gdc/minions.yaml` with `Cluster label: salt_master_ip` pairs!')

    # Create database file if does not exist:
    if not os.path.isfile(config.DB_FILE):
        open(config.DB_FILE, 'w').close()


if __name__ == '__main__':
    init_database()

