from flask import Flask, request, render_template,session
import random
from datetime import timedelta, date
from markupsafe import escape

import mysql.connector
from mysql.connector import Error
app = Flask(__name__)
app.secret_key = 'SOME-RANDOM-KEY-HERE'

db = mysql.connector.connect(host='localhost',
                                         database='Car_dealership',
                                         user='root',
                                         password='62662Tm!',
                                         port=3306)

cursor = db.cursor(buffered=True)


@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/Query_1",methods=['GET'])
def Query_1():
    cursor.execute("select id_dipendente from dipendente_t")
    results = cursor.fetchall()
    dipendente = int(random.choice(list(results))[0])
    session['Dipendente']=dipendente
    return render_template("query_1.html")

@app.route("/solQuery1" ,methods=['GET'])
def SolQuery_1():
    args = request.args
    Nome=args.get("Nome")
    Cognome=args.get("Cognome")
    CF = args.get("CF")
    args = request.args
    Scelta = args.get("Scelta")
    Scelta = Scelta.capitalize()
    Tipo = args.get("Tipo")
    if Tipo == "2":
        Tipo = 1
    elif Tipo == "4":
        Tipo = 0

    session['CF'] = CF
    session['Nome']=Nome
    session['Cognome']=Cognome
    session['Abituale']=False
    session['Cl_vend']=[]
    session['Scelta'] = Scelta
    session['Tipo'] = Tipo
    query1 = f"select Codice_Fiscale,Nome,Cognome \
     from cliente_t \
     where Codice_Fiscale= '{CF}'"
    cursor.execute(query1)
    cliente = cursor.fetchall()
    session['Cliente']=cliente
    l=len(cliente)
    return render_template("solquery1.html",cliente=cliente,l=l,Tipo=Tipo)





@app.route("/SolQuery_2" ,methods=['POST','GET'])
def SolQuery_2():
    if request.method== 'POST':
        via=request.form.get('via',False)
        numero_civico=request.form.get('numero_civico',False)
        cap=request.form.get('cap',False)
        provincia=request.form.get('provincia',False)
        data_nascita=request.form.get('data_nascita',False)
        email=request.form.get('email',False)
        telefono=request.form.get('telefono',False)
        query2=f"insert into Cliente_T (codice_Fiscale, Nome, Cognome, Via, Numero_Civico, CAP, Provincia, Data_Nascita, Email, Telefono, Vendita, Noleggio) \
        values ('{session['CF']}', '{session['Nome']}', '{session['Cognome']}', '{via}', {numero_civico}, '{cap}', '{provincia}', '{data_nascita}', '{email}', '{telefono}', false, false)"
        cursor.execute(query2)
        db.commit()
        return render_template("SolQuery_2.html",CF=session['CF'],nome=session['Nome'],cognome=session['Cognome'])



@app.route("/SolQuery_3",methods=['GET','POST'])
def SolQuery_3():
    query_extra_auguri = f"select email, telefono \
        from Cliente_T \
        where day(Data_Nascita) = day(current_date()) \
        and month(Data_Nascita) = month(current_date()) \
        and Codice_Fiscale = '{session['CF']}'"
    cursor.execute(query_extra_auguri)
    compl = cursor.fetchall()
    l=len(compl)
    return render_template("SolQuery_3.html",compl=compl,l=l,Scelta=session['Scelta'])

@app.route("/Query_4",methods=['GET'])
def Query_4():
    return render_template("Query_4.html")

@app.route("/SolQuery_4", methods=['POST','GET'])
def SolQuery_4():
    if request.method== 'POST':
        brand=request.form.get('brand',False)
        modello=request.form.get('modello',False)
    session['Brand']=brand
    session['Modello']=modello
    if len(session['Cliente'])!=0:
        query2_2 = f"select * \
                    from cliente_vendita_t \
                    where v_codice_fiscale='{session['CF']}'"
        cursor.execute(query2_2)
        session['Cl_vend'] = cursor.fetchall()
    ris4=None

    if len(session['Cl_vend']) != 0:
        query3 = f"select a_v_codice_fiscale \
                from abituale_t \
                where a_v_codice_fiscale = '{session['CF']}'"
        cursor.execute(query3)
        ris4=cursor.fetchall()
        session['Ris4']=ris4
        if (ris4)!= None:
            session['Abituale']=True

    query4 = f"select id_veicolo \
            from veicolo_t, veicolo_vendita_t \
            where Veicolo_T.Id_Veicolo = Veicolo_Vendita_T.V_Id_Veicolo and \
            disponibile = true \
            and modello = '{modello}' \
            and brand = '{brand}' \
            and tipo = {session['Tipo']} \
            and disponibile = True"
    cursor.execute(query4)
    veicoli = cursor.fetchall()
    session['Veicoli']=veicoli
    veicoli_disponibili=[]
    l=0
    if len(veicoli) != 0:
        query5 = f"select id_veicolo, prezzo_proposto, colore, anno, chilometri, cavalli, cilindrata, foto \
                from veicolo_t, veicolo_vendita_t \
                where Id_Veicolo = V_Id_Veicolo and \
                disponibile = true \
                and modello = '{modello}' \
                and brand = '{brand}' \
                and veicolo_vendita_t.tipo = {session['Tipo']}"
        cursor.execute(query5)
        veicoli_disponibili = cursor.fetchall()
        l=len(veicoli_disponibili)
    session['Veicoli_disponibili'] = veicoli_disponibili
    var=["Concludi","Scegli altra Categoria"]
    var_2=["Home","None"]
    session['var_2']=var_2
    session['Var']=var



    return render_template("SolQuery_4.html",ris4=ris4,veicoli_disponibili=veicoli_disponibili,l=l,var=var,var_2=var_2)

