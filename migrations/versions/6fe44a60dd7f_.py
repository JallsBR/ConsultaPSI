"""empty message

Revision ID: 6fe44a60dd7f
Revises: 
Create Date: 2024-09-03 00:59:15.048357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fe44a60dd7f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('status_consulta',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=150), nullable=True),
    sa.Column('sobrenome', sa.String(length=150), nullable=True),
    sa.Column('crp', sa.String(length=20), nullable=True),
    sa.Column('abordagem', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('telefone', sa.String(length=15), nullable=False),
    sa.Column('login', sa.String(length=50), nullable=False),
    sa.Column('senha', sa.String(length=550), nullable=False),
    sa.Column('tipo', sa.String(length=25), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('login'),
    sa.UniqueConstraint('telefone')
    )
    op.create_table('convenio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('convenio', sa.String(length=150), nullable=False),
    sa.Column('valor_consulta', sa.Float(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('convenio')
    )
    op.create_table('paciente',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(length=50), nullable=False),
    sa.Column('sobrenome', sa.String(length=150), nullable=False),
    sa.Column('cpf', sa.String(length=11), nullable=False),
    sa.Column('nascimento', sa.Date(), nullable=False),
    sa.Column('genero', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('ocupacao', sa.String(length=50), nullable=False),
    sa.Column('cep', sa.String(length=8), nullable=False),
    sa.Column('endereco', sa.String(length=150), nullable=False),
    sa.Column('endereco_complemento', sa.String(length=150), nullable=False),
    sa.Column('fone', sa.String(length=15), nullable=False),
    sa.Column('datainicio', sa.Date(), nullable=False),
    sa.Column('convenios_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['convenios_id'], ['convenio.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cpf'),
    sa.UniqueConstraint('email')
    )
    op.create_table('consulta',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('data_marcacao', sa.String(length=50), nullable=False),
    sa.Column('data_consulta', sa.Date(), nullable=False),
    sa.Column('hora_consulta', sa.Time(), nullable=False),
    sa.Column('duracao', sa.String(length=8), nullable=False),
    sa.Column('consulta_status_id', sa.Integer(), nullable=False),
    sa.Column('convenios_id', sa.Integer(), nullable=False),
    sa.Column('id_paciente', sa.Integer(), nullable=False),
    sa.Column('psi_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['consulta_status_id'], ['status_consulta.id'], ),
    sa.ForeignKeyConstraint(['convenios_id'], ['convenio.id'], ),
    sa.ForeignKeyConstraint(['id_paciente'], ['paciente.id'], ),
    sa.ForeignKeyConstraint(['psi_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pacienteconvenio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_convenio', sa.Integer(), nullable=False),
    sa.Column('documento', sa.Text(), nullable=False),
    sa.Column('autoriza_convenio', sa.String(length=25), nullable=False),
    sa.Column('paciente_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_convenio'], ['convenio.id'], ),
    sa.ForeignKeyConstraint(['paciente_id'], ['paciente.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transcricao',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_consulta', sa.Integer(), nullable=False),
    sa.Column('transcricao', sa.String(), nullable=False),
    sa.Column('data_transcricao', sa.String(length=50), nullable=False),
    sa.Column('psi_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_consulta'], ['consulta.id'], ),
    sa.ForeignKeyConstraint(['psi_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('palavras_chave',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_transcricao', sa.Integer(), nullable=False),
    sa.Column('palavra', sa.String(length=30), nullable=True),
    sa.Column('psi_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_transcricao'], ['transcricao.id'], ),
    sa.ForeignKeyConstraint(['psi_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('palavras_chave')
    op.drop_table('transcricao')
    op.drop_table('pacienteconvenio')
    op.drop_table('consulta')
    op.drop_table('paciente')
    op.drop_table('convenio')
    op.drop_table('user')
    op.drop_table('status_consulta')
    # ### end Alembic commands ###
