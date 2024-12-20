CREATE SCHEMA IF NOT EXISTS Car_Dealership;

USE Car_Dealership;

CREATE TABLE IF NOT EXISTS Concessionaria_T (
Id_Concessionaria INT AUTO_INCREMENT NOT NULL,
Nazionalità CHAR(2) NOT NULL,
Città VARCHAR(50) NOT NULL,
Numero_Dipendenti TINYINT(2) NOT NULL,
Numero_Telefono CHAR(10) NOT NULL,
CONSTRAINT Concessionaria_PK PRIMARY KEY(Id_Concessionaria));


CREATE TABLE IF NOT EXISTS Veicolo_T (
Id_Veicolo CHAR(17) NOT NULL,
Anno YEAR NOT NULL,
Data_Acquisto DATE NOT NULL,
Carburante VARCHAR(10) NOT NULL,
Brand VARCHAR(20) NOT NULL,
Modello VARCHAR(50) NOT NULL,
Colore VARCHAR(10) NOT NULL, 
Cavalli SMALLINT(4) NOT NULL,
Cilindrata SMALLINT(4) NOT NULL,
Prezzo_Listino DECIMAL(9,2) NOT NULL,
Vendita BOOLEAN NOT NULL,
Prezzo_Acquisto DECIMAL(9,2) NOT NULL,
Foto VARCHAR(200) NOT NULL,
Id_Concessionaria INT NOT NULL,
CONSTRAINT Veicolo_T_PK PRIMARY KEY (Id_Veicolo),
CONSTRAINT Id_Concessionaria_FK FOREIGN KEY (Id_Concessionaria) 
	REFERENCES Concessionaria_T(Id_Concessionaria));
    

CREATE TABLE IF NOT EXISTS Veicolo_Vendita_T (
V_Id_Veicolo CHAR(17) NOT NULL,
Chilometri NUMERIC(8,2),
Prezzo_Proposto DECIMAL(9,2) NOT NULL,
Tipo BOOLEAN NOT NULL,
Disponibile BOOLEAN NOT NULL,
CONSTRAINT Veicolo_Vendita_T_PK PRIMARY KEY (V_Id_Veicolo),
CONSTRAINT V_Id_Veicolo_FK FOREIGN KEY (V_Id_Veicolo) 
	REFERENCES Veicolo_T(Id_Veicolo));


CREATE TABLE IF NOT EXISTS V_Due_Ruote_T( 
D_V_Id_Veicolo CHAR(17) NOT NULL,
Trasmissione VARCHAR(20) NOT NULL,
Categoria VARCHAR(20) NOT NULL,
CONSTRAINT V_Due_Ruote_T_PK PRIMARY KEY (D_V_Id_Veicolo),
CONSTRAINT D_V_Id_Veicolo_FK FOREIGN KEY (D_V_Id_Veicolo) 
	REFERENCES Veicolo_Vendita_T(V_Id_Veicolo));
    

CREATE TABLE IF NOT EXISTS V_Quattro_Ruote_T(
Q_V_Id_Veicolo CHAR(17) NOT NULL,
Numero_Porte SMALLINT(2) NOT NULL,
Numero_Passeggeri SMALLINT(2) NOT NULL,
Pacchetto_Optional VARCHAR(20) NOT NULL,
Trasmissione VARCHAR(20) NOT NULL,
Categoria VARCHAR(20) NOT NULL,
CONSTRAINT V_Quattro_Ruote_T_PK PRIMARY KEY (Q_V_Id_Veicolo),
CONSTRAINT Q_V_Id_Veicolo_FK FOREIGN KEY (Q_V_Id_Veicolo) 
	REFERENCES Veicolo_Vendita_T(V_Id_Veicolo));
    

Create Table IF NOT EXISTS Veicolo_Noleggio_T(
N_Id_Veicolo CHAR(17) NOT NULL,
Prezzo_Giorno Decimal(9,2) NOT NULL,
Tipo VARCHAR(50) NOT NULL,
Costo_Assicurazione Decimal(6,2) NOT NULL,
Costo_Bollo Decimal(6,2) NOT NULL,
CONSTRAINT Veicolo_Noleggio_T_PK PRIMARY KEY(N_Id_Veicolo),
CONSTRAINT N_Id_Veicolo_FK FOREIGN KEY(N_Id_Veicolo) 
	REFERENCES Veicolo_T(Id_Veicolo));
    

