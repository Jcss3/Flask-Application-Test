# Tabela Usuário;
create table if not exists Usuario(
id int(11) auto_increment primary key,
login varchar(50) not null,
senha varchar(200) not null,
email varchar(200) not null,
hora_Registro timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);