@app.route("/Query_5",methods=['GET'])
def Query_5():
    args = request.args
    scelta_2 = args.get("html")

    session['Scelta_2']=scelta_2
    percentuale_sconto = [0]
    if scelta_2 not in session['var_2']:


        if session['Abituale'] == True:
            query6 = f"select percentuale_sconto \
                                from promozione_T \
                                where brand='{session['Brand']}' and \
                                modello='{session['Modello']}' and \
                                current_date() between data_inizio and data_fine \
                                limit 1"
            cursor.execute(query6)
            percentuale_sconto = cursor.fetchall()

            if len(percentuale_sconto)==0:
                percentuale_sconto=[0]






    session['Percentuale_sconto']=percentuale_sconto

    return render_template("Query_5.html", scelta_2=scelta_2, percentuale_sconto=percentuale_sconto)


@app.route("/SolQuery_5",methods=['GET'])
def SolQuery_5():
    args=request.args
    risposta=args.get("legge")

    risposta=risposta.capitalize()
    if risposta=='Si':
        aliquota_iva = 4

    else:
        aliquota_iva = 22

    ammontare_senza_iva=float(session['Veicoli_disponibili'][int(session['Scelta_2'])][1])
    val_3=['Si','No']
    session['Val_3']=val_3
    id_veicolo_scelto=session['Veicoli_disponibili'][int(session['Scelta_2'])][0]
    session['Id_Veicolo_Scelto']=id_veicolo_scelto
    session['Ammontare_senza_iva']=ammontare_senza_iva
    session['Aliquota_iva']=aliquota_iva

    prezzo_effettivo = (float(ammontare_senza_iva) + float(ammontare_senza_iva) * aliquota_iva / 100) * (1 - float(session['Percentuale_sconto'][0]) / 100)
    return render_template ("SolQuery_5.html",prezzo_effettivo=prezzo_effettivo,ammontare_senza_iva=ammontare_senza_iva,val_3=val_3,id_veicolo_scelto=id_veicolo_scelto)

@app.route("/Query_6",methods=['GET'])
def Query_6():
    args = request.args
    risposta = args.get("categoria")
    if session['Tipo'] == 1:
        query7 = f"select id_veicolo, prezzo_proposto, brand, modello, colore, anno, chilometri, cavalli, cilindrata, foto \
                  from Veicolo_T, Veicolo_Vendita_T, V_due_ruote_T \
                  where Id_Veicolo = V_Id_Veicolo and \
                  V_Id_Veicolo = D_V_Id_Veicolo and \
                  Disponibile = true and \
                  categoria = '{risposta}' and \
                  veicolo_vendita_t.tipo = {session['Tipo']}"
        cursor.execute(query7)
        session['Veicoli_disponibili'] = cursor.fetchall()
    else:
        query7 = f"select id_veicolo, prezzo_proposto, brand, modello, colore, anno, chilometri, cavalli, cilindrata, foto \
                  from Veicolo_T, Veicolo_Vendita_T, V_quattro_ruote_T \
                  where Id_Veicolo = V_Id_Veicolo and \
                  V_Id_Veicolo = Q_V_Id_Veicolo and \
                  Disponibile = true and \
                  categoria = '{risposta}' and \
                  veicolo_vendita_t.tipo = {session['Tipo']}"
        cursor.execute(query7)
        session['Veicoli_disponibili'] = cursor.fetchall()
    l=len(session['Veicoli_disponibili'])
    y = ["Concludi", "Scegli altra Categoria"]
    z = ["Home", "None"]
    session['var_2'] = z
    session['Var'] = y
    return render_template("query_6.html",l=l,y=y,z=z)








@app.route("/Query_8", methods=['GET'])
def Query8():
    args = request.args
    r = args.get('html')
    return render_template("Query_8.html",r=r)

@app.route("/SolQuery_8", methods=['GET'])
def SolQuery8():
    args = request.args
    metodo_pagamento= args.get("metodo")
    metodo_pagamento= metodo_pagamento.capitalize()
    query9_2 = f"update cliente_t \
                    set vendita = True \
                    where Codice_Fiscale = '{session['CF']}'"
    cursor.execute(query9_2)

    if len(session['Cl_vend']) == 0:
        query9_3 = f"insert into Cliente_Vendita_T (V_Codice_Fiscale, Abituale) \
                        values ('{session['CF']}', {session['Abituale']})"
        cursor.execute(query9_3)
        db.commit()

    query10 = f"insert into Vendita_T(Data_Consegna,Data_Ordine,V_Id_Veicolo,Id_Dipendente,V_Codice_Fiscale) values \
                    ('{date.today() + timedelta(days=3)}', '{date.today()}','{session['Id_Veicolo_Scelto']}','{session['Dipendente']}','{session['CF']}')"
    cursor.execute(query10)
    db.commit()

    query11 = f"insert into Pagamento_T (Data_Pagamento,Vendita) \
                    values ('{date.today()}', TRUE)"
    cursor.execute(query11)
    db.commit()

    query_extra = f"select Id_Pagamento \
                    from Pagamento_T \
                    order by Id_Pagamento DESC \
                    limit 1"
    cursor.execute(query_extra)
    Id_Pagamento = cursor.fetchall()

    query_extra2 = f"select Id_Vendita \
                    from Vendita_T \
                    order by Id_Vendita DESC \
                    limit 1"
    cursor.execute(query_extra2)
    Id_Vendita = cursor.fetchall()

    query12 = f"insert into Pagamento_Vendita_T(V_Id_Pagamento,Ammontare_Senza_Iva,Aliquota_Iva,Metodo_Pagamento,Id_Vendita) values \
                    ('{Id_Pagamento[0][0]}', {session['Ammontare_senza_iva']}, {session['Aliquota_iva']},'{metodo_pagamento}','{Id_Vendita[0][0]}')"
    cursor.execute(query12)
    db.commit()

    query13 = f"update veicolo_t \
                    set disponibile = False \
                    where V_Id_Veicolo = '{session['Id_Veicolo_Scelto']}'"
    return render_template("SolQuery_8.html")



