create view cte AS
(SELECT c.id_concessionaria ,v.Id_Veicolo
,       modello
,      brand
,      c.nazionalità
,      c.città

FROM   concessionaria_t c LEFT JOIN veicolo_t v
ON     c.Id_Concessionaria = v.Id_Concessionaria
UNION
SELECT c.id_concessionaria, v.Id_Veicolo  
,     modello
,      brand 
,      c.nazionalità
,      c.città
     
FROM   veicolo_t v RIGHT JOIN concessionaria_t c
ON     v.Id_Concessionaria = c.Id_Concessionaria);

   
   
create view n_2 as
(SELECT c.id_concessionaria ,c.Id_Veicolo
,       modello
,      brand
,      c.nazionalità
,      c.città
,      n_id_veicolo

FROM   cte c LEFT JOIN veicolo_noleggio_t v
ON     c.Id_Veicolo = v.n_id_veicolo
UNION
SELECT c.id_concessionaria, c.Id_Veicolo  
,     modello
,      brand 
,      c.nazionalità
,      c.città
,      n_id_veicolo
FROM   cte c RIGHT JOIN veicolo_noleggio_t v
ON     c.Id_Veicolo = v.n_id_veicolo);

create view n_10 as
(SELECT c.id_concessionaria ,c.Id_Veicolo
,       modello
,      brand
,      c.nazionalità
,      c.città
,      v.n_id_veicolo

FROM   n_2 c LEFT JOIN noleggio_t v
ON     c.Id_Veicolo = v.n_id_veicolo
UNION
SELECT c.id_concessionaria, c.Id_Veicolo  
,      modello
,      brand 
,      c.nazionalità
,      c.città
,      v.n_id_veicolo

FROM   n_2 c RIGHT JOIN noleggio_t v
ON     c.n_Id_Veicolo = v.n_id_veicolo)