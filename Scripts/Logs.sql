create table if not exists Registros(
log_acao varchar(50) not null,
log_login varchar(50) not null,
log_senha varchar(200) not null,
log_email varchar(200) not null,
log_hora_Registro timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);
# Triggers para qualquer mudança na Tabela de usuario
create trigger tr_log_Insercao after insert on Usuario for each row
insert into Registros (log_acao,log_login,log_senha,log_email) values ('Criação de Usuário',New.login,New.senha,New.email);

create trigger tr_log_Update after Update on Usuario for each row
insert into Registros (log_acao,log_login,log_senha,log_email) values ('Atualização de Usuário',New.login,New.senha,New.email);

create trigger tr_log_Delete after Delete on Usuario for each row
insert into Registros (log_acao,log_login,log_senha,log_email) values ('Remoção de Usuário',old.login,old.senha,old.email);