@app.route("/Query_12",methods=['GET'])
def Query_12():
    Noleggio="No"
    session['Noleggio']=Noleggio
    return render_template("Query_12.html")

@app.route("/SolQuery_12",methods=['GET'])
def SolQuery_12():

    data_ordine=date.today()

    valore_2=["Scegli altra categoria","Concludi"]
    valore=["None","Home"]
    session['Valore']=valore
    session['Valore_2']=valore_2
    session['Data']="2000-01-01"
    args=request.args
    brand=args.get('brand')
    modello=args.get('modello')
    data_consegna=args.get('Data_Consegna')
    numero_giorni=args.get('Numero_Giorni')
    session['Brand']=brand
    session['Modello']=modello
    session['Data_Consegna']=data_consegna
    session['Numero_Giorni']=int(numero_giorni)
    session['Data_Ordine']=data_ordine
    verifica=f"select DATEDIff('{data_consegna}','{session['Data']}') as giorni_in, DATEDIff('{data_consegna}','{session['Data']}')+'{numero_giorni}'"
    #Questa query prende il numero di giorni dal 1 gennaio del 2000 e poi un'altra colonna che a questa data aggiunge il numero di giorni di noleggio.
    cursor.execute(verifica)
    verifica_2 = cursor.fetchall()
    session['Verifica_2']=verifica_2
    # Questa query prende per il modello richiesto l'intervallo della data di consegna e data restituzione il numero di giorni
    # dal 1 gennaio 2000, In questo modo abbiamo in termini di numeri di giorni gli intervalli.
    query20 = f"select Veicolo_T.Id_Veicolo,DATEDIff(Data_Consegna,'{session['Data']}') as giorni_in, DATEDIff(Data_Consegna,'{session['Data']}')+Numero_giorni \
            from Veicolo_T,Veicolo_Noleggio_T,Noleggio_T \
            WHERE veicolo_T.Id_veicolo=Veicolo_Noleggio_T.N_Id_Veicolo and \
            Veicolo_Noleggio_T.N_Id_Veicolo=Noleggio_T.N_Id_Veicolo and \
            Modello='{modello}'\
            and tipo='{session['Tipo']}'"
    cursor.execute(query20)
    veicoli = cursor.fetchall()
    veicoli_disponibili = list()
    # Veicoli contiene quindi tutti gli intervalli di prenotazione in numero di giorni rispetto al 1 gennaio 2000
    i = 0
    # Tramite questo while andiamo a verificare quali veicoli sono disponibili con i relativi intervalli
    while i < len(veicoli):
        h = False
        if (veicoli[i][1] <= verifica_2[0][1] and veicoli[i][1] >= verifica_2[0][0]) or (
                veicoli[i][2] >= verifica_2[0][0] and veicoli[i][2] <= verifica_2[0][1]) or (veicoli[i][1]<=verifica_2[0][0] and veicoli[i][2]>=verifica_2[0][1]):
            del (veicoli[i])
            h = True
        if h == False:
            i += 1
    # Ora siccome ci potrebbe essere lo stesso veicolo prenotato più volte vado a prendere solo gli id_veicoli diversi
    # dalla lista veicoli e l'inserisco in veicoli_disponibili.
    for i in veicoli:
        if i[0] not in veicoli_disponibili:
            veicoli_disponibili.append(i[0])
    # Se veicoli_disponibili contiene elementi allora vuol dire che abbiamo veicoli disponibili per quell'intervallo
    session['Veicoli_Disponibili']=veicoli_disponibili
    informazioni=[]
    l=len(veicoli_disponibili)
    if len(session['Veicoli_Disponibili']) != 0:

        # Q9) SE IL VEICOLO E' DISPONIBILE, MOSTRARE TUTTE LE INFORMAZIONI NECESSARIE

        # Con python ho un problema riguardo le tuple con un solo elemento, perchè python mette il valore
        # e aggiunge una virgola, e su sql questo ds errore, quindi mi sono separato i due casi.
        # Qui gestisco quando c'è un solo veicolo disponibile

        if len(veicoli_disponibili) == 1:
            query21 = f"select Brand,Modello,Prezzo_Giorno,Colore,Cavalli,cilindrata,foto,anno \
                    from Veicolo_T,veicolo_Noleggio_T \
                    Where Veicolo_T.Id_VEicolo=Veicolo_Noleggio_T.N_Id_VEicolo and \
                    Veicolo_t.Id_veicolo = '{session['Veicoli_Disponibili'][0]}'"

        else:
            # qui gestisco quando ho più veicoli disponibili
            session['Veicoli_Disponibili'] = tuple(session['Veicoli_Disponibili'])
            # siccome sql vuole che diamo in input una tupla ho trasfromato la lista in una tupla

            query21 = "select Brand,Modello,Prezzo_Giorno,Colore,Cavalli,cilindrata,foto,anno \
                   from Veicolo_T,veicolo_Noleggio_T \
                   Where Veicolo_T.Id_VEicolo=Veicolo_Noleggio_T.N_Id_VEicolo and \
                   Veicolo_t.Id_veicolo in {}".format(session['Veicoli_Disponibili'])
        # la query 21 è la stessa e mi danno tutte le informazioini che servono al cliente per poter
        # effettuare una scelta nel modo migliore
        cursor.execute(query21)
        informazioni = cursor.fetchall()
        session["Informazioni"]=informazioni
    return render_template("SolQuery_12.html",l=l)

