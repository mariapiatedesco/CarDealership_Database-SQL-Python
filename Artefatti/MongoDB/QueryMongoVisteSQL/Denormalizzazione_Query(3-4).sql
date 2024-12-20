create view Query_2 AS
(SELECT v.Id_Veicolo,brand,modello,prezzo_proposto

FROM   veicolo_t v LEFT JOIN veicolo_vendita_t c
ON      v.Id_Veicolo= c.V_Id_Veicolo
UNION
SELECT v.Id_Veicolo,brand,modello,Prezzo_Proposto
     
FROM  veicolo_t v  RIGHT JOIN veicolo_vendita_t c
ON    v.Id_Veicolo= c.V_Id_Veicolo);

create view Query_2_2 AS
(select v.Id_Veicolo,brand,modello,prezzo_proposto,id_vendita,data_consegna
from query_2 v left join vendita_t c
on v.Id_Veicolo=c.V_Id_Veicolo
union
select v.Id_Veicolo,brand,modello,prezzo_proposto,id_vendita,data_consegna
from query_2 v right join vendita_t c
on v.Id_Veicolo=c.V_Id_Veicolo
);

create view Query_2_3 as
(select v.Id_Veicolo,brand,modello,prezzo_proposto,v.id_vendita,data_consegna,v_id_pagamento,(Ammontare_senza_iva+(Ammontare_senza_iva/100*aliquota_iva)) as prezzo_pagato
from query_2_2 v left join pagamento_vendita_t c
on v.Id_vendita=c.id_vendita
union
select v.Id_Veicolo,brand,modello,prezzo_proposto,v.id_vendita,data_consegna,v_id_pagamento,Ammontare_senza_iva+(Ammontare_senza_iva/100*aliquota_iva) as prezzo_pagato
from query_2_2 v right join pagamento_vendita_t c
on v.id_vendita=c.id_vendita
);