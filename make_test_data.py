from votemap.app import create_app
from votemap.model import clear_collections
from votemap.sample_data import make_sample_data

if __name__ == "__main__":
    app = create_app()
    clear_collections()
    make_sample_data()