CREATE TABLE IF NOT EXISTS N_Quattro_Ruote_T( 
Q_N_Id_Veicolo CHAR(17) NOT  NULL,
Categoria VARCHAR(50) NOT NULL,
Trasmissione VARCHAR(20) NOT NULL,
Pacchetto_Optional VARCHAR(30) NOT NULL,
Numero_Porte TINYINT(1) NOT NULL,
Numero_Passeggeri TINYINT(1) NOT NULL,
CONSTRAINT N_Quattro_Ruote_PK PRIMARY KEY(Q_N_Id_Veicolo),
CONSTRAINT Q_N_Id_Veicolo_FK FOREIGN KEY(Q_N_Id_Veicolo) 
	REFERENCES Veicolo_Noleggio_T(N_Id_Veicolo));
    

CREATE TABLE IF NOT EXISTS N_Due_Ruote_T(
D_N_Id_Veicolo CHAR(17) NOT NULL,
Categoria VARCHAR(30) NOT NULL,
Trasmissione VARCHAR(30) NOT NULL,
CONSTRAINT N_Due_Ruote_PK PRIMARY KEY(D_N_Id_Veicolo),
CONSTRAINT D_N_Id_Veicolo_FK FOREIGN KEY(D_N_Id_Veicolo) 
	REFERENCES Veicolo_Noleggio_T(N_Id_Veicolo));


CREATE TABLE IF NOT EXISTS Promozione_T(
Id_Promozione INT(10) AUTO_INCREMENT NOT NULL,
Data_Inizio DATE NOT NULL,
Data_Fine DATE NOT NULL, 
Brand VARCHAR(50) NOT NULL,
Percentuale_Sconto TINYINT(2) NOT NULL,
Modello VARCHAR(50),
CONSTRAINT Promozione_T_PK PRIMARY KEY(Id_Promozione));


CREATE TABLE IF NOT EXISTS Veicolo_Promozione_T(
Id_Promozione INT(10) NOT NULL,
V_Id_Veicolo CHAR(17) NOT NULL,
CONSTRAINT Veicolo_Promozione_T_PK PRIMARY KEY (Id_Promozione,V_Id_Veicolo),
CONSTRAINT Id_Promozione_FK FOREIGN KEY(Id_Promozione) 
	REFERENCES Promozione_T(Id_Promozione),
CONSTRAINT V_Id_Veicolo_FK2 FOREIGN KEY(V_Id_Veicolo) 
	REFERENCES Veicolo_Vendita_T(V_Id_Veicolo));
    

CREATE TABLE IF NOT EXISTS Cliente_T (
Codice_Fiscale CHAR(16) NOT NULL,
Nome VARCHAR(30) NOT NULL,
Cognome VARCHAR(30) NOT NULL,
Via VARCHAR(50) NOT NULL,
Numero_Civico SMALLINT NOT NULL,
CAP CHAR(5) NOT NULL,
Provincia CHAR(2) NOT NULL, # oppure varchar
Data_Nascita DATE NOT NULL,
Email VARCHAR(60) NOT NULL,
Telefono VARCHAR(25) NOT NULL,
Vendita BOOLEAN NOT NULL,
Noleggio BOOLEAN NOT NULL,
CONSTRAINT Cliente_T_PK PRIMARY KEY (Codice_Fiscale));


CREATE TABLE  IF NOT  EXISTS Cliente_Vendita_T(
V_Codice_Fiscale CHAR(16) NOT NULL,
Abituale BOOLEAN NOT NULL,
CONSTRAINT Cliente_Vendita_T_PK PRIMARY KEY(V_Codice_Fiscale),
CONSTRAINT V_Codice_Fiscale_FK FOREIGN KEY(V_Codice_Fiscale) 
	REFERENCES Cliente_T(Codice_Fiscale));
    

CREATE TABLE IF NOT EXISTS Cliente_Noleggio_T(
N_Codice_Fiscale CHAR(16) NOT NULL,
CONSTRAINT Cliente_Noleggio_T_PK PRIMARY KEY(N_Codice_Fiscale),
CONSTRAINT N_Codice_Fiscale_FK FOREIGN KEY(N_Codice_Fiscale) 
	REFERENCES Cliente_T(Codice_Fiscale));
    