@app.route("/Query_13",methods=['GET'])
def Query_13():
    args=request.args
    scelta = args.get("html")
    session['Scelta']=scelta
    prezzi=[]
    if 7 <= int(session['Numero_Giorni']) <= 29:
        print("Abbiamo una promozione per lei, ha uno sconto del 5%")
        sconto = 0.05
    elif session['Numero_Giorni'] >= 30:
        print("Abbiamo una promozione per lei, ha uno sconto del 10%")
        sconto = 0.10
    else:
        sconto = 0
    if scelta!="None" and scelta!="Home":
      if len(session['Veicoli_Disponibili']) == 1:

        query24 = f"select distinct veicolo_Noleggio_T.N_id_veicolo,((prezzo_giorno*{int(session['Numero_Giorni'])})-(prezzo_giorno*{int(session['Numero_Giorni'])}*{sconto}))\
                    from pagamento_noleggio_t,noleggio_T,veicolo_noleggio_T,cliente_noleggio_T,Veicolo_T \
                    where pagamento_noleggio_t.id_noleggio = noleggio_T.id_noleggio and \
                    noleggio_T.n_id_veicolo=veicolo_noleggio_T.n_id_veicolo and \
                    noleggio_t.N_codice_fiscale=cliente_noleggio_T.n_codice_fiscale \
                    and Veicolo_T.Id_Veicolo=Veicolo_Noleggio_T.N_id_Veicolo \
                    and veicolo_noleggio_T.n_id_veicolo = '{session['Veicoli_Disponibili'][0]}'"
        cursor.execute(query24)
        prezzi= cursor.fetchall()

      else:
        for i in session['Veicoli_Disponibili']:
           query24 =f"select distinct veicolo_Noleggio_T.N_id_veicolo,((prezzo_giorno*{int(session['Numero_Giorni'])})-(prezzo_giorno*{int(session['Numero_Giorni'])}*{sconto}))\
                    from pagamento_noleggio_t,noleggio_T,veicolo_noleggio_T,cliente_noleggio_T,Veicolo_T \
                    where pagamento_noleggio_t.id_noleggio = noleggio_T.id_noleggio and \
                    noleggio_T.n_id_veicolo=veicolo_noleggio_T.n_id_veicolo and \
                    noleggio_t.N_codice_fiscale=cliente_noleggio_T.n_codice_fiscale \
                    and Veicolo_T.Id_Veicolo=Veicolo_Noleggio_T.N_id_Veicolo \
                    and veicolo_noleggio_T.n_id_veicolo = '{i}'"
           cursor.execute(query24)
           prezzi_1 = cursor.fetchall()
           prezzi.append(prezzi_1)
    session['Prezzi']=prezzi
    return render_template("Query_13.html",scelta=scelta,prezzi=prezzi,sconto=sconto,l=len(prezzi),int_num_giorni=int(session['Numero_Giorni']))

@app.route("/SolQuery_13",methods=['GET'])
def SolQuery_13():
    args=request.args
    scelta_finale=args.get('html')
    session['Scelta_Finale']=scelta_finale
    città = []
    if scelta_finale not in session['Valore']:
      città_2 = "select città \
                   from Concessionaria_t"
      cursor.execute(città_2)
      città = cursor.fetchall()
      session['Città']=città
      session['Noleggio']="Si"
    return render_template("SolQuery_13.html",città=città,scelta_finale=scelta_finale,l=len(città))


