from app import app
from  flask_migrate import Migrate, MigrateCommand

if  __name__ == '__main__':
  app.manage(debug=True)