CREATE TABLE IF NOT EXISTS Dipendente_T(
Id_Dipendente INT(10) AUTO_INCREMENT NOT NULL,
Nome Varchar(50) NOT NULL,
Cognome VARCHAR(50) NOT NULL,
Salario DECIMAL(8,2) NOT NULL,
Vendite SMALLINT(3) NOT NULL,
Tasso_Commissione SMALLINT(2) NOT NULL,
Email VARCHAR(100) NOT NULL,
Telefono VARCHAR(25) NOT NULL,
Id_Concessionaria INT(10) NOT NULL,
CONSTRAINT Dipendente_T_PK PRIMARY KEY (Id_Dipendente),
CONSTRAINT Id_Concessionaria_FK2 FOREIGN KEY (Id_Concessionaria) 
	REFERENCES Concessionaria_T(Id_Concessionaria));  
    

CREATE TABLE IF NOT EXISTS Vendita_T(
Id_Vendita INT(10) AUTO_INCREMENT NOT NULL,
Data_Consegna DATE NOT NULL,
Data_Ordine DATE NOT NULL,
V_Id_Veicolo CHAR(17) NOT NULL,
Id_Dipendente INT NOT NULL,
V_Codice_Fiscale CHAR(16) NOT NULL,
CONSTRAINT Vendita_T_PK PRIMARY KEY(Id_Vendita),
CONSTRAINT V_Id_Veicolo2_FK FOREIGN KEY(V_Id_Veicolo) 
	REFERENCES Veicolo_Vendita_T(V_Id_Veicolo), 
CONSTRAINT Id_Dipendente_FK FOREIGN KEY(Id_Dipendente) 
	REFERENCES Dipendente_T(Id_Dipendente),
CONSTRAINT V_Codice_Fiscale_FK2 FOREIGN KEY(V_Codice_Fiscale) 
	REFERENCES Cliente_Vendita_T(V_Codice_Fiscale));  


CREATE TABLE IF NOT EXISTS Noleggio_T(
Id_Noleggio INT(10) AUTO_INCREMENT NOT NULL,
Data_Consegna DATE NOT NULL,
Data_Ordine DATE NOT NULL,
Numero_Giorni SMALLINT(3) NOT NULL,
Luogo_Restituzione VARCHAR(50) NOT NULL,
Id_Dipendente INT(17) NOT NULL,
N_Id_Veicolo CHAR(17) NOT NULL,
N_Codice_Fiscale CHAR(16) NOT NULL,
CONSTRAINT Noleggio_T_PK PRIMARY KEY(Id_Noleggio),
CONSTRAINT Id_Dipendente_FK2 FOREIGN KEY(Id_Dipendente) 
	REFERENCES Dipendente_T(Id_Dipendente),  
CONSTRAINT N_Id_Veicolo_FK2 FOREIGN KEY(N_Id_Veicolo) 
	REFERENCES Veicolo_Noleggio_T(N_Id_Veicolo),  
CONSTRAINT N_Codice_Fiscale_FK2 FOREIGN KEY(N_Codice_Fiscale) 
	REFERENCES Cliente_Noleggio_T(N_Codice_Fiscale));


CREATE TABLE IF NOT EXISTS Abituale_T (
A_V_Codice_Fiscale CHAR(16) NOT NULL,
Budget DECIMAL(9,2) NOT NULL,
CONSTRAINT Abituale_T_PK PRIMARY KEY (A_V_Codice_Fiscale),
CONSTRAINT A_V_Codice_Fiscale_FK FOREIGN KEY (A_V_Codice_Fiscale) 
	REFERENCES Cliente_Vendita_T(V_Codice_Fiscale));
    

CREATE TABLE IF NOT EXISTS Abituale_Categoria_T (
C_A_Codice_Fiscale CHAR(16) NOT NULL,
Categoria VARCHAR(20) NOT NULL,
CONSTRAINT Abituale_Categoria_T_PK PRIMARY KEY (C_A_Codice_Fiscale,Categoria),
CONSTRAINT C_A_Codice_Fiscale_FK FOREIGN KEY (C_A_Codice_Fiscale) 
	REFERENCES Abituale_T(A_V_Codice_Fiscale));
    