@app.route("/Query_14",methods=['GET'])
def Query_14():
    session['Veicoli_Disponibili']=[]
    args=request.args
    informazioni=[]
    categoria=args.get('categoria')
    if session['Tipo'] == 0:
      query22 = f"select Brand, Modello,Id_Veicolo \
                  from Veicolo_t,Veicolo_NOleggio_T,N_Quattro_Ruote_T \
                  where veicolo_T.Id_Veicolo= Veicolo_Noleggio_T.N_Id_Veicolo and \
                  Veicolo_Noleggio_T.N_Id_Veicolo=N_Quattro_Ruote_T.Q_N_Id_VEicolo and \
                  categoria = '{categoria}' \
                  and tipo='{session['Tipo']}'"

    else:
      query22 = f"select Brand, Modello,Id_Veicolo \
                    from Veicolo_t,Veicolo_NOleggio_T,N_Due_Ruote_T \
                    where veicolo_T.Id_Veicolo= Veicolo_Noleggio_T.N_Id_Veicolo and \
                    Veicolo_Noleggio_T.N_Id_Veicolo=N_Due_Ruote_T.D_N_Id_VEicolo and \
                    categoria = '{categoria}' \
                    and tipo='{session['Tipo']}'"


    cursor.execute(query22)
    veicoli_stessa_categoria = cursor.fetchall()
    for brand, modello, Id_Veicolo in veicoli_stessa_categoria:
        query20 = f"select Veicolo_T.Id_Veicolo,DATEDIff(Data_Consegna,'{session['Data']}') as giorni_in, DATEDIff(Data_Consegna,'{session['Data']}')+Numero_giorni \
                        from Veicolo_T,Veicolo_Noleggio_T,Noleggio_T \
                        WHERE veicolo_T.Id_veicolo=Veicolo_Noleggio_T.N_Id_Veicolo and \
                        Veicolo_Noleggio_T.N_Id_Veicolo=Noleggio_T.N_Id_Veicolo and \
                        Veicolo_T.Id_Veicolo='{Id_Veicolo}'"
        cursor.execute(query20)
        veicoli_categoria = cursor.fetchall()
        disp = list()

        # Come prima questo while serve per eliminare gli intervalli che si sovrappongono con quelli
        # dati in input dall'utente
        i = 0
        while i < len(veicoli_categoria):
            h = False
            if (veicoli_categoria[i][1] <= session['Verifica_2'][0][1] and veicoli_categoria[i][1] >= session['Verifica_2'][0][0]) or (
                    veicoli_categoria[i][2] >= session['Verifica_2'][0][0] and veicoli_categoria[i][2] <= session['Verifica_2'][0][1]) or (veicoli_categoria[i][1]<=session['Verifica_2'][0][0] and veicoli_categoria[i][2]>=session['Verifica_2'][0][1]):
                del (veicoli_categoria[i])
                h = True
            if h == False:
                i += 1
        # Nel for m'inserisco ogni volta l'id del veicolo se è disponibile in modo da capire quale
        # veicolo vuole il cliente
        for i in veicoli_categoria:
            if i[0] not in session['Veicoli_Disponibili']:
                session['Veicoli_Disponibili'].append(i[0])
                disp.append(i[0])
        # Se in disp ci sono elementi vuol dire che quel veicolo è disponibile, perchè per ogni
        # iterazione del ciclo for ricreo disp come una lista vuota
        if len(disp) == 1:
            # Q9) SE IL VEICOLO E' DISPONIBILE, MOSTRARE TUTTE LE INFORMAZIONI NECESSARIE

            # Qui mostro per i veicoli disponibili le informormazioni per permettere al cliente di scegliere nel modo migliore il veicolo da noleggiare
            query21 = f"select Brand,Modello,Prezzo_Giorno,Colore,Cavalli,cilindrata,foto,anno \
            from Veicolo_T,veicolo_Noleggio_T \
            Where Veicolo_T.Id_VEicolo=Veicolo_Noleggio_T.N_Id_VEicolo and \
            Veicolo_t.Id_veicolo = '{disp[0]}'"
            cursor.execute(query21)
            ris21 = cursor.fetchall()
            for i in ris21:
              informazioni.append(i)
    session['Informazioni']=informazioni
    return render_template("Query_14.html",informazioni=informazioni,l=len(informazioni),l_2=len(session['Veicoli_Disponibili']),categoria=categoria)

@app.route("/Query_15",methods=['GET'])
def Query_15():
    args = request.args
    if session['Noleggio'] == "Si":
          Luogo_Restituzione = args.get('restituzione')
          session['Luogo_Restituzione']=Luogo_Restituzione
    return render_template("Query_15.html",)



@app.route("/SolQuery_15",methods=['POST','GET'])
def SolQuery_15():
    args=request.args
    recensione=args.get("recensione")
    recensione=recensione.capitalize()
    session["Recensione"]=recensione
    if session['Noleggio']=="Si":
        Luogo_Restituzione=args.get("restituzione")
        query36 = f"select N_Codice_Fiscale \
                        from Cliente_Noleggio_T \
                        where N_Codice_Fiscale ='{session['CF']}'"
        cursor.execute(query36)
        ris36 = cursor.fetchall()
        if len(ris36) == 0:
            query37 = f"insert into Cliente_Noleggio_T(N_Codice_Fiscale) \
                            values ('{session['CF']}')"
            cursor.execute(query37)
            db.commit()

        # Inserisco i dati riguardanti il noleggio
        query25 = f"insert into Noleggio_T(Data_Consegna,Data_ordine,Numero_Giorni,Luogo_Restituzione,Id_Dipendente,N_Id_Veicolo,N_Codice_Fiscale) \
                        values ('{session['Data_Consegna']}','{date.today()}',{int(session['Numero_Giorni'])},'{session['Città'][int(session['Luogo_Restituzione'])][0]}','{session['Dipendente']}','{session['Veicoli_Disponibili'][int(session['Scelta_Finale'])]}','{session['CF']}')"
        cursor.execute(query25)
        db.commit()

        # Aggiornare la concessionaria nella quale si trova il veicolo
        # qui prendo l'id della concessionaria
        query26 = f"select Id_Concessionaria \
                        from Concessionaria_T \
                        where città= '{session['Città'][int(session['Luogo_Restituzione'])][0]}'"
        cursor.execute(query26)
        ris26 = cursor.fetchall()

        # Qui aggiorno il luogo di restituzione

        query27 = f"update Veicolo_T \
                        set Id_Concessionaria= {ris26[0][0]} \
                        where Id_Veicolo= '{session['Veicoli_Disponibili'][int(session['Scelta_Finale'])]}'"
        cursor.execute(query27)
        db.commit()
        # prendo l'ultimo id_Noleggio del noleggio effettuato
        query28 = f"select Id_noleggio \
                        from Noleggio_T \
                        order by Id_Noleggio DESC \
                        limit 1 "
        cursor.execute(query28)
        Id_Noleggio = cursor.fetchall()

        # inserisco i dati sul pagamento
        query29 = f"insert into Pagamento_T(Data_Pagamento,Vendita) \
                        values('{date.today()}',0)"
        cursor.execute(query29)
        db.commit()
        # Prendo l'id_pagamento
        query30 = f" select Id_Pagamento \
                        from Pagamento_T \
                        order by Id_Pagamento DESC \
                        limit 1"
        cursor.execute(query30)
        Id_Pagamento = cursor.fetchall()
        if len(session['Prezzi'][0][0])==1:
        # Inseirsco i valori relativi al pagamento
          query31 = f"insert into Pagamento_Noleggio_T(N_Id_Pagamento,Id_Noleggio,Ammontare) \
                        values('{Id_Pagamento[0][0]}','{Id_Noleggio[0][0]}',{session['Prezzi'][int(session['Scelta_Finale'])][1]})"
        else:
            query31 = f"insert into Pagamento_Noleggio_T(N_Id_Pagamento,Id_Noleggio,Ammontare) \
                                    values('{Id_Pagamento[0][0]}','{Id_Noleggio[0][0]}',{session['Prezzi'][int(session['Scelta_Finale'])][0][1]})"
        cursor.execute(query31)
        db.commit()
    return render_template("SolQuery_15.html",recensione=recensione)

