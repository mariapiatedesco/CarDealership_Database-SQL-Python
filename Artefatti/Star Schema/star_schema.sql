create view veicolo_dt_V as
select id_veicolo, carburante, brand, vendita, tipo, categoria, trasmissione, id_concessionaria, prezzo_acquisto as costo
from veicolo_t, veicolo_vendita_t, v_due_ruote_t 
where id_veicolo = v_id_veicolo and
v_id_veicolo = d_v_id_veicolo 
union
(select id_veicolo, carburante, brand, vendita, tipo, categoria, trasmissione, id_concessionaria, prezzo_acquisto as costo
from veicolo_t, veicolo_vendita_t, v_quattro_ruote_t 
where id_veicolo = v_id_veicolo and
v_id_veicolo = q_v_id_veicolo);

#create view fact_table_V as 
select vendita, vendita_t.id_vendita, vendita_t.id_dipendente, vendita_t.data_ordine, 
veicolo_dt_v.id_veicolo, brand, tipo, categoria, carburante, trasmissione,
concessionaria_t.id_concessionaria, nazionalità, numero_dipendenti, 
cliente_t.codice_fiscale, data_nascita, provincia,
 
round((ammontare_senza_iva+ammontare_senza_iva*aliquota_iva/100),0) as ricavo, 
round(costo,0)

from cliente_t, vendita_t, veicolo_dt_v, concessionaria_t, pagamento_vendita_t 

where cliente_t.codice_fiscale = vendita_t.v_codice_fiscale and 
vendita_t.v_id_veicolo = veicolo_dt_v.id_veicolo and 
vendita_t.id_vendita = pagamento_vendita_t.id_vendita and
veicolo_dt_v.id_concessionaria = concessionaria_t.id_concessionaria; 




create view veicolo_dt_N as
select id_veicolo, carburante, brand, veicolo_t.vendita, tipo, categoria, trasmissione, id_concessionaria, 
round(((prezzo_acquisto+costo_assicurazione+costo_bollo)/(select count(*) from noleggio_t where n_id_veicolo = id_veicolo)),0) as costo
from veicolo_t, veicolo_noleggio_t, n_due_ruote_t 
where id_veicolo = n_id_veicolo and
n_id_veicolo = d_n_id_veicolo
union
(select id_veicolo, carburante, brand, veicolo_t.vendita, tipo, categoria, trasmissione, id_concessionaria, 
round(((prezzo_acquisto+costo_assicurazione+costo_bollo)/(select count(*) from noleggio_t where n_id_veicolo = id_veicolo)),0) as costo
from veicolo_t, veicolo_noleggio_t, n_quattro_ruote_t 
where id_veicolo = n_id_veicolo and
n_id_veicolo = q_n_id_veicolo);

#create view fact_table_N as
select vendita, noleggio_t.id_noleggio, noleggio_t.id_dipendente, noleggio_t.data_ordine, 
veicolo_dt_n.id_veicolo, brand, tipo, categoria, carburante, trasmissione,
concessionaria_t.id_concessionaria, nazionalità, numero_dipendenti, 
cliente_t.codice_fiscale, data_nascita, provincia,
 
round(ammontare,0) as ricavo, 
round(costo,0) as costo 

from cliente_t, noleggio_t, veicolo_dt_n, concessionaria_t, pagamento_noleggio_t 

where cliente_t.codice_fiscale = noleggio_t.n_codice_fiscale and 
noleggio_t.n_id_veicolo = veicolo_dt_n.id_veicolo and 
noleggio_t.id_noleggio = pagamento_noleggio_t.id_noleggio and
veicolo_dt_n.id_concessionaria = concessionaria_t.id_concessionaria; 




# FACT TABLE 

create view fact_table as 
select veicolo_dt_v.vendita, vendita_t.id_vendita as id_ordine, vendita_t.id_dipendente, vendita_t.data_ordine, 
veicolo_dt_v.id_veicolo, brand, tipo, categoria, carburante, trasmissione,
concessionaria_t.id_concessionaria, nazionalità, numero_dipendenti, 
cliente_t.codice_fiscale, data_nascita, provincia,
 
round((ammontare_senza_iva+ammontare_senza_iva*aliquota_iva/100),0) as ricavo, 
round(costo,0) as costo, 
round((ammontare_senza_iva+(ammontare_senza_iva*aliquota_iva/100)-costo),0) as profitto

from cliente_t, vendita_t, veicolo_dt_v, concessionaria_t, pagamento_vendita_t 

where cliente_t.codice_fiscale = vendita_t.v_codice_fiscale and 
vendita_t.v_id_veicolo = veicolo_dt_v.id_veicolo and 
vendita_t.id_vendita = pagamento_vendita_t.id_vendita and
veicolo_dt_v.id_concessionaria = concessionaria_t.id_concessionaria

union 

( select veicolo_dt_n.vendita, noleggio_t.id_noleggio as id_ordine, noleggio_t.id_dipendente, noleggio_t.data_ordine, 
veicolo_dt_n.id_veicolo, brand, tipo, categoria, carburante, trasmissione,
concessionaria_t.id_concessionaria, nazionalità, numero_dipendenti, 
cliente_t.codice_fiscale, data_nascita, provincia,
 
round(ammontare,0) as ricavo, 
round(costo,0) as costo,
round((ammontare-costo),0) as profitto

from cliente_t, noleggio_t, veicolo_dt_n, concessionaria_t, pagamento_noleggio_t 

where cliente_t.codice_fiscale = noleggio_t.n_codice_fiscale and 
noleggio_t.n_id_veicolo = veicolo_dt_n.id_veicolo and 
noleggio_t.id_noleggio = pagamento_noleggio_t.id_noleggio and
veicolo_dt_n.id_concessionaria = concessionaria_t.id_concessionaria ); 