CREATE TABLE IF NOT EXISTS Abituale_Brand_Preferito_T (
B_A_Codice_Fiscale CHAR(16) NOT NULL,
Brand_Preferito VARCHAR(50) NOT NULL,
CONSTRAINT Abituale_Brand_Preferito_T_PK PRIMARY KEY (B_A_Codice_Fiscale, Brand_Preferito),
CONSTRAINT B_A_Codice_Fiscale_FK FOREIGN KEY (B_A_Codice_Fiscale) 
	REFERENCES Abituale_T(A_V_Codice_Fiscale));
    

CREATE TABLE IF NOT EXISTS Abituale_Promozione_T(
Id_Promozione INT (10) NOT NULL,
A_V_Codice_Fiscale CHAR(16) NOT NULL,
CONSTRAINT Abituale_Promozione_T_PK PRIMARY KEY (Id_Promozione,A_V_Codice_Fiscale),
CONSTRAINT Id_Promozione2_FK FOREIGN KEY(Id_Promozione) 
	REFERENCES Promozione_T(Id_Promozione),
CONSTRAINT A_V_Codice_Fiscale_FK2 FOREIGN KEY(A_V_Codice_Fiscale) 
	REFERENCES Abituale_T(A_V_Codice_Fiscale));


CREATE TABLE IF NOT EXISTS Pagamento_T( 
Id_Pagamento INT(10) AUTO_INCREMENT NOT NULL,
Data_Pagamento DATE NOT NULL,
Vendita BOOLEAN NOT NULL,    
CONSTRAINT Pagamento_T_PK PRIMARY KEY (Id_Pagamento));


CREATE TABLE IF NOT EXISTS Pagamento_Vendita_T(
V_Id_Pagamento INT(10)  NOT NULL,
Ammontare_Senza_IVA DECIMAL(9,2) NOT NULL,
Aliquota_IVA SMALLINT(2) NOT NULL,
Metodo_Pagamento VARCHAR(50) NOT NULL,
Id_Vendita INT(10) NOT NULL,
CONSTRAINT Pagamento_Vendita_T_PK PRIMARY KEY (V_Id_Pagamento),
CONSTRAINT Id_Vendita3_FK FOREIGN KEY(Id_Vendita) 
	REFERENCES Vendita_T(Id_Vendita),
CONSTRAINT V_Id_Pagamento_FK FOREIGN KEY(V_Id_Pagamento) 
	REFERENCES Pagamento_T(Id_Pagamento));
    

CREATE TABLE IF NOT EXISTS Pagamento_Noleggio_T(
N_Id_Pagamento INT(10)  NOT NULL,
Id_Noleggio INT(10) NOT NULL,
Ammontare DECIMAL(10,2) NOT NULL,
CONSTRAINT Pagamento_Noleggio_T_PK PRIMARY KEY (N_Id_Pagamento),
CONSTRAINT Id_Noleggio4_FK FOREIGN KEY(Id_Noleggio) 
	REFERENCES Noleggio_T(Id_Noleggio),
CONSTRAINT N_Id_Noleggio_FK FOREIGN KEY(N_Id_Pagamento) 
	REFERENCES Pagamento_T(Id_Pagamento));
    

create table if not exists Recensione_T (
Id_Recensione int auto_increment not null, 
Data_Recensione date not null, 
Dipendente varchar(50) not null, 
Veicoli varchar(50) not null,
Codice_Fiscale char(16) not null, 
Id_Dipendente int(10) not null,
constraint Recensione_PK primary key (Id_Recensione), 
constraint Codice_Fiscale_FK foreign key(Codice_Fiscale) 
	references Cliente_T(Codice_Fiscale), 
constraint Id_Dipendente_FK3 foreign key(Id_Dipendente) 
	references Dipendente_T(Id_Dipendente));
    

alter table Promozione_T auto_increment = 150000;
alter table Dipendente_T auto_increment = 2000000;
alter table Vendita_T auto_increment = 800000;
alter table Noleggio_T auto_increment = 900000;
alter table Pagamento_T auto_increment = 700000;
alter table Recensione_T auto_increment = 600000;