@app.route("/Query_16",methods=['POST','GET'])
def Query_16():
    if session['Recensione']=="Si":
        if request.method == 'POST':
            Veicoli = request.form.get('veicoli', False)
            val_dipendenti = request.form.get('dipendente', False)

        if val_dipendenti == "1":
            val_dipendenti = "Molto Insoddisfatto"
        elif val_dipendenti == "2":
            val_dipendenti = "Insoddisfatto"
        elif val_dipendenti == "3":
            val_dipendenti = "Nè Soddisfatto Nè Insoddisfatto"
        elif val_dipendenti == "4":
            val_dipendenti = "Soddisfatto"
        else:
            val_dipendenti = "Molto Soddisfatto"
        if Veicoli == "1":
            Veicoli = "Molto Insoddisfatto"
        elif Veicoli == "2":
            Veicoli = "Insoddisfatto"
        elif Veicoli == "3":
            Veicoli = "Nè Soddisfatto Nè Insoddisfatto"
        elif Veicoli == "4":
            Veicoli = "Soddisfatto"
        else:
            Veicoli = "Molto Soddisfatto"

            # INSERIRE I DATI RELATIVI ALLA RECENSIONE
        query32 = f"insert into Recensione_T(Data_Recensione,Dipendente,Veicoli,Codice_Fiscale,Id_Dipendente) \
                values('{date.today()}','{val_dipendenti}','{Veicoli}','{session['CF']}','{session['Dipendente']}')"
        cursor.execute(query32)
        db.commit()
    return render_template("Query_16.html")



@app.route("/Analitiche",methods=['GET'])
def Analitiche():
    return render_template("AnaliticheQuery.html")

@app.route("/Query_30", methods=['GET'])
def Query_30():
   return render_template("Query_30.html")

@app.route("/SolQuery_30",methods=['GET'])
def SolQuery_30():
    args= request.args
    città=args.get("città")
    data_inizio=args.get("data_inizio")
    data_fine=args.get("data_fine")
    Query_30=f"select brand,modello \
        From Veicolo_Noleggio_T,Noleggio_T,Veicolo_T,Concessionaria_T \
        WHERE Veicolo_Noleggio_T.N_Id_veicolo= Noleggio_T.N_Id_Veicolo and \
        Veicolo_T.Id_Concessionaria=Concessionaria_T.Id_Concessionaria and \
        Veicolo_T.Id_Veicolo =Veicolo_Noleggio_T.N_Id_Veicolo and \
        Città='{città}' and \
        Data_Consegna Between '{data_inizio}' and '{data_fine}' "
    cursor.execute(Query_30)
    ris30=cursor.fetchall()
    return render_template("SolQuery_30.html", ris30=ris30,l=len(ris30),città=città, data_inizio=data_inizio, data_fine=data_fine)
@app.route("/Query_31",methods=['GET'])
def Query_31():
    return render_template("Query_31.html")

@app.route("/SolQuery_31",methods=['GET'])
def SolQuery_31():
    args=request.args
    tipo=args.get("Tipo")
    if tipo=="1":
        tipo_2=2
    else:
        tipo_2=4
    Query_31=f"select * \
        from (Select count(vendita_t.V_Id_Veicolo) as Vendita_Tipo_1 \
              from vendita_T,veicolo_vendita_t \
        where (vendita_T.V_Id_Veicolo = veicolo_vendita_t.V_Id_Veicolo) and \
        veicolo_vendita_t.tipo={tipo}) as t ,(Select count(noleggio_t.N_id_veicolo) as Noleggio_Tipo_1 \
        from noleggio_T,veicolo_noleggio_T \
        where  (noleggio_t.N_Id_Veicolo = veicolo_noleggio_t.N_Id_Veicolo) and veicolo_noleggio_t.tipo={tipo} \
        ) as t_2 "
    cursor.execute(Query_31)
    ris31=cursor.fetchall()
    l=len(ris31)
    return render_template("SolQuery_31.html",ris31=ris31,tipo_2=tipo_2,l=l)
@app.route("/Query_32", methods=['GET'])
def Query_32():
    return render_template("Query_32.html")

@app.route("/SolQuery_32", methods=['GET'])
def SolQuery_32():
    args= request.args
    categoria=args.get("categoria")
    Query_32=f"select nome,cognome, codice_fiscale \
        from (select nome, cognome, codice_fiscale, count(Noleggio_T.N_Id_Veicolo) as NumNoleggi \
              from cliente_t, noleggio_t, N_Quattro_Ruote_T \
              where Noleggio_T.N_Codice_Fiscale = Cliente_T.Codice_Fiscale and \
              Noleggio_T.N_Id_Veicolo = N_Quattro_Ruote_T.Q_N_Id_Veicolo and \
              N_Quattro_Ruote_T.Categoria = '{categoria}' \
              group by Cliente_T.Codice_Fiscale) as Noleggi \
        where NumNoleggi > 2"
    cursor.execute(Query_32)
    ris32 = cursor.fetchall()
    l = len(ris32)
    return render_template("SolQuery_32.html",ris32=ris32, categoria=categoria,l=l)

