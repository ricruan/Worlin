import uvicorn
from server import app, AppConfig  # noqa: F401
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--env', default='dev')
    parser.add_argument('--reload', action='store_true', help='启用热加载')
    args = parser.parse_args()

    uvicorn.run(
        app='app:app',
        host=AppConfig.app_host,
        port=AppConfig.app_port,
        # root_path=AppConfig.app_root_path,
        reload=args.reload or AppConfig.app_reload,
    )
