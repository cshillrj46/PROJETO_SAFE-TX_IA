from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# 🔄 Importa os modelos do projeto
from backend.database import Base

# ⚙️ Este é o objeto de configuração do Alembic, que fornece
# acesso às variáveis definidas no alembic.ini
config = context.config

# 🎯 Ativa o log configurado no alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 🔑 Define o metadata a partir do Base dos modelos
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Executa migrações no modo 'offline'.

    Não conecta diretamente ao banco, apenas gera o SQL.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa migrações no modo 'online'.

    Conecta ao banco e aplica as mudanças diretamente.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