@app.route("/Query_33", methods=['GET'])
def Query_33():
    return render_template("Query_33.html")

@app.route("/SolQuery_33", methods=['GET'])
def SolQuery_33():
    args=request.args
    Query_33="select brand\
                from Noleggi60\
                where Noleggi = (select max(Noleggi) from Noleggi60)"
    cursor.execute(Query_33)
    ris33=cursor.fetchall()
    l = len(ris33)
    return render_template("SolQuery_33.html",ris33=ris33,l=l)

@app.route("/Query_34", methods=['GET'])
def Query_34():
    return render_template("Query_34.html")

@app.route("/SolQuery_34", methods=['GET'])
def SolQuery_34():
    Query_34=f"select * \
        from Provvigioni \
        where Provvigioni = (select max(Provvigioni) from Provvigioni) "
    cursor.execute(Query_34)
    ris34=cursor.fetchall()
    l=len(ris34)
    return render_template("SolQuery_34.html",ris34=ris34,l=l)

@app.route("/Query_35", methods=['GET'])
def Query_35():
    return render_template("Query_35.html")

@app.route("/SolQuery_35", methods=['GET'])
def SolQuery_35():
    Query_35=f"select Promozione_T.Id_Promozione, Abituale_Promozione_T.A_V_Codice_Fiscale, Vendita_T.Id_Vendita \
        from Promozione_T, Abituale_Promozione_T, Vendita_T \
        where Promozione_T.Id_Promozione = Abituale_Promozione_T.Id_Promozione and  \
        Abituale_Promozione_T.A_V_Codice_Fiscale = Vendita_T.V_Codice_Fiscale and \
        Data_Ordine between Promozione_T.Data_Inizio and Promozione_T.Data_Fine "
    cursor.execute(Query_35)
    ris35=cursor.fetchall()
    l=len(ris35)
    return render_template("SolQuery_35.html",ris35=ris35,l=l)

@app.route("/Query_36",methods=['GET'])
def Query_36():
    return render_template("Query_36.html")

@app.route("/SolQuery_36",methods=['GET'])
def SolQuery_36():
    args= request.args
    tipo= args.get("tipo")
    tipo = tipo.capitalize()
    if tipo=="Vendita":
        Query_36=f"select codice_fiscale, count(Vendita_T.Id_Vendita) as Numero_Ordini \
            from cliente_t, vendita_t \
            where codice_fiscale = vendita_t.v_codice_fiscale  \
            group by codice_fiscale"
    else:
        Query_36=f"select codice_fiscale, count(Noleggio_T.Id_Noleggio) as Numero_Ordini \
            from cliente_t, Noleggio_T \
            where codice_fiscale = noleggio_t.n_codice_fiscale \
            group by codice_fiscale "
    cursor.execute(Query_36)
    ris36=cursor.fetchall()
    l=len(ris36)
    return render_template("SolQuery_36.html",ris36=ris36,tipo=tipo,l=l)

@app.route("/Query_37", methods=['GET'])
def Query_37():
    return render_template("Query_37.html")

@app.route("/SolQuery_37", methods=['GET'])
def SolQuery_37():
    args=request.args
    Codice_Fiscale=args.get("CF")
    Query_37=f"select id_veicolo, foto \
        from Veicolo_T, Vendita_T, Cliente_VEndita_T \
        where Veicolo_T.Id_Veicolo = Vendita_T.V_Id_Veicolo and \
        Cliente_Vendita_T.V_Codice_Fiscale= '{Codice_Fiscale}' and \
        Data_Ordine = (select min(Data_Ordine) from Vendita_T,Cliente_Vendita_T \
                       where Cliente_VEndita_T.V_Codice_Fiscale=Vendita_T.V_Codice_Fiscale and \
                       Cliente_Vendita_T.V_Codice_Fiscale='{Codice_Fiscale}') "
    cursor.execute(Query_37)
    ris37=cursor.fetchall()
    l=len(ris37)
    return render_template("SolQuery_37.html",ris37=ris37, Codice_Fiscale=Codice_Fiscale,l=l)
@app.route("/Query_38",methods=['GET'])
def Query_38():
    return render_template("Query_38.html")

@app.route("/SolQuery_38",methods=['GET'])
def SolQuery_38():
    args=request.args
    brand=args.get("brand")
    numero_giorni=args.get("numero_giorni")
    Query_38=f"select Id_Veicolo, Prezzo_Giorno*'{numero_giorni}' as PReventivo \
        from Veicolo_T, Veicolo_Noleggio_T \
        where Veicolo_T.Id_Veicolo = Veicolo_Noleggio_T.N_Id_Veicolo and \
        Brand = '{brand}'"
    cursor.execute(Query_38)
    ris38=cursor.fetchall()
    l=len(ris38)
    return render_template("SolQuery_38.html",ris38=ris38, brand=brand, numero_giorni=numero_giorni,l=l)

@app.route("/Query_39",methods=['GET'])
def Query_39():
    return render_template("Query_39.html")

@app.route("/SolQuery_39",methods=['GET'])
def SolQuery_39():
    Query_39=f"select * \
        from NumeroRecensioniPositive_Dip \
        where NumRecPos = (select max(NumRecPos) from NumeroRecensioniPositive_Dip) "
    cursor.execute(Query_39)
    ris39=cursor.fetchall()
    l=len(ris39)
    return render_template("SolQuery_39.html",ris39=ris39,l=l)

