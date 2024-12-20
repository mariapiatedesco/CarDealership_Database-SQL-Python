# Unica tabella per Veicolo_Noleggio

SELECT Categoria_q,Trasmissione_q, Categoria_D,Trasmissione_d, 
Pacchetto_optional, Numero_Porte, Numero_Passeggeri, N_Id_veicolo,
Prezzo_Giorno,Tipo,Costo_Assicurazione,Costo_Bollo,Tipo
FROM Veicolo_Noleggio_T,
(SELECT D_N_Id_Veicolo,N_quattro_Ruote_T.Categoria 
as Categoria_q, N_quattro_Ruote_T.Trasmissione as Trasmissione_q,
Q_N_Id_Veicolo, N_Due_Ruote_T.Categoria as Categoria_D, 
N_due_Ruote_T.Trasmissione as Trasmissione_d, Pacchetto_optional, 
Numero_Porte, Numero_Passeggeri 
FROM N_Due_Ruote_T RIGHT JOIN N_Quattro_Ruote_T ON D_N_Id_Veicolo=Q_N_Id_Veicolo 
UNION 
SELECT D_N_Id_Veicolo, N_quattro_Ruote_T.Categoria as Catgoria_q,
N_quattro_Ruote_T.Trasmissione as Trasmissione_q, Q_N_Id_Veicolo, 
N_Due_Ruote_T.Categoria as Categoria_D, N_due_Ruote_T.Trasmissione as Trasmissione_d, 
Pacchetto_optional, Numero_Porte, Numero_Passeggeri   
FROM N_Due_Ruote_T LEFT JOIN N_Quattro_Ruote_T 
ON D_N_Id_Veicolo=Q_N_Id_Veicolo) AS D_Q_Ruote
WHERE (Veicolo_Noleggio_T.N_Id_Veicolo=D_Q_Ruote.D_N_Id_Veicolo) OR 
(Veicolo_Noleggio_T.N_Id_Veicolo=D_Q_Ruote.Q_N_Id_Veicolo);


# Unica tabella per Veicolo_Vendita

SELECT Categoria_q, Trasmissione_q, Categoria_D, Trasmissione_d, 
Pacchetto_optional, Numero_Porte, Numero_Passeggeri, V_Id_veicolo,
Chilometri, Prezzo_proposto, Tipo,Disponibile
FROM Veicolo_Vendita_T, 
(SELECT D_V_Id_Veicolo, V_quattro_Ruote_T.Categoria as Categoria_q,
V_quattro_Ruote_T.Trasmissione as Trasmissione_q,
Q_V_Id_Veicolo,V_Due_Ruote_T.Categoria as Categoria_D, 
V_due_Ruote_T.Trasmissione as Trasmissione_d, 
Pacchetto_optional, Numero_Porte, Numero_Passeggeri 
FROM V_Due_Ruote_T RIGHT JOIN V_Quattro_Ruote_T 
ON D_V_Id_Veicolo=Q_V_Id_Veicolo 
UNION 
SELECT D_V_Id_Veicolo, V_quattro_Ruote_T.Categoria as Categoria_q,
V_quattro_Ruote_T.Trasmissione as Trasmissione_q, 
Q_V_Id_Veicolo,V_Due_Ruote_T.Categoria as Categoria_D,
V_due_Ruote_T.Trasmissione as Trasmissione_d, Pacchetto_optional, 
Numero_Porte, Numero_Passeggeri   
FROM V_Due_Ruote_T 
LEFT JOIN V_Quattro_Ruote_T 
ON D_V_Id_Veicolo=Q_V_Id_Veicolo) AS D_Q_Ruote
WHERE (Veicolo_Vendita_T.V_Id_Veicolo=D_Q_Ruote.D_V_Id_Veicolo) OR 
(Veicolo_Vendita_T.V_Id_Veicolo=D_Q_Ruote.Q_V_Id_Veicolo);


# Unica tabella per Pagamento

SELECT Id_Pagamento, Data_Pagamento, Vendita, Ammontare_Senza_Iva, 
Aliquota_iva, Metodo_Pagamento, Id_Vendita, Id_Noleggio, 
Ammontare as Ammontare_Noleggio
FROM Pagamento_T, 
(SELECT * 
FROM Pagamento_Vendita_T 
RIGHT JOIN Pagamento_Noleggio_T 
ON Pagamento_Noleggio_T.N_Id_Pagamento=Pagamento_Vendita_T.V_Id_Pagamento
UNION
SELECT * 
FROM Pagamento_Vendita_T 
LEFT JOIN Pagamento_Noleggio_T 
ON Pagamento_Noleggio_T.N_Id_Pagamento=Pagamento_Vendita_T.V_Id_Pagamento) 
AS V_N_Pagamento
WHERE (Pagamento_T.Id_Pagamento=V_N_Pagamento.V_Id_Pagamento) OR 
(Pagamento_T.Id_Pagamento=V_N_Pagamento.N_Id_Pagamento);


# Unica tabella per Cliente

Select Codice_Fiscale, Nome, Cognome, Via, Numero_Civico, CAP, Provincia, 
Data_Nascita, Email, Telefono,Vendita, Noleggio,abituale
FROM   Cliente_T 
LEFT JOIN 
(SELECT * FROM Cliente_Vendita_T 
RIGHT JOIN Cliente_Noleggio_T 
ON V_Codice_Fiscale=N_Codice_Fiscale
UNION 
SELECT * FROM Cliente_Vendita_T 
LEFT JOIN Cliente_Noleggio_T 
ON V_Codice_Fiscale=N_Codice_Fiscale) AS V_N_Cliente 
ON (Cliente_T.Codice_Fiscale=V_N_Cliente.V_Codice_Fiscale) OR 
(Cliente_T.Codice_Fiscale=V_N_Cliente.N_Codice_Fiscale); 


# VERTICAL PARTITIONING

select Codice_Fiscale,Telefono,Email FROM Cliente_T;
select Codice_Fiscale,Nome,Cognome,Numero_Civico,CAP,Provincia,Vendita,Noleggio FROM Cliente_t;


# INDICIZZAZIONE

CREATE INDEX V_ORD_CON_IDX ON Veicolo_T(Id_Concessionaria);

CREATE INDEX MOD_IDX ON Veicolo_T(Modello);
CREATE INDEX BRAND_IDX ON Veicolo_T(Brand);

CREATE INDEX PROM_IDX ON Promozione_T(Brand);


# LOOKUP TABLES

CREATE ViEW  Cat AS
select DISTINCT Categoria
FROM V_Quattro_Ruote_T;

UPDATE v_quattro_ruote_t
SET Categoria="A"
WHERE Categoria="Sportiva";

UPDATE v_quattro_ruote_t
SET Categoria="B"
WHERE Categoria="Utilitaria";

UPDATE v_quattro_ruote_t
SET Categoria="C"
WHERE Categoria="Suv";

UPDATE v_quattro_ruote_t
SET Categoria="D"
WHERE Categoria="Berlina";

select distinct V_Quattro_Ruote_T.CAtegoria, Cat.Categoria
FROM V_quattro_Ruote_T,CAT;