@app.route("/Query_40",methods=['GET'])
def Query_40():
    return render_template("Query_40.html")

@app.route("/SolQuery_40",methods=['GET'])
def SolQuery_40():
    Query_40 = f"select * \
        from NumeroRecensioniNegative_Dip \
        where NumRecNeg = (select max(NumRecNeg) from NumeroRecensioniNegative_Dip) "
    cursor.execute(Query_40)
    ris40 = cursor.fetchall()
    l=len(ris40)
    return render_template("SolQuery_40.html", ris40=ris40,l=l)

@app.route("/Query_41",methods=['GET'])
def Query_41():
    return render_template("Query_41.html")

@app.route("/SolQuery_41",methods=['GET'])
def SolQuery_41():
    Query_41 = f"select Id_Concessionaria \
        from NumeroRecensioniPositive_Conc \
        where NumRecPos = (select max(NumRecPos) from NumeroRecensioniPositive_Conc) "
    cursor.execute(Query_41)
    ris41 = cursor.fetchall()
    l=len(ris41)
    return render_template("SolQuery_41.html", ris41=ris41,l=l)


@app.route("/Query_42", methods=['GET'])
def Query_42():
   return render_template("Query_42.html")

@app.route("/SolQuery_42",methods=['GET'])
def SolQuery_42():
    args = request.args
    Query_42=f"select Nome, Cognome, email, telefono\
                from Cliente_T\
                where day(Data_Nascita) = day(current_date()) and month(Data_Nascita) = month(current_date());"
    cursor.execute(Query_42)
    ris42 = cursor.fetchall()
    l=len(ris42)
    return render_template("SolQuery_42.html", ris42=ris42,l=l)

@app.route("/Query_43", methods=['GET'])
def Query_43():
   return render_template("Query_43.html")

@app.route("/SolQuery_43",methods=['GET'])
def SolQuery_43():
    args=request.args
    periodo=args.get("periodo")
    periodo=periodo.capitalize()
    if periodo=="Estate":
        Query_43=f"select * \
        from PeriodoEstivo \
        where NumeroVendite = (select max(NumeroVendite) from PeriodoEstivo) "
    elif periodo=="Inverno":
        Query_43=f"select * \
                from PeriodoInvernale \
                where NumeroVendite = (select max(NumeroVendite) from PeriodoInvernale) "
    elif periodo=='Autunno':
        Query_43=f"select * \
                from PeriodoAutunnale \
                where NumeroVendite = (select max(NumeroVendite) from PeriodoAutunnale) "
    elif periodo=="Primavera":
        Query_43="select * \
                from PeriodoPrimaverile \
                where NumeroVendite = (select max(NumeroVendite) from PeriodoPrimaverile) "
    cursor.execute(Query_43)
    ris43 = cursor.fetchall()
    l=len(ris43)
    return render_template("SolQuery_43.html", ris43=ris43, periodo=periodo,l=l)




@app.route("/Query_44", methods=['GET'])
def Query_44():
   return render_template("Query_44.html")

@app.route("/SolQuery_44",methods=['GET'])
def SolQuery_44():
    args = request.args
    brand = args.get("brand")
    Query_44=f"select avg(Ammontare_Senza_IVA+Ammontare_Senza_IVA*Aliquota_IVA/100)-(select avg(Ammontare_Senza_IVA+Ammontare_Senza_IVA*Aliquota_IVA/100) as PrezzoMedioBrand \
        from Pagamento_Vendita_T, Veicolo_T, vendita_t \
        where Pagamento_Vendita_T.Id_Vendita = Vendita_t.Id_Vendita and \
        Vendita_T.V_Id_Veicolo = Veicolo_t.Id_Veicolo and \
        brand = '{brand}') as Differenza \
        from Pagamento_Vendita_T "
    cursor.execute(Query_44)
    ris44 = cursor.fetchall()
    l = len(ris44)
    return render_template("SolQuery_44.html", ris44=ris44,brand=brand,l=l)


@app.route("/Query_45", methods=['GET'])
def Query_45():
   return render_template("Query_45.html")

@app.route("/SolQuery_45",methods=['GET'])
def SolQuery_45():
    args = request.args
    Query_45=f"select sum(prezzo_listino-(ammontare_senza_iva+ammontare_senza_iva*aliquota_iva/100)) as differenza \
        from veicolo_t, Vendita_t, Pagamento_Vendita_T \
        where Veicolo_T.Id_Veicolo = Vendita_T.V_Id_Veicolo and \
        Vendita_T.Id_Vendita = Pagamento_Vendita_T.Id_Vendita"
    cursor.execute(Query_45)
    ris45 = cursor.fetchall()
    l = len(ris45)
    return render_template("SolQuery_45.html", ris45=ris45,l=l)


@app.route("/Query_46", methods=['GET'])
def Query_46():
   return render_template("Query_46.html")

@app.route("/SolQuery_46",methods=['GET'])
def SolQuery_46():
    args = request.args
    Query_46=f"select * \
        from GiorniDeposito \
        where giorni > (select avg(giorni) from GiorniDeposito) "
    cursor.execute(Query_46)
    ris46 = cursor.fetchall()
    l = len(ris46)
    return render_template("SolQuery_46.html", ris46=ris46,l=l)



@app.route("/action_page",methods=['GET'])
def action():
    return render_template("action-page.html")

@app.route("/Storia",methods=['GET'])
def Storia():
    return render_template("Storia.html")
